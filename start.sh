#!/bin/bash

caminho=$(pwd)
clear
echo
echo
echo "Starting DisSafe Dashboard"
echo
echo
"$caminho/.venv/bin/python" "$caminho/run.py"
echo
echo