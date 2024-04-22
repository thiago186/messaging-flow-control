from pydantic import BaseModel

from schemas import Message, MessageChannels


def get_channel(channel: MessageChannels) -> BaseModel:
    """Get the channel object based on the channel type"""

    
    if channel == MessageChannels.mock:
        from message_channels.mock_channel import MockChannel
        return MockChannel()
    
    raise ValueError(f'Channel {channel} is not supported')
    


if __name__ == '__main__':
    msg = Message(content='Hello, World!', to='555-555-5555', from_='555-555-5556')
    channel = get_channel(MessageChannels.mock)
    channel.send_message(msg)