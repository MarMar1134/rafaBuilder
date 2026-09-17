import os
import sys
import util.logger as logger

from fileManager.files import FilePath

HEADERS_CACHE_FILE = "headers.rach"
SOURCES_CACHE_FILE = "sources.rach"
OBJECTS_CACHE_FILE = "objects.rach"
STATIC_LIBS_CACHE_FILE = "staticLibs.rach"
DYNAMIC_LIBS_CACHE_FILE = "dynamicLibs.rach"

HEADER_EXTENSIONS = ["h", "hpp"]
SRC_EXTENSIONS = ["c", "cpp"]
OBJ_EXTENSIONS = ["o", "obj"]

cacheDir = os.path.join(os.getcwd(), "rbCache")

def assignCachePath(filePath: FilePath, errorMessage: str):
    cachePath = ""

    if (filePath.extension in HEADER_EXTENSIONS):
        cachePath = os.path.join(cacheDir, HEADERS_CACHE_FILE)
    elif (filePath.extension in SRC_EXTENSIONS):
        cachePath = os.path.join(cacheDir, SOURCES_CACHE_FILE)
    elif (filePath.extension in OBJ_EXTENSIONS):
        cachePath = os.path.join(cacheDir, OBJECTS_CACHE_FILE)
    elif ("dll" in filePath.name):
        cachePath = os.path.join(cacheDir, DYNAMIC_LIBS_CACHE_FILE)
    elif (filePath.extension == "a"):
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
    dynamicLibsCache = os.path.join(cacheDir, DYNAMIC_LIBS_CACHE_FILE)

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

    if (not os.path.exists(dynamicLibsCache)):
        with open(dynamicLibsCache, "x") as dlCache:
            dlCache.close()

def readLibCache(libName: str, isDynamic: bool = False):
    if (isDynamic):
        cachePath = os.path.join(cacheDir, DYNAMIC_LIBS_CACHE_FILE)
    else:
        cachePath = os.path.join(cacheDir, STATIC_LIBS_CACHE_FILE)

    objFiles = {}

    if (not os.path.exists(cachePath)):
        logger.error(f"Tried to read unexistent cache file: '{cachePath}'")
        sys.exit(1)

    logger.debug(f"Requested file: '{libName}'")
    with open(cachePath, "r") as cacheFile:
        lines = cacheFile.readlines()

        for index, line in enumerate(lines):
            pureLine = line.strip()

            if (libName in pureLine):
                logger.debug(f"Found '{libName}' on cache file '{STATIC_LIBS_CACHE_FILE}'")

                libObjects = pureLine.split("{").pop(1).split("}").pop(0)

                for libObject in libObjects.split(","):
                    objName = libObject.split(":").pop(0)
                    objDate = libObject.split(":").pop(1)

                    objFiles[objName] = objDate

                return index, objFiles

    return None, None

def readCache(filePath: FilePath):
    cachePath = assignCachePath(filePath, f"Tried to read unknown file from cache: '{filePath.name}'")

    if (not os.path.exists(cachePath)):
        logger.error(f"Tried to read unexistent cache file: '{cachePath}'")
        sys.exit(1)

    logger.debug(f"Requested file: '{filePath.name}'")
    with open(cachePath, "r") as cache:
        lines = cache.readlines()

        for index, line in enumerate(lines):
            pureLine = line.strip()

            if (filePath.name in pureLine):
                fileDate = pureLine.split(":").pop(1)

                logger.debug(f"Found '{filePath.name}' on cache file '{cachePath}', with modification date: '{fileDate}'")

                return index, fileDate

    return None, None

def writeLibCache(libPath: FilePath, objFileDates: dict[str, str], isDynamic: bool = False):
    if (isDynamic):
        cachePath = os.path.join(cacheDir, DYNAMIC_LIBS_CACHE_FILE)
    else:
        cachePath = os.path.join(cacheDir, STATIC_LIBS_CACHE_FILE)

    if (not os.path.exists(cachePath)):
        logger.error(f"Tried to write to unkwown cache: '{cachePath}'")
        sys.exit(1)

    index, cachedDate = readLibCache(libPath.name, isDynamic)

    with open(cachePath, "r") as cacheFile:
        lines = cacheFile.readlines()

    fileFormat = libPath.name + ":{"
    objFormat = ""

    for objFile, objDate in objFileDates.items():
        objFormat += objFile + ":" + objDate + ","
        
    fileFormat += objFormat
    fileFormat = fileFormat[:-1] + "}\n"

    if (index is not None):
        if (cachedDate != libPath.date):
            lines[index] = fileFormat
            logger.debug(f"Updated file: '{libPath.name}' on cache, with modification date: '{libPath.date}'. Previous date: '{cachedDate}'")
        else:
            logger.debug(f"File '{libPath.name}' didn't needed to be recached")
    else:
        lines.append(fileFormat)
        logger.debug(f"Written new file to cache: '{libPath.name}', with modification date: '{libPath.date}'")

    with open(cachePath, "w") as cacheFile:
           cacheFile.writelines(lines)

def writeCache(filePath: FilePath):
    cachePath = assignCachePath(filePath, f"Tried to write unknown file to cache: '{filePath.name}'")

    if (not os.path.exists(cachePath)):
        logger.error(f"Tried to write to unkwown cache: '{cachePath}'")
        sys.exit(1)
    
    lineIndex, cachedFileDate = readCache(filePath)
    fileFormat = filePath.name + ":" + filePath.date + "\n"

    with open(cachePath, "r") as cacheFile:
        lines = cacheFile.readlines()

    if ((lineIndex is not None)):
        if (cachedFileDate != filePath.date):
            lines[lineIndex] = fileFormat
            logger.debug(f"Updated file: '{filePath.name}' on cache, with modification date: '{filePath.date}'. Previous date: '{cachedFileDate}'")
        else:
            logger.debug(f"File '{filePath.name}' didn't needed to be recached")
    else:
        lines.append(fileFormat)
        logger.debug(f"Written new file to cache: '{filePath.name}', with modification date: '{filePath.date}'")

    with open(cachePath, "w") as cacheFile:
        cacheFile.writelines(lines)