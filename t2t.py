HELP_DOC = """
TABLE TO TABLE
by Angelo Chan

This is a program for basic table file parsing.

Users can choose to retain the table file format or change it to another file
format. Users select which columns of data will be retained, and which order the columns
will appear in, in the output file. Users can perform basic filtering on the
rows of data.

Accepted file formats:
    - TSV (Tab-Separated Values)
    - CSV (Comma-Separated Values)
    - SSV (Space-Separated Values)

Filtering options (For data in the specified column):
    - EQUALS str        (Data must match the specified text exactly)
    - NOT EQUALS str    (Data must not match the specified value exactly)
    - CONTAINS          (Data must contain the specified value/substring)
    - NOT CONTAINS      (Data must not contain the specified value/substring)
    - GREATER THAN      (Data must be stricly greater than the specified value)
    - GREAQUALS         (Data must be equal to or greater than the specified
                        value)
    - LESS THAN         (Data must be stricly less than the specified value)
    - LEQUALS           (Data must be equal to or less than the specified value)
    - EQUALS int        (Data must match the specified value exactly)
    - NOT EQUALS int    (Data must not match the specified value exactly)
    - EQUALS float      (Data must match the specified value exactly)
    - NOT EQUALS float  (Data must not match the specified value exactly)



USAGE:

    python27 t2t.py <input_path> <{input_format}> <output_path>
            [-f {output_format}] <col_no>... [filter]...



MANDATORY:

    input_path 

        The filepath of the input file.

    input_format

        The file format of the input file. Acceptable options are:
            tsv - Tab-separated values
            csv - Comma-separated values
            ssv - Space-separated values

    output_path

        The filepath of the output file.

OPTIONAL:

    output_format

        The file format of the output file. If no format is specified, the
        output format will be the same as the input format. Acceptable options
        are:
            tsv - Tab-separated values
            csv - Comma-separated values
            ssv - Space-separated values

    col_no

        The columns of data which are to be kept in the output file. The order
        in which the columns are specified will be the order in which they will
        be outputted.

        At least one column needs to be specified. The same column can be
        specified multiple times.

        The column numbers use the index 1 system, not index 0. Ex. To keep the
        first column, enter "1".

    filter

        Optional.
        
        Filtering criteria by which columns are included or excluded. Specifying
        a filtering criteria requires 4 components:

            "<type>col<col_no><operator><query>"

        Examples:

            1) "col2=M"     (Include rows where column 2 is "M")
            2) "!col3<18"   (Exclude rows where column 3 is less than 18)
            3) "+col6!:X"   (Include rows where column 6 does not contain "X")

        Components:

            type

                Specifies whether the criteria is for inclusion or exclusion.
                Leaving it blank will default to inclusion. (Example 1)
                "+" indicates this is an inclusion criteria. (Example 3)
                "!" or "-" indicates this is an exclusion criteria. (Example 2)

            col_no

                The column number on whih the filtering criteria is applied. The
                column numbers use the index 1 system, not index 0. Ex. To
                filter on the first column, enter "1".

            operator

                The kind of filtering to be performed. Valid operators are:

                    =   Equals <string query>
                    !=  Does not equal <string query>
                    :   Contains <query>
                    !:  Does not contain <query>
                    >   Greater than <query>
                    <   Less than <query>
                    >=  Equal to or greater than <query>
                    <=  Equal to or less than <query>
                    i=  Equals <int query>
                    i!= Does not equal <int query>
                    f=  Equals <float query>
                    f!= Does not equal <float query>
                
                The "Equals" and Does not equal" operators can compare ints with
                floats.
                
                NOTE: Some of these operations requires the entire argument
                be enclosed in single or double inverted commas to work
                properly.

            query

                The value used as the substring or cutoff.



EXAMPLES:

    python27 t2t.py Test_Data_1.tsv tsv Test_Output.csv csv 2 3 4 5 col5=Desert
            "col3>1.8" 

USAGE:

    python27 t2t.py <input_path> <{input_format}> <output_path>
            [-f {output_format}] <col_no>... [filter]...
"""



