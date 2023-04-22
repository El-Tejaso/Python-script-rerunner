# This script is just a frontend.

import src
import os
import time

# Stores all possible commands. 
commands = {}

def get_possible_next_arg(string : str, default=None):
    if ' ' in string:
        return string.split(' ', maxsplit=1)

    return [string, default]


def run_cmd(cmd):
    [cmd, args] = get_possible_next_arg(cmd, "")

    if cmd not in commands:
        print(f"{cmd} is not a valid command. For a list of valid commands, use the 'help' command")
        return
    
    try:
        print(end="\n")
        commands[cmd](args)
        print(end="\n")
    except Exception as err:
        print ("an error occured when trying to execute the command:\n")
        print(err)

def run_program():
    print("Started. Enter 'help' for help")

    while True:
        # print("> ", end="")
        cmd = input("> ")

        run_cmd(cmd)


def help(sub_command):
    """Lists all commands and the first line of their docs. Run help [command] for non-abridged help on a command."""

    if sub_command != "":
        if sub_command not in commands:
            raise Exception(f"Command not found - {sub_command}")
        
        print(commands[sub_command].__doc__)
    else:
        for k, v in commands.items():
            pydoc = v.__doc__
            if pydoc != None:
                lines = pydoc.count("\n")
                if lines > 0:
                    [pydoc, _] = pydoc.split('\n', maxsplit=1)
                    pydoc += f" ({lines} more lines)"
            
            print(k, "\t", pydoc)


commands["help"] = help

def cd(args):
    """Sets the current working directory"""

    os.chdir(args)
    print("changed current directory to :", os.getcwd())
    ls("")

def ls(args):
    """List all files in the current working directory"""

    dirs = os.listdir(os.getcwd())
    print("Files:\n\t" + ", ".join(dirs))

def run(args):
    """Usage: run [filename] [delimiter_after]. This reads an entire python file, and then runs it. You can optionally run all code after a specific string."""

    [file, delim] = get_possible_next_arg(args, "")

    print(f"running {file} ...\n")
    t0 = time.time()
    
    src.run_file(file, from_delimiter=delim)

    print(f"\ndone in {time.time()-t0}s")

def eval_fn(args):
    """Evaluates the python expression, and prints the output"""

    output = src.run_code_raw(args)
    print(end="\n")
    print(output)

def clear(args):
    src.clear()
    print("globals cleared")

def exit_fn(args):
    """No points for guessing this one"""

    print("See you next time!")
    exit(0)

def run_section(args):
    """(Not yet implemented) This command runs a a section of your file. 
        (Note that the 'section' construct is made up by this program, and not from the python language)
        You can split up your file into sections with a very specific style of comment, like this for example:

            # ---- Init
            import pandas as pd
            import numpy as np
            import mlframework as ml # I haven't done much ML stuff recently, so I will just do some made up thing for this example
            
            sparse_matrix = np.read(
                pandas.read_csv("100gigMatrix.csv") # TODO: stop storing this as a csv, what were we thinking
            )

            # ---- Training the network

            gpt6 = ml.llm("gpt6")
            gpt6.use_weights(sparse_matrix)

            # ---- Test the program

            transcript = "Could you please write me gpt7? I would really appreciate it, thanks"
            while !gpt6.reached_stopword():
                response = response + gpt6.infer_next_line(response)

            ... 

        With this command, you can run each of these "Init", "Training the network" or "Test the program" stages separately.
        Running `section Init` should run everything after # ---- Init up to the next # ---- section. 
    """

    [file, section] = get_possible_next_arg(args, None)
    if section == None:
        raise Exception("No section was specified. Type 'help section' for more info")

def vars(filterStr):
    """Lists all variables (Note: __builtins__ are hidden). Run vars [name] to filter the list"""

    # we want to ignore __builtins__, so this is 1 and not 0, like you would expect
    if len(src.run_file_globals) <= 1:
        print("No globals yet. Run a script or two, and come back")
        return

    filterStr = filterStr.lower()
    for k, v in src.run_file_globals.items():
        if k == "__builtins__":
            continue

        if filterStr != "" and filterStr not in k:
            continue

        readable_string = v.__str__().replace("\t", "    ")
        if '\n' in readable_string:
            readable_string = readable_string.split('\n')[0]

        max_len = 100
        if len(readable_string) > max_len:
            readable_string = readable_string[0:max_len-3] + "..."

        print(f"\t'{k}' [{type(v)}] : {readable_string}")

commands["cd"] = cd
commands["ls"] = ls
commands["run"] = run
commands["section"] = run_section
commands[">"] = eval_fn
commands["clear"] = clear
commands["exit"] = exit_fn
commands["vars"] = vars

if __name__ == "__main__":
    # # Some sort of testing
    # run_cmd("cd testing")
    # run_cmd("run init")
    # run_cmd("run algorithm")
    # run_cmd("vars")

    # start loop now
    run_program()