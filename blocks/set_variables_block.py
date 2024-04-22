import ast
import logging

from typing import Any, Dict

from blocks.basicBlock import BasicBlock
from schemas import BlockStatus

"""
The SetVariablesBlock is a block that sets variables to be used in the flow.
You can set variables with static values just by declaring
"variables": {"x": 1}

You can also use the inbound/outbound values of other blocks by using the following syntax:
"variables": {
    "x": "{{block_name.outbound}}",
    "y": "{{block_name2.inbound}}"
    }

To break down the value from another block into a dictionary, you can use the following syntax:
The outbound value will be converted to a dictionary, and the subvalue will be extracted from it.
"variables": {
                "x": "{{block_name.outbound.subvalue}}"
            }
"""



class SetVariablesBlock(BasicBlock):
    
    original_variables: dict = {}
    variables: dict = {}
    blocks: list = []

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self.original_variables = self.variables.copy()

    def run_block(self, data: Dict[str, Any]) -> Dict[str, Any]:

        self.variables = self.update_dinamic_values()

        if self.variables is not None:
            for field, value in self.variables.items():
                logging.debug(f"Setting variable {field} to {value}")
                data[field] = value

        self.status = BlockStatus.success
        self.run_next_block = True
        return {
            "next_block_name": self.next_block_name,
            "run_next_block": self.run_next_block,
            "variables": data
            }
    
    def get_block_value(self, block_name, boundarie_type: str):
        """Get the value of a variable in a block. boundarie_type needs to be 'inbound' or 'outbound'"""
        for block in self.blocks:
            logging.debug(f"block name: {block.name_in_flow}")
            if block.name_in_flow == block_name:
                logging.debug(f"block found: {block.name_in_flow}")
                atribute_value = getattr(block, boundarie_type)
                if atribute_value:
                    return atribute_value
                else:
                    logging.debug(f"block {block_name} has no {boundarie_type} value")
                    return ""
            
        return None
    
    def get_query_info(self, variable_str: str):
        """
        Gets the block_name and value to be extracted based on a formatted string
        INPUTS:
            variable_str: a string formatted as '{{block_name.value}}'

        OUTPUTS:
            block_name: the name of the block
            value: the value to be extracted from the block
        """

        text_inside = variable_str.split("{{")[-1].split("}}")[0]

        if len(text_inside.split(".")) == 2:
            block_name, value = text_inside.split(".")
            dict_key = None
        elif len(text_inside.split(".")) == 3:
            block_name, value, dict_key = text_inside.split(".")

        return block_name, value, dict_key

    
    def update_dinamic_values(self):
        """
        Updates all values inside self.variables that are formatted as '{{block_name.value}}'
        """
        self.variables = self.original_variables.copy()
        if self.variables is not None:
            for key, value in self.variables.items():
                value = str(value)
                if '{{' in value and '}}' in value:
                    logging.debug(f"updating value: {value}")
                    block_name, boundarie_type, dict_value = self.get_query_info(value)
                    self.variables[key] = self.get_block_value(block_name, boundarie_type)
                    if dict_value:
                        logging.debug(f"retrieving value from dictionary: {dict_value}")
                        self.variables[key] = self.variables[key][dict_value]

        return self.variables
    

if __name__ == "__main__":
    block = SetVariablesBlock(
        name_in_flow="primeiro_bloco",
        next_block_name="segundo_bloco",
        variables={"nome": "Gabriel", "idade": 22},
    )
    to_be_updated = {
        "new_var": "1",
        "idade": 23
    }
    block.run_block() #triggering the block
    msg = "Teste de resposta do usuário"
    block.run_block() #receiving user answer
    # print(block)