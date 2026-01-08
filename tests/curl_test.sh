#!/bin/bash

# Quick test for the Doorbell Compliment Service
# Usage: ./curl_test.sh sample.jpg

FILE=${1:-sample.jpg}

curl -X POST \
  -F "file=@${FILE}" \
  http://localhost:8000/compliment \
  | jq .

