import os
import sys
import logger
import tasks as task
from parser import defineParser
from fileManager import files, cache

def main():
    parser = defineParser()
    args = parser.parse_args()
    logger.configure(args)

    if (args.cmd is None):
        parser.print_help()
        sys.exit(1)

    workDir: str = os.getcwd()

    attributes = files.getAttributes(workDir)

    compiler = attributes[files.Attribute.COMPILER]
    srcDir = workDir + "\\" + attributes[files.Attribute.SOURCE_DIR]
    appName = attributes[files.Attribute.APP_NAME]

    srcFilePaths = files.getFilePathsFromDir(srcDir)

    #cache.createCacheFromList(srcFilePaths)

    #for file in srcFilePaths:
        #lineNum, cachedDate = cache.readCache(files.getFileName(file))
        #logger.info(f"Cache line {lineNum}:{cachedDate}")
        #cache.writeFileToCache(file)

    #cache.writeFilesToCache(srcFilePaths)

    option = args.cmd

    if (option == "check"):
        logger.main("Searching for 'attributes.rafa'")

        configFound = task.rafaCheck(workDir)

        if (not configFound):
            logger.error(f"Config file 'attributes.rafa' was not found on '{workDir}'")
            sys.exit(1)
        else:
            logger.main(f"Config file 'attributes.rafa' found on '{workDir}'")
    elif(option == "compile"):
        logger.main("Compiling source files...")

        task.rafaCompile(compiler, workDir, srcFilePaths)

        logger.main("Compilation complete! You can find your object files under '<workDir>/build'")
        sys.exit(0)
    elif(option == "link"):
        logger.main("Linking object files...")

        task.rafaLink(compiler, workDir, appName)

        logger.main("Compilation complete! You can find your executable under '<workDir>/bin'")
        sys.exit(0)
    elif(option == "make"):
        logger.main("Compiling source files and linking them...")

        task.rafaMake(compiler, workDir, srcFilePaths, appName)

        logger.main("Compilation complete! You can find your executable under '<workDir>/bin'")
        sys.exit(0)
    elif(option == "run"):
        logger.main("Compiling source files and linking them...")

        task.rafaRun(compiler, workDir, srcFilePaths, appName)

        logger.main("Run complete!")
        sys.exit(0)
    elif(option == "clean"):
        logger.main("Cleaning build and bin directories...")

        task.rafaClean(workDir)

        sys.exit(0)

if __name__ == "__main__":
    main()