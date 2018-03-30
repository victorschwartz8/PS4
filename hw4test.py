#!/usr/bin/python

# Auto Tester for Duke CS/ECE 250, Homework 4, Spring 2017

import sys,os,platform
from optparse import OptionParser

test_dir = 'tests'
suite_names = ['boolean', 'arithmetic', 'shift', 'memory', 'control', 'io' ]
suites = {
    "arithmetic": [
        { "desc": "\"add\", \"addi\", \"sub\" instructions", "args": ['-c 10 -ic 1,reset=1:2,reset=0'] },
    ],
    "boolean": [
        { "desc": "\"nand\", \"xor\" instructions", "args": ['-c 10 -ic 1,reset=1:2,reset=0'] },
    ],
    "shift": [
        { "desc": "\"shl\", \"shra\" instructions", "args": ['-c 10 -ic 1,reset=1:2,reset=0'] },
    ],
    "memory": [
        { "desc": "\"sw\", \"lw\" instructions", "args": ['-c 20 -ic 1,reset=1:2,reset=0'] },
    ],
    "control": [
        { "desc": "\"bgt\", \"beqz\", \"jal\", \"j\", \"jr\" instructions", "args": ['-c 12 -ic 1,reset=1:2,reset=0'] },
    ],
    "io": [
        { "desc": "\"input\", \"output\" instructions", "args": ['-lk tests/io.buffer -c 20 -tty full'] },
    ],
}


parser = OptionParser("Usage: %prog [options] <suite>")
 
parser.add_option("-v", "--verbose", dest="verbose", help="Print extra info.", action="store_true")
 
(options, args) = parser.parse_args()

if (len(args)<=0):
    print "\033[31;7mSelf Tester\033[m for Duke CS/ECE 250, Homework 4, Spring 2017"
    print ""
    parser.print_help()
    print ""
    print "Where <suite> is one of:"
    print "  %-15s: Run all program tests" % ("ALL",)
    print "  %-15s: Remove all the test output produced by this tool" % ("CLEAN",)
    for suite_name in suite_names:
        print "  %-15s: Run tests for %s instructions." % (suite_name,suite_name)
    sys.exit(1)
 
verbose_mode=options.verbose
requested_suite_name = args[0]

def get_expected_output_filename(suite_name, test_num):
    return "tests/%s_expected_%d.txt" % (suite_name, test_num)
    
def get_actual_output_filename(suite_name, test_num):
    return "tests/%s_actual_%d.txt" % (suite_name, test_num)
    
def get_diff_filename(suite_name, test_num):
    return "tests/%s_diff_%d.txt" % (suite_name, test_num)

def get_imem_name(suite_name):
    return "tests/%s.imem.lgsim" % (suite_name)

def get_dmem_name(suite_name):
    return "tests/%s.dmem.lgsim" % (suite_name)

def clean():
    my_system("rm -f "+test_dir+"/*_actual_*.txt")
    my_system("rm -f "+test_dir+"/*_diff_*.txt")

    
def verbose_print(s):
    if verbose_mode: sys.stdout.write("\033[36m%s\033[m\n" % s)

def my_system(command):
    verbose_print("$ %s" % command)
    r = os.system(command)
    if platform.system()[-1] == 'x':
        return r>>8 # platforms ending in 'x' are probably Linux/Unix, and they put exit status in the high byte
    else:
        return r # windows platforms just return exit status directly
    
def run_test_suite(suite_name):
    suite = suites[suite_name]
    if not os.path.isfile('hw4.circ'):
        print "\033[91m%s: Circ file not found in current directory, expected: hw4.circ\033[m" % (suite_name)
        return
    if not os.path.isfile('logisim_cli.jar'):
        print "\033[91m%s: Logisim JAR file not found in current directory, expected: logisim_cli.jar\033[m" % (suite_name)
        return
    for test_num,test in enumerate(suite):
        desc = test['desc']
        args = test['args']
        expected_output_filename = get_expected_output_filename(suite_name, test_num)
        actual_output_filename = get_actual_output_filename(suite_name, test_num)
        diff_filename = get_diff_filename(suite_name, test_num)
        
	if not os.path.isfile(expected_output_filename):
            print "\033[91m%s: Expected output file not found in tests directory, expected: %s\033[m" % (suite_name, expected_output_filename)
            return

        is_pass = True
        reason = ''
        imem_name = get_imem_name(suite_name)
	if not os.path.isfile(imem_name):
	    print "\033[91m%s: Expected imem file not found in tests directory, expected: %s\033[m" % (suite_name, imem_name)
            return
	dmem_name = get_dmem_name(suite_name)
	if not os.path.isfile(dmem_name):
	    print "\033[91m%s: Expected imem file not found in tests directory, expected: %s\033[m" % (suite_name, dmem_name)
            return
	
        command = "java -jar logisim_cli.jar -f hw4.circ -lo %s -la %s %s > %s" % (imem_name, dmem_name, " ".join(args), actual_output_filename)
        r = my_system(command)
        if r != 0:
            is_pass = False
            reason += "Exit status is non-zero. "
            
	command = "diff -bwB %s %s > %s" % (expected_output_filename, actual_output_filename, diff_filename)
	r = my_system(command)
	if r != 0 and is_pass == True:
            is_pass = False
            reason += "Output differs from expected (see diff for details). "

        if is_pass: result_string = "\033[32;7mpass\033[m"
        else:       result_string = "\033[41mFAIL\033[0;31m %s\033[m" % reason
        print "%10s test (%-45s): %s" % (suite_name, desc, result_string)

if requested_suite_name == "ALL":
    for suite_name in suite_names:
        run_test_suite(suite_name)
elif requested_suite_name == "CLEAN":
    clean()
elif requested_suite_name in suite_names:
    run_test_suite(requested_suite_name)
else:
    print "%s: No such test suite" % (requested_suite_name)
