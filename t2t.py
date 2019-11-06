HELP_DOC = """
TABLE TO TABLE
by Angelo Chan

This is a program for basic table file parsing.

Users can choose to retain the table file format or change it to another file
format. Users select which columns of data will be retained, and which order the columns
will appear in, in the output file. Users can perform basic filtering on the rows of data.

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
"""



# Imported Modules #############################################################

import sys



# Strings ######################################################################

STR__use_help = "\nUse the -h option for help:\n\t python t2t.py -h"

STR__no_inputs = "\nERROR: No inputs were given."

# Lists ########################################################################

LIST__help = ["-h", "-H", "-help", "-Help", "-HELP"] 



# Dictionaries #################################################################



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
    Parse_Command_Line_Input__t2t(sys.argv)


