import os
import sys
import platform
import subprocess
import util.logger as logger
import fileManager.cache as cache

from fileManager.files import FilePath
from util.checks import libNeedsRecompileCheck 

def linkExecutable(compiler: str, workDir: str, appName: str, staticLibs: list[str] | None = None):
    command = compiler + " "
    buildDir = os.path.join(workDir, "build")
    binDir = os.path.join(workDir, "bin")
    
    if (not os.path.exists(buildDir)):
        logger.error("Can't build executable as '/build' doesn't exist. Try using 'rb compile' to generate .o files")
        sys.exit(1)
    
    objFilePaths = FilePath.getFilePathsWithoutSubdirs(buildDir)
    
    for objFilePath in objFilePaths:
        logger.debug(f"On link executable task, object file path: '{objFilePath.path}'")
        if (not objFilePath.extension == "o" or not os.path.isfile(objFilePath.path)):
            continue
    
        command = command + objFilePath.path + " "

    if (staticLibs):
        for staticLib in staticLibs:
            if (not os.path.exists(os.path.join(buildDir, staticLib, f"bin/lib{staticLib}.a "))):
                linkStaticLib(workDir, staticLib)

            command = command + f"bin/lib{staticLib}.a "
    
    if (not os.path.exists(binDir)):
        os.mkdir(binDir)
    
    command = command + "-o " + "bin/" + appName

    if (platform.system() == "Windows"):
        command = command + ".exe"
    
    logger.debug(f"Linker 'make exe' command: {command}")
    
    subprocess.run(command)

def linkStaticLib(workDir: str, libName: str):
    buildDir = os.path.join(workDir, "build", libName)
    binDir = os.path.join(workDir, "bin")

    logger.debug(f"on link static lib task, object files directory: '{buildDir}")

    if (not os.path.exists(buildDir)):
        logger.error("Can't build static library as '/build' doesn't exist. Try using 'rb compile' to generate .o files")
        sys.exit(1)

    objFilePaths = FilePath.getFilePaths(buildDir)

    logger.debug(f"On link static lib task, object file paths: '{objFilePaths}'")

    fullLibName = "lib" + libName + ".a"

    if (not libNeedsRecompileCheck(fullLibName, objFilePaths) and os.path.exists(os.path.join(binDir, fullLibName))):
        logger.info(f"Static lib '{libName}' didn't need recompilation")
        logger.debug(f"Skipped library linking process for lib '{libName}', as it wasn't needed")
        return

    libOutputDir = os.path.join("bin", fullLibName)

    command = f"ar rcs {libOutputDir} "

    objFileDates = {}

    for objFilePath in objFilePaths:
        if (not objFilePath.extension == "o"):
            continue

        objFileDates[objFilePath.name] = objFilePath.getFileDate()
                
        command = command + objFilePath.path + " "

    logger.debug(f"Linker 'make staticLib' command: '{command[:-1]}'")

    if (not os.path.exists(binDir)):
        os.mkdir(binDir)

    subprocess.run(command[:-1])

    libPath = FilePath(os.path.join("bin", fullLibName.strip()))

    cache.writeLibCache(libPath, objFileDates)

def linkDynamicLib(compiler: str, workDir: str, appName: str):
    buildDir = os.path.join(workDir, "build")
    binDir = os.path.join(workDir, "bin")
    
    if (not os.path.exists(buildDir)):
        logger.error("Can't build static library as '/build' doesn't exist. Try using 'rb compile' to generate .o files")
        sys.exit(1)
    
    objFilePaths = FilePath.getFilePaths(buildDir)
    objFileDates = {}

    if (platform.system() == "Windows"):
        libName = appName + ".dll"

        command = compiler + " --shared "
    else:
        libName = "lib" + appName + ".so"

        command = compiler + " -shared -fPIC "

    for objFilePath in objFilePaths:
        if (not objFilePath.extension == "o"):
            continue
    
        objFileDates[objFilePath.name] = objFilePath.getFileDate()

        if ("main" in objFilePath.name):
            logger.warning("Dynamic libraries shouldn't have a 'main' file")
                    
        command = command + objFilePath.path + " "

    command = command + f"-o bin/{libName}"

    if (platform.system() == "Windows"):
        importantLibName = "lib" + appName + ".dll.a"
        command = command + f" -Wl,--out-implib,bin/{importantLibName}"

    logger.debug(f"Linker 'make dynamicLib' command: {command}")

    if (not os.path.exists(binDir)):
            os.mkdir(binDir)
    
    subprocess.run(command)
    
    libPath = FilePath(os.path.join("bin", libName))
    
    cache.writeLibCache(libPath, objFileDates, True)