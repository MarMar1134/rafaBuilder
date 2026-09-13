import os
import sys
import tasks as task
import files

currentDir: str = os.getcwd()

attributes = files.getAttributes(currentDir)

compiler = attributes[files.Attribute.COMPILER]
srcDir = currentDir + "\\" + attributes[files.Attribute.SOURCE_DIR]
appName = attributes[files.Attribute.APP_NAME]

srcFiles = files.getFilesFromDir(srcDir)

if (len(sys.argv) < 2):
    print("[RAFABUILDER][ERROR] Usage: build.py <Option> [-v|--verbose]"
    "\nOptions:"
    "\n-c: creates .o files and stores them under '/build'"
    "\n-l: links the .o files found on '/build'. If no files are found, returns an error."
    "\n-o: creates .o files and links them. The executable is stored under '/bin'"
    "\n-r: searchs for .o files under '/build' and tries to create an executable. If not .o files are found, it creates them and then runs the executable")
    exit(1)

runWithInfo: bool = False

if (len(sys.argv) == 3 and (sys.argv[2] == "-v" or sys.argv[2] == "--verbose")):
    runWithInfo: bool = True
elif(len(sys.argv) == 3):
    print("[RAFABUILDER][WARNING] Run with '-v' for extra info\n")

option: str = sys.argv[1]

print("[RAFABUILDER][MAIN] compiling project...")

if(option == "-c"):
    task.rafaCompile(compiler, currentDir, srcFiles, runWithInfo)

    print("[RAFABUILDER][MAIN] Compilation complete! You can find your object files under '<workDir>/build'")
    exit(0)
elif(option == "-l"):
    task.rafaLink(compiler, currentDir, appName, runWithInfo)

    print("[RAFABUILDER][MAIN] Compitation complete! You can find your executable under '<workDir>/bin'")
    exit(0)
elif(option == "-o"):
    task.rafaMake(compiler, currentDir, srcFiles, appName, runWithInfo)

    print("[RAFABUILDER][MAIN] Compitation complete! You can find your executable under '<workDir>/bin'")
    exit(0)
elif(option == "-r"):
    task.rafaRun(compiler, currentDir, srcFiles, appName, runWithInfo)

    exit(0)