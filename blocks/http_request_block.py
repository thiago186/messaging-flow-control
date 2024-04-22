import requests

from blocks.basicBlock import BasicBlock
from schemas import BlockStatus

class HTTPBlock(BasicBlock):
    headers: dict = {}
    options: dict = {}
    body: dict = {}
    variables: dict = {} #variables that comes from the flow. Usefull for dynamic values on API routes or body

    def run_block(self, event: dict):
        
        if self.status == BlockStatus.ready:

            self.headers = self.format_dict(self.headers, self.variables)
            self.options = self.format_dict(self.options, self.variables)
            self.body = self.format_dict(self.body, self.variables)

            #print(f"formatted headers: {self.headers}")
            #print(f"formatted options: {self.options}")
            #print(f"formatted body: {self.body}")
            

            try:
                response = requests.request(
                    method=self.options.get("method", "GET"),
                    url=self.options.get("url", ""),
                    headers=self.headers,
                    json=self.body
                )
                response = response.json()
            except Exception as e:
                response = e
            

            self.status = BlockStatus.success
            self.outbound = response
            self.run_next_block = True

            return {
                "next_block_name": self.next_block_name,
                "run_next_block": self.run_next_block,
            }

    def format_dict(self, dict_: dict, variables: dict):
        #print(f'received variables: {variables}')
        #print(f"received dict: {dict_}")
        for key, value in dict_.items():
            if isinstance(value, str):
                dict_[key] = value.format(**variables)
            elif isinstance(value, dict):
                dict_[key] = self.format_dict(value, variables)
        return dict_