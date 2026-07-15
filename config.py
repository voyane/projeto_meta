import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "meta-web-chave-secreta-dev"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:js123456@localhost:5432/meta_web"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
    TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"
    STORE_WHATSAPP_NUMBER = os.environ.get("STORE_WHATSAPP_NUMBER", "258845421616")
    MPESA_NUMBER = os.environ.get("MPESA_NUMBER", "845421616")
    EMOLA_NUMBER = os.environ.get("EMOLA_NUMBER", "875421616")
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
