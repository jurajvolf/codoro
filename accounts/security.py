"""
Bezpečnostné utilitky a ochranné mechanizmy platformy Codoro:
- Rate limiting (ochrana pred brute-force útokmi na login, registráciu, reset hesla a sandbox)
- Bot protection (honeypot detekcia automatizovaných robotov)
- Input validation & sanitization (safe_int, sanitize_text, open-redirect ochrana)
- Row-Level Security (RLS) kontroly vlastníctva záznamov pre učiteľov a triedy
- Bezpečná validácia nahrávaných súborov (allowlist prípon, MIME typov a magic bytes)
- Šifrovanie a kryptografické podpisovanie citlivých údajov
"""
import base64
import hashlib
import hmac
import os
import re
from django.conf import settings
from django.core.cache import cache
from django.core import signing
from django.utils.http import url_has_allowed_host_and_scheme


def get_client_ip(request):
    """Získa klientsku IP adresu zo žiadosti (zohľadňuje reverse proxy hlavičku)."""
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    if xff:
        return xff.split(',')[0].strip()[:64]
    return (request.META.get('REMOTE_ADDR') or '127.0.0.1')[:64]


def _rate_limit_key(request, scope, identifier=''):
    ip = get_client_ip(request)
    ident_hash = hashlib.sha256(f"{ip}:{identifier}".encode('utf-8')).hexdigest()[:20]
    return f"codoro_rl:{scope}:{ident_hash}"


def is_rate_limited(request, scope, limit=10, window_seconds=300, identifier='', increment=True):
    """
    Sliding/fixed-window rate limiter využívajúci Django cache.
    Vráti True, ak bol prekročený povolený počet pokusov v časovom okne.
    """
    key = _rate_limit_key(request, scope, identifier=identifier)
    current = cache.get(key, 0)
    if current >= limit:
        return True
    if increment:
        if current == 0:
            cache.set(key, 1, timeout=window_seconds)
        else:
            try:
                cache.incr(key)
            except ValueError:
                cache.set(key, current + 1, timeout=window_seconds)
    return False


def reset_rate_limit(request, scope, identifier=''):
    """Vymaže počítadlo rate-limitu (napr. po úspešnom prihlásení)."""
    key = _rate_limit_key(request, scope, identifier=identifier)
    cache.delete(key)


def check_honeypot(request, field_name='website_url'):
    """
    Overí skryté honeypot pole proti automatizovaným spam robotom.
    Vráti True, ak je žiadosť legitímna (pole je prázdne), False ak ide o bota.
    """
    val = (request.POST.get(field_name) or '').strip()
    return len(val) == 0


def safe_int(value, default=0, min_val=None, max_val=None):
    """
    Bezpečne skonvertuje vstup na celé číslo bez vyhodenia ValueError / TypeError.
    Voliteľne oreže hodnotu do intervalu [min_val, max_val].
    """
    try:
        if value is None or value == '':
            result = default
        else:
            result = int(str(value).strip())
    except (ValueError, TypeError):
        result = default

    if min_val is not None and result < min_val:
        result = min_val
    if max_val is not None and result > max_val:
        result = max_val
    return result


def sanitize_text(value, max_length=None):
    """Odstráni nulové bajty, riadiace znaky a oreže text na maximálnu dĺžku."""
    if value is None:
        return ''
    cleaned = str(value).replace('\x00', '').strip()
    # Odstránenie nebezpečných riadiacich znakov okrem \n, \r, \t
    cleaned = re.sub(r'[\x01-\x08\x0b\x0c\x0e-\x1f\x7f]', '', cleaned)
    if max_length is not None and len(cleaned) > max_length:
        cleaned = cleaned[:max_length]
    return cleaned


