import logging
import re

from django.core.cache import cache
from django.http import HttpResponseForbidden

logger = logging.getLogger(__name__)

# Patterns targeting vulnerabilities or configuration files (bots/scanners)
SCANNER_PATTERNS = [
    re.compile(r"\.php$", re.IGNORECASE),
    re.compile(r"\.env$", re.IGNORECASE),
    re.compile(r"/\.git", re.IGNORECASE),
    re.compile(r"^/wp-", re.IGNORECASE),
    re.compile(r"/actuator/", re.IGNORECASE),
    re.compile(r"/\.vscode/", re.IGNORECASE),
    re.compile(r"/\.idea/", re.IGNORECASE),
    re.compile(r"\.action$", re.IGNORECASE),
    re.compile(r"/xmlrpc", re.IGNORECASE),
    re.compile(r"pom\.properties$", re.IGNORECASE),
    re.compile(r"pom\.xml$", re.IGNORECASE),
    re.compile(r"/ecp/", re.IGNORECASE),
    re.compile(r"/cgi-bin/", re.IGNORECASE),
    re.compile(r"phpinfo", re.IGNORECASE),
    re.compile(r"/config\.json$", re.IGNORECASE),
    re.compile(r"/\.DS_Store$", re.IGNORECASE),
]


class BlockScannersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = self.get_client_ip(request)

        # Check if the IP is currently banned
        if cache.get(f"banned_ip_{ip}"):
            return HttpResponseForbidden(
                "Forbidden: Request blocked due to malicious scanning activity."
            )

        # Check if the requested path matches any scanner patterns
        path = request.path
        for pattern in SCANNER_PATTERNS:
            if pattern.search(path):
                # Ban the IP for 24 hours (86400 seconds)
                cache.set(f"banned_ip_{ip}", True, 86400)
                logger.warning(
                    f"Banned IP {ip} for 24 hours for requesting scanner path: {path}"
                )
                return HttpResponseForbidden(
                    "Forbidden: Request blocked due to malicious scanning activity."
                )

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            # Under a proxy (like Traefik/Coolify), X-Forwarded-For contains a list of IPs, the first is the real client
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip


class CSRFExemptForAllauthHeadless:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request is to an allauth headless endpoint
        if request.path.startswith("/_allauth/browser/v1/"):
            # Set the _dont_enforce_csrf_checks attribute
            setattr(request, "_dont_enforce_csrf_checks", True)

        response = self.get_response(request)
        return response
