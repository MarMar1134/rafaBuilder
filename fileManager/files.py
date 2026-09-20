import os
import sys
import util.logger as logger

def isValidFile(fileName: str):
    fileExtension = fileName.split(".").pop(1)

    return fileExtension == "cpp" or fileExtension == "c" \
            or fileExtension == "hpp" or fileExtension == "h" \
            or fileExtension == "o" or fileExtension == "obj"

class FilePath:
    def __init__(self, rawPath: str):
        #if (not os.path.exists(rawPath)):
        #    with open(rawPath, "x") as file:
        #        file.close()

        self.path = rawPath

        pathComponents = self.path.split("\\") or self.path.split("/")
        pathComponents.reverse()

        self.name = pathComponents.pop(0)

        self.extension = self.name.split(".").pop(1)

    def getFileDate(self):
        return str(os.path.getmtime(self.path))
    

    @staticmethod
    def getFilePaths(srcDir: str) -> list[FilePath]:
        filePaths: list[FilePath] = []

        if (not os.path.exists(srcDir)):
            logger.error(f"Directory '{srcDir}' doesn't exists")
            sys.exit(1)
        
        srcFilePaths = os.scandir(srcDir)

        if (srcFilePaths is None):
            logger.error(f"Path: '{srcDir}' has no files")
            sys.exit(1)

        for srcFilePath in srcFilePaths:
            if (os.path.isfile(srcFilePath)):

                filePath = FilePath(srcFilePath.path.split(os.getcwd()).pop(1)[1:])

                if (not isValidFile(filePath.name)):
                    continue

                filePaths.append(filePath)
            else:
                newDir = os.path.join(srcDir, srcFilePath.name)

                for newFilePath in FilePath.getFilePaths(newDir):
                    filePaths.append(newFilePath)

        return filePaths

    @staticmethod
    def getFilePathsWithoutSubdirs(srcDir: str) -> list[FilePath]:
        filePaths: list[FilePath] = []
        
        if (not os.path.exists(srcDir)):
            logger.error(f"Directory '{srcDir}' doesn't exists")
            sys.exit(1)
                
        srcFilePaths = os.scandir(srcDir)
        
        if (srcFilePaths is None):
            logger.error(f"Path: '{srcDir}' has no files")
            sys.exit(1)
        
        for srcFilePath in srcFilePaths:
            if (os.path.isfile(srcFilePath)):
                filePath = FilePath(srcFilePath.path.split(os.getcwd()).pop(1)[1:])
        
                if (not isValidFile(filePath.name)):
                    continue
        
                filePaths.append(filePath)

        return filePaths