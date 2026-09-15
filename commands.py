import os
import sys
import subprocess
import shutil
import logger
import fileManager.files as files
import fileManager.cache as cache
from checks import existsDirectoryCheck

def compileCommand(compiler: str, workDir: str, filePaths: list[str]):
    buildDir = os.path.join(workDir , "build")

    if (not os.path.exists(buildDir)):
        os.mkdir(buildDir)

    subprocess.run(f"cd {buildDir}", shell=True)

    for filePath in filePaths:
        if (filePath.split(".").pop(1) != "cpp"):
            continue
        else:
            _, cachedDate = cache.readCache(files.getFileName(filePath))

            logger.debug(f"File date: '{os.path.getmtime(filePath)}'; cached date: '{cachedDate}'")

            if (cachedDate == str(os.path.getmtime(filePath))):
                logger.info(f"File '{files.getFileName(filePath)}' didn't needed to be recompiled")
                continue

            command = compiler + " -c "

            fileName = filePath.split("\\")
            fileName.reverse()
            fileName = fileName.pop(0)

            command = command + filePath + " -o " + "build/" + fileName[:-4] + ".o"

            logger.info(f"Compiling '{fileName}'...")
            logger.debug(f"Compile command: {command}")

            cache.writeFileToCache(filePath)

            subprocess.run(command, shell=True)

def linkFromBuildCommand(compiler: str, workDir: str, appName: str):
    command = compiler + " "
    buildDir = os.path.join(workDir, "build")
    binDir = os.path.join(workDir, "bin")

    if (not existsDirectoryCheck(buildDir, "Can't build as '/build' doesn't exist. Try using 'rb compile' to generate .o files")):
        sys.exit(1)

    objFiles = files.getFilePathsFromDir(buildDir)

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

def linkFromSourceCommand(compiler: str, workDir: str, srcFiles: list[str], appName: str):
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

def runCommand(currentDir: str, appName: str):
    execDir = currentDir + "\\bin\\"
    execCommand = ".\\bin\\" + appName

    logger.info(f"Running '{execCommand}' from '{execDir}'")

    subprocess.run(f"cd {execDir}", shell=True)
    subprocess.run(execCommand, shell=True)