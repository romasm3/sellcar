
"""Site-wide visitor tracking middleware with GeoIP + bot detection."""

import os

import re

from django.conf import settings



# ─── Bot user-agent patterns (extensive list) ───

BOT_PATTERN = re.compile(

    # Search engines

    r'bot|crawl|spider|slurp|bing|yandex|baidu|duckduck|googlebot|'

    # Social/messaging previews

    r'facebookexternalhit|whatsapp|telegram|twitter|linkedin|discord|slack|'

    # SEO/scrapers

    r'semrush|ahrefs|mj12|dotbot|petalbot|screamingfrog|serpstat|megaindex|'

    # AI crawlers

    r'gptbot|chatgpt|claudebot|ccbot|perplexity|anthropic|cohere|bytespider|'

    # HTTP clients (almost always bots)

    r'python-requests|python-urllib|python/|urllib|'

    r'curl/|wget/|go-http|java/|okhttp|apache-httpclient|libwww|'

    # Headless browsers

    r'headless|phantomjs|selenium|puppeteer|playwright|chromedriver|webdriver|'

    # Monitoring

    r'uptimerobot|pingdom|statuscake|newrelic|'

    # Security scanners

    r'masscan|nmap|zgrab|sqlmap|nikto|wpscan|censysinspect|'

    # Generic

    r'scraper|fetch|http_request',

    re.IGNORECASE,

)



SKIP_PATHS = (

    '/admin/',

    '/admin-moderate/',

    '/static/',

    '/media/',

    '/ajax/',

    '/api/',

    '/favicon.ico',

    '/robots.txt',

    '/sitemap.xml',

)



# ─── Suspicious paths (bot scanners) ───

# FIX: removed `^/` anchors — match anywhere in path (catches //cms/wp-includes/)

SUSPICIOUS_PATTERNS = re.compile(

    r'\.(php|asp|aspx|jsp|cgi|env|git|sql|bak|zip|tar|log|ini)(\?|$|/)|'

    r'wp-includes|wp-admin|wp-login|wp-content|wp-json|xmlrpc|wlwmanifest|'

    r'/wordpress|/joomla|/drupal|/phpmyadmin|/phpadmin|/myadmin|/pma/|'

    r'/\.git|/\.env|/\.aws|/\.ssh|/\.htaccess|/\.DS_Store|'

    r'/cgi-bin|/admin\.php|/login\.php|/shell|/cmd|/owa/|/ecp/|/autodiscover/|'

    r'/eval|/exec|/passwd|/etc/|/proc/|/var/|/vendor/|/backup|/dump\.sql|'

    r'\.\./|%2e%2e|%2f|\.well-known/security|'

    r'/cms/|/web/|/shop/|/blog/|/wp/|/wp1/|/test/|/site/|/2019/|/2020/|/2021/',

    re.IGNORECASE,

)



# ─── GeoIP setup ───

_geoip_reader = None



def _get_geoip_reader():

    """Lazy-load GeoIP DB once, keep in memory."""

    global _geoip_reader

    if _geoip_reader is not None:

        return _geoip_reader



    try:

        import geoip2.database

        db_path = os.path.join(settings.BASE_DIR, 'data', 'GeoLite2-Country.mmdb')

        if os.path.exists(db_path):

            _geoip_reader = geoip2.database.Reader(db_path)

    except Exception as e:

        print(f"[GeoIP] init failed: {e}")

        _geoip_reader = None



    return _geoip_reader





def _lookup_country(ip):

    """Returns (country_code, country_name) or ('', '') if not found."""

    if not ip:

        return ('', '')



    if ip.startswith(('10.', '192.168.', '127.', '172.16.', '172.17.', '172.18.',

                      '172.19.', '172.20.', '172.21.', '172.22.', '172.23.',

                      '172.24.', '172.25.', '172.26.', '172.27.', '172.28.',

                      '172.29.', '172.30.', '172.31.', '169.254.')):

        return ('LOCAL', 'Local')



    reader = _get_geoip_reader()

    if not reader:

        return ('', '')



    try:

        response = reader.country(ip)

        code = response.country.iso_code or ''

        name = response.country.name or ''

        return (code, name)

    except Exception:

        return ('', '')





def detect_bot(user_agent: str, path: str) -> tuple:

    """

    Returns (is_bot, reason).

    Reason: empty_ua | ua_pattern | path_scan | ''

    """

    ua = user_agent or ''

    if not ua:

        return (True, 'empty_ua')

    if BOT_PATTERN.search(ua):

        return (True, 'ua_pattern')

    if SUSPICIOUS_PATTERNS.search(path or ''):

        return (True, 'path_scan')

    return (False, '')





class VisitorTrackingMiddleware:

    def __init__(self, get_response):

        self.get_response = get_response



    def __call__(self, request):

        self._maybe_log(request)

        return self.get_response(request)



    def _maybe_log(self, request):

        if request.method != 'GET':

            return



        path = request.path

        for skip in SKIP_PATHS:

            if path.startswith(skip):

                return



        ua = request.META.get('HTTP_USER_AGENT', '')

        is_bot, bot_reason = detect_bot(ua, path)



        xff = request.META.get('HTTP_X_FORWARDED_FOR')

        if xff:

            ip = xff.split(',')[0].strip()

        else:

            ip = request.META.get('REMOTE_ADDR')



        if not ip:

            return



        country_code, country_name = _lookup_country(ip)

        referrer = request.META.get('HTTP_REFERER', '')[:500]



        try:

            from apps.analytics.models import PageView

            PageView.objects.create(

                ip_address=ip,

                user=request.user if request.user.is_authenticated else None,

                path=path[:500],

                country=country_code[:2],

                country_name=country_name[:100],

                user_agent=ua[:500],

                is_bot=is_bot,

                bot_reason=bot_reason,

                referrer=referrer,

            )

        except Exception:

            pass

