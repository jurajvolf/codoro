"""Middleware platformy Codoro."""


class StreakMiddleware:
    """
    Pri každej požiadavke prihláseného študenta skontroluje stav denného Streaku.
    Ak študent vynechal deň, séria sa preruší (alebo sa spotrebuje zmrazenie)
    a na dashboarde sa mu ponúkne záchrana za Doros. Zápis do DB nastáva iba pri zmene.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, 'user', None)
        if user is not None and user.is_authenticated and not user.is_teacher():
            user.refresh_streak_state()
        return self.get_response(request)