# Configurations ###############################################################

AUTORUN = True

WRITE_PREVENT = False # Completely prevent overwritting existing files
WRITE_CONFIRM = True # Check to confirm overwritting existing files

PRINT_ERRORS = True
PRINT_PROGRESS = True



# Imported Modules #############################################################

import sys



# Enums ########################################################################

class OP:
    EQUALS=1
    NOT_EQUAL=2
    CONTAINS=3
    NOT_CONTAIN=4
    GREATER_THAN=5
    GREAQUALS=6
    LESS_THAN=7
    LEQUALS=8
    EQUALS__INT=9
    NOT_EQUAL__INT=10
    EQUALS__FLOAT=11
    NOT_EQUAL__FLOAT=12



# Strings ######################################################################

STR__use_help = "\nUse the -h option for help:\n\t python t2t.py -h"

STR__no_inputs = "\nERROR: No inputs were given."
STR__insufficient_inputs = "\nERROR: Not enough inputs were given."

STR__IO_error_read = "\nERROR: Input file does not exist or could not be "\
        "opened."
STR__IO_error_write_forbid = """
ERROR: You specified an output file which already exists and the administrator
for this program has forbidden all overwrites. Please specify a different
output file, move the currently existing file, or configure the default options
in t2t.py."""
STR__IO_error_write_unable = """
ERROR: Unable to write to the specified output file."""
STR__invalid_file_format = """
ERROR: Invalid {io} file format: {s}

Please specify one of:
    tsv
    csv
    ssv"""

STR__specify_an_output_format = "\nERROR: Please specify an output format if "\
        "you use the -f argument."

STR__invalid_argument = "\nERROR: Invalid argument: {s}"

STR__at_least_one_column = "\nERROR: Please specify at least one column."

STR__overwrite_confirm = "\nFile already exists. Do you wish to overwrite it? "\
        "(y/n): "

STR__invalid_operation = "\nERROR: Invalid operation specified."



STR__parsing_args = "\nParsing arguments..."

STR__t2t_begin = "\nRunning Table2Table..."

STR__t2t_complete = "\nTable2Table successfully finished."



# Lists ########################################################################

LIST__help = ["-h", "-H", "-help", "-Help", "-HELP"]

LIST__yes = ["Y", "y", "YES", "Yes", "yes", "T", "t", "TRUE", "True", "true"]
LIST__no = ["N", "n", "NO", "No", "no", "F", "f", "FALSE", "False", "false"]

LIST__tsv = ["\t", "T", "t", "TSV", "Tsv", "tsv", "TAB", "Tab", "tab"]
LIST__csv = [",", "C", "c", "CSV", "Csv", "csv", "COMMA", "Comma", "comma"]
LIST__ssv = [" ", "S", "s", "SSV", "Ssv", "ssv", "SPACE", "Space", "space"]

LIST__search_ops = ["=", "!=", ":", "!:", ">", ">=", "<", "<=",
        "i=", "i!=", "f=", "f!="] # Syn with DICT__ops

LIST__math_ops = [OP.GREATER_THAN, OP.GREAQUALS, OP.LESS_THAN, OP.LEQUALS]
LIST__math_ops_i = [OP.EQUALS__INT, OP.NOT_EQUAL__INT]
LIST__math_ops_f = [OP.EQUALS__FLOAT, OP.NOT_EQUAL__FLOAT]



# Dictionaries #################################################################

DICT__delim = {}
for i in LIST__tsv: DICT__delim[i] = "\t"
for i in LIST__csv: DICT__delim[i] = ","
for i in LIST__ssv: DICT__delim[i] = " "



