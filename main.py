import os
import sys
import logger
import core.tasks as task
import core.attributes as att
import fileManager.cache as cache

from argParser import defineParser
from fileManager import files

def main():
    parser = defineParser()
    args = parser.parse_args()
    logger.configure(args)
    cache.inicializeCache()

    if (args.cmd is None):
        parser.print_help()
        sys.exit(1)

    workDir: str = os.getcwd()

    attributes = att.getAttributes(workDir)

    compiler = attributes[att.Attribute.COMPILER]
    srcDir = workDir + "\\" + attributes[att.Attribute.SOURCE_DIR]
    appName = attributes[att.Attribute.APP_NAME]

    srcFilePaths = files.getFilePathsFromDir(srcDir)

    option = args.cmd

    if (option == "check"):
        logger.main("Searching for 'attributes.rafa'")

        configFound = task.rafaCheck(workDir)

        if (not configFound):
            logger.error(f"Config file 'attributes.rafa' was not found on '{workDir}'")
            sys.exit(1)
        else:
            logger.task(f"Config file 'attributes.rafa' found on '{workDir}'")
    elif(option == "compile"):
        task.rafaCompile(compiler, workDir, srcFilePaths)

        logger.task("Task completed! You can find your object files under '<workDir>/build'")
        sys.exit(0)
    elif(option == "link"):
        task.rafaLink(compiler, workDir, appName)

        logger.task("Task completed! You can find your executable under '<workDir>/bin'")
        sys.exit(0)
    elif(option == "make"):
        task.rafaMake(compiler, workDir, srcFilePaths, appName)

        logger.task("Task completed! You can find your executable under '<workDir>/bin'")
        sys.exit(0)
    elif(option == "run"):
        logger.main("Starting run...")
        task.rafaRun(compiler, workDir, srcFilePaths, appName)

        sys.exit(0)
    elif(option == "clean"):
        logger.main("Cleaning '/build' '/bin' and '/rbCache'...")

        task.rafaClean(workDir)

        logger.task("Cleaning complete!")

        sys.exit(0)

if __name__ == "__main__":
    main()