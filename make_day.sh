#!/bin/bash

dayId=day$1

mkdir $dayId
touch $dayId/notes.txt
touch $dayId/input.txt
cp read.py $dayId/main.py