DICT__ops = {
        "=":   OP.EQUALS, 
        "!=":  OP.NOT_EQUAL,
        ":":   OP.CONTAINS,
        "!:":  OP.NOT_CONTAIN,
        ">":   OP.GREATER_THAN,
        ">=":  OP.GREAQUALS,
        "<":   OP.LESS_THAN,
        "<=":  OP.LEQUALS,
        "i=":  OP.EQUALS__INT, 
        "i!=": OP.NOT_EQUAL__INT,
        "f=":  OP.EQUALS__FLOAT, 
        "f!=": OP.NOT_EQUAL__FLOAT
        } # Sync with LIST__search_ops



# File Processing Code #########################################################

def Table_To_Table(path_in, delim_in, path_out, delim_out, columns,
            inc_filters, exc_filters):
    """
    Function which performs the basic table file parsing.
    
    @path_in
            (str - filepath)
            The filepath of the input file. 
    @delim_in
            (str)
            The delimiter use by the input file.
    @path_out
            (str - filepath)
            The filepath of the output file. 
    @delim_out
            (str)
            The delimiter use by the output file.
    @columns
            (list<int>)
            An list of the columns to be retained from the input file, in that
            specified order.
            Uses the 0-index system. (The first column's index number is 0)
    @inc_filters
    @exc_filters
            (list<int,int,str/int/float>)
            A list of filtering criteria. [inc_filters] is a list of criteria
            for inclusion while [exc_filters] is a list of criteria for
            exclusion.
            Each item in the list is a criteria.
            Each criteria item consists of three parts:
                1) The column number of the data to be filtered.
                2) An integer denoting the type of filtering operation:
                    1:  EQUALS (string)
                    2:  NOT_EQUAL (string)
                    3:  CONTAINS
                    4:  NOT_CONTAIN
                    5:  GREATER_THAN
                    6:  GREAQUALS
                    7:  LESS_THAN
                    8:  LEQUALS
                    9:  EQUALS (int)
                    10: NOT_EQUAL (int)
                    11: EQUALS (float)
                    12: NOT_EQUAL (float)
                3) The string/substring/cutoff used for filtering.
    
    Return a value of 0 if the function runs successfully.
    
    Table_To_Table(str, str, str, str, list<int>, list<int,int,str/int/float>,
            list<int,int,str/int/float>) -> int
    """
    printP(STR__t2t_begin)
    
    # Initialize
    r = open(path_in, "U")
    w = open(path_out, "w")

    line = r.readline()

    # Main Loop
    while line:
        
        data = Parse_Line(line, delim_in)

        test = Filter(data, inc_filters, exc_filters)

        if test:
            string = Create_Output(data, columns, delim_out)
            w.write(string)
        
        # Main Loop (2)
        line = r.readline()

    # Finish
    w.close()
    r.close()

    # Exit
    printP(STR__t2t_complete)
    return 0



def Parse_Line(line, delim):
    """
    Parse the raw output of a line from a table file and return a list
    containing all the data values in that line.

    Newline characters are excluded.

    Parse_Line(str, str) -> list<str>
    """
    result = line.split(delim)
    if result[-1][-1] == "\n" or result[-1][-1] == "\r":
        result[-1] = result[-1][:-1]
    return result



def Create_Output(data, columns, delim):
    """
    Take a list of data values, a list of column numbers and a delimiter and
    produce a string indended to be written to an output table file.

    The list of column numbers determines which values from [data] are kept, and
    in what order.

    Create_Output(list<str>, list<int>, str) -> str
    """
    first = columns[0]
    others = columns[1:]

    sb = data[first]
    for i in others:
        sb += (delim + data[i])

    sb += "\n"

    return sb



def Filter(data, inc_filters, exc_filters):
    """
    Take a list of data values, and 2 lists of filtering criteria. Return True
    if the data meets all inclusion criteria and does not meet any exclusion
    criteria. Return false otherwise.

    Filter(list<str>, list<int, int, str/int/float>,
            list<int, int, str/int/float>) -> bool
    """
    inc = Filter_Inc(data, inc_filters)
    exc = Filter_Exc(data, exc_filters)
    if inc and not exc: return True
    return False

