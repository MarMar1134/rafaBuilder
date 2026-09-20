import os
import sys
import shutil
import util.logger as logger
import fileManager.cache as cache

from fileManager.files import FilePath

CPP_COMPILERS = ["g++", "clang", "c++"]
C_COMPILERS = ["gcc", "clang", "cc"]

def noAttributesCheck(configFile: str, noCompiler: bool, noSrcDir: bool, noAppName: bool, noProjectType: bool):
    if (not noCompiler):
        logger.error(f"'{configFile}' doesn't have 'compiler' attribute")
        sys.exit(1)
    elif(not noSrcDir):
        logger.error(f"'{configFile}' doesn't have 'srcDir' attribute")
        sys.exit(1)
    elif(not noAppName):
        logger.error(f"'{configFile}' doesn't have 'appName' attribute")
        sys.exit(1)
    elif(not noProjectType):
        logger.error(f"'{configFile}' doesn't have 'projectType' attribute")
        sys.exit(1)

def compilerInstalledCheck(configFile: str, compiler: str):
    if (not shutil.which(compiler)):
        logger.error(f"On {configFile}, '{compiler}' compiler is not present on this system's PATH")
        sys.exit(1)

def libNeedsRecompileCheck(libName: str, objFilePaths: list[FilePath]):
    _, cachedObjFiles = cache.readLibCache(libName)

    if (cachedObjFiles is None):
        return True

    for objFilePath in objFilePaths: 
        _, cachedObjFileDate = cache.readCache(objFilePath)

        if (objFilePath not in cachedObjFiles):
            return True
        
        if (cachedObjFiles[objFilePath.name] != cachedObjFileDate):
            return True

    return False

def existsSrcDirCheck(srcDir: str):
    workingDir = os.path.join(os.getcwd(), srcDir)

    return os.path.exists(workingDir)

def isSourceFileCheck(fileExtension: str):
    return fileExtension == "cpp" or fileExtension == "c"

def compilerMatchesLanguageCheck(srcDir: str, compiler: str):
    filesDir = os.path.join(os.getcwd(), srcDir)

    if not os.path.exists(filesDir):
        logger.error(f"Path: '{filesDir}' is not valid")
        sys.exit(1)

    def fileGetter(dir: str) -> list[str]:
        srcFilePaths = os.scandir(dir)
        
        if (srcFilePaths is None):
            logger.warning(f"Path: '{dir}' has no files")

        filePaths = []
        
        for srcFilePath in srcFilePaths:
            if (os.path.isfile(srcFilePath)):
                filePaths.append(srcFilePath.name)
            else:
                newDir = os.path.join(dir, srcFilePath.name)
        
                for newFile in fileGetter(newDir):
                    filePaths.append(newFile)

        return filePaths

    files = fileGetter(filesDir)

    for file in files:
        if (file.split(".").pop(1) == "cpp" and not (compiler in CPP_COMPILERS)):
            logger.warning(f"Utilizing a 'c' compiler to work with 'cpp' files")
            return
        elif(file.split(".").pop(1) == "c" and not (compiler in C_COMPILERS)):
            logger.warning(f"Utilizing a 'cpp' compiler to work with 'c' files")
            return