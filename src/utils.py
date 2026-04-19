import json
from typing import Callable

from d2functions import *
from d3functions import *


def load_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


def load_functions(
    configs: dict[str, list[dict[str, float]]],
) -> dict[str, tuple[Callable, str]]:
    functions = {}

    for func_name, params_list in configs.items():
        func = globals().get(func_name)

        if func is not None:
            for param in params_list:
                display_label = param.pop("label", None)
                params_str = "_".join(f"{k}:{v}" for k, v in param.items())
                functions[display_label] = [
                    lambda *args, f=func, p=param: f(*args, **p),
                    params_str,
                ]
        else:
            print(f"⚠️ 警告: 在 utils.py 的全局空间中找不到名为 '{func_name}' 的函数。")

    return functions
