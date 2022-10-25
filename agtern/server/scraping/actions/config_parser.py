from typing import Callable, List, Union, Type, Any, Dict

from pydantic import validate_arguments, ValidationError

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
            print(f"ERROR: Action {company_name}:{action_num} does not have an \"action\" property. Skipping!")
            continue
        action_name = action_config["action"]
        action = get_action(action_name)
        if action is None:
            print(f"ERROR: Unknown action {company_name}:{action_num} ({action_name}). Skipping!")
            continue

        # Assign parameters and inject dependencies
        parameters_dict = {}
        parameters_valid = True
        for parameter_name, parameter in action.parameters.items():
            annotation = parameter.annotation
            if annotation in dependencies:
                parameters_dict[parameter_name] = dependencies[annotation]
            elif parameter_name not in action_config:
                print(f"ERROR: Action {company_name}:{action_num} is missing required parameter "
                      f"{parameter_name}: {parameter.annotation} Skipping!")
                parameters_valid = False
                break
            else:
                parameters_dict[parameter_name] = action_config[parameter_name]
        if not parameters_valid:
            continue  # Skip this action

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
                print(f"DEBUG: Executing action {action.name}({', '.join(arg_strings)})")
                try:
                    # Create validator and validate arguments
                    validator = validate_arguments(config=config)(action.execute)
                    # Attempt to call the function
                    validator.vd.call(**parameters_dict)
                except ValidationError as errors:
                    print(errors)

            return wrapper

        prepared_actions.append(wrap_action(action, parameters_dict))
    return prepared_actions
