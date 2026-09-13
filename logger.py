def configure(args):
    global vModeEnabled, qModeEnabled, dModeEnabled
    vModeEnabled = args.verbose
    qModeEnabled = args.quiet
    dModeEnabled = args.debug

def main(msg):
    print(f"[RAFABUILDER][MAIN] {msg}")

def info(msg):
    if (vModeEnabled and not qModeEnabled):
        print(f"[RAFABUILDER][INFO] {msg}")

def debug(msg):
    if (dModeEnabled):
        print(f"[RAFABUILDER][DEBUG] {msg}")

def warning(msg):
    if (qModeEnabled):
        print(f"[RAFABUILDER][WARNING] {msg}")

def error(msg):
    print(f"[RAFABUILDER][ERROR] {msg}")