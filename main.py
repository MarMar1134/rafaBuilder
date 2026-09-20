import os
import sys
import util.logger as logger
import core.tasks as task
import core.attributes as att
import fileManager.cache as cache

from util.argParser import defineParser
from fileManager.files import FilePath

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

    if (option == "check"):
        logger.task("Searching for 'attributes.rafa'...")

        configFound = task.rafaCheck(workDir)

        if (not configFound):
            logger.error(f"Config file 'attributes.rafa' was not found on '{workDir}'")
            sys.exit(1)
        else:
            attributes = att.getAttributes(workDir)

            logger.task(f"Config file 'attributes.rafa' found on '{workDir}'")

            logger.info(f"Showing 'attributes.rafa' contents...")
            logger.info(f"'compiler' set to: '{attributes[att.Attribute.COMPILER]}'")
            logger.info(f"'srcDir' set to: '{attributes[att.Attribute.SOURCE_DIR]}'")
            logger.info(f"'appName' set to: '{attributes[att.Attribute.APP_NAME]}'")
            logger.info(f"'projectType' set to: '{attributes[att.Attribute.PROJECT_TYPE]}'")

            for staticLib in attributes[att.Attribute.STATIC_LIBS]:
                logger.info(f"Added static library: '{staticLib}'")

            for dynamicLib in attributes[att.Attribute.DYNAMIC_LIBS]:
                logger.info(f"Added static library: '{dynamicLib}'")

            sys.exit(0)

    if (not os.path.exists(os.path.join(workDir, "rbCache"))):
        cache.inicializeCache()

    attributes = att.getAttributes(workDir)
    
    compiler = attributes[att.Attribute.COMPILER]
    srcDir = workDir + "\\" + attributes[att.Attribute.SOURCE_DIR]
    appName = attributes[att.Attribute.APP_NAME]
    projectType: att.ProjectType = attributes[att.Attribute.PROJECT_TYPE]
    
    srcFilePaths: list[FilePath] = FilePath.getFilePaths(srcDir)

    if(option == "compile"):
        task.rafaCompile(compiler, workDir, attributes[att.Attribute.STATIC_LIBS])

        logger.task("Task completed! You can find your object files under '<workDir>/build'")
        sys.exit(0)
    elif(option == "link"):
        task.rafaLink(compiler, workDir)

        logger.task("Task completed! You can find your executable under '<workDir>/bin'")
        sys.exit(0)
    elif(option == "make"):
        task.rafaMake(compiler, workDir, attributes[att.Attribute.STATIC_LIBS])

        logger.task("Task completed! You can find your executable under '<workDir>/bin'")
        sys.exit(0)
    elif(option == "run"):
        if (projectType != att.ProjectType.EXECUTABLE):
            logger.warning(f"'projectType' is set to '{projectType.value}', this task will be treated as 'make'")

        task.rafaRun(compiler, workDir, appName, projectType, attributes[att.Attribute.STATIC_LIBS])

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