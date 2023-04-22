run_file_globals = {}
globals_info = {}

def clear():
    global run_file_globals
    run_file_globals = {}

def run_code_raw(code):
    try:
        return eval(code, run_file_globals, run_file_globals)
    except Exception as err:
        # TODO: better error logging.
        raise err


def run_file(file, from_delimiter):
    text = None
    try:
        text = open(file).read()
    except Exception as err:
        try:
            text = open(file + ".py").read()
        except:
            pass

        if text == None:
            raise err
        
    if from_delimiter != "":
        if from_delimiter not in text:
            raise Exception(f"The file {file} does not contain the delimiter {from_delimiter} anywhere")
        
        [_, text] = text.split(from_delimiter, maxsplit=1)

    try:
        exec(text, run_file_globals)
    except Exception as err:
        # TODO: better error logging
        raise err
    
    

def get_variable(variable):
    if variable not in run_file_globals:
        return [False, None]

    return [True, run_file_globals[variable]]