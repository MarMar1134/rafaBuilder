import os
import sys
import re
import util.logger as logger

from enum import Enum
from util.checks import noAttributesCheck, compilerMatchesLanguageCheck, compilerInstalledCheck, existsSrcDirCheck

class Attribute(Enum):
    COMPILER = 0
    SOURCE_DIR = 1
    APP_NAME = 2
    PROJECT_TYPE = 3
    STATIC_LIBS = 4
    DYNAMIC_LIBS = 5

class ProjectType(Enum):
    EXECUTABLE = "EXECUTABLE"
    STATIC_LIB = "STATIC_LIB"
    DYNAMIC_LIB = "DYNAMIC_LIB"

CONFIG_FILE_NAME = "attributes.rafa"

ATTRIBUTE_PATTERN = re.compile(r'^(\w+)\(\s*"([^"]*)"\s*\)\s*$')

PROJECT_TYPE_PATTERN = re.compile(r'^(\w+)\(\s*(EXECUTABLE|STATIC_LIB|DYNAMIC_LIB)\s*\)\s*$')

#STATIC_LIBS_PATTERN = re.compile(r'^(\w+)\(\s*')

LIBS_ATTRIBUTE_PATTERN = re.compile( r'^(addDynamicLibs|addStaticLibs)\s*\(\s*("[A-Za-z_][A-Za-z0-9_]*"(?:\s*,\s*"[A-Za-z_][A-Za-z0-9_]*")*)\s*\)$' )

def parseAttributeLine(lineNumber: int, currentLine: str):
    match = ATTRIBUTE_PATTERN.match(currentLine)

    if (not match):
        projectMatch = PROJECT_TYPE_PATTERN.match(currentLine)

        if (projectMatch):
            return parseProjectTypeLine(lineNumber, currentLine, projectMatch)
        else:
            libsMatch = LIBS_ATTRIBUTE_PATTERN.match(currentLine)

            if (libsMatch):
                return parseLibsAttributeLine(lineNumber, currentLine, libsMatch)

            if (currentLine.count('"') % 2 != 0):
                logger.error(f"On {CONFIG_FILE_NAME}, parseAttributeLine(), line {lineNumber}: unclosed quotes: '{currentLine}'")
            else:
                logger.error(f"On {CONFIG_FILE_NAME}, parseAttributeLine(), Wrong format on line {lineNumber}: '{currentLine}'. Expected: attributeName(\"value\")")
            sys.exit(1)

    attrName, value = match.group(1), match.group(2)

    if (value.strip() == ""):
        logger.error(f"On {CONFIG_FILE_NAME}, line {lineNumber}: empty value for '{attrName}'")
        sys.exit(1)

    return attrName, value

def parseProjectTypeLine(lineNumber: int, currentLine: str, match):
    if (not match):
            logger.error(f"On {CONFIG_FILE_NAME}, parseProjectLine(), Wrong format on line {lineNumber}: '{currentLine}'. Expected: projectType(PROJECT_TYPE)")
            sys.exit(1)

    attrName, value = match.group(1), match.group(2)

    if (value.strip() == ""):
        logger.error(f"On {CONFIG_FILE_NAME}, parseProjectLine(), line {lineNumber}: empty value for '{attrName}'")
        sys.exit(1)
    
    return attrName, value

def parseLibsAttributeLine(lineNumber: int, currentLine: str, libsMatch):
    if (not libsMatch): 
        logger.error( f"On {CONFIG_FILE_NAME}, parseLibsAttributeLine(), Wrong format on line {lineNumber}: '{currentLine}'. Expected: addLibType(\"lib1\", \"lib2\",...)")
        sys.exit(1)

    attrName = libsMatch.group(1)
    libs = libsMatch.group(2)

    libsList = libs.split(",")
    filteredLibs = []

    for lib in libsList:
        filteredLibs.append(lib.strip().strip('"'))

    return attrName, filteredLibs

def getAttributes(workDir: str):
    configPath = os.path.join(workDir, CONFIG_FILE_NAME)

    if (not os.path.isfile(configPath)):
        logger.error(f"'{CONFIG_FILE_NAME}' not found in '{workDir}'")
        sys.exit(1)

    attributes = {}
    attributes[Attribute.STATIC_LIBS] = []
    attributes[Attribute.DYNAMIC_LIBS] = []

    #TODO: Make an attribute table
    hasCompilerAttribute: bool = False
    hasSrcDirAttribute: bool = False
    hasAppNameAttribute: bool = False
    hasProjectTypeAttribute: bool = False
    
    hasAddDynamicLibAttribute: bool = False

    with open(os.path.join(workDir, CONFIG_FILE_NAME)) as configFile:
        for lineNumber, line in enumerate(configFile.readlines(), start=1):
            currentLine = line.strip()

            if (not currentLine):
                continue

            attributeName, attributeVal = parseAttributeLine(lineNumber, currentLine)

            if (attributeName == "compiler" and not hasCompilerAttribute):
                attributes[Attribute.COMPILER] = attributeVal
                hasCompilerAttribute = True
            elif (attributeName == "srcDir" and not hasSrcDirAttribute):
                attributes[Attribute.SOURCE_DIR] = attributeVal
                hasSrcDirAttribute = True
            elif (attributeName == "appName" and not hasAppNameAttribute):
                attributes[Attribute.APP_NAME] = attributeVal
                hasAppNameAttribute = True
            elif (attributeName == "projectType" and not hasProjectTypeAttribute):
                if (not attributeVal in ProjectType):
                    logger.error(f"Attribute value '{attributeVal}' is not allowed for attribute type '{attributeName}'." + " Acepted values are {EXECUTABLE;STATIC_LIB;DYNAMIC_LIB}")
                    sys.exit(1)

                if (attributeVal == ProjectType.EXECUTABLE.value):
                    projectType = ProjectType.EXECUTABLE
                elif (attributeVal == ProjectType.STATIC_LIB.value):
                    projectType = ProjectType.STATIC_LIB
                else:
                    projectType = ProjectType.DYNAMIC_LIB
                            
                attributes[Attribute.PROJECT_TYPE] = projectType

                hasProjectTypeAttribute = True
            elif(attributeName == "addStaticLibs"):
                attributes[Attribute.STATIC_LIBS].extend(attributeVal)

            elif(attributeName == "addDynamicLibs" and not hasAddDynamicLibAttribute):
                attributes[Attribute.DYNAMIC_LIBS].extend(attributeVal)
                
                hasAddDynamicLibAttribute = True
            else:
                logger.warning(f"On attributes.rafa, line {lineNumber} unknown attribute: '{attributeName}'")

    noAttributesCheck(CONFIG_FILE_NAME, hasCompilerAttribute, hasSrcDirAttribute, hasAppNameAttribute, hasProjectTypeAttribute)

    compilerInstalledCheck(CONFIG_FILE_NAME, attributes[Attribute.COMPILER])

    compilerMatchesLanguageCheck(attributes[Attribute.SOURCE_DIR], attributes[Attribute.COMPILER])

    if(not existsSrcDirCheck(attributes[Attribute.SOURCE_DIR])):
        logger.error(f"The specified source dir '{attributes[Attribute.SOURCE_DIR]}' doesn't exist")
        sys.exit(1)

    return attributes