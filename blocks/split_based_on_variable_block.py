import logging
from typing import Any, Optional

from pydantic import Field

from blocks.basicBlock import BasicBlock
from schemas import BlockStatus

"""
The SplitVariableBlock is a block that splits the flow based on a variable.
You can set the variable to be used in the flow just by declaring
{
    "variable": "x"
    "branches": {
        "1": "block_name1",
        "2": "block_name2",
        "default": "block_name3"
        "on_error": "block_name4"
    }
}
The branches are the possible values of the variable and the block that will be executed if the condition is met.
"""


class SplitVariableBlock(BasicBlock):
    """A block that splits the flow based on a variable"""

    variable: str
    variables: dict = {}
    branches: dict
    next_block_name: Optional[str] = None


    def run_block(self, event):
        """
        Run the block
        """
        logging.debug(f"running split block with variable {self.variable}")
        logging.debug(f"variables: {self.variables}")
        logging.debug(f"variable value: {self.variables[self.variable]}")
        try:
            for condition in self.branches.keys():
                logging.debug(f"checking for condition {condition}")
                if str(self.variables[self.variable]) == str(condition):
                    logging.debug(f"Condition {condition} met for variable {self.variable}")
                    self.next_block_name = self.branches[condition]
                    break
            if self.next_block_name is None:
                logging.debug(f"No condition met. Running none_met branch")
                self.next_block_name = self.branches.get('default', None)

            self.status = BlockStatus.success
            self.run_next_block = True

        except Exception as e:
            logging.error(f"Error splitting flow: {e}")
            self.status = BlockStatus.failed
            self.next_block_name = self.branches.get('on_error', None)
            if self.next_block_name is None:
                self.run_next_block = False
                self.is_final_block = True


        return {
            "next_block_name": self.next_block_name,
            "run_next_block": True
        }