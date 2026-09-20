import os
import sys
import subprocess
import shutil
import util.logger as logger
import fileManager.cache as cache
import core.attributes as attribute
import core.linker as linker

from core.attributes import Attribute, ProjectType, getAttributes
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
        projectType = ProjectType.DYNAMIC_LIB.value
    elif (args.projectType == 1):
        projectType = ProjectType.STATIC_LIB.value
    else:
        projectType = ProjectType.EXECUTABLE.value
    
    if (os.path.exists(attributesPath)):
        logger.error(f"'attributes.rafa' already exists on working directory '{os.getcwd()}'")
        sys.exit(1)
    
    compilerAttribute = f"compiler(\"{compiler}\")\n"
    srcDirAttribute = f"srcDir(\"{srcDir}\")\n"
    appNameAttribute = f"appName(\"{appName}\")\n"
    projectTypeAttribute = f"projectType({projectType})"
    
    attributeLines = [
        compilerAttribute,
        srcDirAttribute,
        appNameAttribute,
        projectTypeAttribute
    ]
    
    with open(attributesPath, "x") as attributesFile:
        attributesFile.writelines(attributeLines)

def _compileLibCommand(compiler: str, workDir: str, libDir: str, libName: str):
    srcFilePaths = FilePath.getFilePaths(libDir)
    objFilePath = os.path.join(workDir , "build", libName)

    logger.debug(f"On compileLib sub-task, Work dir: '{libDir}'")
    logger.debug(f"On compileLib sub-task, build dir: '{objFilePath}'")
    
    if (not os.path.exists(objFilePath)):
        os.mkdir(objFilePath)
    
    subprocess.run(f"cd {objFilePath}", shell=True)
    
    for filePath in srcFilePaths:
        if (not isSourceFileCheck(filePath.extension)):
            logger.debug(f"File '{filePath.name}' is a '{filePath.extension}' file")
            continue
        else:
            logger.debug(f"On compiling task, compiling source file '{filePath.path}'")
    
            _, cachedDate = cache.readCache(filePath)
    
            if (cachedDate == filePath.getFileDate()):
                logger.info(f"File '{filePath.name}' didn't needed to be recompiled")
                logger.debug(f"Skipping compiling process for '{filePath.name}', as it wasn't needed")
                continue
    
            command = compiler + " -c "
    
            fileOutputPath = os.path.join("build", libName, filePath.name[:-4] + ".o")
             
            command = command + filePath.path + " -o " + fileOutputPath
    
            logger.info(f"Compiling '{filePath.name}'...")
            logger.debug(f"Compile command: {command}")
    
            cache.writeCache(filePath)
    
            subprocess.run(command, shell=True)
    
            objFilePath = FilePath(os.path.join("build", libName, filePath.name[:-4] + ".o"))
    
            logger.debug(f"Object file path: '{objFilePath.path}'")
    
            cache.writeCache(objFilePath)

def compileCommand(compiler: str, workDir: str, libName: str | None = None):
    projectAttributes = getAttributes(workDir)

    if (libName):
        libDir = os.path.join(workDir, projectAttributes[Attribute.SOURCE_DIR], "libs", libName)
        _compileLibCommand(compiler, workDir, libDir, libName)
        return
    else:
        
        srcFilePaths = FilePath.getFilePaths(os.path.join(workDir, projectAttributes[Attribute.SOURCE_DIR], "src"))

    objFilePath = os.path.join(workDir, "build")

    logger.debug(f"On compile task, Work dir: '{workDir}'")
    logger.debug(f"On compile task, build dir: '{objFilePath}'")

    if (not os.path.exists(objFilePath)):
        os.mkdir(objFilePath)

    subprocess.run(f"cd {objFilePath}", shell=True)

    for filePath in srcFilePaths:
        if (not isSourceFileCheck(filePath.extension)):
            logger.debug(f"File '{filePath.name}' is a '{filePath.extension}' file")
            continue
        else:
            logger.debug(f"On compiling task, compiling source file '{filePath.path}'")

            _, cachedDate = cache.readCache(filePath)

            if (cachedDate == filePath.getFileDate()):
                logger.info(f"File '{filePath.name}' didn't needed to be recompiled")
                logger.debug(f"Skipping compiling process for '{filePath.name}', as it wasn't needed")
                continue

            command = compiler + " -c "

            fileOutputPath = os.path.join("build", filePath.name[:-4] + ".o")

            command = command + filePath.path + " -o " + fileOutputPath

            logger.info(f"Compiling '{filePath.name}'...")
            logger.debug(f"Compile command: {command}")

            cache.writeCache(filePath)

            subprocess.run(command, shell=True)

            objFilePath = FilePath(os.path.join("build", filePath.name[:-4] + ".o"))

            logger.debug(f"Object file path: '{objFilePath.path}'")

            cache.writeCache(objFilePath)

def linkCommand(compiler: str, workDir: str):
    projectAttributes = attribute.getAttributes(workDir)

    if (projectAttributes[Attribute.PROJECT_TYPE] == ProjectType.EXECUTABLE):
        linker.linkExecutable(compiler, workDir, projectAttributes[Attribute.APP_NAME], projectAttributes[Attribute.STATIC_LIBS])
    #elif (projectAttributes[Attribute.PROJECT_TYPE] == ProjectType.STATIC_LIB):
    #    linker.linkStaticLib(workDir, appName)
    #elif (projectAttributes[Attribute.PROJECT_TYPE] == ProjectType.DYNAMIC_LIB):
    #    linker.linkDynamicLib(compiler, workDir, appName)

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