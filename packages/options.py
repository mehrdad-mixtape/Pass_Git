from .libs import (
    dataclasses, sys, itertools,
    Callable, Any, Dict, Tuple, List, Generator,
    Table, Text, HORIZONTALS
)
from .globalFunc import goodbye, pprint
from .colors import SUPPORTED_COLOR


@dataclasses.dataclass(slots=True, eq=False, frozen=True)
class Method:
    do_this: Callable[[Any], Any]
    has_input: bool
    type_input: type
    default_input: Any
    is_required: bool
    help_description: str


class Options:
    """
    Argument Parser!
    
    1. Make option object:
    
        option = Option()
    
    2. Assign function to option object:
    
        - Decorate function with option object
    
            @option('-s')

            def do_you_wanna_something_to_do():
                ...
            
            @option('--opt')

            def do_you_wanna_something_to_do():
                ...
            
            @option('-s', '--opt')

            def do_you_wanna_something_to_do():
                ...
            
            @option('-s', '--opt', has_input=True, type_input=type)

            def do_you_wanna_something_to_do(arg: type):
                ...

            @option('-s', '--opt', required=True)

            def do_you_wanna_something_to_do():
                ...
    """

    __slots__ = ("project_name", "__option_method", "__run_without_help", "__intro")

    def __init__(self, project_name: str, intro: str='', run_without_help: bool=True):
        self.project_name = project_name
        self.__option_method: Dict[str, Method] = {
            ('--help',): Method(self.__help, False, None, None, False, f"Show help Screen of {project_name}")
        }
        self.__intro = intro
        self.__run_without_help = run_without_help


    def __repr__(self):
        return f"Input Args: {sys.argv} to parse"


    def __call__(
            self, *options: Tuple[str],
            has_input: bool=False,
            type_input: type=None,
            default_input: Any=None,
            is_required: bool=False,
            help_description: str="...",
        ):
        """
            options: start with - or --.
            has_input: maybe the options include the argument after them.
            type_input: type of arguments after option and depends on has_input.
            default_input: get default input if user don't give enough arg to option.
            is_required: force to use option.
            help_description: the description for option about how to use option.
        """
        def __decorator__(func: Callable[[Any], Any]) -> Callable[[None], None]:

            for exist_opt in self.__option_method:
                for opt in exist_opt:
                    goodbye(
                        opt in options,
                        cause="Duplicate option=({0}) selected for [bold]{1}[/], But now [bold]{2}[/] used for [bold]{3}[/]".format(
                            opt, func.__name__, opt, self.__option_method.get(exist_opt).do_this.__name__
                        )
                    )

            self.__option_method[options] = Method(func, has_input, type_input, default_input, is_required, help_description)

        return __decorator__


    @property
    def option_method(self) -> Dict[str, Method]:
        return self.__option_method


    @property
    def all_options(self) -> List[str]:
        opt_lst: List[str] = []

        for option in self.option_method:
            for opt in option: opt_lst.append(opt)

        return opt_lst


    def parse(self) -> Generator[Tuple[Tuple[str], Any], None, None]:

        goodbye(
            len(sys.argv) < 2 and not self.__run_without_help,
            cause=f"Run program with --help for more information."
        )

        # Handle option validation and combination
        for i, opt_argv in enumerate(sys.argv, start=1):
            if not opt_argv.startswith(('-', '--')):
                continue # valid options can start with - --

            # Handle the complete-options: Example ==> --add --list --dump
            else:
                goodbye( # if user enter just - or --
                    opt_argv in ('-', '--'),
                    cause=f"Invalid option=({opt_argv})"
                )

                for option in self.option_method:
                    if opt_argv in option: # -t in ('-t', '--type') ?
                        break

                else: goodbye(True, cause=f"Invalid option=({opt_argv})")

            yield self.__executer(option, i)                

            # TODO: It's not work properly!!!
            # Convert -ald to -a -l -d and parse it individually
            # Handle the abbreviation-options: Example ==> -a -l -d
            # Handle the mixed abbreviation-options: Example ==> -ald = -dal

        # Handle is_required flag
        for option, method in self.option_method.items():
            for opt in option:
                if not (opt not in sys.argv and method.is_required == True): break

            else:
                goodbye(
                    True,
                    cause="Input CMD: {0} <missing-option>\nThis missing-option=({1}) is Required, use --help to see".format(
                        ' '.join(sys.argv), ' '.join(option)
                ))


    def __executer(self, option: Tuple[str], option_index: int) -> Any:

        method: Method = self.option_method[option]
        output: Any = None

        if not method.has_input:
            return option, method.do_this()

        try:
            arg_input = sys.argv[option_index]

            goodbye(
                method.type_input is None,
                cause=f"Get type-of-arguments=({arg_input}) after [bold]{option}[/]",
            )
            goodbye(
                method.default_input is not None
                and not isinstance(method.default_input, method.type_input),
                cause="Gave bad-default-argument=({0}) after [bold]{1}[/], type_input=[bold]{2}[/] & default_input=[bold]{3}[/] are inconsistent!".format(
                    method.default_input, option, method.type_input.__name__, method.default_input
            ))
            # script.py -r 10 -o -p good // -o in middle and it has default input
            if arg_input in self.all_options:
                goodbye(
                    method.default_input is None,
                    cause=f"Not enough-argument after [bold]{option}[/], use --help for more information.",
                )
                goodbye(
                    not isinstance(method.default_input, method.type_input),
                    cause="Gave bad-default-argument=({0}) after [bold]{1}[/], type_input=[bold]{2}[/] & default_input=[bold]{3}[/] are inconsistent!".format(
                        method.default_input, option, method.type_input.__name__, method.default_input
                ))

                return option, method.do_this(method.type_input(method.default_input))

            arg_input = method.type_input(arg_input)
            output = method.do_this(arg_input)

        except IndexError:
            goodbye(
                method.default_input is None,
                cause=f"Not enough-argument after [bold]{option}[/], use --help for more information.",
            )
            goodbye(
                not isinstance(method.default_input, method.type_input),
                cause="Gave bad-default-argument=({0}) after [bold]{1}[/], type_input=[bold]{2}[/] & default_input=[bold]{3}[/] are inconsistent!".format(
                    method.default_input, option, method.type_input.__name__, method.default_input
            ))

            # script.py -r 10 -p good -o // -o in end and it has default input
            output = method.do_this(method.type_input(method.default_input))

        except ValueError:
            goodbye(
                method.default_input is None,
                cause="Gave bad-argument=({0}) after [bold]{1}[/], type_input=[bold]{2}[/] & arg_input=[bold]{3}[/] are inconsistent!".format(
                    arg_input, option, method.type_input.__name__, arg_input
            ))

            output = method.do_this(method.default_input)

        except TypeError:
            goodbye(
                True,
                cause=f"You enabled [bold]has_input[/] for {method.do_this.__name__}(), Write input-argument for it"
            )

        return option, output


    def __help(self) -> None:
        CYCLE_COLOR = itertools.cycle(SUPPORTED_COLOR)

        table = Table(
            "Options",
            "Required",
            # "Function",
            "Help",
            box=HORIZONTALS,
            title=f"""{self.project_name}""",
        )

        pprint(self.__intro)

        for option, method in self.option_method.items():
            table.add_row(
                Text(' '.join(option), style=f"bold italic {next(CYCLE_COLOR)}"),
                Text('<<<-----' if method.is_required else '', style="bold"),
                # method.do_this.__name__,
                Text(method.help_description, justify=True),

            )

        pprint(table)
        sys.exit()
