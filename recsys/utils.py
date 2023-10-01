import ast

from typing import List


def parse(parsed_column) -> List:
    L = []
    for i in ast.literal_eval(parsed_column):
        L.append(i['name'])
    return L

