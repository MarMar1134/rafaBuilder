import os
import util.logger as logger
import core.commands as cmd

from fileManager.files import FilePath
from core.attributes import ProjectType

def rafaInit(args):
    cmd.initCommand(args)

def rafaCheck(workDir: str) -> bool:
    for file in os.scandir(workDir):
        if (not os.path.isfile(file)):
            continue

        if (file.name == "attributes.rafa"):
            return True

    return False

def rafaCompile(compiler: str, workDir: str, staticLibs: list[str] | None):
    logger.main("Compiling files...")

    cmd.compileCommand(compiler, workDir)

    if (staticLibs):
        for staticLib in staticLibs:
            cmd.compileCommand(compiler, workDir, staticLib)

    logger.main("Compiling complete!")

def rafaLink(compiler: str, workDir: str):
    logger.main(f"Linking files...")

    cmd.linkCommand(compiler, workDir)

    logger.main("Linking complete!")

def rafaMake(compiler: str, workDir: str, staticLibs: list[str] | None = None):
    #logger.main("Compiling files...")
    rafaCompile(compiler, workDir, staticLibs)
    #logger.main("Compiling complete!")

    #logger.main(f"Linking files...")
    rafaLink(compiler, workDir)
    #logger.main("Linking complete!")

def rafaRun(compiler: str, workDir: str, appName: str, projectType: ProjectType, staticLibs: list[str] | None = None):
    rafaMake(compiler, workDir, staticLibs)

    if (projectType == ProjectType.EXECUTABLE):
            logger.main("Starting run...")
            cmd.runCommand(workDir, appName)
            logger.main("Run complete!")

def rafaClean(workDir: str):
    cmd.cleanCommand(workDir)

def rafaRemove(workDir: str):
    cmd.cleanCommand(workDir, True)