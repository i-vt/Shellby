# Define the URL and the path to the file
$url = 'http://localhost:8080/'
$filePath = '/home/x/Documents/file.txt'

# Read the file content
$fileContent = [System.IO.File]::ReadAllBytes($filePath)

# Create a dictionary for the cookies
$cookies = @{ auth_token = 'secure_token' }

# Create the body content
$formData = @{
    file = [System.IO.FileStream]::new($filePath, [System.IO.FileMode]::Open, [System.IO.FileAccess]::Read)
}

# Send the POST request
$response = Invoke-RestMethod -Uri $url -Method Post -InFile $filePath -ContentType 'multipart/form-data' -WebSession (New-Object Microsoft.PowerShell.Commands.WebRequestSession -Property @{Cookies = $cookies})

# Print the response status code and text
Write-Output $response.StatusCode
Write-Output $response.Content
