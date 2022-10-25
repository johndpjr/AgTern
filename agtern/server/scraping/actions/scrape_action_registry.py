from __future__ import annotations

from inspect import signature
from typing import Callable, List

from .models import ScrapeAction

registry: dict[str, ScrapeAction] = {}


def register_action(name: str, function: Callable):
    if name.lower() in registry.keys():
        raise Exception(f"The action name \"{name}\" has already been assigned!")
    # The following returns a dict-like object mapping the name of the parameter to a parameter object
    function_signature = signature(function)
    registry[name.lower()] = ScrapeAction(name=name.lower(), parameters=function_signature.parameters, execute=function)


def get_action(name: str) -> ScrapeAction | None:
    try:
        return registry[name.lower()]
    except KeyError:
        return None


def get_action_names() -> List[str]:
    return [key for key in registry.keys()]
