from typing import List, Union


def enforce_list(val: Union[List, str]):
    if isinstance(val, list):
        return val
    elif isinstance(val, str):
        return val.split(",")
