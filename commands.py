import os
import files

def compileCommand(compiler: str, workDir: str, srcFiles: list[str], runWithInfo: bool):
    baseCommand = compiler + " -c "
    buildDir = workDir + "\\build"

    if not os.path.exists(buildDir):
        os.mkdir(buildDir)

    os.system(f"cd {buildDir}")

    for file in srcFiles:
        if file.split(".").pop(1) != "cpp":
            continue
        else:
            fileName = file.split("\\")
            fileName.reverse()
            fileName = fileName.pop(0)

            command = baseCommand + file + " -o " + "build\\" + fileName[:-4] + ".o"

            if (runWithInfo):
                print(f"[RAFABUILDER][INFO] compiling '{fileName}'")

            os.system(command)

    return command

def linkFromBuildCommand(compiler: str, workDir: str, appName: str, runWithInfo: bool):
    command = compiler + " "
    buildDir = workDir + "\\build"
    binDir = workDir + "\\bin"

    if (not os.path.exists(buildDir)):
        print("[RAFABUILDER][ERROR] Can't build as '/build' doesn't exist. Try using -c to generate .o files")
        exit(1)

    objFiles = files.getFilesFromDir(buildDir)

    for file in objFiles:
        if (runWithInfo):
            print(f"[RAFABUILDER][INFO] linking '{file}'")

        command = command + file + " "

    if (not os.path.exists(binDir)):
        os.mkdir(binDir)

    command = command + "-o " + "bin/" + appName

    return command

def linkFromCppCommand(compiler: str, workDir: str, srcFiles: list[str], pAppName: str, runWithInfo: bool):
    command = compiler

    for file in srcFiles:
        if file.split(".").pop(1) != "cpp":
            continue
        else:
            if (runWithInfo):
                print(f"[RAFABUILDER][INFO] compiling '{file}'")

            command = command + " " + file

    if not os.path.exists(workDir + "\\bin"):
        os.mkdir(workDir + "\\bin")

    command = command + " -o bin/" + pAppName + ".exe"

    return command