#!/bin/bash
python3 -m venv .env
source .env/bin/activate
echo 'click==7.1.2
pandas
openpyxl
selenium
beautifulsoup4
' > requirements.txt

pip install -r requirements.txt