def Filter_Inc(data, inc_filters):
    """
    Take a list of data values, and a list of inclusion criteria. Return True
    if the data meets all inclusion criteria. Return False otherwise.

    Filter(list<str>, list<int, int, str/int/float>) -> bool
    """
    for f in inc_filters:
        b = Filter_Single(data, f)
        if not b: return False
    return True

def Filter_Exc(data, exc_filters):
    """
    Take a list of data values, and a list of exclusion criteria. Return True
    if the data meets any of the exclusion criteria. Return False otherwise.

    Filter(list<str>, list<int, int, str/int/float>) -> bool
    """
    for f in exc_filters:
        b = Filter_Single(data, f)
        if b: return True
    return False

def Filter_Single(data, criteria):
    """
    Take a list of data values, and a list representing a filter criteria.
    Return True if the data meets the criteria. Return False otherwise.

    The criteria item consists of three parts:
        1) The column number of the data to be filtered.
        2) An integer denoting the type of filtering operation:
            1:  EQUALS (string)
            2:  NOT_EQUAL (string)
            3:  CONTAINS
            4:  NOT_CONTAIN
            5:  GREATER_THAN
            6:  GREAQUALS
            7:  LESS_THAN
            8:  LEQUALS
            9:  EQUALS (int)
            10: NOT_EQUAL (int)
            11: EQUALS (float)
            12: NOT_EQUAL (float)
        3) The string/substring/cutoff used for filtering.

    Filter(list<str>, [int, int, str/int/float]) -> bool
    """
    col, op, query = criteria
    
    if op == OP.EQUALS:
        if data[col] == query: return True
        return False
    
    elif op == OP.NOT_EQUAL:
        if data[col] != query: return True
        return False
    
    elif op == OP.CONTAINS:
        if query in data[col]: return True
        return False
    
    elif op == OP.NOT_CONTAIN:
        if query not in data[col]: return True
        return False
    
    elif op == OP.GREATER_THAN:
        try:
            d = int(data[col])
        except:
            d = float(data[col])
        if d > query: return True
        return False
    
    elif op == OP.GREAQUALS:
        try:
            d = int(data[col])
        except:
            d = float(data[col])
        if d >= query: return True
        return False
    
    elif op == OP.LESS_THAN:
        try:
            d = int(data[col])
        except:
            d = float(data[col])
        if d < query: return True
        return False
    
    elif op == OP.LEQUALS:
        try:
            d = int(data[col])
        except:
            d = float(data[col])
        if d <= query: return True
        return False
    
    elif op == OP.EQUALS__INT:
        d = int(data[col])
        if d == query: return True
        return False
    
    elif op == OP.NOT_EQUAL__INT:
        d = int(data[col])
        if d != query: return True
        return False
    
    elif op == OP.EQUALS__FLOAT:
        d = float(data[col])
        if d == query: return True
        return False
    
    elif op == OP.NOT_EQUAL__FLOAT:
        d = float(data[col])
        if d != query: return True
        return False
    
    else:
        raise Exception(STR__invalid_operation)



# Command Line Parsing #########################################################

