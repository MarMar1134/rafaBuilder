import os
import sys
from fileManager.files import getFileExtension, getFileExtensionFromPath, getFileName
import util.logger as logger

HEADERS_CACHE_FILE = "headers.rach"
SOURCES_CACHE_FILE = "sources.rach"
OBJECTS_CACHE_FILE = "objects.rach"
STATIC_LIBS_CACHE_FILE = "staticLibs.cach"

HEADER_EXTENSIONS = ["h", "hpp"]
SRC_EXTENSIONS = ["c", "cpp"]

cacheDir = os.path.join(os.getcwd(), "rbCache")

def assignCachePath(requestedFile: str, errorMessage: str):
    cachePath = ""

    if (os.path.isfile(requestedFile)):
        if (getFileExtension(requestedFile) in HEADER_EXTENSIONS):
            cachePath = os.path.join(cacheDir, HEADERS_CACHE_FILE)
        elif (getFileExtension(requestedFile) in SRC_EXTENSIONS):
            cachePath = os.path.join(cacheDir, SOURCES_CACHE_FILE)
        elif (getFileExtension(requestedFile) == "o"):
            cachePath = os.path.join(cacheDir, OBJECTS_CACHE_FILE)
        elif (getFileExtension(requestedFile) == "a"):
            cachePath = os.path.join(cacheDir, STATIC_LIBS_CACHE_FILE)
        else:
            logger.error(errorMessage)
            sys.exit(1)
    else:
        if (getFileExtensionFromPath(requestedFile) in HEADER_EXTENSIONS):
            cachePath = os.path.join(cacheDir, HEADERS_CACHE_FILE)
        elif (getFileExtensionFromPath(requestedFile) in SRC_EXTENSIONS):
            cachePath = os.path.join(cacheDir, SOURCES_CACHE_FILE)
        elif (getFileExtensionFromPath(requestedFile) == "o"):
            cachePath = os.path.join(cacheDir, OBJECTS_CACHE_FILE)
        elif (getFileExtensionFromPath(requestedFile) == "a"):
            cachePath = os.path.join(cacheDir, STATIC_LIBS_CACHE_FILE)
        else:
            logger.error(errorMessage)
            sys.exit(1)

    return cachePath

def inicializeCache():
    if (not os.path.exists(cacheDir)):
        logger.debug("Creating 'rbCache' directory...")
        os.makedirs(cacheDir)
        
    headersCache = os.path.join(cacheDir, HEADERS_CACHE_FILE)
    sourcesCache = os.path.join(cacheDir, SOURCES_CACHE_FILE)
    objectsCache = os.path.join(cacheDir, OBJECTS_CACHE_FILE)
    staticLibsCache = os.path.join(cacheDir, STATIC_LIBS_CACHE_FILE)

    if (not os.path.exists(headersCache)):
        with open(headersCache, "x") as hCache:
            hCache.close()

    if (not os.path.exists(sourcesCache)):
        with open(sourcesCache, "x") as sCache:
            sCache.close()

    if (not os.path.exists(objectsCache)):
        with open(objectsCache, "x") as oCache:
            oCache.close()

    if (not os.path.exists(staticLibsCache)):
        with open(staticLibsCache, "x") as slCache:
            slCache.close()

def readStaticLibCache(requestedFile: str):
    cachePath = os.path.join(cacheDir, STATIC_LIBS_CACHE_FILE)
    objFiles = {}

    if (not os.path.exists(cachePath)):
        logger.error(f"Tried to read unexistent cache file: '{cachePath}'")
        sys.exit(1)

    logger.debug(f"Requested file: '{requestedFile}'")
    with open(cachePath, "r") as cacheFile:
        lines = cacheFile.readlines()

        for _, line in enumerate(lines):
            pureLine = line.strip()

            if (requestedFile.strip() in pureLine):
                logger.debug(f"Found '{requestedFile.strip()}' on cache file '{STATIC_LIBS_CACHE_FILE}'")

                libObjects = pureLine.split("{").pop(1).split("}").pop(0)

                for libObject in libObjects.split(","):
                    objName = libObject.split(":").pop(0)
                    objDate = libObject.split(":").pop(1)

                    objFiles[objName] = objDate

                return objFiles

    return None

def readCache(requestedFile: str):
    cachePath = assignCachePath(requestedFile, f"Tried to read unknown file from cache: '{requestedFile}'")

    if (not os.path.exists(cachePath)):
        logger.error(f"Tried to read unexistent cache file: '{cachePath}'")
        sys.exit(1)

    logger.debug(f"Requested file: '{requestedFile}'")
    with open(cachePath, "r") as cache:
        lines = cache.readlines()

        for index, line in enumerate(lines):
            pureLine = line.strip()

            if (requestedFile in pureLine):
                fileDate = pureLine.split(":").pop(1)

                logger.debug(f"Found '{requestedFile}' on cache file '{getFileName(cachePath)}', with modification date: '{fileDate}'")

                return index, fileDate

    return None, None

def writeStaticLibCache(libName: str, objFileDates: dict[str, str]):
    cachePath = os.path.join(cacheDir, STATIC_LIBS_CACHE_FILE)

    if (not os.path.exists(cachePath)):
        logger.error(f"Tried to write to unkwown cache: '{cachePath}'")
        sys.exit(1)

    fileFormat = libName.strip() + ":{"
    objFormat = ""

    for objFile, objDate in objFileDates.items():
        objFormat += objFile + ":" + objDate + ","
        
    fileFormat += objFormat
    fileFormat = fileFormat[:-1] + "}"

    with open(cachePath, "r+") as cacheFile:
        cacheFile.writelines(fileFormat)
        logger.debug(f"Written cache line: '{fileFormat}'")
    

def writeCache(filePath: str):
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