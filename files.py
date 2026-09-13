import os
from enum import Enum

class Attribute(Enum):
    COMPILER = 0
    SOURCE_DIR = 1
    APP_NAME = 2

def getAttributes(currentDir: str):
    attributes = {}
    
    hasCompilerAttribute: bool = False
    hasSrcDirAttribute: bool = False
    hasAppNameAttribute: bool = False

    try:
        configFile = open(currentDir + "\\attributes.raf")
        
        for line in configFile.readlines():
            if("compiler" in line and not hasCompilerAttribute):
                hasCompilerAttribute = True

                attributes[Attribute.COMPILER] = line.split("\"").pop(1)
            elif("srcDir" in line and not hasSrcDirAttribute):
                hasSrcDirAttribute = True

                attributes[Attribute.SOURCE_DIR] = line.split("\"").pop(1)
            elif("appName" in line and not hasAppNameAttribute):
                hasAppNameAttribute = True

                attributes[Attribute.APP_NAME] = line.split("\"").pop(1)

        configFile.close()
    except Exception as e:
        print(f"[RAFABUILDER] Error: {e}")
        exit(1)
    
    if (not hasCompilerAttribute):
        print("[RAFABUILDER]-[ERROR] attributes.raf does not specify the compiler")
        exit(1)
    elif(not hasSrcDirAttribute):
        print("[RAFABUILDER]-[ERROR] attributes.raf does not specify the root directory")
        exit(1)
    elif(not hasAppNameAttribute):
        print("[RAFABUILDER]-[WARNING] attributes.raf does not specify the executable name. If you want to build a .exe, you must specify one.")

    return attributes

def getFilesFromDir(srcDir: str) -> list[str]:
    files = []

    if not os.path.exists(srcDir):
        print(f"path:'{srcDir}' is not valid")
        exit(1)
    
    srcFiles = os.scandir(srcDir)

    if srcFiles is None:
        print(f"path:'{srcDir}' has no files")
        exit(1)

    for file in srcFiles:
        if os.path.isfile(file):
            filePath = file.path.split(os.getcwd() + "\\").pop(1)

            files.append(filePath)
        else:
            newDir = srcDir + "\\" + file.name

            for newFile in getFilesFromDir(newDir):
                files.append(newFile)

    return files

def runProgram(currentDir: str, appName: str):
    execDir = currentDir + "\\bin\\"
    execCommand = ".\\bin\\" + appName

    os.system(f"cd {execDir}")
    os.system(f"{execCommand}")