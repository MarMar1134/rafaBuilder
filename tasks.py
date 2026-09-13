import os
import subprocess
import files
import logger
import commands as cmd

def rafaCompile(compiler: str, workDir: str, srcFiles: list[str]):
    cmd.compileCommand(compiler, workDir, srcFiles)

def rafaLink(compiler: str, workDir: str, appName: str):
    command = cmd.linkFromBuildCommand(compiler, workDir, appName)

    subprocess.run(command, shell=True)

def rafaMake(compiler: str, workDir: str, srcFiles: list[str], appName: str):
    command = cmd.linkFromCppCommand(compiler, workDir, srcFiles, appName)

    subprocess.run(command, shell=True)

def rafaRun(compiler: str, workDir: str, srcFiles: list[str], appName: str):
    command = cmd.linkFromCppCommand(compiler, workDir, srcFiles, appName)

    subprocess.run(command, shell=True)

    logger.main("Compilation complete!")

    files.runProgram(workDir, appName)

def rafaClean(workDir: str):
    cmd.cleanCommand(workDir)

    logger.main("Compilation complete!")

def rafaCheck(workDir: str) -> bool:
    for file in os.scandir(workDir):
        if (not os.path.isfile(file)):
            continue

        if (file.name == "attributes.rafa"):
            return True

    return False
    