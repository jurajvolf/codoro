"""
Context processors for accounts app.
Provides active language (ui_lang / lang) and user preferences across all templates.
"""

def language_context(request):
    """
    Guarantees that `lang` and `ui_lang` are ALWAYS available in every template,
    whether the user is authenticated or an anonymous visitor.
    """
    lang = 'sk'
    
    # 1. Query parameter override (e.g. ?lang=en or ?lang=sk)
    query_lang = request.GET.get('lang')
    if query_lang in ['sk', 'en']:
        lang = query_lang
        request.session['ui_lang'] = lang
        if hasattr(request, 'user') and request.user.is_authenticated:
            if hasattr(request.user, 'preferred_language') and request.user.preferred_language != lang:
                request.user.preferred_language = lang
                request.user.save(update_fields=['preferred_language'])
    # 2. Authenticated user preference
    elif hasattr(request, 'user') and request.user.is_authenticated and hasattr(request.user, 'preferred_language') and request.user.preferred_language:
        lang = request.user.preferred_language
        request.session['ui_lang'] = lang
    # 3. Session preference
    elif 'ui_lang' in request.session and request.session['ui_lang'] in ['sk', 'en']:
        lang = request.session['ui_lang']
    # 4. Cookie fallback
    elif request.COOKIES.get('codoro_lang') in ['sk', 'en']:
        lang = request.COOKIES.get('codoro_lang')
        request.session['ui_lang'] = lang

    return {
        'lang': lang,
        'ui_lang': lang,
    }
