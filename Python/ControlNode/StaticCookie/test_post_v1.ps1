# Define the URL and the path to the file
$url = 'http://localhost:8080/'
$filePath = '/Temp/file.txt'

# Read the file content
$fileContent = Get-Content -Path $filePath -Raw

# Create a dictionary for the cookies
$cookies = @{ auth_token = 'secure_token' }

# Create a form-data body
$formData = @{
    file = New-Object System.Net.Http.FormFileContent($filePath, [System.Text.Encoding]::UTF8.GetBytes($fileContent), 'text/plain')
}

# Send the POST request
$response = Invoke-WebRequest -Uri $url -Method Post -Form $formData -WebSession (New-Object Microsoft.PowerShell.Commands.WebRequestSession -Property @{Cookies = $cookies})

# Print the response status code and text
Write-Output $response.StatusCode
Write-Output $response.Content
