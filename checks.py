import os
import sys
import shutil
import logger

CPP_COMPILERS = ["g++", "clang++", "c++"]
C_COMPILERS = ["gcc", "clang", "cc"]

def noAttributesCheck(configFile: str, noCompiler: bool, noSrcDir: bool, noAppName: bool):
    if (not noCompiler):
        logger.error(f"'{configFile}' doesn't have 'compiler' attribute")
        sys.exit(1)
    elif(not noSrcDir):
        logger.error(f"'{configFile}' doesn't have 'srcDir' attribute")
        sys.exit(1)
    elif(not noAppName):
        logger.warning(f"'{configFile}' doesn't have 'appName' attribute")
        #sys.exit(1)

def compilerInstalledCheck(configFile: str, compiler: str):
    if (not shutil.which(compiler)):
        logger.error(f"On {configFile}, '{compiler}' compiler is not present on this system's PATH")
        sys.exit(1)

def existsPathCheck(filePath: str):
    return os.path.exists(filePath)     

def unknownDirectoryCheck(configFile: str | None, dir: str, customMsg: str | None) -> bool:
    baseMessage = "" 

    if (not (configFile is None)):
        baseMessage = baseMessage + f"On {configFile}, Source directory '{dir}' does not exist"
    elif(customMsg is None):
        baseMessage = baseMessage + f"Source directory '{dir}' does not exist"
    else:
        baseMessage = baseMessage + customMsg

    if(not os.path.exists(dir)):
        logger.error(baseMessage)
        return False

    return True

def existsDirectoryCheck(dir: str, customMsg: str | None) -> bool:
    return unknownDirectoryCheck(None, dir, customMsg)

def compilerMatchesLanguageCheck(srcDir: str, compiler: str):
    workDir = os.getcwd()
    filesDir = os.path.join(workDir, srcDir)

    if not os.path.exists(filesDir):
        logger.error(f"Path:'{filesDir}' is not valid")
        sys.exit(1)

    def fileGetter(dir: str) -> list[str]:
        files = os.scandir(dir)
        
        if (files is None):
            logger.warning(f"Path:'{dir}' has no files")

        srcFiles = []
        
        for file in files:
            if (os.path.isfile(file)):
                srcFiles.append(file.name)
            else:
                newDir = dir + "\\" + file.name
        
                for newFile in fileGetter(newDir):
                    srcFiles.append(newFile)

        return srcFiles

    files = fileGetter(filesDir)

    for file in files:
        if (file.split(".").pop(1) == "cpp" and not (compiler in CPP_COMPILERS)):
            return -1
        elif(file.split(".").pop(1) == "c" and not (compiler in C_COMPILERS)):
            return -2

    return 0