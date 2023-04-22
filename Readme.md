# Python advanced REPL

This is an interactive python script that can run python files, and preserve the global state between runs.
It is helpful for when the initialization step of your code (like loading a large csv or asset) takes a long time, which would make rerunning the script over and over again directly a bit unpractical. 

A Jupyter notebook seems to be the accepted solution for this kind of problem, but I don't like it because:
- Your can't work on your code as a collection of python files forming a software module
- You can't edit the code with an editor of your choice unless that editor has a Jupyter Notebook extension
    - The Jupyter Notebook extension is not guaranteed to work all the time. Maybe if it had worked for me today, I wouldn't have made this ...
- It is overkill for something that can be achieved quite simply

## How to use

Download the main.py and put it somewhere.

Now run it like `python main.py`. You should get an interactive REPL-like command line interface. 
Type `help` and hit enter to see all the commands you have.

An example use:

```
D:\Some\Directory>python main.py
Started. Enter 'help' for help
> cd testing

changed current directory to : D:\Projects\Python\ComputeGraph\testing
Files:
        algorithm.py, init.py

> run algorithm.py

running algorithm.py ...
an error occured when trying to execute the command:

name 'x' is not defined
```

Note that this will run arbitrary python code, with `exec`.
Also, try to avoid running code that will ask for input, make sure you are doing that `if __name__ == "__main__":` thing.


```
> run init.py

running init.py ...

done

> run algorithm.py

running algorithm.py ...
55

done

> vars

        x: 55
        function: <function function at 0x0000024B22178AF0>

>

```

Note that the 



## Future

Something I can implement here that is probably impossible to do in Jupyter is something that keeps track of state, and
can undo/redo the results of executing a particular python script. 
It should also be possible to keep track of an undo tree, if a linear track isn't enough. 
Not sure how useful it is, but I am fairly certain it can be done, for variables that can be deep-copied, at least.
There will be some things for which it is pretty much impossible.