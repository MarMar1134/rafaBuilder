import os
import sys
import subprocess
import shutil
import files
import logger
from checks import existsDirectoryCheck

def compileCommand(compiler: str, workDir: str, srcFiles: list[str]):
    buildDir = workDir + "\\build"

    if (not os.path.exists(buildDir)):
        os.mkdir(buildDir)

    subprocess.run(f"cd {buildDir}", shell=True)

    for file in srcFiles:
        if file.split(".").pop(1) != "cpp":
            continue
        else:
            command = compiler + " -c "

            fileName = file.split("\\")
            fileName.reverse()
            fileName = fileName.pop(0)

            command = command + file + " -o " + "build/" + fileName[:-4] + ".o"

            logger.info(f"Compiling '{fileName}'...")

            logger.debug(f"Compile command: {command}")

            subprocess.run(command, shell=True)

def linkFromBuildCommand(compiler: str, workDir: str, appName: str):
    command = compiler + " "
    buildDir = workDir + "\\build"
    binDir = workDir + "\\bin"

    if (not existsDirectoryCheck(buildDir, "Can't build as '/build' doesn't exist. Try using 'rb compile' to generate .o files")):
        sys.exit(1)

    objFiles = files.getFilesFromDir(buildDir)

    for file in objFiles:
        if (not file.split(".").pop(1) == "o"):
            continue
        
        logger.info(f"Linking '{file}'...")

        file = file.replace("\\", "/")

        command = command + file + " "

    if (not os.path.exists(binDir)):
        os.mkdir(binDir)

    

    command = command + "-o " + "bin/" + appName

    logger.debug(f"Linker command: {command}")

    return command

def linkFromCppCommand(compiler: str, workDir: str, srcFiles: list[str], appName: str):
    command = compiler

    for file in srcFiles:
        if file.split(".").pop(1) != "cpp":
            continue
        else:
            logger.info(f"Compiling '{file}'...")

            file = file.replace("\\", "/")
            command = command + " " + file

    if not os.path.exists(workDir + "\\bin"):
        os.mkdir(workDir + "\\bin")

    command = command + " -o bin/" + appName

    logger.debug(f"Compile command: {command}")

    return command

def cleanCommand(workDir: str):
    buildDir = workDir + "\\build"
    binDir = workDir + "\\bin"

    if (not os.path.exists(buildDir) and not os.path.exists(binDir)):
        logger.warning("Nothing to clean. '/build' and '/bin' don't exist")
        sys.exit(0)

    if (not os.path.exists(buildDir)):
        logger.warning("Nothing to clean. '/build' doesn't exist")

    logger.debug(f"'/build' full path: {buildDir}")
    logger.info("Removing '/build'...")

    shutil.rmtree(buildDir, ignore_errors=True)

    if (not os.path.exists(binDir)):
        logger.warning("Nothing to clean. '/bin' doesn't exist")

    logger.debug(f"'/bin' full path: {binDir}")
    logger.info("Removing '/bin'...")

    shutil.rmtree(binDir, ignore_errors=True)