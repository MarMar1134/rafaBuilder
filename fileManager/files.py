import os
import sys
import util.logger as logger

from util.checks import isValidFileCheck

class FilePath:
    def __init__(self, rawPath: str):
        self.path = rawPath

        pathComponents = self.path.split("\\") or self.path.split("/")
        pathComponents.reverse()

        self.name = pathComponents.pop(0)

        self.extension = self.name.split(".").pop(1)

        self.date = str(os.path.getmtime(self.path))

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
                logger.debug(f"Src file: '{srcFilePath.path}'")

                filePath = FilePath(srcFilePath.path.split(os.getcwd()).pop(1)[1:])

                if (not isValidFileCheck(filePath.name)):
                    continue

                filePaths.append(filePath)
                logger.debug(f"File path added: '{filePath.path}'")
            else:
                newDir = os.path.join(srcDir, srcFilePath.name)

                for newFilePath in FilePath.getFilePaths(newDir):
                    filePaths.append(newFilePath)

        return filePaths