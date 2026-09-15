import os
import sys
from fileManager.files import getFileExtension, getFileExtensionFromPath, getFileName
import logger

HEADERS_CACHE_FILE = "headers.rach"
SRC_CACHE_FILE = "sources.rach"
CACHE_FILE_NAME = "cache.rach"

HEADER_EXTENSIONS = ["h", "hpp"]
SRC_EXTENSIONS = ["c", "cpp"]

cacheDir = os.path.join(os.getcwd(), "rbCache")

def makeFilePathAndDatesTable(filePaths: list[str]) -> dict[str, str]:
    fileTable = {}

    for filePath in filePaths:
        fileTable[filePath] = os.path.getmtime(filePath)

    return fileTable

def assignCachePath(requestedFile: str, errorMessage: str):
    cachePath = ""

    if (os.path.isfile(requestedFile)):
        if (getFileExtension(requestedFile) in HEADER_EXTENSIONS):
            cachePath = os.path.join(cacheDir, HEADERS_CACHE_FILE)
        elif (getFileExtension(requestedFile) in SRC_EXTENSIONS):
            cachePath = os.path.join(cacheDir, SRC_CACHE_FILE)
        else:
            logger.error(errorMessage)
            sys.exit(1)
    else:
        if (getFileExtensionFromPath(requestedFile) in HEADER_EXTENSIONS):
            cachePath = os.path.join(cacheDir, HEADERS_CACHE_FILE)
        elif (getFileExtensionFromPath(requestedFile) in SRC_EXTENSIONS):
            cachePath = os.path.join(cacheDir, SRC_CACHE_FILE)
        else:
            logger.error(errorMessage)
            sys.exit(1)

    return cachePath

def inicializeCache():
    if (not os.path.exists(cacheDir)):
        logger.debug("Creating 'rbCache' directory...")
        os.makedirs(cacheDir)
        
    headersCache = os.path.join(cacheDir, HEADERS_CACHE_FILE)
    sourcesCache = os.path.join(cacheDir, SRC_CACHE_FILE)

    if (not os.path.exists(headersCache)):
        with open(headersCache, "x") as hCache:
            hCache.close()

    if (not os.path.exists(sourcesCache)):
        with open(sourcesCache, "x") as sCache:
            sCache.close()

def createCache(filePath: str):
    if (not os.path.exists(cacheDir)):
            logger.debug("Creating 'rbCache' directory...")
            os.makedirs(cacheDir)
    
    headersCache = os.path.join(cacheDir, HEADERS_CACHE_FILE)
    sourcesCache = os.path.join(cacheDir, SRC_CACHE_FILE)

    fileFormat = getFileName(filePath) + ":" + str(os.path.getmtime(filePath)) + "\n"

    if (getFileExtensionFromPath(filePath) in HEADER_EXTENSIONS):
        if (not os.path.exists(headersCache)):
            with open(headersCache, "x") as hCache:
                hCache.write(fileFormat)
        else:
            logger.warning(f"Tried to create existing cache file: '{headersCache}'")
    elif (getFileExtensionFromPath(filePath) in SRC_EXTENSIONS):
        if (not os.path.exists(sourcesCache)):
            with open(sourcesCache, "x") as sCache:
                sCache.write(fileFormat)
        else:
            logger.warning(f"Tried to create existing cache file: '{sourcesCache}'")
    else:
        logger.error(f"Unknown file format: '{getFileName(filePath)}'")
        sys.exit(1)

def readCache(requestedFile: str):
    cachePath = assignCachePath(requestedFile, f"Tried to read unknown file from cache: '{requestedFile}'")

    if (not os.path.exists(cachePath)):
        logger.error(f"Tried to read unexistent cache file: '{cachePath}'")
        sys.exit(1)

    with open(cachePath, "r") as cache:
        lines = cache.readlines()

        for index, line in enumerate(lines):
            pureLine = line.strip()

            if (requestedFile in pureLine):
                fileDate = pureLine.split(":").pop(1)

                logger.debug(f"Found '{requestedFile}' on cache file '{getFileName(cachePath)}', with modification date: '{fileDate}'")

                return index, fileDate

    return None, None

def writeFileToCache(filePath: str):
    fileName = getFileName(filePath)
    cachePath = assignCachePath(filePath, f"Tried to write unknown file to cache: '{getFileName(filePath)}'")

    if (not os.path.exists(cachePath)):
        logger.error(f"Tried to write to unkwown cache: '{cachePath}'")
        sys.exit(1)
    
    lineIndex, cachedFileDate = readCache(fileName)
    currentFileDate = str(os.path.getmtime(filePath))
    fileFormat = fileName + ":" + currentFileDate + "\n"

    with open(cachePath, "r") as cacheFile:
        lines = cacheFile.readlines()

    if ((lineIndex is not None)):
        if (cachedFileDate != currentFileDate):
            lines[lineIndex] = fileFormat
            logger.debug(f"Updated file: '{fileName}' on cache, with modification date: '{currentFileDate}'. Previous date: '{cachedFileDate}'")
        else:
            logger.debug(f"File '{fileName}' didn't needed to be recached")
    else:
        lines.append(fileFormat)
        logger.debug(f"Written new file to cache: '{fileName}', with modification date: '{currentFileDate}'")

    with open(cachePath, "w") as cacheFile:
        cacheFile.writelines(lines)

def writeFilesToCache(filePaths: list[str]):
    for filePath in filePaths:
        writeFileToCache(filePath)