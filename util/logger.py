import colorama

colorama.init(autoreset=True)

def configure(args):
    global vModeEnabled, qModeEnabled, dModeEnabled
    vModeEnabled = args.verbose
    qModeEnabled = args.quiet
    dModeEnabled = args.debug

def task(msg):
    print(f"{colorama.Fore.GREEN}[RAFABUILDER][TASK] {msg}")

def main(msg):
    if (not qModeEnabled):
        print(f"[RAFABUILDER][MAIN] {msg}")

def info(msg):
    if (vModeEnabled and not qModeEnabled):
        print(f"{colorama.Fore.LIGHTBLUE_EX}[RAFABUILDER][INFO] {msg}")

def debug(msg):
    if (dModeEnabled):
        print(f"{colorama.Fore.LIGHTGREEN_EX}[RAFABUILDER][DEBUG] {msg}")

def warning(msg):
    if (not qModeEnabled):
        print(f"{colorama.Fore.YELLOW}[RAFABUILDER][WARNING] {msg}")

def error(msg):
    print(f"{colorama.Fore.RED}[RAFABUILDER][ERROR] {msg}")