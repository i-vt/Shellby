import os, base64, datetime, json
def stringToBase64(s):
    return base64.b64encode(s.encode('utf-8'))

def base64ToString(b):
    return base64.b64decode(b).decode('utf-8')

def replaceIfExists(primary_string: str = "", string_to_replace: str = ""):
    if "" in [primary_string, string_to_replace] or string_to_replace not in primary_string: return primary_string
    while string_to_replace in primary_string: primary_string = primary_string.replace(string_to_replace,"")
    return primary_string


def setVariables(string_passed: str = "", ip: str = "10.10.10.256", port: str = "90001", shell: str = "/bin/sh"):
    string_passed = replaceIfExists(string_passed,ip)
    string_passed = replaceIfExists(string_passed,port)
    string_passed = replaceIfExists(string_passed,shell)


with  open("OneLinerShells.txt", "r") as objFile: 
    content = objFile.read()
    arr = content.split("\n")
    with open('copy_paste.b64', 'wb') as out_file: out_file.write(stringToBase64(content))


shells = {"date":str(datetime.datetime.now())}
counter = 0
for i in arr:
    counter += 1 
    encoded = stringToBase64(i)
    decoded = base64ToString(encoded)
    if "10.10.10.256" not in decoded: continue
    if "|" in decoded:
        print(decoded)
        split  = decoded.split("|")[0]
        decoded = replaceIfExists(decoded,split + "|")
        print(counter,split, decoded)

        shells[split] = str(stringToBase64(decoded))

print(shells)

print(json.dumps(shells, indent = 4), 8)

with open('data.json', 'w') as out_file:
     json.dump(shells, out_file)

