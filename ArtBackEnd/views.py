from django.http import JsonResponse
from django.conf import settings

def health_check(request):
    try:
        response_data = {
  
    'status': 'healthy',
    'env_variables': {
        'DEBUG': settings.DEBUG,
        'SECRET_KEY': settings.SECRET_KEY,
        'EMAIL_HOST_USER': settings.EMAIL_HOST_USER,
        'FIREBASE_PROJECT_ID': getattr(settings, 'F_PROJECT_ID', 'Not Set'),
        'FIREBASE_PRIVATE_KEY_ID': getattr(settings, 'F_PRIVATE_KEY_ID', 'Not Set'),
        'FIREBASE_PRIVATE_KEY': getattr(settings, 'F_PRIVATE_KEY', 'Not Set'),
        'FIREBASE_CLIENT_EMAIL': getattr(settings, 'F_CLIENT_EMAIL', 'Not Set'),
        'FIREBASE_CLIENT_ID': getattr(settings, 'F_CLIENT_ID', 'Not Set'),
        'FIREBASE_AUTH_URI': getattr(settings, 'F_AUTH_URI', 'Not Set'),
        'FIREBASE_TOKEN_URI': getattr(settings, 'F_TOKEN_URI', 'Not Set'),
        'FIREBASE_AUTH_PROVIDER_X509_CERT_URL': getattr(settings, 'F_AUTH_PROVIDER_X509_CERT_URL', 'Not Set'),
        'FIREBASE_CLIENT_X509_CERT_URL': getattr(settings, 'F_CLIENT_X509_CERT_URL', 'Not Set'),
        'DJANGO_ALLOWED_HOSTS': settings.ALLOWED_HOSTS,
        'DJANGO_CORS_ALLOWED_ORIGINS': getattr(settings, 'CORS_ALLOWED_ORIGINS', 'Not Set'),
        'APPLICATION_INSIGHTS_INSTRUMENTATION_KEY': getattr(settings, 'APPLICATION_INSIGHTS_INSTRUMENTATION_KEY', 'Not Set'),
    }
}

    except Exception as e:
        response_data = {
            'status': 'unhealthy',
            'error': str(e)
        }
    return JsonResponse(response_data)
