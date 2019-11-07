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
    - EQUALS        (Data must match the specified value exactly)
    - NOT EQUALS    (Data must not match the specified value exactly)
    - CONTAINS      (Data must contain the specified value/substring)
    - NOT CONTAINS  (Data must not contain the specified value/substring)
    - GREATER THAN  (Data must be stricly greater than the specified value)
    - GREAQUALS     (Data must be equal to or greater than the specified value)
    - LESS THAN     (Data must be stricly less than the specified value)
    - LEQUALS       (Data must be equal to or less than the specified value)



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

                    =   Equals <query>
                    !=  Does not equal <query>
                    :   Contains <query>
                    !:  Does not contain <query>
                    >   Greater than <query>
                    <   Less than <query>
                    >=  Equal to or greater than <query>
                    <=  Equal to or less than <query>

            query

                The value used as the substring or cutoff.
"""



# Configurations ###############################################################

WRITE_PREVENT = False # Completely prevent overwritting existing files
WRITE_CONFIRM = True # Check to confirm overwritting existing files



# Imported Modules #############################################################

import sys



# Defaults #####################################################################



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
STR__input_format = """
ERROR: Invalid {io} file format: {s}
Please specify one of:
    tsv
    csv
    ssv"""

STR__overwrite_confirm = "\nFile already exists. Do you wish to overwrite it? "\
        "(y/n): "



# Lists ########################################################################

LIST__help = ["-h", "-H", "-help", "-Help", "-HELP"]

LIST__yes = ["Y", "y", "YES", "Yes", "yes", "T", "t", "TRUE", "True", "true"]
LIST__no = ["N", "n", "NO", "No", "no", "F", "f", "FALSE", "False", "false"]

LIST__tsv = ["\t", "T", "t", "TSV", "Tsv", "tsv", "TAB", "Tab", "tab"]
LIST__csv = [",", "C", "c", "CSV", "Csv", "csv", "COMMA", "Comma", "comma"]
LIST__ssv = [" ", "S", "s", "SSV", "Ssv", "ssv", "SPACE", "Space", "space"]



# Dictionaries #################################################################

DICT__delim = {}
for i in LIST__tsv: DICT__delim[i] = "\t"
for i in LIST__csv: DICT__delim[i] = ","
for i in LIST__ssv: DICT__delim[i] = " "



# File Processing Code #########################################################



# Command Line Parsing #########################################################

def Parse_Command_Line_Input__t2t(raw_command_line_input):
    """
    Parse the command line input.
    """
    # Remove the runtime environment variable and program name from the inputs
    inputs = Strip_Non_Inputs(raw_command_line_input)

    # No inputs
    if not inputs:
        print(STR__no_inputs)
        print(STR__use_help)
        return 1
  
    # Help option
    if inputs[0] in LIST__help:
        print(HELP_DOC)
        return 0

    # Initial validation
    if len(inputs) < 4:
        print(STR__insufficient_inputs)
        print(STR__use_help)
        return 1
    
    valid_in = Validate_Read_Path(inputs[0])
    if valid_in == 1:
        print(STR__IO_error_read)
        return 1
    
    delim_in = Validate_File_Format(inputs[1])
    if not delim_in:
        print(STR__input_format.format(io = "input", s = inputs[1]))
        return 1
    
    valid_out = Validate_Write_Path(inputs[2])
    if valid_out == 2: return 0
    if valid_out == 3:
        print(STR__IO_error_write_forbid)
        return 1
    if valid_out == 4:
        print(STR__In_error_write_unable)
        return 1

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



def Strip_Non_Inputs(list1):
    """
    Remove the runtime environment variable and program name from the inputs.
    Assumes this module was called and the name of this module is in the list of
    command line inputs.

    Strip_Non_Inputs(list) -> list
    """
    try:
        index = list1.index("t2t.py")
    except:
        index = list1.index("t2t")
    return list1[index+1:]



# Main Loop ####################################################################

if __name__ == "__main__":
    exit_code = Parse_Command_Line_Input__t2t(sys.argv)


