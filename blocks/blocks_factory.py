from schemas import BlockTypes

def get_block(block_infos: dict):
    """Return the class of the block type"""

    block_type = block_infos.get('block_type')
    
    if block_type == BlockTypes.single_message:
        from blocks.single_message_block import SingleMessageBlock
        return SingleMessageBlock(**block_infos)
    
    if block_type == BlockTypes.send_and_reply:
        from blocks.send_and_reply_block import SendReplyBlock
        return SendReplyBlock(**block_infos)
    
    if block_type == BlockTypes.set_variables:
        from blocks.set_variables_block import SetVariablesBlock
        return SetVariablesBlock(**block_infos)

    if block_type == BlockTypes.http_request:
        from blocks.http_request_block import HTTPBlock
        return HTTPBlock(**block_infos)
    
    if block_type == BlockTypes.split_variable:
        from blocks.split_based_on_variable_block import SplitVariableBlock
        return SplitVariableBlock(**block_infos)

    raise ValueError(f'{block_type} is not a valid block type.')
    

import json

if __name__ == "__main__":
    with open('./flows/flow1.json', 'r') as file:
        block_infos = json.load(file)

    blocks = []
    for block_name in block_infos.keys():
        block_infos[block_name]['name_in_flow'] = block_name
        block = get_block(block_infos[block_name])
        blocks.append(block)
