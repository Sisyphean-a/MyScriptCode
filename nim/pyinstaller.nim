import os, osproc, strutils, sequtils
import system
import streams

proc checkPyInstaller(): bool =
  if findExe("pyinstaller") == "":
    if findExe("pip") != "":
      discard execProcess("pip install pyinstaller")
    else:
      echo "请先安装 pip"
      return false
  return true

proc getPyFiles(): seq[string] =
  let files = toSeq(walkFiles("*"))
  result = filter(files, proc (x: string): bool = x.endsWith(".py"))

proc printPyFiles(pyFiles: seq[string]) =
  echo "当前目录下的 .py 文件："
  for i, file in pyFiles:
    echo $i & ". " & file

proc getTargetFile(pyFiles: seq[string]): string =
  echo "请输入要打包的文件序号："
  let fileNum = parseInt(readLine(stdin))
  result = pyFiles[fileNum]

proc packageFile(targetFile: string, noConsole = false) =
  if noConsole:
    discard execProcess("pyinstaller --onefile -w " & targetFile)
  else:
    discard execProcess("pyinstaller --onefile " & targetFile)

proc moveFile(targetFile: string) =
  let targetExe = targetFile[0 .. ^4] & ".exe"
  if fileExists(targetExe):
    removeFile(targetExe)
  moveFile("dist/" & targetExe, targetExe)

  if dirExists("__pycache__"):
    removeDir("__pycache__")
  removeDir("build")
  removeDir("dist")
  removeFile(targetFile[0 .. ^4] & ".spec")

if not checkPyInstaller():
  quit(1)
let pyFiles = getPyFiles()
printPyFiles(pyFiles)
let targetFile = getTargetFile(pyFiles)
echo "是否需要打包成无控制台版本？(y/n)："
let noConsole = toLowerAscii(readLine(stdin)) == "y"
echo "正在打包中，请稍后..."
packageFile(targetFile, noConsole)
moveFile(targetFile)
echo "打包完成"
discard readLine(stdin)
