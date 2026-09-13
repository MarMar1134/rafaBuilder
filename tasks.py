import os
import commands as cmd
import files

def rafaCompile(compiler: str, workDir: str, srcFiles: list[str], runWithInfo: bool):
    cmd.compileCommand(compiler, workDir, srcFiles, runWithInfo)

def rafaLink(compiler: str, workDir: str, appName: str, runWithInfo: bool):
    command = cmd.linkFromBuildCommand(compiler, workDir, appName, runWithInfo)

    os.system(command)

def rafaMake(compiler: str, workDir: str, srcFiles: list[str], pAppName: str, runWithInfo: bool):
    command = cmd.linkFromCppCommand(compiler, workDir, srcFiles, appName, runWithInfo)

    os.system(command)

def rafaRun(compiler: str, workDir: str, srcFiles: list[str], pAppName: str, runWithInfo: bool):
    command = cmd.linkFromCppCommand(compiler, workDir, srcFiles, appName, runWithInfo)

    os.system(command)

    print("[RAFABUILDER][MAIN] Compilation complete!")
    print("[RAFABUILDER][MAIN] Running program...")

    files.runProgram(currentDir, appName)
