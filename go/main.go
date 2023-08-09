package main

import (
    "bufio"
    "fmt"
    "os"
    "os/exec"
    "path/filepath"
    "strconv"
    "strings"
)

func checkPyinstaller() bool {
    if _, err := exec.LookPath("pyinstaller"); err != nil {
        if _, err := exec.LookPath("pip"); err == nil {
            cmd := exec.Command("pip", "install", "pyinstaller")
            cmd.Run()
        } else if _, err := exec.LookPath("python"); err == nil {
            fmt.Println("请先安装 pip")
            return false
        } else {
            fmt.Println("请先安装 python")
            return false
        }
    }
    return true
}


func getPyFiles() []string {
    files, _ := filepath.Glob("*.py")
    return files
}

func printPyFiles(pyFiles []string) {
    fmt.Println("当前目录下的 .py 文件：")
    for i, file := range pyFiles {
        fmt.Printf("%d. %s\n", i+1, file)
    }
}

func getTargetFile(pyFiles []string) string {
    reader := bufio.NewReader(os.Stdin)
    fmt.Print("请输入要打包的文件序号：")
    fileNumStr, _ := reader.ReadString('\n')
    fileNumStr = strings.TrimSpace(fileNumStr)
    fileNum, _ := strconv.Atoi(fileNumStr)
    targetFile := pyFiles[fileNum-1]
    return targetFile
}

func packageFile(targetFile string, noConsole bool) {
    if noConsole {
        cmd := exec.Command("pyinstaller", "--onefile", "-w", targetFile)
        cmd.Stdout = os.Stdout
        cmd.Stderr = os.Stderr
        cmd.Run()
    } else {
        cmd := exec.Command("pyinstaller", "--onefile", targetFile)
        cmd.Stdout = os.Stdout
        cmd.Stderr = os.Stderr
        cmd.Run()
    }
}


func moveFile(targetFile string) {
    exeName := strings.TrimSuffix(targetFile, ".py") + ".exe"
    if _, err := os.Stat(exeName); err == nil {
        os.Remove(exeName)
    }
    os.Rename(filepath.Join("dist", exeName), exeName)

    if _, err := os.Stat("__pycache__"); err == nil {
        os.RemoveAll("__pycache__")
    }
    os.RemoveAll("build")
    os.RemoveAll("dist")
    os.Remove(strings.TrimSuffix(targetFile, ".py") + ".spec")
}

func main() {
    if !checkPyinstaller() {
        os.Exit(0)
    }
    pyFiles := getPyFiles()
    printPyFiles(pyFiles)
    targetFile := getTargetFile(pyFiles)
    reader := bufio.NewReader(os.Stdin)
    fmt.Print("是否需要打包成无控制台版本？(y/n)：")
    noConsoleStr, _ := reader.ReadString('\n')
    noConsoleStr = strings.TrimSpace(noConsoleStr)
    noConsole := strings.ToLower(noConsoleStr) == "y"
    packageFile(targetFile, noConsole)
    moveFile(targetFile)
    fmt.Println("打包完成，回车键关闭程序...")
    reader.ReadString('\n')
}
