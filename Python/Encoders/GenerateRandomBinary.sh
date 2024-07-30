#!/bin/bash

# Function to display usage
usage() {
    echo "Usage: $0 <output_file> <size_in_bytes>"
    exit 1
}

# Check for the correct number of arguments
if [ "$#" -ne 2 ]; then
    usage
fi

OUTPUT_FILE=$1
SIZE_IN_BYTES=$2

# Check if size is a valid number
if ! [[ "$SIZE_IN_BYTES" =~ ^[0-9]+$ ]]; then
    echo "Error: Size must be a valid number."
    usage
fi

# Generate random binary file
dd if=/dev/urandom of="$OUTPUT_FILE" bs=1 count="$SIZE_IN_BYTES" iflag=fullblock

# Confirm completion
if [ $? -eq 0 ]; then
    echo "Random binary file '$OUTPUT_FILE' of size $SIZE_IN_BYTES bytes has been created."
else
    echo "Failed to create random binary file."
    exit 1
fi

