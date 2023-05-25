"""error"""

from typing import Callable, Any


def input_error(func: Callable[..., Any]) -> Callable[..., str]:
    """Decorator for handling input errors"""
    def wrapper_input_error(*args: tuple) -> str:
        """Wrapper function for handling input errors"""
        try:
            func(*args)
            return ""

        except TypeError as error:
            return f"TypeError: {error}"
  
        except ValueError as error:
            return f"ValueError: {error}"

        except KeyError as error:
            return f"KeyError: {error}"
        
    return wrapper_input_error