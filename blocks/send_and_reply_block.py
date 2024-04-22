from typing import Optional
import logging

from pydantic import BaseModel, Field

from blocks.basicBlock import BasicBlock, BaseMessageBlock
from exceptions import MissingFieldException
from message_channels.channels_factory import get_channel
from schemas import BlockStatus, Message, MessageChannels


class SendReplyBlock(BaseMessageBlock):
    """A block that sends a message and waits for a reply"""

    message: Optional[Message] = None

    def __init__(self, **data):
        super().__init__(**data)
        self.message = Message(
            to=self.to,
            from_=self.from_,
            content=self.sending_content,
        )
        

    def run_block(self, event=None):
        """Send the message and update the status of the block"""

        logging.debug(f"received event inside send_reply_block: {event}")
        self.message.content = self.sending_content

        if isinstance(event, Message):
            self.message = event

        if self.message is None:
            raise MissingFieldException("message")

        if self.messaging_channel is None:
            raise MissingFieldException("messaging_channel")

        # if self.status == BlockStatus.ready:
        channel = get_channel(self.messaging_channel)
        channel.send_message(self.message)

        self.outbound = self.message.content
        self.status = BlockStatus.running

        return {
            "next_block_name": self.name_in_flow,
            "run_next_block": False,
        }

        # else:
        #     logging.info(
        #         "This block has already started or been executed. Not running again."
        #     )

    def continue_block(self, event=None):
        """Continue to the next block"""

        if event is not None:
            #print(f"getting user response")
            self.message.content = str(event)

        if self.status == BlockStatus.running:
            self.status = BlockStatus.success
            self.inbound = self.message.content
            self.run_next_block = True

            return {
                "next_block_name": self.next_block_name,
                "run_next_block": self.run_next_block,
            }

        else:
            logging.info(
                "This block has not been executed yet. Run the block before continuing."
            )

    def reset_block(self):
        """Reset the block to its initial state"""
        self.status = BlockStatus.ready
        self.run_next_block = False


if __name__ == "__main__":
    message_to_send = Message(
        content="Teste de primeira msg", to="123456789", from_="987654321"
    )
    block = SendReplyBlock(
        messaging_channel=MessageChannels.mock,
        name_in_flow="primeiro_bloco",
        message=message_to_send,
        reply=Message(content="Teste de resposta", to="987654321", from_="123456789"),
        next_block="segundo_bloco",
    )
    block.run_block()
    block.message.content = "essa seria a resposta teste do usuário"
    block.continue_block()
