import os
import sys
import subprocess
import util.logger as logger
from fileManager import files
from fileManager import cache

def libNeedsRecompileCheck(libName: str, objFilePaths: list[str]):
    cachedObjFiles = cache.readStaticLibCache(libName)

    if (cachedObjFiles is None):
        return True

    for objFilePath in objFilePaths: 
        objFileName = files.getFileName(objFilePath)
        _, objFileDate = cache.readCache(files.getFileName(objFilePath))

        #logger.debug(f"cached obj file date: '{cachedObjFiles[objFileName]}', actual obj file date: '{objFileDate}'. Equals? '{cachedObjFiles[objFileName] == objFileDate}'")
        
        if (cachedObjFiles[objFileName] != objFileDate):
            return True

    return False

def linkExecutable(compiler: str, workDir: str, appName: str):
    command = compiler + " "
    buildDir = os.path.join(workDir, "build")
    binDir = os.path.join(workDir, "bin")
    
    if (not os.path.exists(buildDir)):
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
    
    subprocess.run(command)

def linkStaticLib(workDir: str, appName: str):
    buildDir = os.path.join(workDir, "build")
    binDir = os.path.join(workDir, "bin")

    if (not os.path.exists(buildDir)):
        logger.error("Can't build static library as '/build' doesn't exist. Try using 'rb compile' to generate .o files")
        sys.exit(1)

    objFilePaths = files.getFilePathsFromDir(buildDir)

    libName = "lib" + appName + ".a "

    if (not libNeedsRecompileCheck(libName, objFilePaths) and os.path.exists(os.path.join(binDir, libName))):
        logger.info(f"Static lib '{appName}' didn't need recompilation")
        logger.debug(f"Skipped library linking process, as it wasn't needed")
        return

    command = "ar rcs bin/" + libName

    objFileDates = {}

    for objFilePath in objFilePaths:
        if (not objFilePath.split(".").pop(1) == "o"):
            continue


        objFileName = files.getFileName(objFilePath)
        objFileDate = str(os.path.getmtime(objFilePath))

        objFileDates[objFileName] = objFileDate

        objFilePath = objFilePath.replace("\\", "/")
                
        command = command + objFilePath + " "

    logger.debug(f"Linker 'make staticLib' command: '{command}'")

    if (not os.path.exists(binDir)):
        os.mkdir(binDir)

    subprocess.run(command)

    cache.writeStaticLibCache(libName, objFileDates)