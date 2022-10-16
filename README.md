# cpp-interpreter
An "interpreter" layer for cpp, written in BASH and uses g++ (gcc) as its compiler.  

## Installation
1. Clone this project: `git clone https://github.com/nimaaskarian/cpp-interpreter`  
2. Put cpp.sh into your path (`cp cpp-interpretor/cpp.sh /bin/cpp`), or make a function in your shell's rc file like so:  
`function cpp(){  
    /path/to/cpp-interpretor/cpp.sh $@  
}`

## Usage
- You may use this project in any UNIX-based operating system that has g++ in its path.  
- General usage is like so: `cpp filename.cpp`, or if you want the binary to be created in your current directory, pass `-pwd` option like so: `cpp filename.cpp -pwd` or `cpp -pwd filename.cpp`.
