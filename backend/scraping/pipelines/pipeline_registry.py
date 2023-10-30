from typing import Any, Callable, Union


class Pipeline:
    def __init__(self, action_name: str, company_name: str, function: Callable):
        self.action_name = action_name
        self.company_name = company_name
        self.function = function

    @property
    def name(self):
        return f"{self.company_name}:{self.action_name}".lower()

    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)


registry: dict[str, dict[str, Pipeline]] = {}


def register_pipeline(pipeline: str, company_name: str, function: Callable):
    name = f"{company_name}:{pipeline}".lower()
    if company_name not in registry.keys():
        registry[company_name] = {}
    elif pipeline in registry[company_name].keys():
        raise Exception(f'The action name "{name}" has already been assigned!')
    registry[company_name][pipeline] = Pipeline(pipeline, company_name, function)


def get_pipeline(pipeline: str, company_name: str) -> Union[Pipeline, None]:
    try:
        return registry[company_name][pipeline]
    except KeyError:
        return None


def get_pipelines_for_company(company_name: str) -> dict[str, Pipeline]:
    try:
        return registry[company_name]
    except KeyError:
        return {}


def get_pipeline_names() -> list[str]:
    names = []
    for company_name in registry.keys():
        for action_name in registry[company_name].keys():
            names.append(f"{company_name}:{action_name}".lower())
    return names


def noop(*args, **kwargs):
    return None


def pipeline_decorator(
    pipeline_name: str, before: Callable = noop, after: Callable = noop
) -> Callable:
    """Returns a decorator that returns a function that registers a pipeline with the specified name."""

    def decorator_declared(company_name: str) -> Callable:
        """Returns a decorator that registers a pipeline for the specified company."""

        def decorator_called(function: Callable) -> Callable:
            """Registers a pipeline. Returns the function unchanged."""

            def function_executed(*args, **kwargs) -> Any:
                """Returns a function unchanged."""
                # TODO: Dependency injection based on function signature?
                before()
                return_value = function(*args, **kwargs)
                after()
                return return_value

            register_pipeline(pipeline_name, company_name, function_executed)
            return function_executed

        return decorator_called

    return decorator_declared
