#!/bin/bash
sleep 30
stress -c 22 -m 22  &
sleep 30
python3 workloadrunstress.py $1
