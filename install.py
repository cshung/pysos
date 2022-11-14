from sys import stdin
from os import listdir
from os import getcwd
from os import path
from os import mkdir

class installer:
    def __init__(self):
        self.currentDirectory = path.dirname(path.abspath(__file__))
        self.installDirectory = None
        self.srcDirectory = None

    def run(self):
        self.getInstallDirectory()
        if path.exists(self.installDirectory):
            print("The given installation path is invalid")
        else:
            self.install()

    def getInstallDirectory(self):
        defaultInstallDirectory = self.currentDirectory + "\\pysos"
        print("pysos installation")
        print(("Please enter the installation location [%s]: " % defaultInstallDirectory), end="", flush="True")
        self.installDirectory = stdin.readline().strip()
        if self.installDirectory == "":
            self.installDirectory = defaultInstallDirectory

    def install(self):
        mkdir(self.installDirectory)
        self.obtainPykd()
        self.srcDirectory = self.currentDirectory + "\\src"
        scripts = listdir(self.srcDirectory)
        commands = [script[0:len(script)-3] for script in scripts if not script.startswith("lib") and script.endswith(".py")]
        for command in commands:
            self.generateScript(command)
        self.generateLoader(commands)
        print("Installation completed")
        print("Use the command '$$>a<%s\\pysos.script' to load pysos" % self.installDirectory)

    def obtainPykd(self):
        # TODO: Automate this
        pass

    def generateScript(self, command):
        # This command instructs WinDBG to make the command an alias to the underlying !py extension
        scriptTemplate = "as %s !py %s\\%s.py"
        script = scriptTemplate % (command, self.srcDirectory, command)
        scriptFileName = "%s\\%s.script" % (self.installDirectory, command)
        with open(scriptFileName, "w") as scriptFile:
            scriptFile.writelines([script])
    
    def generateLoader(self, commands):
        loaderFileName = "%s\\pysos.script" % self.installDirectory
        lines = []
        lines.append(".load %s\\pykd.dll\n" % self.installDirectory)
        for command in commands:
            lines.append("$$>a<%s\\%s.script\n" % (self.installDirectory, command))
        lines.append("al")
        with open(loaderFileName, "w") as loaderFile:
            loaderFile.writelines(lines)

def main():
    installer().run()

if __name__ == "__main__":
    main()