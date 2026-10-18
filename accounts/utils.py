"""Pomocné funkcie zdieľané medzi všetkými modulmi Codoro."""
from django.utils.http import url_has_allowed_host_and_scheme


def safe_int(value, default=0, min_value=None, max_value=None):
    """Bezpečne prevedie hodnotu z POST formulára na int (chráni pred chybou 500 pri neplatnom vstupe)."""
    try:
        result = int(str(value).strip())
    except (TypeError, ValueError):
        result = default
    if min_value is not None:
        result = max(min_value, result)
    if max_value is not None:
        result = min(max_value, result)
    return result


def tr(lang, sk_text, en_text):
    """Vráti text v aktívnom jazyku používateľa (SK / EN)."""
    return en_text if lang == 'en' else sk_text


def user_lang(request):
    """Zistí aktívny jazyk rozhrania pre prihláseného aj neprihláseného používateľa."""
    if request.user.is_authenticated and request.user.preferred_language:
        return request.user.preferred_language
    return request.session.get('ui_lang', 'sk')


def safe_redirect_target(request, fallback='/'):
    """Ochrana proti Open Redirect: povolí iba návrat na rovnakú doménu."""
    target = request.META.get('HTTP_REFERER', '')
    if target and url_has_allowed_host_and_scheme(target, allowed_hosts={request.get_host()},
                                                  require_https=request.is_secure()):
        return target
    return fallback
