from enum import Enum
import json
from uuid import uuid4
from typing import List, Optional
import logging

from pydantic import AliasChoices, BaseModel, Field

from blocks.blocks_factory import get_block
from blocks.set_variables_block import SetVariablesBlock
from blocks.split_based_on_variable_block import SplitVariableBlock
from blocks.http_request_block import HTTPBlock
from exceptions import MissingFieldException
from schemas import BlockStatus, MessageChannels

class BasicFlow(BaseModel):
    """A basic flow that runs a sequence of blocks"""

    to: str
    from_: str = Field(..., validation_alias=AliasChoices('from_', 'from'))
    flow_status: BlockStatus = BlockStatus.ready
    flow_file: str
    flow_name: str
    curr_channel: Optional[MessageChannels] = None
    next_block_name: Optional[str] = None
    curr_block_name: Optional[str] = None
    previous_block_name: Optional[str] = None
    run_next_block: Optional[bool] = False
    flow_id: str = Field(default_factory=lambda: str(uuid4()))
    blocks: Optional[list] = []
    variables: Optional[dict] = {}

    def __init__(self, **data):
        super().__init__(**data)
        self.get_flow_blocks()
        if self.curr_block_name is None:
            self.curr_block_name = self.blocks[0].name_in_flow

    def get_flow_blocks(self):
        """Get the blocks of the flow"""

        if self.blocks == []:
            if self.flow_file is None:
                raise MissingFieldException("flow_file")
            try:
                with open(f"./flows/{self.flow_file}", 'r') as file:
                    block_infos = json.load(file)
            except FileNotFoundError:
                raise FileNotFoundError(f"File {self.flow_file} not found")
                        
            for block_name in block_infos.keys():
                block_infos[block_name]['name_in_flow'] = block_name
                block_infos[block_name]['messaging_channel'] = self.curr_channel
                block_infos[block_name]['to'] = self.to
                block_infos[block_name]['from_'] = self.from_

                block = get_block(block_infos[block_name])
                self.blocks.append(block)

    def run_flow(self, event:str=None):
        """
        Run the flow. The event is passed to the first block of the flow.
        The event that triggers run function is always a string with the content sent by the user.
        """

        logging.debug(f"running flow with event: {event}")
        self.run_next_block = True
        self.flow_status = BlockStatus.running

        while self.run_next_block and (self.flow_status != BlockStatus.success and self.flow_status != BlockStatus.failed):
            logging.debug(f"########running/continuing block {self.curr_block_name}########")

            block = self.get_block_by_name(self.curr_block_name)

            if isinstance(block, SetVariablesBlock):
                block.blocks = [ block_ for block_ in self.blocks if block_.status == BlockStatus.success]
                event = self.variables
            
            if isinstance(block, HTTPBlock):
                block.variables = self.variables

            if isinstance(block, SplitVariableBlock):
                block.variables = self.variables

            # if self.previous_block_name is not None:
            #     block.previous_block = self.get_block_by_name(self.previous_block_name)
            if block.status != BlockStatus.running:
                logging.debug(f"block {block.name_in_flow} is ready. running block")
                keys_to_change = block.run_block(event)
            elif block.status == BlockStatus.running:
                logging.debug(f"block {block.name_in_flow} is running. continuing block")
                keys_to_change = block.continue_block(event)            
            
            logging.debug(f"block ran. keys to change: {keys_to_change}")
            self.update_flow_values(keys_to_change)
            
            if block.is_final_block:
                self.curr_block_name = "Stopped"
                self.flow_status = BlockStatus.success
                self.previous_block_name = block.name_in_flow
                logging.debug(f"encountered final block. stopping flow: {self}")
                self.run_next_block = False
                break
            
            if block.status == BlockStatus.success:
                logging.debug(f"block {block.name_in_flow} was successful. moving to next block")
                self.curr_block_name = block.next_block_name
                self.previous_block_name = block.name_in_flow

            # if self.curr_block_name == "terceiro_bloco":
            #     logging.debug('breadking ')
            #     break
            condition = self.run_next_block and (self.flow_status != BlockStatus.success and self.flow_status != BlockStatus.failed)
            logging.debug(f"condition: {condition}")
            # logging.debug(f"ending block run. flow: {self}")

    def get_block_by_name(self, name):
        for block in self.blocks:
            if block.name_in_flow == name:
                return block
            
        logging.debug("could not get the block")
        raise ValueError(f"Could not find block '{name}'")
            
    def update_flow_values(self, values_to_change: dict):
        """Update specified attribute values of the BasicFlow object."""
        if values_to_change is not None:
            for key, value in values_to_change.items():
                if key == "variables":
                    for var_key, var_value in value.items():
                        self.variables[var_key] = var_value
                else:
                    if isinstance(value, bool):
                        # print(f'self: {self}')
                        setattr(self, key, value)
                    else:
                        if hasattr(self, key):
                            setattr(self, key, value)
                        else:
                            # print(f"Attribute {key} not found in BasicFlow.")
                            raise AttributeError(f"Attribute {key} not found in BasicFlow.")


if __name__ == "__main__":
    
    logging.basicConfig(level=logging.DEBUG)
    from schemas import Message
    flow = BasicFlow(
        flow_file="support_example_flow.json",
        flow_name="flow1",
        curr_channel=MessageChannels.mock,
        from_="whatsapp:me",
        to="whatsapp:you"
    )
    flow.run_flow() # triggering flow
    # flow.run_flow("tudo bem, e você?")