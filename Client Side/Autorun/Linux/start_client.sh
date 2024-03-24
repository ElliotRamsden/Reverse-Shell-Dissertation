#!/bin/bash

if ! pgrep -f main.py; then
    nohup python3 ~/Artefact/Client/main.py >/dev/null 2>&1 &
fi
