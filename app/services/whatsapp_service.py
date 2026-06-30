from twilio.rest import Client
from flask import current_app


def enviar_whatsapp(phone, code):
    sid = current_app.config.get("TWILIO_ACCOUNT_SID")
    token = current_app.config.get("TWILIO_AUTH_TOKEN")
    from_whatsapp = current_app.config.get("TWILIO_WHATSAPP_NUMBER")

    if not sid or not token or not from_whatsapp:
        print("=" * 60)
        print("Twilio WhatsApp não configurado.")
        print("Código:", code)
        print("Telefone:", phone)
        print("=" * 60)
        return False

    try:
        client = Client(sid, token)

        message = client.messages.create(
            from_=from_whatsapp,
            to=f"whatsapp:{phone}",
            body=f"Metamorphose Fit: seu código de recuperação é {code}. Expira em 10 minutos."
        )

        print("WhatsApp enviado:", message.sid)
        return True

    except Exception as e:
        print("=" * 60)
        print("Erro ao enviar WhatsApp:", e)
        print("Código:", code)
        print("Telefone:", phone)
        print("=" * 60)
        return False