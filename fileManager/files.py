import os
import sys
import logger
from checks import noAttributesCheck, compilerMatchesLanguageCheck, compilerInstalledCheck, unknownDirectoryCheck, existsDirectoryCheck
from enum import Enum

CONFIG_FILE_NAME = "attributes.rafa"

class Attribute(Enum):
    COMPILER = 0
    SOURCE_DIR = 1
    APP_NAME = 2

def getAttributes(workDir: str):
    configPath = os.path.join(workDir, CONFIG_FILE_NAME)

    if (not os.path.isfile(configPath)):
        logger.error(f"'{CONFIG_FILE_NAME}' not found in '{workDir}'")
        sys.exit(1)

    attributes = {}

    #TODO: Make an attribute table
    hasCompilerAttribute: bool = False
    hasSrcDirAttribute: bool = False
    hasAppNameAttribute: bool = False

    with open(workDir + "\\" + CONFIG_FILE_NAME) as configFile:
        for lineNumber, line in enumerate(configFile.readlines(), start=1):
            currentLine = line.strip()

            if (not currentLine):
                continue

            if("compiler" in currentLine and not hasCompilerAttribute):
                attribute = currentLine.split("\"")

                if (len(attribute) < 2 or attribute[1].strip() == ""):
                    logger.error(f"On {CONFIG_FILE_NAME}, Wrong format on line {lineNumber}: '{currentLine}'")
                    sys.exit(1)
            
                attributes[Attribute.COMPILER] = attribute[1]

                hasCompilerAttribute = True
            elif("srcDir" in currentLine and not hasSrcDirAttribute):
                attribute = currentLine.split("\"")
                
                if (len(attribute) < 2 or attribute[1].strip() == ""):
                    logger.error(f"On {CONFIG_FILE_NAME}, Wrong format on line {lineNumber}: '{currentLine}'")
                    sys.exit(1)
            
                attributes[Attribute.SOURCE_DIR] = attribute[1]

                hasSrcDirAttribute = True
            elif("appName" in currentLine and not hasAppNameAttribute):
                attribute = currentLine.split("\"")
                                
                if (len(attribute) < 2 or attribute[1].strip() == ""):
                    logger.error(f"On {CONFIG_FILE_NAME}, Wrong format on line {lineNumber}: '{currentLine}'")
                    sys.exit(1)
            
                attributes[Attribute.APP_NAME] = attribute[1]

                hasAppNameAttribute = True
    
    noAttributesCheck(CONFIG_FILE_NAME, hasCompilerAttribute, hasSrcDirAttribute, hasAppNameAttribute)

    isCorrectCompiler = compilerMatchesLanguageCheck(attributes[Attribute.SOURCE_DIR], attributes[Attribute.COMPILER])

    if (isCorrectCompiler == -1):
        logger.warning(f"Utilizing a 'c' compiler to work with 'cpp' files")
    elif(isCorrectCompiler == -2):
        logger.warning(f"Utilizing a 'cpp' compiler to work with 'c' files")

    compilerInstalledCheck(CONFIG_FILE_NAME, attributes[Attribute.COMPILER])
    
    if(not unknownDirectoryCheck(CONFIG_FILE_NAME, attributes[Attribute.SOURCE_DIR], None)):
        sys.exit(1)

    return attributes

def getFilePathsFromDir(srcDir: str) -> list[str]:
    import fileManager.cache as cache

    srcFilePaths = []

    if (not existsDirectoryCheck(srcDir, f"Path: '{srcDir}' is not valid")):
        sys.exit(1)
    
    srcFiles = os.scandir(srcDir)

    if (srcFiles is None):
        logger.error(f"Path: '{srcDir}' has no files")
        sys.exit(1)

    for srcFfile in srcFiles:
        if (os.path.isfile(srcFfile)):
            filePath = srcFfile.path.split(os.getcwd() + "\\").pop(1)

            logger.debug(f"File path added: '{filePath}'")

            srcFilePaths.append(filePath)
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