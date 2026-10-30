"""Middleware platformy Codoro pre bezpečnostné hlavičky, ochranu súborov a správu Streaku."""
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from accounts.security import validate_uploaded_file
from config.db_routers import set_active_db, reset_active_db, ensure_demo_database, DEMO_USERNAMES


class DemoRoutingMiddleware:
    """
    Smeruje požiadavky demo relácií (student, ucitel, martin_k) do izolovanej simulovanej databázy 'demo'.
    Zabezpečuje, že žiadny demo používateľ nemôže modifikovať ani čítať ostré produkčné dáta.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        is_demo = False
        session = getattr(request, 'session', None)

        # 1. Už existujúca demo session
        if session and session.get('is_demo_mode', False):
            is_demo = True
        # 2. Prihlasovací POST pokus s demo používateľským menom
        elif request.method == 'POST' and request.path.endswith('/login/') and request.POST.get('username', '').strip().lower() in DEMO_USERNAMES:
            is_demo = True
        # 3. Explicitné demo URL cesty
        elif request.path.startswith('/demo/'):
            is_demo = True

        request.is_demo = is_demo
        token = None

        if is_demo and 'demo' in getattr(settings, 'DATABASES', {}):
            ensure_demo_database()
            token = set_active_db('demo')

        try:
            response = self.get_response(request)
            return response
        finally:
            if token is not None:
                reset_active_db(token)


class SecurityHeadersMiddleware:
    """
    Pridáva bezpečnostné HTTP hlavičky (CSP, Permissions-Policy, X-Content-Type-Options,
    X-Frame-Options, Referrer-Policy, Cache-Control pre statické súbory, CORS kontrolu)
    a chráni nahrávanie súborov pred škodlivými príponami/obsahom.
    """

    CSP_POLICY = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://cdn.jsdelivr.net; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdnjs.cloudflare.com; "
        "font-src 'self' https://fonts.gstatic.com data:; "
        "img-src 'self' data: blob:; "
        "connect-src 'self'; "
        "frame-ancestors 'none'; "
        "base-uri 'self'; "
        "form-action 'self'; "
        "object-src 'none';"
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Globálna kontrola nahrávaných súborov (Restrict & Secure File Uploads)
        if request.FILES:
            for _, uploaded_file in request.FILES.items():
                is_valid, err_msg = validate_uploaded_file(uploaded_file)
                if not is_valid:
                    return HttpResponseBadRequest(err_msg)

        response = self.get_response(request)

        # 2. Bezpečnostné HTTP hlavičky
        response.setdefault('X-Content-Type-Options', 'nosniff')
        response.setdefault('X-Frame-Options', 'DENY')
        response.setdefault('Referrer-Policy', 'strict-origin-when-cross-origin')
        response.setdefault(
            'Permissions-Policy',
            'camera=(), microphone=(), geolocation=(), payment=(), usb=(), interest-cohort=()'
        )
        response.setdefault('Cross-Origin-Opener-Policy', 'same-origin')
        response.setdefault('Content-Security-Policy', self.CSP_POLICY)

        # 3. Kontrola CORS hlavičiek (iba povolené originy)
        origin = request.META.get('HTTP_ORIGIN')
        allowed_origins = getattr(settings, 'CORS_ALLOWED_ORIGINS', [])
        if origin and origin in allowed_origins:
            response['Access-Control-Allow-Origin'] = origin
            response['Vary'] = 'Origin'

        # 4. Cache-Control pre statické súbory (Performance & Lighthouse)
        if request.path.startswith('/static/'):
            response.setdefault('Cache-Control', 'public, max-age=31536000, immutable')

        return response


class StreakMiddleware:
    """
    Pri každej požiadavke prihláseného študenta skontroluje stav denného Streaku.
    Ak študent vynechal deň, séria sa preruší (alebo sa spotrebuje zmrazenie)
    a na dashboarde sa mu ponúkne záchrana za Doros. Zápis do DB nastáva iba pri zmene.
    Zároveň chráni interné rozhranie /admin/ pred neautorizovaným prístupom.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, 'user', None)

        # Ochrana /admin/ (Django ORM Admin) - prístup len pre ADMIN a superuserov
        if request.path.startswith('/admin/'):
            if not user or not user.is_authenticated:
                return redirect('login')
            if not (getattr(user, 'role', None) == 'ADMIN' or user.is_superuser):
                return redirect('dashboard')

        if user is not None and user.is_authenticated and not user.is_teacher():
            user.refresh_streak_state()
        return self.get_response(request)
