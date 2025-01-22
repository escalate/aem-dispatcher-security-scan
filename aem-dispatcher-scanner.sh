#!/bin/bash
# ========================================================================================
# Title: AEM Scanner
# Description: AEM Dispatcher Scanner is a tool for scanning AEM Dispatcher for vulnerabilities.
# Author: Felix Börner
# Script Version: 1.0
# Script Author: Davorin Špičko
# Script Date: 2025-01-10
# ========================================================================================

NO_COLOR='\033[0m'
GREEN='\033[0;32m'
ORANGE='\033[0;33m'

clear

cat << 'EOF'
    _     _____  __  __                                   
   / \   | ____||  \/  |                                  
  / _ \  |  _|  | |\/| |                                  
 / ___ \ | |___ | |  | |                                  
/_/__ \_\|_____||_|  |_|      _         _                 
|  _ \ (_) ___  _ __    __ _ | |_  ___ | |__    ___  _ __ 
| | | || |/ __|| '_ \  / _` || __|/ __|| '_ \  / _ \| '__|
| |_| || |\__ \| |_) || (_| || |_| (__ | | | ||  __/| |   
|____/ |_||___/| .__/  \__,_| \__|\___||_| |_| \___||_|   
/ ___|   ___  _|_|  _ __   _ __    ___  _ __              
\___ \  / __|/ _` || '_ \ | '_ \  / _ \| '__|             
 ___) || (__| (_| || | | || | | ||  __/| |                
|____/  \___|\__,_||_| |_||_| |_| \___||_|                                          

EOF

echo -e "\nSelect an option:\n"
echo -e "  1. Setup (Clean) environment"
echo -e "  2. Build docker image\n"

read -p "Enter your choice [1-2]: " choice

case $choice in
    1)
        echo -e "${ORANGE}\nCleaning environment...${NO_COLOR}\n"
        if [[ -d .venv ]]; then
            rm -rf .venv/
        fi
        for pyc in $(find . -name "*.pyc"); do
            rm -f $pyc
        done
        for pycache in $(find . -name "__pycache__" ); do
            rm -rf $pycache
        done
        
        echo -e "${ORANGE}Installing virtual environment...${NO_COLOR}\n"
        if [[ ! -z "$(conda -V)" ]]; then
            conda create -q -p .venv python=3.12 -y
            conda install -q pip -p "$(pwd)/.venv" -y
        else
            python3 -m venv .venv
        fi
        
        echo -e "${ORANGE}Installing dependencies...${NO_COLOR}"
        .venv/bin/pip3 install -q -r requirements.txt
        .venv/bin/pip3 install -q -r requirements-dev.txt
        
        echo -e "${GREEN}\n*************************************************************************"
        echo -e "Environment setup complete!"
        echo -e "*************************************************************************\n${NO_COLOR}"
        ;;
    2)
        docker build -t aem-dispatcher-scanner .
        ;;
    *)
        echo "Unknown option! Exiting..."
        exit 0
        ;;
esac

