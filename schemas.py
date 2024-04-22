from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, AliasChoices

class BlockStatus(str, Enum):
    """
    The status of a block in a flow
    Possible values are: 
    - ready: the block is ready to be executed
    - running: the block is currently being executed
    - success: the block was executed successfully
    """
    
    ready = 'ready'
    running = 'running'
    success = 'success'
    failed = 'failed'


class BlockTypes(str, Enum):
    """The types of blocks that can be used in a flow"""

    single_message = 'single_message'
    send_and_reply = 'send_and_reply'
    set_variables = 'set_variables'
    http_request = 'http_request'
    split_variable = 'split_variable'


class MessageChannels(str, Enum):
    """The channels where a message can be sent"""

    twilio = "twilio"
    mock = 'mock'


class Message(BaseModel):
    """A message to be sent to a recipient"""

    content: str
    to: str
    from_: str = Field(..., validation_alias=AliasChoices('from_', 'from'))
    type: str = 'text'

