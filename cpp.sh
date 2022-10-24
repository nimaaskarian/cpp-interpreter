#!/bin/bash
errorStart="> cpp-interpreter error: "
logStart="> cpp-interpreter: "
noFileError="$errorStart No files passed !!"

if [ $# -eq 0 ]; then
  echo $noFileError
  exit 1
fi

for arg in "$@"
do 
  if [[ "$arg" == "-pwd" ]]; then
    isPwd=1
    dir=$PWD
  fi
done

if [[ "$dir" == "" ]]; then 
  if [[ $# -eq 0 ]]; then 
    echo $noFileError
    exit 1
  fi
elif [[ $# -lt 2 ]]; then 
    echo $noFileError
    exit 1
fi

for input in "$@"
do
  if [[ ! "$input" == "-pwd" ]]; then 
    if [ -f "$input" ]; then 
      if [[ $dir == "" ]]; then
        dir=/tmp/cpp-interpreter
      fi
      trimmedInput=${input#*/}
      output=$dir/${trimmedInput%.*}
      if [[ isPwd -eq 1 ]]; then
        output=$dir/${input%.*}
      fi
      if [ ! -d $dir ]; then
        mkdir $dir
      fi
      g++ "$input" -o "$output"
      if [ $? -eq 0 ]; then 
        echo "$logStart Running $input"
        "$output"
      fi
    else 
      echo "$errorStart File $input not found !!"
    fi
  fi
done
