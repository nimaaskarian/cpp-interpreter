#!/bin/bash
noFileEr="No files passed !!"
if [ $# -eq 0 ]; then
  echo $noFileEr
  exit 1
fi

for arg in "$@"
do 
  if [[ "$arg" == "-pwd" ]]; then
    dir=$PWD
  fi
done

if [[ "$dir" == "" ]]; then 
  if [[ $# -eq 0 ]]; then 
    echo $noFileEr
    exit 1
  fi
elif [[ $# -lt 2 ]]; then 
    echo $noFileEr
    exit 1
fi

for input in "$@"
do
  if [[ ! "$input" == "-pwd" ]]; then 
    if [ -f "$input" ]; then 
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
      echo "File $input not found !!"
    fi
  fi
done
