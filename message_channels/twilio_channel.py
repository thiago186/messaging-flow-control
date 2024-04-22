
from twilio.rest import Client

from pydantic import BaseModel, Field

from settings import settings
from schemas import Message


client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
class TwilioChannel(BaseModel):
    """A Twilio channel to send messages"""

    def send_message(self, message: Message, **kwargs):
        """Send a message to the recipient"""
        message = client.messages.create(
            from_=message.from_,
            to=message.to,
            body=message.content,
        )
        
        return message


if __name__ == "__main__":
    twilio_channel = TwilioChannel()
    content ="Olá. Investidor(a)!\nÉ uma pena você ter cancelado seu trial da Suno Premium...\nPensando nisso, decidimos disponibilizar uma condição especial para um grupo seleto de pessoas, e você está dentro dele!\nPara garantir sua condição especial, você poderia me informar qual o motivo do cancelamento?"

    message = Message(
        to="whatsapp:+558182860171",
        from_=settings.twilio_phone,
        content="dps eu posso sair botando tudo"
    )
    result = twilio_channel.send_message(message)
    print("Message sent!")