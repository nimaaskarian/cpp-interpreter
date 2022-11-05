#!/bin/python3
import sys
import subprocess
import os
import time

default_dir = "/tmp/cpp-interpreter"

args = sys.argv[1:]
quite = "-q" in args
more_minimal = "-M" in args
def init():
    defined_args=["-wd", "-m","-M", "-q", "-j","-h","--help"]
    if "-h" in args or "--help" in args or len(args) == 0:
        print("""Usage: cpy [FILES...] [OPTIONS...] [G++ OPTIONS...]

Help Option:
    -h           Shows help options

Application Options:
    -m           Minimal file paths
    -M           Don't show compile info
    -j           Compile FILES into one binary
    -q           Quite (no messages)
    -wd          Export binary in working directory

G++ Options:
    Any options beside Application Options will be passed to G++ itself. 
    If you're getting compile errors and you don't know why, its probably an
    issue with an option.""")
        return

    if "-j" in args:
        files = [arg for arg in args if arg not in defined_args]
        dir = make_dir_name(files[0])
        print_name = make_print_name(files)
        run(compile(files,make_compile_path(dir, files[0]),print_name),print_name)
    else:
        for arg in args:
            if arg in defined_args: continue
            print_name = make_print_name([arg])

            if not os.path.exists(arg):
                print(filenotfound_error_msg.format(print_name))
                continue
            dir = make_dir_name(arg)

            run(compile([arg],make_compile_path(dir, arg),print_name),print_name)
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

info_msg = bcolors.HEADER + "INFO: {}"
running_msg = info_msg.format("running: {}")
compiling_msg = info_msg.format("compiling: {}")
compiled_msg = info_msg.format("compiled in {}")

error_msg = bcolors.FAIL+"ERROR: {}"
filenotfound_error_msg = error_msg.format("file '{}' not found")
compile_error_msg = error_msg.format("compile failed")
running_error_msg = error_msg.format("smth went wrong in running")

def make_dir_name(path):
    if "-wd" in args: return os.path.dirname(path)
    if not os.path.exists(default_dir):
        os.makedirs(default_dir)
    return default_dir


def make_print_name(paths):
    if "-m" in args: 
        return ", ".join([os.path.basename(path) for path in paths])
    return ", ".join(paths)

def make_compile_path(dir,path):
    filename=os.path.basename(path)
    filename_without_ext = os.path.splitext(filename)[0]
    return os.path.join(dir, filename_without_ext)
    

def run(file,fullname):
    if file == "": return
    if not quite:
        print(running_msg.format(fullname)+bcolors.ENDC)
    try:
        subprocess.run([file])
    except: 
        try:
            subprocess.run(["./"+file])
        except:
            if not quite:
                print("\n"+running_error_msg)

def compile(inputs,output,filename):
    start_time = time.time()
    if not quite and not more_minimal:
        print(compiling_msg.format(filename)+bcolors.ENDC)
    child = subprocess.Popen(["g++"] + inputs + ["-o", output ],stdout=subprocess.PIPE)
    child.communicate()
    if child.returncode != 0:
        if not quite:
            print(compile_error_msg)
        return ""

    if not quite and not more_minimal:
        print(compiled_msg.format(str(round((time.time()-start_time)*1000)/1000) + "s")+bcolors.ENDC)
    return output

init()
