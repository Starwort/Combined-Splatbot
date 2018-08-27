#!/bin/bash
echo a > restart.txt
while [ -f restart.txt ]
do
    rm restart.txt
    git pull
    python3.6 randomiser.py
done