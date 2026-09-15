import os
import sys
import util.logger as logger
from util.checks import isValidFileCheck

def getFilePathsFromDir(srcDir: str) -> list[str]:
    srcFilePaths = []

    if (not os.path.exists(srcDir)):
        logger.error(f"Directory '{srcDir}' doesn't exists")
        sys.exit(1)
    
    srcFiles = os.scandir(srcDir)

    if (srcFiles is None):
        logger.error(f"Path: '{srcDir}' has no files")
        sys.exit(1)

    for srcFfile in srcFiles:
        if (os.path.isfile(srcFfile)):
            filePath = srcFfile.path.split(os.getcwd() + "\\").pop(1)

            if (not isValidFileCheck(getFileName(filePath))):
                continue

            srcFilePaths.append(filePath)
            logger.debug(f"File path added: '{filePath}'")
        else:
            newDir = os.path.join(srcDir, srcFfile.name)

            for newFilePath in getFilePathsFromDir(newDir):
                srcFilePaths.append(newFilePath)

    return srcFilePaths

def getFileName(filePath: str) -> str:
    pathComponents = filePath.split("\\")
    pathComponents.reverse()
        
    fileName = pathComponents.pop(0)

    return fileName

def getFileExtension(fileName: str) -> str:
    fileExtension = fileName.split(".").pop(1)

    return fileExtension

def getFileExtensionFromPath(filePath: str) -> str:
    pathComponents = filePath.split("\\")
    pathComponents.reverse()
            
    fileName = pathComponents.pop(0)
    fileExtension = fileName.split(".").pop(1)

    return fileExtension

def getFileNames(filePaths: list[str]) -> list[str]:
    fileNames = []
    
    for filePath in filePaths:
        fileName = getFileName(filePath)
        
        fileNames.append(fileName)
    
    return fileNames

def getFileNamesByExtension(filePaths: list[str], extension: str) -> list[str]:
    fileNames = []

    for filePath in filePaths:
        pathComponents = filePath.split("\\")
        pathComponents.reverse()

        fileName = pathComponents.pop(0)
        fileExtension = fileName.split(".").pop(1)

        if (fileExtension == extension):
            fileNames.append(fileName)
        else:
            continue

    return fileNames

def getFilePathsByExtension(filePaths: list[str], extension: str) -> list[str]:
    sortedFilePaths = []
    
    for filePath in filePaths:
        pathTuple = filePath.split("\\")
        pathTuple.reverse()
    
        fileName = pathTuple.pop(0)
        fileExtension = fileName.split(".").pop(1)
    
        if (fileExtension == extension):
            sortedFilePaths.append(filePath)
        else:
            continue
    
    return sortedFilePaths