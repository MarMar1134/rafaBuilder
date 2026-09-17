import os
import sys
import util.logger as logger

from enum import Enum
from util.checks import noAttributesCheck, compilerMatchesLanguageCheck, compilerInstalledCheck, existsSrcDirCheck

class Attribute(Enum):
    COMPILER = 0
    SOURCE_DIR = 1
    APP_NAME = 2
    PROJECT_TYPE = 3

class ProjectType(Enum):
    EXECUTABLE = "executable"
    STATIC_LIB = "staticLib"
    DYNAMIC_LIB = "dynamicLib"

CONFIG_FILE_NAME = "attributes.rafa"

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
    hasProjectTypeAttribute: bool = False

    with open(os.path.join(workDir, CONFIG_FILE_NAME)) as configFile:
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
            elif("projectType" in currentLine and not hasProjectTypeAttribute):
                attribute = currentLine.split("\"")
                                                
                if (len(attribute) < 2 or attribute[1].strip() == ""):
                    logger.error(f"On {CONFIG_FILE_NAME}, Wrong format on line {lineNumber}: '{currentLine}'")
                    sys.exit(1)

                if (not attribute[1] in ProjectType):
                    logger.error(f"Attribute value '{attribute[1]}' is not allowed for attribute type 'projectType'")
                    sys.exit(1)
                            
                attributes[Attribute.PROJECT_TYPE] = attribute[1]

                hasProjectTypeAttribute = True
    
    noAttributesCheck(CONFIG_FILE_NAME, hasCompilerAttribute, hasSrcDirAttribute, hasAppNameAttribute, hasProjectTypeAttribute)

    compilerInstalledCheck(CONFIG_FILE_NAME, attributes[Attribute.COMPILER])

    isCorrectCompiler = compilerMatchesLanguageCheck(attributes[Attribute.SOURCE_DIR], attributes[Attribute.COMPILER])

    if (isCorrectCompiler == -1):
        logger.warning(f"Utilizing a 'c' compiler to work with 'cpp' files")
    elif(isCorrectCompiler == -2):
        logger.warning(f"Utilizing a 'cpp' compiler to work with 'c' files")

    if(not existsSrcDirCheck(attributes[Attribute.SOURCE_DIR])):
        logger.error(f"The specified source dir '{attributes[Attribute.SOURCE_DIR]}' doesn't exist")
        sys.exit(1)

    return attributes