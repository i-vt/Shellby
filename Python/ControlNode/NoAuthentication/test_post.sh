#!/bin/bash

# Variables
FILE_PATH="/home/user/Documents/file.txt"
SERVER_URL="http://localhost:8080"


FILENAME=$(basename "$FILE_PATH")

# Check if the file exists
if [ ! -f "$FILE_PATH" ]; then
  echo "File not found: $FILE_PATH"
  exit 1
fi

# Upload the file using curl
curl -v -F "file=@$FILE_PATH" -H "filename: $FILENAME" $SERVER_URL

# Print the status
if [ $? -eq 0 ]; then
  echo "File uploaded successfully"
else
  echo "File upload failed"
fi
