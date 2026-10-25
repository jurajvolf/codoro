"""Middleware platformy Codoro pre bezpečnostné hlavičky, ochranu súborov a správu Streaku."""
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from accounts.security import validate_uploaded_file


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
