import os
import sys
import subprocess
import logger
import core.attributes as attribute
import core.commands as cmd

def rafaCheck(workDir: str) -> bool:
    for file in os.scandir(workDir):
        if (not os.path.isfile(file)):
            continue

        if (file.name == "attributes.rafa"):
            return True

    return False

def rafaCompile(compiler: str, workDir: str, filePaths: list[str]):
    logger.main("Compiling files...")

    cmd.compileCommand(compiler, workDir, filePaths)

    logger.main("Compiling complete!")

def rafaLink(compiler: str, workDir: str, appName: str):
    command = cmd.linkCommand(compiler, workDir, appName)

    logger.main(f"Linking files...")
    logger.debug(f"Link command: '{command}'")

    subprocess.run(command, shell=True)

    logger.main("Linking complete!")

def rafaMake(compiler: str, workDir: str, filePaths: list[str], appName: str):
    logger.main("Compiling files...")
    cmd.compileCommand(compiler, workDir, filePaths)
    logger.main("Compiling complete!")

    logger.main(f"Linking files...")
    subprocess.run(cmd.linkCommand(compiler, workDir, appName))
    logger.main("Linking complete!")

def rafaRun(compiler: str, workDir: str, filePaths: list[str], appName: str):
    proyectAttributes = attribute.getAttributes(workDir)

    if (proyectAttributes[attribute.Attribute.PROJECT_TYPE] != "executable"):
        logger.error(f"Can't run non-executable app '{proyectAttributes[attribute.Attribute.APP_NAME]}'. Try configuring your project as 'executable'")
        sys.exit(1)

    cmd.compileCommand(compiler, workDir, filePaths)
        
    subprocess.run(cmd.linkCommand(compiler, workDir, appName))

    cmd.runCommand(workDir, appName)

    logger.main("Run complete!")

def rafaClean(workDir: str):
    cmd.cleanCommand(workDir)
    