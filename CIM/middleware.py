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
