from django.shortcuts import redirect
from django.template import TemplateDoesNotExist

class TemplateNotFoundRedirectMiddleware:
    """
    Middleware to catch TemplateDoesNotExist exceptions and redirect to a specified URL.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except TemplateDoesNotExist:
            return redirect('bill_url')  # Redirect to the billing URL
