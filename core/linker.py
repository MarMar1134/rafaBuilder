import os
import sys
import subprocess
import util.logger as logger
import fileManager.cache as cache

from fileManager.files import FilePath

def libNeedsRecompileCheck(libName: str, objFilePaths: list[FilePath]):
    _, cachedObjFiles = cache.readLibCache(libName)

    if (cachedObjFiles is None):
        return True

    for objFilePath in objFilePaths: 
        _, cachedObjFileDate = cache.readCache(objFilePath)
        
        if (cachedObjFiles[objFilePath.name] != cachedObjFileDate):
            return True

    return False

def linkExecutable(compiler: str, workDir: str, appName: str):
    command = compiler + " "
    buildDir = os.path.join(workDir, "build")
    binDir = os.path.join(workDir, "bin")
    
    if (not os.path.exists(buildDir)):
        logger.error("Can't build executable as '/build' doesn't exist. Try using 'rb compile' to generate .o files")
        sys.exit(1)
    
    objFilePaths = FilePath.getFilePaths(buildDir)
    
    for objFilePath in objFilePaths:
        if (not objFilePath.extension == "o"):
            continue
    
        command = command + objFilePath.path + " "
    
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

    objFilePaths = FilePath.getFilePaths(buildDir)

    libName = "lib" + appName + ".a "

    if (not libNeedsRecompileCheck(libName, objFilePaths) and os.path.exists(os.path.join(binDir, libName))):
        logger.info(f"Static lib '{appName}' didn't need recompilation")
        logger.debug(f"Skipped library linking process, as it wasn't needed")
        return

    command = "ar rcs bin/" + libName

    objFileDates = {}

    for objFilePath in objFilePaths:
        if (not objFilePath.extension == "o"):
            continue

        objFileDates[objFilePath.name] = objFilePath.date
                
        command = command + objFilePath.path + " "

    logger.debug(f"Linker 'make staticLib' command: '{command}'")

    if (not os.path.exists(binDir)):
        os.mkdir(binDir)

    subprocess.run(command)

    libPath = FilePath(os.path.join("bin", libName.strip()))

    cache.writeLibCache(libPath, objFileDates)

def linkDynamicLib(compiler: str, workDir: str, appName: str):
    buildDir = os.path.join(workDir, "build")
    binDir = os.path.join(workDir, "bin")
    
    if (not os.path.exists(buildDir)):
        logger.error("Can't build static library as '/build' doesn't exist. Try using 'rb compile' to generate .o files")
        sys.exit(1)
    
    objFilePaths = FilePath.getFilePaths(buildDir)
    
    libName = "lib" + appName + ".dll"
    importantLibName = "lib" + appName + ".dll.a"

    command = compiler + " --shared "

    objFileDates = {}

    for objFilePath in objFilePaths:
        if (not objFilePath.extension == "o"):
            continue
    
        objFileDates[objFilePath.name] = objFilePath.date

        if ("main" in objFilePath.name):
            logger.warning("Dynamic libraries shouldn't have a 'main' file")
                    
        command = command + objFilePath.path + " "

    command = command + f"-o bin/{libName} -Wl,--out-implib,bin/{importantLibName}"

    logger.debug(f"Linker 'make dynamicLib' command: {command}")

    if (not os.path.exists(binDir)):
            os.mkdir(binDir)
    
    subprocess.run(command)
    
    libPath = FilePath(os.path.join("bin", libName))
    
    cache.writeLibCache(libPath, objFileDates, True)