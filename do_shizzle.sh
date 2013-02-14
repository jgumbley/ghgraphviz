#!/bin/bash
set -e
python make_chart.py
sfdp output.out -Tpng > out.png
open -a Preview out.png
