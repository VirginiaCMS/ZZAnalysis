#! /bin/bash

python jetpt.py $1 $2 $3
python jeteta.py $1 $2 $3 
python njet.py $1 $2 $3
python pteta.py $1 $2 $3
eog *.png