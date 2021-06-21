from typing import Dict, List

SEPARATOR = ","

def arr_2_str(strings: List[str]) -> str:
    return SEPARATOR.join(strings)


def str_2_arr(string: str) -> List[str]:
    return string.split(SEPARATOR)
