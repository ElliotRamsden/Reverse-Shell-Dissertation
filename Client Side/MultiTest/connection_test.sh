#!/bin/bash

for i in {1..2}; do
	gnome-terminal -- bash -c "python3 client.py; exec bash"
done

exit 0
