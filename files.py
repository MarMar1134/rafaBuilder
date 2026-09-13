import os
import sys
import subprocess
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

def getFilesFromDir(srcDir: str) -> list[str]:
    srcFiles = []

    if (not existsDirectoryCheck(srcDir, f"Path: '{srcDir}' is not valid")):
        sys.exit(1)
    
    files = os.scandir(srcDir)

    if files is None:
        logger.error(f"Path: '{srcDir}' has no files")
        sys.exit(1)

    for file in files:
        if os.path.isfile(file):
            filePath = file.path.split(os.getcwd() + "\\").pop(1)

            logger.debug(f"File added: '{filePath}'")

            srcFiles.append(filePath)
        else:
            newDir = srcDir + "\\" + file.name

            for newFile in getFilesFromDir(newDir):
                srcFiles.append(newFile)

    return srcFiles

def runProgram(currentDir: str, appName: str):
    execDir = currentDir + "\\bin\\"
    execCommand = ".\\bin\\" + appName

    logger.info(f"Running '{execCommand}' from '{execDir}'")

    subprocess.run(f"cd {execDir}", shell=True)
    subprocess.run(execCommand, shell=True)