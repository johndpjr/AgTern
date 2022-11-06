from typing import Callable, List, Union, Type, Any, Dict

from pydantic import validate_arguments, ValidationError
from pydantic.main import BaseModel
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pydantic.decorator import ValidatedFunction  # not declared in __all__

from agtern.common import LOG
from .scrape_action_registry import get_action
from .models import ScrapingContext


def parse_config(
        context: ScrapingContext,
        scraping_actions: List[dict],
        config: Union[None, Type[Any], Dict[str, Any]] = None,
        dependencies: Dict[str, Any] = None
) -> List[Callable]:
    if dependencies is None:
        dependencies = {}
    dependencies["ScrapingContext"] = context

    prepared_actions = []
    company_name = context.company
    action_num = 0
    for action_config in scraping_actions:
        action_num += 1
        if "action" not in action_config:
            LOG.error(f"Action {company_name}:{action_num} does not have an \"action\" property. Skipping!")
            continue
        action_name = action_config["action"]
        action = get_action(action_name)
        if action is None:
            LOG.error(f"Unknown action {company_name}:{action_num} ({action_name}). Skipping!")
            continue

        # Assign parameters and inject dependencies
        parameters_dict = {}
        for parameter_name, parameter in action.parameters.items():
            annotation = parameter.annotation
            if annotation in dependencies:
                parameters_dict[parameter_name] = dependencies[annotation]
            elif parameter_name in action_config:
                parameters_dict[parameter_name] = action_config[parameter_name]

        def wrap_action(action, parameters_dict):
            """Returns a wrapped version of action.execute that validates parameters before executing"""

            def wrapper():
                """Logs to the console, validates parameters, then calls action.execute"""
                arg_strings = []
                for name, value in parameters_dict.items():
                    if isinstance(value, str):
                        arg_strings.append(f"{name}=\"{value}\"")
                    else:
                        arg_strings.append(f"{name}={value}")
                LOG.debug(f"Executing action {action.name}({', '.join(arg_strings)})")
                try:
                    # Create validator and validate arguments
                    validator: ValidatedFunction = validate_arguments(config=config)(action.execute).vd
                    # Attempt to call the function
                    validator.call(**parameters_dict)
                except ValidationError as errors:
                    LOG.error(errors)

            return wrapper

        prepared_action = wrap_action(action, parameters_dict)
        prepared_action.action = action
        prepared_action.parameters_dict = parameters_dict
        prepared_actions.append(prepared_action)
    return prepared_actions
