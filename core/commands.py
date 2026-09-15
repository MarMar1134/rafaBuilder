import os
import sys
import subprocess
import shutil
import logger
import fileManager.files as files
import fileManager.cache as cache
import core.attributes as attribute
import core.linker as linker

from core.attributes import Attribute
from checks import existsPathCheck

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

def linkCommand(compiler: str, workDir: str, appName: str):
    proyectAttributes = attribute.getAttributes(workDir)
    command = ""

    if (proyectAttributes[Attribute.PROJECT_TYPE] == "executable"):
        command = linker.linkExecutable(compiler, workDir, appName)
    elif (proyectAttributes[Attribute.PROJECT_TYPE] == "staticLib"):
        command = linker.linkStaticLib(workDir, appName)

    return command

def cleanCommand(workDir: str):
    buildDir = os.path.join(workDir, "build")
    binDir = os.path.join(workDir, "bin")
    cacheDir = os.path.join(workDir, "rbCache")

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

    logger.debug(f"/rbCache full path: {cacheDir}")
    logger.info(f"Removing /rbCache...")

    shutil.rmtree(cacheDir, ignore_errors=True)

def runCommand(currentDir: str, appName: str):
    execDir = currentDir + "\\bin\\"
    execCommand = ".\\bin\\" + appName

    logger.info(f"Running '{execCommand}' from '{execDir}'")

    subprocess.run(f"cd {execDir}", shell=True)
    subprocess.run(execCommand, shell=True)