def Parse_Command_Line_Input__t2t(raw_command_line_input):
    """
    Parse the command line input and call the Table_To_Table function with
    appropriate arguments if the command line input is valid.
    """
    printP(STR__parsing_args)
    # Remove the runtime environment variable and program name from the inputs
    inputs = Strip_Non_Inputs(raw_command_line_input)

    # No inputs
    if not inputs:
        printE(STR__no_inputs)
        printE(STR__use_help)
        return 1
  
    # Help option
    if inputs[0] in LIST__help:
        print(HELP_DOC)
        return 0

    # Initial validation
    if len(inputs) < 4:
        printE(STR__insufficient_inputs)
        printE(STR__use_help)
        return 1
    
    valid_in = Validate_Read_Path(inputs[0])
    if valid_in == 1:
        printE(STR__IO_error_read)
        return 1
    
    delim_in = Validate_File_Format(inputs[1])
    if not delim_in:
        printE(STR__invalid_file_format.format(io = "input", s = inputs[1]))
        return 1
    
    valid_out = Validate_Write_Path(inputs[2])
    if valid_out == 2: return 0
    if valid_out == 3:
        printE(STR__IO_error_write_forbid)
        return 1
    if valid_out == 4:
        printE(STR__In_error_write_unable)
        return 1
    
    # Set up rest of the parsing
    path_in = inputs.pop(0)
    inputs.pop(0) # delim_in
    path_out = inputs.pop(0)
    delim_out = delim_in # Default behaviour
    columns = []
    inc_filters = []
    exc_filters = []
    
    # Parse the rest
    while inputs:
        arg = inputs.pop(0)
        if arg == "-f": # Output file format
            try:
                temp = inputs.pop(0)
                delim = Validate_File_Format(temp)
            except:
                printE(STR__specify_an_output_format)
                return 1
            if delim:
                delim_out = delim
            else:
                printE(STR__invalid_file_format.format(io = "output", s = temp))
                return 1
        else: # Column number of filtering criteria
            flag_error = True

            arg = Strip_X(arg)

            # If column number
            c = Validate_Column_Number(arg)
            if c != -1:
                columns.append(c)
                flag_error = False

            # If filter criteria
            f_ = Validate_Filter(arg)
            # f_ is either [] or [int, [int,int,str/int/float]]
            if f_:
                t, f = f_
                if t: inc_filters.append(f)
                else: exc_filters.append(f)
                flag_error = False

            # Neither column nor filter
            if flag_error:
                printE(STR__invalid_argument.format(s = arg))
                printE(STR__use_help)
                return 1
    
    # Ensure at least one column
    if not columns:
        printE(STR__at_least_one_column)
        return 1
    
    # Run program
    Table_To_Table(path_in, delim_in, path_out, delim_out, columns,
            inc_filters, exc_filters)
    
    # Safe exit
    return 0



def Validate_Read_Path(filepath):
    """
    Validates the filepath of the input file.
    Return 0 if the filepath is valid.
    Return 1 otherwise.

    Validate_Read_Path(str) -> int
    """
    try:
        f = open(filepath, "U")
        f.close()
        return 0
    except:
        return 1


    
def Validate_Write_Path(filepath):
    """
    Validates the filepath of the input file.
    Return 0 if the filepath is writtable.
    Return 1 if the user decides to overwrite an existing file.
    Return 2 if the user declines to overwrite an existing file.
    Return 3 if the file exists and the program is set to forbid overwriting.
    Return 4 if the program is unable to write to the filepath specified.

    Validate_Write_Path(str) -> int
    """
    try:
        f = open(filepath, "U")
        f.close()
    except: # File does not exist. 
        try:
            f = open(filepath, "w")
            f.close()
            return 0 # File does not exist and it is possible to write
        except:
            return 4 # File does not exist but it is not possible to write
    # File exists
    if WRITE_PREVENT: return 3
    if WRITE_CONFIRM:
        confirm = raw_input(STR__overwrite_confirm)
        if confirm not in LIST__yes: return 2
    # User is not prevented from overwritting and may have chosen to overwrite
    try:
        f = open(filepath, "w")
        f.close()
        if WRITE_CONFIRM: return 1 # User has chosen to overwrite existing file
        return 0 # Overwriting existing file is possible
    except:
        return 4 # Unable to write to specified filepath



def Validate_File_Format(string):
    """
    Validates the file format specified.
    Return the appropriate delimiter.
    Return an empty string if the file format is invalid.

    Validate_File_Format(str) -> str
    """
    return DICT__delim.get(string, "")



def Strip_X(string):
    """
    Strips leading and trailing inverted commans or brackets if a matching pair
    are flanking the string.

    Strip_X(str) -> str
    """
    if (    (string[0] == string[-1] == "\"") or
            (string[0] == string[-1] == "\'") or
            (string[0] == "(" and string[-1] == ")") or
            (string[0] == "{" and string[-1] == "}") or
            (string[0] == "[" and string[-1] == "]") or
            (string[0] == "<" and string[-1] == ">")
            ):
        return string[1:-1]
    return string



