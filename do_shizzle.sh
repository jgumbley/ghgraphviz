#!/bin/bash
set -e
python make_chart.py
dot output.out -Tpng > out.png
open -a Preview out.png
