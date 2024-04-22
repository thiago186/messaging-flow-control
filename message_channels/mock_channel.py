from schemas import Message

from pydantic import BaseModel, Field

class MockChannel(BaseModel):
    """A mock channel for testing purposes"""
    
    def send_message(self, message: Message, **kwargs):
        """Send a message to the recipient"""
        print(f'Sending message to {message.to} from {message.from_}: {message.content}')