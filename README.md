# cpp-interpreter
An "interpreter" layer for cpp, compiles your cpp file and shows the output directly, written in BASH and uses g++ (gcc) as its compiler.  

Without cpp-interpreter 😩            |  With cpp-interpreter 😎
:-------------------------:|:-------------------------:
![cpp-interpreter-sc1](https://user-images.githubusercontent.com/88832088/196025282-1bc693e8-5d87-401d-95fb-ef02544ba733.png)  | ![cpp-interpreter-sc2](https://user-images.githubusercontent.com/88832088/196025305-e0bae19f-e202-4d44-8ac7-666946580efb.png)



## Installation
1. Install gcc (If you didn't find your distro, consult in your distro's docs in how to install):
    - #### Arch (and arch based distros like endeavor, artix)  
        `sudo pacman -S gcc`
    - #### Debian (and debian/ubuntu based distros like mint)  
        `sudo apt install build-essential`
2. Do `g++ -v` to verify the installation. (it shouldn't give you an error)
3. Clone this project: `git clone https://github.com/nimaaskarian/cpp-interpreter`  
4. Put cpp.sh into your path (`cp cpp-interpreter/cpp.sh /bin/cpp`), or make a function in your shell's rc file like so:  
`function cpp(){  
    /path/to/cpp-interpreter/cpp.sh $@  
}`

## Usage
- You may use this project in any UNIX-based operating system that has g++ in its path.  
- General usage is like so: `cpp filename.cpp`.
- You may also use this command with multiple cpp files: `cpp file1.cpp file2.cpp fileX.cpp whatever.cpp`
- If you want the binary (or binaries) to be created in your current directory, you can pass `-pwd` option: `cpp -pwd filename.cpp` or `cpp file1.cpp file2.cpp -pwd file3.cpp`.

## WHY?
It's easier this way, specially if you're new to cpp and trying to figure out whats going on.
