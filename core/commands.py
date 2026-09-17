import os
import sys
import subprocess
import shutil
import util.logger as logger
import fileManager.cache as cache
import core.attributes as attribute
import core.linker as linker

from core.attributes import Attribute
from fileManager.files import FilePath
from util.checks import isSourceFileCheck

def initCommand(args):
    cache.inicializeCache()
    
    compiler = args.compiler
    srcDir = args.srcDir
    appName = args.appName
    projectType = ""
    
    attributesPath = os.path.join(os.getcwd(), "attributes.rafa")
    
    if (args.projectType == 2):
        projectType = "dynamicLib"
    elif (args.projectType == 1):
        projectType = "staticLib"
    else:
        projectType = "executable"
    
    if (os.path.exists(attributesPath)):
        logger.error(f"'attributes.rafa' already exists on working directory '{os.getcwd()}'")
        sys.exit(1)
    
    compilerAttribute = "compiler(\"" + compiler + "\")\n"
    srcDirAttribute = "srcDir(\"" + srcDir + "\")\n"
    appNameAttribute = "appName(\"" + appName + "\")\n"
    projectTypeAttribute = "projectType(\"" + projectType + "\")"
    
    attributeLines = [
        compilerAttribute,
        srcDirAttribute,
        appNameAttribute,
        projectTypeAttribute
    ]
    
    with open(attributesPath, "x") as attributesFile:
        attributesFile.writelines(attributeLines)

def compileCommand(compiler: str, workDir: str, filePaths: list[FilePath]):
    objFilePath = os.path.join(workDir , "build")

    if (not os.path.exists(objFilePath)):
        os.mkdir(objFilePath)

    subprocess.run(f"cd {objFilePath}", shell=True)

    for filePath in filePaths:
        if (not isSourceFileCheck(filePath.extension)):
            logger.debug(f"File '{filePath.name}' is a '{filePath.extension}' file")
            continue
        else:
            _, cachedDate = cache.readCache(filePath)

            if (cachedDate == filePath.date):
                logger.info(f"File '{filePath.name}' didn't needed to be recompiled")
                logger.debug(f"Skipping compiling process for '{filePath.name}', as it wasn't needed")
                continue

            command = compiler + " -c "

            command = command + filePath.path + " -o " + "build/" + filePath.name[:-4] + ".o"

            logger.info(f"Compiling '{filePath.name}'...")
            logger.debug(f"Compile command: {command}")

            cache.writeCache(filePath)

            subprocess.run(command, shell=True)

            objFilePath = FilePath(os.path.join("build", filePath.name[:-4] + ".o"))

            logger.debug(f"Object file path: '{objFilePath.path}'")

            cache.writeCache(objFilePath)

def linkCommand(compiler: str, workDir: str, appName: str):
    projectAttributes = attribute.getAttributes(workDir)

    if (projectAttributes[Attribute.PROJECT_TYPE] == "executable"):
        linker.linkExecutable(compiler, workDir, appName)
    elif (projectAttributes[Attribute.PROJECT_TYPE] == "staticLib"):
        linker.linkStaticLib(workDir, appName)
    elif (projectAttributes[Attribute.PROJECT_TYPE] == "dynamicLib"):
        linker.linkDynamicLib(compiler, workDir, appName)

def runCommand(currentDir: str, appName: str):
    #TODO: Generalize command for Linux and MacOS
    execCommand = f".\\bin\\{appName}.exe"

    logger.info(f"Running '{execCommand}' from '{currentDir}'")

    subprocess.run(execCommand, shell=True)

def cleanCommand(workDir: str, removeRafa: bool = False):
    buildDir = os.path.join(workDir, "build")
    binDir = os.path.join(workDir, "bin")
    cacheDir = os.path.join(workDir, "rbCache")

    if (not os.path.exists(buildDir) and not os.path.exists(binDir) and not os.path.exists(cacheDir)):
        logger.warning("Nothing to clean. '/build', '/bin' and '/rbCache' don't exist")
        sys.exit(0)

    if (not os.path.exists(buildDir)):
        logger.warning("'/build' doesn't exist. Skipping task...")

    logger.debug(f"'/build' full path: {buildDir}")
    logger.info("Removing '/build'...")

    shutil.rmtree(buildDir, ignore_errors=True)

    if (not os.path.exists(binDir)):
        logger.warning("'/bin' doesn't exist. Skipping task...")

    logger.debug(f"'/bin' full path: {binDir}")
    logger.info("Removing '/bin'...")

    shutil.rmtree(binDir, ignore_errors=True)

    logger.debug(f"'/rbCache' full path: {cacheDir}")
    logger.info(f"Removing '/rbCache'...")

    shutil.rmtree(cacheDir, ignore_errors=True)

    if (removeRafa):
        attributesPath = os.path.join(workDir, "attributes.rafa")

        logger.debug(f"'attributes.rafa' full path: {attributesPath}")
        logger.info(f"Removing 'attributes.rafa'...")

        os.remove(attributesPath)