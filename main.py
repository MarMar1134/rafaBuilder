import os
import sys
import util.logger as logger
import core.tasks as task
import core.attributes as att
import fileManager.cache as cache

from util.argParser import defineParser
from fileManager import files

def main():
    parser = defineParser()
    args = parser.parse_args()
    logger.configure(args)
    workDir: str = os.getcwd()

    if (args.cmd is None):
        parser.print_help()
        sys.exit(1)

    option = args.cmd

    if (option == "init"):
        logger.main("Initializing working directory...")

        task.rafaInit(args)

        logger.task(f"Working directory '{workDir}' has been initialized!")
        sys.exit(0)

    attributes = att.getAttributes(workDir)

    compiler = attributes[att.Attribute.COMPILER]
    srcDir = workDir + "\\" + attributes[att.Attribute.SOURCE_DIR]
    appName = attributes[att.Attribute.APP_NAME]
    projectType = attributes[att.Attribute.PROJECT_TYPE]

    srcFilePaths = files.getFilePathsFromDir(srcDir)

    if (option == "check"):
        logger.main("Searching for 'attributes.rafa'")

        configFound = task.rafaCheck(workDir)

        if (not configFound):
            logger.error(f"Config file 'attributes.rafa' was not found on '{workDir}'")
            sys.exit(1)
        else:
            logger.task(f"Config file 'attributes.rafa' found on '{workDir}'")

            logger.main(f"'compiler' set to: '{attributes[att.Attribute.COMPILER]}'")
            logger.main(f"'srcDir' set to: '{attributes[att.Attribute.SOURCE_DIR]}'")
            logger.main(f"'appName' set to: '{attributes[att.Attribute.APP_NAME]}'")
            logger.main(f"'projectType' set to: '{attributes[att.Attribute.PROJECT_TYPE]}'")
            sys.exit(0)

    cache.inicializeCache()

    if(option == "compile"):
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

        if (projectType != "executable"):
            logger.warning(f"'projectType' is set to '{projectType}', this task will be treated as 'make'")

        task.rafaRun(compiler, workDir, srcFilePaths, appName, projectType)

        logger.task("Run complete!")

        sys.exit(0)
    elif(option == "clean"):
        logger.main("Cleaning '/build' '/bin' and '/rbCache'...")

        task.rafaClean(workDir)

        logger.task("Cleaning complete!")

        sys.exit(0)
    elif(option == "remove"):
        logger.main(f"Removing RafaBuilder...")

        task.rafaRemove(workDir)

        logger.task(f"RafaBuilder has been removed from working directory '{workDir}'")
        sys.exit(0)

if __name__ == "__main__":
    main()