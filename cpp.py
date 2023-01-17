#!/bin/python3
import sys
import subprocess
import os
import time
import hashlib

default_dir = "/tmp/cpp-interpreter/"
defined_args=["-sd", "-wd", "-m","-M", "-q", "-j","-h","-r","--help","--stdin","--gcc","--repeat","--force"]

args = sys.argv[1:]
def init():
    if (hasArgs("--stdin")):
        filename = "/tmp/cpy-stdin-"+str(time.time())+".cpp"
        f = open(filename, "a")
        try:
            for line in sys.stdin:
                if (line):
                    f.write(line)
        except KeyboardInterrupt:
            conPrint("\n"+info_msg.format('recieving inputs ended'))
        f.close()
        args.append(filename)
    if hasArgs(["-h", "--help"]) or len(args) == 0:
        conPrint("""Usage: cpy [FILES...] [OPTIONS...] [G++ OPTIONS...]

Help Option:
  -h, --help         Shows help options

Application Options:
  -m                 Minimal file paths
  -M                 Don't show compile info
  -j                 Compile FILES into one binary
  -q                 Quite (no messages)
  -wd                Export binary in working directory
  -sd                Export binary in same directory as .cpp file
  --force            Force recompile
  --stdin            Gets input f rom stdin
  --gcc              Use gcc instead of g++ (for c language)
  -r,--repeat        Repeats compiling and running. hit ^C repeatedly to abort

G++ Options:
  Any options beside Application Options will be passed 
  to G++ itself. If you're getting compile errors and you
  don't know why, its probably an issue with an option.""")
        return

    if hasArgs("-j"):
        files = [arg for arg in args if arg not in defined_args]
        dir = make_dir_name(files[0])
        print_name = make_print_name(files)
        return run(compile(files,os.path.join(dir, make_compound_hash(files)),print_name),print_name)
    else:
        files=[arg for arg in args if arg not in defined_args and not arg.startswith("-")]
        compiler_args=[arg for arg in args if arg not in defined_args and arg.startswith("-")]
        for file in files:
            if file in defined_args: continue
            print_name = make_print_name([file])

            if not os.path.exists(file):
                conPrint(filenotfound_error_msg.format(print_name))
                continue
            dir = make_dir_name(file)
            return run(compile([file],make_compile_path(dir, file),print_name,compiler_args),print_name)

    if (hasArgs("--stdin")):
        os.remove(filename)

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
# warning_msg = bcolors.WARNING+"WARNING: {}"
filenotfound_error_msg = error_msg.format("file '{}' not found")
compile_error_msg = error_msg.format("compile failed")
running_error_msg = error_msg.format("something went wrong in running")
interrupt_error_msg = error_msg.format("user keyboard interrupt (exited)")

def make_dir_name(path):
    if hasArgs("-sd"): return os.path.dirname(path)
    if hasArgs("-wd"): return os.path.dirname("./")
    if not os.path.exists(default_dir):
        os.makedirs(default_dir)
    return default_dir

def make_compound_hash(files):
        hash = ""
        files.sort()
        for file in files:
            if hash:
                hash+="-"
            hash+=file_hash(file)
        return hash
def file_hash(path):
    f=open(path, "r")
    return hashlib.md5( f.read().encode() ).hexdigest()

def make_print_name(paths):
    if hasArgs("-m"): 
        return ", ".join([os.path.basename(path) for path in paths])
    return ", ".join(paths)

def make_compile_path(dir,path):
    # filename=os.path.basename(path)
    # filename_without_ext = os.path.splitext(filename)[0]
    return os.path.join(dir, file_hash(path))
    

def run(file,fullname):
    if file == "": return
    conPrint(running_msg.format(fullname)+bcolors.ENDC)
    code=1
    try:
        subprocess.run([file])
        code=0
    except KeyboardInterrupt: 
        conPrint("\n"+interrupt_error_msg)
        code=1
    except Exception:
        conPrint("\n"+running_error_msg)
    finally: return code

def compile(inputs,output,filename,compile_args=[]):

    if not hasArgs("--force"):
        if hasArgs("-j"):
            if (os.path.isfile(default_dir+make_compound_hash(inputs))):
                return output
        else:
            inputs = [ input for input in inputs if not os.path.isfile(default_dir+file_hash(input))]

    if not len(inputs):
        return output
    start_time = time.time()
    conPrint(compiling_msg.format(filename)+bcolors.ENDC)
    compiler = "gcc" if hasArgs("--gcc") else "g++"
    child = subprocess.Popen([compiler] +compile_args+ inputs +   ["-o", output ],stdout=subprocess.PIPE)
    child.communicate()
    if child.returncode != 0:
        conPrint(compile_error_msg)
        return ""

    if not hasArgs("-M"):
        conPrint(compiled_msg.format(str(round((time.time()-start_time)*1000)/1000) + "s")+bcolors.ENDC)
    return output

def hasArgs(input):
    # check if input is a list
    doesntExist = Exception(error_msg.format(f"Argument {input} doesn't exist"))
    if type(input) != list: 
        if not input in defined_args: raise doesntExist
        return input in args
    # input its a list here
    for item in input:
        if not item in defined_args: raise doesntExist
        if item in args: return True
    return False

def conPrint(*messages):
    if not hasArgs("-q"):
        print(*messages)


while True:
    if init()==1:
        break
    if not hasArgs(["-r","--repeat"]):
        break
