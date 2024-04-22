from typing import Optional, List

from pydantic import AliasChoices, BaseModel, Field

from schemas import BlockStatus, MessageChannels

class BasicBlock(BaseModel):
    """A basic block in a flow"""

    status: BlockStatus = BlockStatus.ready
    name_in_flow: str
    next_block_name: str
    # previous_block: Optional['BasicBlock'] = None
    run_next_block: bool = Field(default=False, description='Whether to run the next block immediately after sending the message')
    inbound: Optional[str] = None
    outbound: Optional[str] = None
    is_final_block: bool = False

    def run_block(self, event=None):
        """Run the block"""
        pass

    def continue_block(self, event=None):
        """
        Continue running the block. Usefull for blocks like send_and_reply
        that continues it's execution during more than one event.
        """
        pass

    def reset_block(self):
        """Reset the block to its initial state"""
        pass

class BaseMessageBlock(BasicBlock):
    """A block that sends a message to the recipient"""
    sending_content: str
    messaging_channel: MessageChannels
    to: str
    from_: str = Field(..., validation_alias=AliasChoices('from_', 'from'))




if __name__ == '__main__':
    block = BasicBlock(
        name_in_flow='primeiro_bloco',
        next_block_name='segundo_bloco',
    )
    #print(block)