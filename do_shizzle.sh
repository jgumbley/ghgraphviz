#!/bin/bash
set -e
python make_chart.py
fdp output.out -Tpng > out.png
open -a Preview out.png
