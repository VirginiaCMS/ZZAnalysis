#! /bin/bash

python jetpt.py $1 $2
python jeteta.py $1 $2
python njet.py $1 $2
eog *.png