#!/bin/python3
import sys, subprocess, os, time, hashlib, argparse

default_dir = "/tmp/cpp-interpreter/"
# defined_args=["-sd", "-wd","--pkg", "-m","-M", "-q", "-j","-h","-r","--help","--stdin","--gcc","--repeat","--force","-o"]

# args = sys.argv[1:]
parser = argparse.ArgumentParser(prog=sys.argv[0])
parser.add_argument('-q', '--quite',dest="quite", action="store_true", help="Don't print messages")
parser.add_argument('-r', '--repeat',dest="repeat", action="store_true", help="Repeat running/compiling process until user interrupt")
parser.add_argument('-j', '--join',dest="join", action="store_true", help="Compile files together instead of compiling one by one")
parser.add_argument('-c', '--compiler=',dest="compiler", action="store",help="backend compiler (default is g++)",default="g++")
parser.add_argument('-m', '--minimal-paths', dest="minimal", action="store_true",help="Minimal file paths")
parser.add_argument('-M', '--no-compile-messages', dest="no_compile_messages",
                    action="store_true",help="Don't print compile messages")
parser.add_argument('-f', '--force', dest="force", action="store_true",help="Force recompile")
parser.add_argument('-o', '--output=', dest="output", action="store",help="Output file name")
parser.add_argument('-Oc', '--compiler-options=', dest="compiler_options", action="store",help="Compiler options (passed to COMPILER)",default=[])
parser.add_argument('-Or', '--run-options=', dest="run_options", action="store",help="Run options (passed to the binary file)",default=[])
parser.add_argument('-sd', '--select-directory=', dest="select_directory", action="store",help="Select a directory to compile to",default="")
parser.add_argument('-wd', '--working-directory', dest="working_directory", action="store_true",help="Compile in working directory")
parser.add_argument('-', '--stdin', dest="stdin", action="store_true",help="Get input from stdin")
parser.add_argument('--pkg=', dest="pkg", action="store",help="Append pkg-config flag and libs to compiler")
parser.add_argument('files', nargs='*', action="store")
args = parser.parse_args()

if len( sys.argv ) <= 1 or not len(args.files):
    parser.print_usage()
def init():
    if (args.stdin):
        filename = "/tmp/cpy-stdin-"+str(time.time())+".cpp"
        f = open(filename, "a")
        try:
            for line in sys.stdin:
                if (line):
                    f.write(line)
        except KeyboardInterrupt:
            conPrint("\n"+info_msg.format('recieving inputs ended'))
        f.close()
        args.files.append(filename)

    if args.join:
        dir = make_dir_name()
        print_name = make_print_name(args.files)
        return run(compile(args.files,os.path.join(dir, make_compound_hash(args.files)),print_name,dir),print_name)
    else:
        for file in args.files:
            print_name = make_print_name([file])

            if not os.path.exists(file):
                conPrint(filenotfound_error_msg.format(print_name))
                continue
            dir = make_dir_name()
            return run(compile([file],make_compile_path(dir, file),print_name,dir),print_name)

    if (args.stdin):
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

def make_dir_name():
    if args.select_directory: return os.path.dirname(args.select_directory)
    if args.working_directory: return os.path.dirname("./")
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
    if args.minimal: 
        return ", ".join([os.path.basename(path) for path in paths])
    return ", ".join(paths)

def make_compile_path(dir,path):
    # filename=os.path.basename(path)
    # filename_without_ext = os.path.splitext(filename)[0]
    if args.output:
        name = args.output
    else:
        name = file_hash(path)

    return os.path.join(dir, name)
    

def run(file,fullname):
    if file == "": return
    conPrint(running_msg.format(fullname)+bcolors.ENDC)
    code=1
    try:
        subprocess.run([os.path.join(args.select_directory,file)]+args.run_options)
        code=0
    except KeyboardInterrupt: 
        conPrint("\n"+interrupt_error_msg)
        code=1
    except Exception as e:
        print(e)
        conPrint("\n"+running_error_msg)
    finally: return code

def compile(inputs,output,filename,dir,compile_args=args.compiler_options):

    if not args.force:
        if args.join:
            if (os.path.isfile(os.path.join(dir, make_compound_hash(inputs)))):
                return output
        else:
            inputs = [ input for input in inputs if not os.path.isfile(make_compile_path(dir,input))]

    if not len(inputs):
        return output
    start_time = time.time()
    conPrint(compiling_msg.format(filename)+bcolors.ENDC)
    if args.pkg:
        compile_args += subprocess.check_output("pkg-config --cflags "+args.pkg, shell=True).split()
        compile_args += subprocess.check_output("pkg-config --libs "+args.pkg, shell=True).split()
    child = subprocess.Popen([args.compiler] +compile_args+ inputs +   ["-o", output ],stdout=subprocess.PIPE)
    child.communicate()
    if child.returncode != 0:
        conPrint(compile_error_msg)
        return ""

    if not args.no_compile_messages:
        conPrint(compiled_msg.format(str(round((time.time()-start_time)*1000)/1000) + "s")+bcolors.ENDC)
    return output

def conPrint(*messages):
    if not args.quite:
        print(*messages)


while True:
    if init()==1:
        break
    if not args.repeat:
        break
