from .libs import Callable, Any, sys
from .logger import logger

def exception_handler(*exceptions, cause: str='', do_this: Callable=sys.exit) -> Callable[[Any], Any]:
    def __decorator__(func: Callable) -> Callable[[Any], Any]:
        def __wrapper__(*args, **kwargs) -> Any:
            try:
                results = func(*args, **kwargs)
            except exceptions as err:
                if cause:
                    logger(f"\n{cause}", severity=1)

                else:
                    logger(f"\n{err}", severity=1)

                do_this()

            else:
                return results

        return __wrapper__
    return __decorator__
