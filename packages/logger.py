from .libs import datetime, inspect, Table, Style, os, log_console

TIME = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S").replace(' ', '_')
DEBUG_FLAG = False
OFFSET = 9

COLOR = {
    5: "[blue]{}[/]",
    4: "[green]{}[/]",
    3: "[purple]{}[/]",
    2: "[salmon1]{}[/]",
    1: "[red]{}[/]",
}

SEVERITY = {
    5: 'DEBUG',
    4: 'INFO',
    3: 'NOTICE',
    2: 'WARNING',
    1: 'ERROR',
}

def logger(
    *msgs, filename: str=f"logFile.log",
    severity: int=4, color: str='', save: bool=False,
    flush: bool=False, nameno:str='' ,lineno: int=0
) -> None:
    """
        Show logs in stdin

        @parmas:
            path: select path to save the log-file
            severity: priority of log
            color: set specific color for msgs
            save: save or not log to log-file
            flush: print live log in begging of line

        SUPPORTED COLOR:
            red
            green
            yellow
            blue
            purple
            cyan
                        cyan
            white
            black
            dark_orange
            medium_violet_red
            slate_blue3
            grey74
            hot_pink
            gold1
            orange4
 
        LOG STYLE:
            Console:
                [SEVERITY]. MSG
            logFile:
                DATE CLOCK [SEVERITY]. MSG

        SEVERITY:
            = 5: DEBUG
            = 4: INFO
            = 3: NOTICE
            = 2: WARNING
            = 1: ERROR
    """

    if severity == 5 and not DEBUG_FLAG: return
    # if color: assert color in SUPPORTED_COLOR, f"Invalid Specific {color=} for msg"

    date, clock = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S').split(' ')

    for msg in msgs:
        if save:
            with open(f"./{TIME}_{filename}", mode='a') as log_file:
                log_file.write(
                    f"{date} {clock} [{SEVERITY.get(severity)}], {msg}\n"
                )

        text_clock = f"| {clock}"
        text_severity = f"[{COLOR.get(severity).format(SEVERITY.get(severity))}]"
        text_msg = f"{'[{}]'.format(color) if color else ''}{msg}".strip()
        if not lineno and not nameno:
            name_path = inspect.getouterframes(inspect.currentframe())[1].filename.split('/')[-1]
            line_path = inspect.getouterframes(inspect.currentframe())[1].lineno
        else:
            name_path = nameno
            line_path = lineno

        text_path = f"{name_path}:{line_path}"
        width_msg = os.get_terminal_size().columns - 3 - (len(text_clock) + OFFSET + len(text_path))

        grid = Table.grid(padding=(0, 1))
        grid.add_column(style=Style(color='cyan'))
        grid.add_column(width=OFFSET)
        grid.add_column(width=width_msg)
        grid.add_column(style=Style(italic=True))

        grid.add_row(text_clock, text_severity, text_msg, text_path)
        log_console.print(grid, end='\r' if flush else '\n')