def safe_redirect_url(request, next_url, fallback='/'):
    """
    Zabráni Open Redirect zraniteľnosti — povolí len relatívne URL na rovnakom hostiteľovi.
    """
    if next_url and url_has_allowed_host_and_scheme(
        url=next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return next_url
    return fallback


def can_teacher_access_student(teacher, student):
    """
    Row-Level Security (RLS) kontrola pre učiteľa:
    - SuperAdmin / ADMIN má prístup ku všetkým záznamom.
    - Učiteľ má prístup k žiakom vo svojich triedach alebo k žiakom, ktorí zatiaľ nemajú priradeného iného učiteľa.
    """
    if not teacher or not teacher.is_authenticated:
        return False
    if getattr(teacher, 'role', None) == 'ADMIN' or teacher.is_superuser:
        return True
    if getattr(teacher, 'role', None) != 'TEACHER' and not teacher.is_staff:
        return False
    if getattr(student, 'role', None) in ('ADMIN', 'TEACHER') and student.id != teacher.id:
        return False
    sc = getattr(student, 'school_class', None)
    if sc is None or sc.teacher_id is None or sc.teacher_id == teacher.id:
        return True
    return False


def can_teacher_access_class(teacher, school_class):
    """Row-Level Security kontrola pre školskú triedu."""
    if not teacher or not teacher.is_authenticated:
        return False
    if getattr(teacher, 'role', None) == 'ADMIN' or teacher.is_superuser:
        return True
    if getattr(teacher, 'role', None) != 'TEACHER' and not teacher.is_staff:
        return False
    return school_class.teacher_id is None or school_class.teacher_id == teacher.id


ALLOWED_IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.webp'}
ALLOWED_IMAGE_MIMES = {'image/png', 'image/jpeg', 'image/webp'}


def validate_uploaded_file(uploaded_file, max_size_mb=2):
    """
    Bezpečnostná kontrola nahrávaného súboru:
    1. Maximálna veľkosť (predvolene 2 MB).
    2. Povolená prípona (.png, .jpg, .jpeg, .webp).
    3. Kontrola MIME typu.
    4. Kontrola hlavičky súboru (magic bytes) proti podvrhnutým skriptom.
    Vráti (is_valid: bool, error_msg: str).
    """
    if not uploaded_file:
        return False, "Žiadny súbor nebol nahraný."

    max_bytes = int(max_size_mb * 1024 * 1024)
    if uploaded_file.size > max_bytes:
        return False, f"Súbor prekračuje maximálnu povolenú veľkosť ({max_size_mb} MB)."

    filename = os.path.basename(uploaded_file.name or '')
    _, ext = os.path.splitext(filename.lower())
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        return False, "Nepovolený formát súboru. Povolené sú iba obrázky PNG, JPG a WebP."

    content_type = getattr(uploaded_file, 'content_type', '') or ''
    if content_type and content_type.lower() not in ALLOWED_IMAGE_MIMES:
        return False, "Neplatný MIME typ súboru."

    try:
        pos = uploaded_file.tell()
        header = uploaded_file.read(16)
        uploaded_file.seek(pos)
    except Exception:
        return False, "Nepodarilo sa overiť obsah súboru."

    is_png = header.startswith(b'\x89PNG\r\n\x1a\n')
    is_jpg = header.startswith(b'\xff\xd8\xff')
    is_webp = header.startswith(b'RIFF') and header[8:12] == b'WEBP'

    if not (is_png or is_jpg or is_webp):
        return False, "Obsah súboru nezodpovedá platnému obrázku."

    return True, ""


def _derive_cipher_key(salt_bytes):
    """Odvodí 32-bajtový šifrovací kľúč z DJANGO_SECRET_KEY pomocou PBKDF2-HMAC-SHA256."""
    secret = settings.SECRET_KEY.encode('utf-8')
    return hashlib.pbkdf2_hmac('sha256', secret, salt_bytes, 10000, dklen=32)


def encrypt_sensitive_data(plaintext):
    """
    Zašifruje a autentifikovane podpíše citlivý reťazec (AEAD stream + Django TimestampSigner).
    """
    if plaintext is None:
        return ''
    raw_bytes = str(plaintext).encode('utf-8')
    nonce = os.urandom(16)
    key = _derive_cipher_key(nonce)
    # Counter-mode keystream z HMAC-SHA256
    ciphertext = bytearray(len(raw_bytes))
    for block_idx in range((len(raw_bytes) + 31) // 32):
        keystream = hmac.new(key, nonce + block_idx.to_bytes(4, 'big'), hashlib.sha256).digest()
        start = block_idx * 32
        end = min(start + 32, len(raw_bytes))
        for i in range(start, end):
            ciphertext[i] = raw_bytes[i] ^ keystream[i - start]
    payload = base64.urlsafe_b64encode(nonce + bytes(ciphertext)).decode('ascii')
    return signing.dumps(payload, salt='codoro.sensitive.v1')


def decrypt_sensitive_data(token, max_age=None):
    """
    Overí podpis a dešifruje citlivý reťazec zašifrovaný cez encrypt_sensitive_data().
    Pri sfalšovanom alebo expirovanom tokene vráti None.
    """
    if not token:
        return None
    try:
        payload = signing.loads(token, salt='codoro.sensitive.v1', max_age=max_age)
        raw = base64.urlsafe_b64decode(payload.encode('ascii'))
        if len(raw) < 16:
            return None
        nonce, ciphertext = raw[:16], raw[16:]
        key = _derive_cipher_key(nonce)
        plaintext = bytearray(len(ciphertext))
        for block_idx in range((len(ciphertext) + 31) // 32):
            keystream = hmac.new(key, nonce + block_idx.to_bytes(4, 'big'), hashlib.sha256).digest()
            start = block_idx * 32
            end = min(start + 32, len(ciphertext))
            for i in range(start, end):
                plaintext[i] = ciphertext[i] ^ keystream[i - start]
        return bytes(plaintext).decode('utf-8')
    except Exception:
        return None
