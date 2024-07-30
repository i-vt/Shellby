#!/bin/bash

# Configuration
URL="http://localhost:8080/"
USERNAME="admin"
PASSWORD="password"
FILE_PATH="/home/x/Documents/file.txt"

# Encode credentials to base64
ENCODED_CREDENTIALS=$(echo -n "$USERNAME:$PASSWORD" | base64)

# Send POST request with file upload
response=$(curl -X POST "$URL" \
    -H "Authorization: Basic $ENCODED_CREDENTIALS" \
    -F "file=@$FILE_PATH")

# Output result
echo "$response"

