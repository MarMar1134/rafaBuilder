import os
import util.logger as logger
import core.commands as cmd

from fileManager.files import FilePath

def rafaInit(args):
    cmd.initCommand(args)

def rafaCheck(workDir: str) -> bool:
    for file in os.scandir(workDir):
        if (not os.path.isfile(file)):
            continue

        if (file.name == "attributes.rafa"):
            return True

    return False

def rafaCompile(compiler: str, workDir: str, filePaths: list[FilePath]):
    logger.main("Compiling files...")

    cmd.compileCommand(compiler, workDir, filePaths)

    logger.main("Compiling complete!")

def rafaLink(compiler: str, workDir: str, appName: str):
    logger.main(f"Linking files...")

    cmd.linkCommand(compiler, workDir, appName)

    logger.main("Linking complete!")

def rafaMake(compiler: str, workDir: str, filePaths: list[FilePath], appName: str):
    logger.main("Compiling files...")
    cmd.compileCommand(compiler, workDir, filePaths)
    logger.main("Compiling complete!")

    logger.main(f"Linking files...")
    cmd.linkCommand(compiler, workDir, appName)
    logger.main("Linking complete!")

def rafaRun(compiler: str, workDir: str, filePaths: list[FilePath], appName: str, projectType: str):
    if (projectType == "executable" and os.path.exists(os.path.join(workDir, "bin", appName + ".exe"))):
        logger.info("Running directy, as compilation wasn't needed")
        cmd.runCommand(workDir, appName)
        return

    cmd.compileCommand(compiler, workDir, filePaths)
        
    cmd.linkCommand(compiler, workDir, appName)

    if (projectType == "executable"):
            cmd.runCommand(workDir, appName)

def rafaClean(workDir: str):
    cmd.cleanCommand(workDir)

def rafaRemove(workDir: str):
    cmd.cleanCommand(workDir, True)