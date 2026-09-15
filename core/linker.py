import os
import sys
import logger
from fileManager import files
from checks import existsPathCheck

def linkExecutable(compiler: str, workDir: str, appName: str):
    command = compiler + " "
    buildDir = os.path.join(workDir, "build")
    binDir = os.path.join(workDir, "bin")
    
    if (not existsPathCheck(buildDir)):
        logger.error("Can't build executable as '/build' doesn't exist. Try using 'rb compile' to generate .o files")
        sys.exit(1)
    
    objFiles = files.getFilePathsFromDir(buildDir)
    
    for objFile in objFiles:
        if (not objFile.split(".").pop(1) == "o"):
            continue
    
        objFile = objFile.replace("\\", "/")
    
        command = command + objFile + " "
    
    if (not os.path.exists(binDir)):
        os.mkdir(binDir)
    
    command = command + "-o " + "bin/" + appName + ".exe"
    
    logger.debug(f"Linker 'make exe' command: {command}")
    
    return command

def linkStaticLib(workDir: str, appName: str):
    buildDir = os.path.join(workDir, "build")
    binDir = os.path.join(workDir, "bin")

    if (not existsPathCheck(buildDir)):
            logger.error("Can't build static library as '/build' doesn't exist. Try using 'rb compile' to generate .o files")
            sys.exit(1)

    command = "ar rcs bin/lib" + appName + ".a "
      
    objFiles = files.getFilePathsFromDir(buildDir)

    for objFile in objFiles:
        if (not objFile.split(".").pop(1) == "o"):
            continue

        objFile = objFile.replace("\\", "/")
             
        command = command + objFile + " "

    logger.debug(f"Linker 'make staticLib' command: {command}")

    return command