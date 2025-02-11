#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <text> <emoji>"
    exit 1
fi

# Assign arguments to variables
TEXT=$1
EMOJI=$2

# Run the curl request
curl -X GET "https://elite.niceygy.net/status?text=${TEXT}&emoji=${EMOJI}"
echo \n