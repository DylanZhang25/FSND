import os
import secrets

from dotenv import load_dotenv
load_dotenv()

'''
@COMPLETED_7
Third-Party Authentication

CRITERIA:
- Configure third-party authentication systems

MEETS SPECIFICATIONS:
- Auth0 is set up and running at the time of submission. All required 
  configuration settings are included in a bash file which export:
    - The Auth0 Domain Name
    - The JWT code signing secret
    - The Auth0 Client ID
'''


'''
@COMPLETED_8
Third-Party Authentication

CRITERIA:
- Configure roles-based access control (RBAC)

MEETS SPECIFICATIONS:
- Roles and permission tables are configured in Auth0.
- Access of roles is limited. Includes at least two different roles with 
  different permissions.
- The JWT includes the RBAC permission claims.
'''


class DatabaseConfig:
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Auth0Config:
    AUTH0_AUDIENCE = os.getenv('AUTH0_AUDIENCE')
    AUTH0_RESPONSE_TYPE_ACCESS_TOKEN = os.getenv(
        'AUTH0_RESPONSE_TYPE_ACCESS_TOKEN')
    AUTH0_RESPONSE_TYPE_ID_TOKEN = os.getenv(
        'AUTH0_RESPONSE_TYPE_ID_TOKEN')
    AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
    AUTH0_REDIRECT_URI = os.getenv('AUTH0_REDIRECT_URI')
    AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
    AUTH0_ALGORITHMS = os.getenv('AUTH0_ALGORITHMS')

    @staticmethod
    def get_auth0_url_for_id_token():
        nonce = secrets.token_hex(8)
        # Build Auth0 Login URL,
        # And add nonce at the end of the url to get Auth0 id-token
        auth0_url_for_id_token = (
            f"https://{Auth0Config.AUTH0_DOMAIN}/authorize?"
            f"audience={Auth0Config.AUTH0_AUDIENCE}&"
            f"response_type={Auth0Config.AUTH0_RESPONSE_TYPE_ID_TOKEN}&"
            f"client_id={Auth0Config.AUTH0_CLIENT_ID}&"
            f"redirect_uri={Auth0Config.AUTH0_REDIRECT_URI}&"
            f"nonce={nonce}&"
            f"scope=openid profile"
        )
        return auth0_url_for_id_token

    @staticmethod
    def get_auth0_url_for_access_token():
        # Build Auth0 Login URL to get Auth0 access_token
        auth0_url_for_access_token = (
            f"https://{Auth0Config.AUTH0_DOMAIN}/authorize?"
            f"audience={Auth0Config.AUTH0_AUDIENCE}&"
            f"response_type={Auth0Config.AUTH0_RESPONSE_TYPE_ACCESS_TOKEN}&"
            f"client_id={Auth0Config.AUTH0_CLIENT_ID}&"
            f"redirect_uri={Auth0Config.AUTH0_REDIRECT_URI}"
        )
        return auth0_url_for_access_token
