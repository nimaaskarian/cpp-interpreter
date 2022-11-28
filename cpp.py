#!/bin/python3
import sys
import subprocess
import os
import time

default_dir = "/tmp/cpp-interpreter"

args = sys.argv[1:]
def init():
    defined_args=["-wd", "-m","-M", "-q", "-j","-h","-r","--help","--stdin","--gcc","--repeat"]
    if ("--stdin" in args):
        filename = "/tmp/cpy-stdin-"+str(time.time())+".cpp"
        f = open(filename, "a")
        try:
            for line in sys.stdin:
                if (line):
                    f.write(line)
        except KeyboardInterrupt:
            print("\n"+info_msg.format('recieving inputs ended'))
        f.close()
        args.append(filename)
    if hasArgs(["-h", "--help"]) or len(args) == 0:
        print("""Usage: cpy [FILES...] [OPTIONS...] [G++ OPTIONS...]

Help Option:
  -h, --help         Shows help options

Application Options:
  -m                 Minimal file paths
  -M                 Don't show compile info
  -j                 Compile FILES into one binary
  -q                 Quite (no messages)
  -wd                Export binary in working directory
  -sd                Export binary in same directory as .cpp file
  --stdin            Gets input f rom stdin
  --gcc              Use gcc instead of g++ (for c language)
  -r,--repeat        Repeats compiling and running. hit ^C repeatedly to abort

G++ Options:
  Any options beside Application Options will be passed 
  to G++ itself. If you're getting compile errors and you
  don't know why, its probably an issue with an option.""")
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
                return 1
                continue
            dir = make_dir_name(arg)

            run(compile([arg],make_compile_path(dir, arg),print_name),print_name)
    if ("--stdin" in args):
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
filenotfound_error_msg = error_msg.format("file '{}' not found")
compile_error_msg = error_msg.format("compile failed")
running_error_msg = error_msg.format("something went wrong in running")
interrupt_error_msg = error_msg.format("user keyboard interrupt")

def make_dir_name(path):
    if hasArgs("-sd"): return os.path.dirname(path)
    if hasArgs("-wd"): return os.path.dirname("./")
    if not os.path.exists(default_dir):
        os.makedirs(default_dir)
    return default_dir


def make_print_name(paths):
    if hasArgs("-m"): 
        return ", ".join([os.path.basename(path) for path in paths])
    return ", ".join(paths)

def make_compile_path(dir,path):
    filename=os.path.basename(path)
    filename_without_ext = os.path.splitext(filename)[0]
    return os.path.join(dir, filename_without_ext)
    

def run(file,fullname):
    if file == "": return
    conPrint(running_msg.format(fullname)+bcolors.ENDC)
    try:
        subprocess.run([file])
    except KeyboardInterrupt: 
        conPrint("\n"+interrupt_error_msg)
    except Exception:
        conPrint("\n"+running_error_msg)

def compile(inputs,output,filename):
    start_time = time.time()
    conPrint(compiling_msg.format(filename)+bcolors.ENDC)
    compiler = "gcc" if hasArgs("--gcc") else "g++"
    child = subprocess.Popen([compiler] + inputs + ["-o", output ],stdout=subprocess.PIPE)
    child.communicate()
    if child.returncode != 0:
        conPrint(compile_error_msg)
        return ""

    if not hasArgs("-M"):
        conPrint(compiled_msg.format(str(round((time.time()-start_time)*1000)/1000) + "s")+bcolors.ENDC)
    return output

def hasArgs(input):
    # check if input is a list
    if type(input) != list: return input in args
    # input its a list here
    for item in input:
        if item in args: return True
    return False

def conPrint(*messages):
    if not hasArgs("-q"):
        print(*messages)


while True:
    error = init()
    if error == 1 or not hasArgs(["-r","--repeat"]):
        break
