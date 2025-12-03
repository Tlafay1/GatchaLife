from rest_framework.authentication import SessionAuthentication

class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    SessionAuthentication without CSRF check.
    This is needed because the app is designed to work without explicit authentication
    (using the first user), but when an admin is logged in, the session cookie is sent,
    triggering CSRF checks which fail because the frontend doesn't handle CSRF tokens.
    """
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening
