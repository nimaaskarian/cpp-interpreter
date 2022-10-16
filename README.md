# cpp-interpreter
An "interpreter" layer for cpp, compiles your cpp file and shows the output directly, written in BASH and uses g++ (gcc) as its compiler.  

## Installation
1. Install gcc (If you didn't find your distro, search in your distros docs in how to install):
    - Arch (and arch based distros): `sudo pacman -S gcc`
    - Debian (and debian/ubuntu based distros like mint): `sudo apt install build-essential`
   then do `gcc -v` to verify the installation. 
2. Clone this project: `git clone https://github.com/nimaaskarian/cpp-interpreter`  
3. Put cpp.sh into your path (`cp cpp-interpretor/cpp.sh /bin/cpp`), or make a function in your shell's rc file like so:  
`function cpp(){  
    /path/to/cpp-interpretor/cpp.sh $@  
}`

## Usage
- You may use this project in any UNIX-based operating system that has g++ in its path.  
- General usage is like so: `cpp filename.cpp`, or if you want the binary to be created in your current directory, pass `-pwd` option like so: `cpp filename.cpp -pwd` or `cpp -pwd filename.cpp`.
