#!/usr/bin/env python

import json
from litellm import completion
import requests
from schema import InputSchema
from utils import get_logger
import yaml

logger = get_logger(__name__)

def main(input_: InputSchema):

    logger.info(f"Running job: {input_}")

    messages = []
    messages.append(
        {'role': 'system', 'content': input_.system_message}
    )
    messages.append(
        {'role': 'user', 'content': input_.prompt}
    )
    
    response = completion(
            model=input_.model,
            messages=messages,
            api_base=input_.api_base,
    )

    return response.choices[0].message["content"]


if __name__ == "__main__":

    with open("chat/component.yaml", 'r') as cfg_file:
        cfg = yaml.safe_load(cfg_file)

    input_ = InputSchema(
        prompt=cfg["inputs"]["prompt"],
        system_message=cfg["inputs"]["system_message"],
        model=cfg["inputs"]["model"],
        api_base=cfg["inputs"]["api_base"],
    )
    print(main(input_))