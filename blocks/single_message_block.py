from typing import Optional
import logging

from pydantic import BaseModel, Field

from blocks.basicBlock import BaseMessageBlock
from exceptions import MissingFieldException
from message_channels.channels_factory import get_channel
from schemas import BlockStatus, Message, MessageChannels


class SingleMessageBlock(BaseMessageBlock):
    """A block that sends a single message to the recipient. It does not wait for a response."""

    message: Optional[Message] = None

    def __init__(self, **data):
        super().__init__(**data)

        
    def run_block(self, event=None):
        """Send the message and update the status of the block"""

        if self.messaging_channel is None:
            raise MissingFieldException("messaging_channel")

        if self.status == BlockStatus.ready:

            self.message = Message(
                to=self.to,
                from_=self.from_,
                content=self.sending_content,
            )

            channel = get_channel(self.messaging_channel)
            channel.send_message(self.message)
            self.outbound = self.message.content
            self.status = BlockStatus.success
            self.run_next_block = True

            return {
                "next_block_name": self.next_block_name,
                "run_next_block": self.run_next_block,
            }

        else:
            logging.info("This block has already been executed. Not running again.")

    def continue_block(self, event=None):
        """Continue to the next block"""
        logging.info("This block has no method continue_block()")

    def reset_block(self):
        """Reset the block to its initial state"""
        self.status = BlockStatus.ready
        self.run_next_block = False


if __name__ == "__main__":
    block = SingleMessageBlock(
        messaging_channel=MessageChannels.mock,
        name_in_flow="primeiro_bloco",
        message=Message(
            content="Teste de primeira msg", to="123456789", from_="987654321"
        ),
        next_block="segundo_bloco",
    )