def Validate_Column_Number(string):
    """
    Validates and returns the column number specified.

    Returns the column number under an index 0 system if valid.
    Return -1 if the input is invalid.

    @string
        (str)
        A string denoting the column number under the index 1 system.
        
    Validate_Column_Number(str) -> int
    """
    try:
        n = int(string)
    except:
        return -1
    if n < 1: return -1
    return n - 1 # Input is in index 1 system, output is in index 0



def Validate_Filter(string):
    """
    Validates and returns a filter criteria.

    Return a specific list of values if the string denotes a valid filtering
    criteria. The list contains an integer and another list. The integer
    indicates whether the criteria is for inclusion or exclusion. 1 for
    inclusion, 0 for exclusion. The sublist contains three values. The first
    is an int denoting the column to be filtered. The second is an int denoting
    the kind of filtering to be performed. The third is the string, int or float
    used for filtering.

    The input for column number needs to be in the index-1 system while the
    output for column number will be in the index-0 system.
    
    Return an empty list if the input is invalid.

    @string
        (str)
        A string denoting the filtering criteria to be used
        
    Validate_Column_Number(str) -> [int, [int,int,str/float]]
    Validate_Column_Number(str) -> []
    """
    # Setup
    inc_exc = None
    col = None
    op = None
    query = None
    
    s = ""
    
    # Check the inc/exc flag, exlude the inc/exc char and "col"
    temp = string.split("col", 1)
    try:
        flag, string = temp
    except:
        return [] # No "col"
    if flag == "+" or flag == "": inc_exc = 1
    elif flag == "!" or flag == "-": inc_exc = 0
    else: return []
    
    # Get and validate column
    index = 0
    try:
        while string[index].isdigit(): index += 1
    except:
        return [] # Everything after "col" is just digits
    
    col_ = string[:index] # Split the string further
    string = string[index:] 
    
    col = Validate_Column_Number(col_) # Validate the column number
    if col == -1: return []
    
    # Check for operator
    for k in LIST__search_ops: # Requires a specific order. DICT__ops.keys() 
        if k in string:        # gives the keys in a scrambled order.
            if string.index(k) == 0:
                op = DICT__ops[k]
                s = k
    if not op:
        return []
    
    # Validate query
    query_ = string.replace(s, "")
    
    if op in LIST__math_ops: # Greater,less,greaquals,lequals
        try:
            query = int(query_)
        except: # Not a float
            try:
                query = float(query_)
            except:
                print query
                return [] # Not an int either. Math operation impossible
    elif op in LIST__math_ops_i: # Integer equal/unequal
        try:
            query = int(query_)
        except:
            return [] # Not an int
    elif op in LIST__math_ops_f: # Float equal/unequal
        try:
            query = float(query_)
        except:
            return [] # Not a float
    else:
        query = query_ # String operation
    
    # Return filter (all tests passed)
    return [inc_exc, [col, op, query]]



def Strip_Non_Inputs(list1):
    """
    Remove the runtime environment variable and program name from the inputs.
    Assumes this module was called and the name of this module is in the list of
    command line inputs.

    Strip_Non_Inputs(list) -> list
    """
    if "t2t.py" in list1[0]: return list1[1:]
    return list1[2:]



# Controlled Print Statements ##################################################

def printE(string):
    """
    A wrapper for the basic print statement.

    It is intended to be used for printing error messages.

    It can be controlled by a global variable.
    """
    if PRINT_ERRORS: print(string)


def printP(string):
    """
    A wrapper for the basic print statement.

    It is intended to be used for printing progress messages.

    It can be controlled by a global variable.
    """
    if PRINT_PROGRESS: print(string)



# Main Loop ####################################################################

if AUTORUN and (__name__ == "__main__"):
    exit_code = Parse_Command_Line_Input__t2t(sys.argv)


