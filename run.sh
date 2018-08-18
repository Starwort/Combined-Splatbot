#!/bin/bash
echo a > restart.txt
while [ -f restart.txt ]
do
    git pull
    python3.6 randomiser.py
done