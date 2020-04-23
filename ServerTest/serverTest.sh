#!/bin/bash
echo "Beginning Server Testing"

python3 RequestTest.py 1 1 1
python3 RequestTest.py 0 0 0
python3 RequestTest.py 1 2 0 
python3 RequestTest.py 9999 0 0 
python3 RequestTest.py 0 9999 1 

echo "Testing complete"

