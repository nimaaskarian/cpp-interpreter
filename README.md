# cpp-interpreter
An "interpreter" layer for cpp, compiles your cpp file and shows the output directly, written in BASH/Python3 and uses g++ (gcc) as its compiler.  

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
4. Put cpp.py into your path (`cp cpp-interpreter/cpp.py /bin/cpy` or do a symlink: `ln -sr cpp-interpreter/cpp.py /bin/cpy`), or make a function in your shell's rc file like so:  
`alias cpy=/absolute/path/to/cpp-interpreter/cpp.py`

## Usage
- You may use this project in any UNIX-based operating system that has g++ in its path.  
- General usage is like so: `cpy filename.cpp`.
- use `--help` or `-h` option to see help options.

## Uninstall
1. Remove from path
    - Remove alias definition from your rc file.
    - Or if you did the cp or symlink, use `rm /bin/cpy`
2. Go where you did the `git clone https://github.com/nimaaskarain/cpp-interpreter` and `rm -rf cpp-interpreter`
3. please don't do this this is a good script :(

## Why?
- It's easier this way, specially if you're new to cpp and trying to figure out whats going on.
- It won't create annoying binaries in your git repository, that you will need to delete everytime you want to commit.
- It may be better to use `make`. But this project will slowly become more.
