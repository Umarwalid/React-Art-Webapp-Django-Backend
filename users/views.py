import os
import json
import logging
import firebase_admin
from firebase_admin import auth
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login
from django.contrib.auth.models import User
from .authentication import FirebaseAuthentication
import environ
from pathlib import Path

# Set up logging
logger = logging.getLogger(__name__)

# Define the base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize environment variables
env = environ.Env(
    DEBUG=(bool, False)
)


env_file = os.path.join(BASE_DIR, '.env')
if os.path.exists(env_file):
    environ.Env.read_env(env_file)

# Initialize Firebase Admin SDK if not already initialized
try:
    if not firebase_admin._apps:
        firebase_config = {
            "type": env('FIREBASE_TYPE'),
            "project_id": env('FIREBASE_PROJECT_ID'),
            "private_key_id": env('FIREBASE_PRIVATE_KEY_ID'),
            "private_key": env('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),
            "client_email": env('FIREBASE_CLIENT_EMAIL'),
            "client_id": env('FIREBASE_CLIENT_ID'),
            "auth_uri": env('FIREBASE_AUTH_URI'),
            "token_uri": env('FIREBASE_TOKEN_URI'),
            "auth_provider_x509_cert_url": env('FIREBASE_AUTH_PROVIDER_X509_CERT_URL'),
            "client_x509_cert_url": env('FIREBASE_CLIENT_X509_CERT_URL'),
        }

        # Initialize Firebase Admin SDK with the configuration
        cred = firebase_admin.credentials.Certificate(firebase_config)
        firebase_admin.initialize_app(cred)
except KeyError as e:
    logger.error(f'Missing environment variable for Firebase configuration: {str(e)}')
except ValueError as e:
    logger.error(f'Error in Firebase configuration: {str(e)}')
except Exception as e:
    logger.error(f'Unexpected error initializing Firebase Admin SDK: {str(e)}')
    raise

@csrf_exempt
def firebase_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            id_token = data.get('idToken')
            
            if not id_token:
                return JsonResponse({'status': 'error', 'message': 'ID token is required'}, status=400)
            
            # Verify the Firebase ID token
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token['uid']  
            email = decoded_token.get('email') 
            
          
            user, created = User.objects.get_or_create(username=uid, defaults={'email': email})
            
            login(request, user)
            
            
            return JsonResponse({'status': 'success', 'message': 'User logged in successfully'})
        
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format'}, status=400)
        except auth.InvalidIdTokenError:
            return JsonResponse({'status': 'error', 'message': 'Invalid ID token'}, status=400)
        except auth.ExpiredIdTokenError:
            return JsonResponse({'status': 'error', 'message': 'ID token expired'}, status=400)
        except auth.RevokedIdTokenError:
            return JsonResponse({'status': 'error', 'message': 'ID token revoked'}, status=400)
        except Exception as e:
           
            logger.error(f'Unexpected error: {str(e)}')
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
