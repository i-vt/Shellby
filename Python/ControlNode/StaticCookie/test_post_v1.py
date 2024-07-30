import requests

url = 'http://localhost:8080/'
files = {'file': open('/home/x/Documents/file.txt', 'rb')}
cookies = {'auth_token': 'secure_token'}

response = requests.post(url, files=files, cookies=cookies)

print(response.status_code)
print(response.text)
