## Flow-Control

Flow-Control is a framework designed to create and manage a sequence of actions in a chat-based interface. This system enables the development of versatile chatbots tailored for various messaging services, offering dynamic interaction models based on user input and predefined action blocks.

## Purpose
The primary goal of Flow-Control is to simplify the integration and management of complex workflows within chat environments. By leveraging a modular approach, users can define and execute a series of conditional and sequential actions that guide conversations and perform automated tasks.

## Action blocks
Each flow is composed by action blocks. Each block performs a different type of action, from saving internal flow variables to http requests and sending a message to the user.

Currently there are 5 available action blocks: 
- Single Message Block: Sends a simple message to the user. Usefull for sending template messages that doensn't require answer.
- Send and Reply Block: Sends a message to the user and waits for a reply.
- Set variable Block: Sets an intern variable based on previous blocks to be used later in the flow.
- Http Request Block: Performs a http request to a given url. It can be used to connect to APIs like OpenAI for building LLM chatbots.
- Split Based on Variable Block: Splits the flow based on a variable value. It can be used to take different actions based on variables values.


## Quick start

Let's create a simple flow that sends a support message to the user and waits for a reply. The file must be saved inside flows directory

```json
{
  "first_block":  {
    "block_type": "send_and_reply",
    "sending_content": "Hi! How can I help you? Type 1 for support or 2 for sales.",
    "next_block_name": "set_variable",
  },
  "set_variable": {
    "block_type": "set_variables",
    "next_block_name": "split_on_answer",
    "variables": {
        "user_answer": "{{first_block.inbound}}"
    }
  },
  "split_on_answer": {
    "block_type": "split_variable",
    "variable": "user_answer",
    "branches":{
        "1": "support_msg",
        "2": "sales_msg",
        "default": "other_block",
        "on_error": "other_block"
    }
  },
    "support_msg": {
        "block_type": "single_message",
        "sending_content": "You selected support. Please wait a moment.",
        "next_block_name": "end_flow",
        "is_final_block": true
    },
    "sales_msg": {
        "block_type": "single_message",
        "sending_content": "You selected sales. Please wait a moment.",
        "next_block_name": "end_flow",
        "is_final_block": true
    },
    "other_block": {
        "block_type": "single_message",
        "sending_content": "I'm sorry, I didn't understand your answer. Please try again.",
        "next_block_name": "first_block"
    },

}
```


Now we declared the flow, let's instantiate it and run it.

```python
    from schemas import Message
    from flows import BasicFlow
    flow = BasicFlow(
        flow_file="flow1.json",
        flow_name="flow1",
        curr_channel=MessageChannels.mock,
        from_="whatsapp:me",
        to="whatsapp:you"
    )
    flow.run_flow() # triggering flow
```

