
import firebase_admin
from firebase_admin import credentials
from app.core.dependencies import get_service_account_credentials


def initialize_firebase():
    """Initialize Firebase Admin SDK with service account credentials."""
    try:
        # Check if Firebase is already initialized
        firebase_admin.get_app()
        print("Firebase already initialized")
    except ValueError:
        # Firebase not initialized, initialize it
        service_account_path = get_service_account_credentials()

        cred = credentials.Certificate(service_account_path)

        firebase_admin.initialize_app(cred)
        print("✅ Firebase initialized successfully")

