#!/bin/bash
noFileEr="No files passed !!"
if [ $# -eq 0 ]; then
  echo $noFileEr
  exit 1
fi
input=$1
if [[ "$1" == "-pwd" ]]; then
  dir=$PWD
  input=$2
elif [[ "$2" == "-pwd" ]]; then
  dir=$PWD
fi

if [ $input == "" ]; then 
  echo $noFileEr
  exit 1
fi

if [ -f $input ]; then 
  if [[ $dir == "" ]]; then
    dir=/tmp/cpp-interpreter
  fi
  output=$dir/${input%.*}
  if [ ! -d $dir ]; then
    mkdir $dir
  fi
  g++ "$input" -o "$output"
  if [ $? -eq 0 ]; then 
    "$output"
  fi
else 
  echo "File not found !!"
  exit 1
fi
