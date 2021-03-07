
import sys


# Create all the necessary token types for the Parser:
TKN_Boolean             = 'INIT_BOOLEAN'
TKN_Assign              = 'ASSIGN'
TKN_BooleanT            = 'TRUE'
TKN_BooleanF            = 'FALSE'
TKN_ParenthesisL        = 'LPAR'
TKN_ParenthesisR        = 'RPAR'
TKN_CurlyL              = 'LBRA'
TKN_CurlyR              = 'RBRA'
TKN_Semicolon           = 'SEMICOLON'
TKN_IfStatement         = 'STMT_IF'
TKN_ElseStatement       = 'STMT_ELSE'
TKN_ELIFStatement       = 'STMT_ELIF'
TKN_Equals              = 'EQUALS'
TKN_NOTEQ               = 'NOT_EQUALS'
TKN_NOT                 = 'NOT'
TKN_LT                  = 'LESS_THAN'
TKN_LTEQ                = 'LESS_THAN_OR_EQUAL'
TKN_GT                  = 'GREATER_THAN'
TKN_GTEQ                = 'GREATER_THAN_OR_EQUAL'
TKN_Variable            = 'VARIABLE'
TKN_Integer             = 'INTEGER'
TKN_Float               = 'FLOAT'
TKN_NewLine             = 'NEW_LINE'

# In order to check if the syntax of a sentence is correct, we need to compare the current index to multiple
# Tokens which will take more space and make the code unnecessarily longer. To eliminate that, we created lists
# containing the necessary tokens for each step then we will use the built-in function which will check if
# something is in a list:
Boolean_Expressions_Parameters = [TKN_Variable, TKN_Integer, TKN_Float]
Boolean_Expressions_Comparisons = [TKN_Equals, TKN_NOTEQ, TKN_GT, TKN_GTEQ, TKN_LT, TKN_LTEQ]

Assignment_Functions_Tokens = [TKN_Assign, TKN_Semicolon]
Assignment_Functions_Valid_Initializations = [TKN_Variable, TKN_Integer, TKN_Float, TKN_BooleanT, TKN_BooleanF]

IF_ELIF_Statement_Tokens = [TKN_ParenthesisL, TKN_ParenthesisR, TKN_CurlyL, TKN_CurlyR]
ELSE_Statement_Tokens = [TKN_CurlyL, TKN_CurlyR]
IF_ELIF_ELSE_Statements_Tokens = [TKN_IfStatement, TKN_ELIFStatement, TKN_ElseStatement]


def Perform_Parsing(Tokens_List):

    # Create a new list which will store only the Tokens without their values:
    Original_Tokens_Types_List = []

    # Create a For Loop which will iterate through the list from the Lexer and append the Token Type
    # to the list created above:
    for i in range(0, len(Tokens_List)):
        Original_Tokens_Types_List.append(Tokens_List[i].Token_Type)

    # Append at the end of the list one token which resembles a new line:
    Original_Tokens_Types_List.append(TKN_NewLine)

    # Create a variable to store the line number. This will be used to indicate the line number if an
    # error is found:
    Current_Line_Number = 1

    # Create a variable to store the list iterator. This will be used to iterate over the list:
    List_Iterator = 0

    # Send the Tokens Types List, the list iterator, and the line number to the method called Check_Semantics:
    Check_Semantics(Original_Tokens_Types_List, List_Iterator, Current_Line_Number)


    return





# Create a method which will check the semantics of each sentence in the source code, then send it to the
# appropriate method:
def Check_Semantics(Tokens_List, List_Iterator, Current_Line_Number):


    if len(Tokens_List) == 1 and Tokens_List[0] == TKN_NewLine:
        print("Source Code Can't Be Empty!")
        sys.exit()
    elif len(Tokens_List) < 3:
        print("ERROR: Invalid Syntax. Line " + str(Current_Line_Number))
        sys.exit()
    elif List_Iterator == len(Tokens_List):
        print("Source Code is Correct")
        sys.exit()

    # Create a variable to store the index of the New Line token. Once a sentence ends in the source code,
    # we will store it in a Temporary_List then continue to check the semantics of the Temporary_List only
    # rather than the entire Source Code.

    NewLine_Index = 0
    Temporary_List = []

    # gets rid of enter pressed in the source code (in other word empty lines), increments the line number
    # and calls check semantics again with passing the updates line number.
    if Tokens_List[List_Iterator] == TKN_NewLine:
        Current_Line_Number = Increment_Current_Line_Number(Current_Line_Number)
        del Tokens_List[List_Iterator]
        Check_Semantics(Tokens_List, List_Iterator, Current_Line_Number)
        return


    # This will detect the new line token and store its index in the newline_Index variable

    for i in range(List_Iterator, len(Tokens_List)):
        if Tokens_List[i] == TKN_NewLine:
            NewLine_Index = i
            break

    # Append all the tokens from the List Iterator till the index of the NewLine. After this for loop, the list
    # called Temporary_List will contain the Tokens of one line only:
    for i in range(List_Iterator, NewLine_Index):
        Temporary_List.append(Tokens_List[i])

    # Unless the token is if, elif, else, a line of code cannot contain only one element
    if len(Temporary_List) == 1 and Temporary_List[0] not in IF_ELIF_ELSE_Statements_Tokens:
        print("ERROR: Invalid Syntax. Line " + str(Current_Line_Number))
        sys.exit()



    # From here the program will check the sentence to determine whether it is a boolean
    # initialization, an assignment function, a boolean expression, or an IF or ELIF or ELSE Statement.


    if Temporary_List[0] == TKN_Boolean:
        del Temporary_List[0]
        Assignment_Function_Check(Temporary_List, Tokens_List, NewLine_Index, Current_Line_Number, 1)



    if Temporary_List[0] in IF_ELIF_ELSE_Statements_Tokens:
        Default_Statement_Check(Tokens_List, List_Iterator, Current_Line_Number)

    # If the first word in the sentence is either a variable, integer, or float, the program will enter
    # this loop for further checking:
    elif (Temporary_List[0] == TKN_Variable
          or Temporary_List[0] == TKN_Integer
          or Temporary_List[0] == TKN_Float) \
            and (Temporary_List[1] not in IF_ELIF_Statement_Tokens):   # paranthesis or curly brackets

        # If the first index is a variable and the second is an "=" symbol, it means that the sentence
        # is an Assignment function, so it will be sent to the method assignment function check.
        if Temporary_List[0] == TKN_Variable \
                and Temporary_List[1] == TKN_Assign \
                and Temporary_List[1] not in IF_ELIF_Statement_Tokens:
            Assignment_Function_Check(Temporary_List, Tokens_List, NewLine_Index, Current_Line_Number, 0)

        # If the first index is either a variable, integer, or float, and the next index in the list is
        # boolean comparison symbol, it means that the sentence is a boolean expression. So we will send
        # it to the method called Boolean_Expression_Check:
        elif (Temporary_List[0] == TKN_Variable
              or Temporary_List[0] == TKN_Integer
              or Temporary_List[0] == TKN_Float) \
                and (Temporary_List[1] in Boolean_Expressions_Comparisons):
            Boolean_Expression_Check(Temporary_List, Tokens_List, NewLine_Index, Current_Line_Number)

        # If the second index wasn't a boolean comparison symbol, we will print an error message with the
        # necessary information for the user, as well as the line number:
        else:
            print("ERROR! Second Character in code line must be either one of the following:")
            print("=, equals, !=, <, <=, >, >=")
            print("Error At Line " + str(Current_Line_Number))
            sys.exit()

    # If it was none of the above, it means that the sentence is wrong. So we will print an error message
    # with the appropriate information as well as the line number:
    else:
        print("ERROR: Invalid Syntax. Line " + str(Current_Line_Number))
        sys.exit()


    return




# First must be a variable, then an assigning symbol "=", then either true, false, variable, int, or float.
# Finally, it must have a semicolon at the end. An example is shown below:
# Variable /// = /// true | false | Variable | Integer | Float /// ;
def Assignment_Function_Check(Temp_Tokens_List, Original_Tokens_List, New_Line_Index, Current_Line_Number, Flag):

    # Create a list which will contain the Tokens that are missing from the sentence:
    Difference_List = []

    # Create a For Loop which will compare each Token in the sentence with the required Tokens which we
    # stored in a list called Assignment_Functions_Tokens. If a required Token is missing from the sentence,
    # the loop will append it to the list created above:
    for i in range(0, len(Assignment_Functions_Tokens)):
        if Assignment_Functions_Tokens[i] not in Temp_Tokens_List:
            Difference_List.append(Assignment_Functions_Tokens[i])

    # If the length of the list created above doesn't equal 0, it means that there are important elements
    # missing from the sentence. So we will iterate through the list and print the error message that's
    # appropriate to each missing Token:
    if len(Difference_List) != 0:
        for i in range(0, len(Difference_List)):
            if Difference_List[i] == TKN_Assign:
                print("Missing Assigning Symbol '='. Line " + str(Current_Line_Number))
                sys.exit()
            elif Difference_List[i] == TKN_Semicolon:
                print("Missing Semicolon Symbol ';'. Line " + str(Current_Line_Number))
                sys.exit()

    # If the program reaches here, it means that the sentence contains all the required Tokens. Now, the
    # program will check if the Tokens are in the right order or not. If a Token isn't found at the correct
    # index of the sentence, an error message will be printed, which can be seen from all the else statements
    # at the  end of each loop:
    if Temp_Tokens_List[0] == TKN_Variable:
        if Temp_Tokens_List[1] == TKN_Assign:

            # We used a Flag to check that if it equals 1, it means that this sentence came from a boolean
            # initialization function. This means that it can either be set to "true" or "false" and nothing
            # else. So if the sentence was a boolean initialization function, the program will enter this
            # loop:
            if Flag == 1:
                if Temp_Tokens_List[2] == TKN_BooleanT or Temp_Tokens_List[2] == TKN_BooleanF:
                    if Temp_Tokens_List[3] == TKN_Semicolon:

                        # If the program has reached here, it means that the boolean initialization sentence
                        # was completely correct. The program will print a success message, increment the
                        # current line number, then call the method called Check_Semantics again, however this
                        # time the List_Iterator will be set to the index of the value of (NewLine Token + 1).
                        # This means that the program will skip the first sentence and perform the same checks
                        # starting from the next sentence:
                        print("Correct Boolean Initialization. Line " + str(Current_Line_Number))
                        New_Current_Line_Number = Increment_Current_Line_Number(Current_Line_Number)
                        Check_Semantics(Original_Tokens_List, (New_Line_Index + 1), New_Current_Line_Number)
                    else:
                        print("Missing Semicolon Symbol ';'. Line " + str(Current_Line_Number))
                        sys.exit()
                else:
                    print("ERROR! Boolean Variable must be initialized to either one of the following:")
                    print("true, false")
                    print("Error At Line " + str(Current_Line_Number))
                    sys.exit()

            # If the Flag equals 0, it means that the sentence wasn't a boolean initialization function. This
            # means that the variable can be set to either "true", "false", "variable", "integer", "float".
            # So the program will enter this loop:
            elif Flag == 0:
                if Temp_Tokens_List[2] == TKN_BooleanT \
                        or Temp_Tokens_List[2] == TKN_BooleanF \
                        or Temp_Tokens_List[2] == TKN_Variable \
                        or Temp_Tokens_List[2] == TKN_Integer \
                        or Temp_Tokens_List[2] == TKN_Float:
                    if Temp_Tokens_List[3] == TKN_Semicolon:

                        # If the program has reached here, it means that the variable initialization sentence
                        # was completely correct. The program will print a success message, increment the
                        # current line number, then call the method called Check_Semantics again, however this
                        # time the List_Iterator will be set to the index of the value of (NewLine Token + 1).
                        # This means that the program will skip the first sentence and perform the same checks
                        # starting from the next sentence:
                        print("Correct Variable Initialization. Line " + str(Current_Line_Number))
                        New_Current_Line_Number = Increment_Current_Line_Number(Current_Line_Number)
                        Check_Semantics(Original_Tokens_List, (New_Line_Index + 1), New_Current_Line_Number)
                    else:
                        print("Missing Semicolon Symbol ';'. Line " + str(Current_Line_Number))
                        sys.exit()
                else:
                    print("ERROR! Variable must be initialized to either one of the following:")
                    print("true, false, int, float, or another variable")
                    print("Error At Line " + str(Current_Line_Number))
                    sys.exit()
            else:
                print("Either Syntax Error or Missing Assigning Symbol '='. Line " + str(Current_Line_Number))
                sys.exit()
        else:
            print("Missing Variable Name. Line " + str(Current_Line_Number))
            sys.exit()


    return





# Variable | Integer | Float /// equals, !=, <, <=, >, >= /// Variable | Integer | Float
def Boolean_Expression_Check(Temp_Tokens_List, Original_Tokens_List, New_Line_Index, Current_Line_Number):

    # A boolean expression sentence must contain at least 3 elements. If the program finds less than
    # 3, it will print an error message. We do so by checking the length of the sentence:
    if len(Temp_Tokens_List) != 3:
        print("ERROR! Revise Boolean Expression Syntax. Line " + str(Current_Line_Number))
        sys.exit()


    if Temp_Tokens_List[0] in Boolean_Expressions_Parameters:
        if Temp_Tokens_List[1] in Boolean_Expressions_Comparisons:
            if Temp_Tokens_List[2] in Boolean_Expressions_Parameters: # x = y;

                # If the program has reached here, it means that the boolean expression was completely
                # correct. The program will print a success message, increment the current line number,
                # then call the method called Check_Semantics again, however this time the List_Iterator
                # will be set to the index of the value of (NewLine Token + 1). This means that the program
                # will skip the first sentence and perform the same checks starting from the next sentence:
                print("Correct Boolean Comparison Expression. Line " + str(Current_Line_Number))
                New_Current_Line_Number = Increment_Current_Line_Number(Current_Line_Number)
                Check_Semantics(Original_Tokens_List, (New_Line_Index + 1), New_Current_Line_Number)
            else:
                print("ERROR! Parameter must be either one of the following:")
                print("variable, int, float")
                print("Error At Line " + str(Current_Line_Number))
                sys.exit()
        else:
            print("ERROR! Boolean Comparison must be either one of the following:")
            print("equals, !=, <, <=, >, >=")
            print("Error At Line " + str(Current_Line_Number))
            sys.exit()
    else:
        print("ERROR! Parameter must be either one of the following:")
        print("variable, int, float")
        print("Error At Line " + str(Current_Line_Number))
        sys.exit()


    return





# This method is specific to checking the IF, ELIF, ELSE Statements.
# First can be either an if, elif, or else Token. Then it has to contain left and right parenthesis. Inside the
# left and right parenthesis there should be a boolean expression. After that the sentence has to contain left
# and right curly brackets. Inside the left and right curly brackets there should be an assignment function. Since
# the IF and ELIF Statements share the same syntax but the ELSE doesn't, an example of both syntaxes is shown below:
# if | elif /// ( /// boolean expression /// ) /// { /// assignment function /// }
# else /// { /// assignment function /// }
def Default_Statement_Check(Tokens_List, List_Iterator, Current_Line_Number):

    # Create a list to store in it the full statement:
    Current_Default_Statement = []

    # Our program must have the IF, ELIF, ELSE Statements written in two separate lines. The first
    # line will contain the boolean expression, and the second line will contain the assignment function.
    # This means that we need to get the index of the second NewLine Token from the original list. To do
    # so, we call a method dedicated to finding the index of the second NewLine Token called Get_Second_NewLine_Index:
    Second_NewLine_Index = Get_Second_NewLine_Index(Tokens_List, List_Iterator, 0)

    # If the Second_NewLine_Index equals 0, it means that the IF / ELIF / ELSE Statement isn't complete.
    # The program will print the appropriate error message:
    if Second_NewLine_Index == 0:
        print("ERROR: IF / ELIF / ELSE Statement Not Complete. Line " + str(Current_Line_Number))
        sys.exit()

    # If the program reaches here it means that the program has found two lines. So it will append
    # all the tokens that are written in the two lines in the list called Current_Default_Statement:
    for i in range(List_Iterator, Second_NewLine_Index):
        Current_Default_Statement.append(Tokens_List[i])

    # Since the program has iterated through 2 lines of code, we will increment the current line number
    # to stay correct:
    Current_Line_Number = Increment_Current_Line_Number(Current_Line_Number)

    # Create a list which will contain the Tokens that are missing from the sentence:
    Difference_List = []

    # Create a For Loop which will compare each Token in the sentence with the required Tokens which we
    # stored in a list called Assignment_Functions_Tokens. If a required Token is missing from the sentence,
    # the loop will append it to the list created above:

    # Create a For Loop which will compare each Token in the sentence with the required Tokens which we
    # stored in two separate lists. We used separate lists because the syntax of the ELSE Statement is
    # different from the IF and ELIF Statements. We check if the first Token in the sentence is an IF or
    # ELIF Statement Token, we check for missing Tokens from the list called IF_ELIF_Statement_Tokens:
    # If a required Token is missing from the sentence, the loop will append it to the list called Difference_List:
    if Current_Default_Statement[0] == TKN_IfStatement or Current_Default_Statement[0] == TKN_ELIFStatement:
        for i in range(0, len(IF_ELIF_Statement_Tokens)):
            if IF_ELIF_Statement_Tokens[i] not in Current_Default_Statement:
                Difference_List.append(IF_ELIF_Statement_Tokens[i])

    # If the first Token in the sentence is an ELSE Statement Token, we check for missing Tokens from the
    # list called ELSE_Statement_Tokens:
    # If a required Token is missing from the sentence, the loop will append it to the list called Difference_List:
    else:
        for i in range(0, len(ELSE_Statement_Tokens)):
            if ELSE_Statement_Tokens[i] not in Current_Default_Statement:
                Difference_List.append(ELSE_Statement_Tokens[i])

    # If the length of the list created above doesn't equal 0, it means that there are important elements
    # missing from the sentence. So we will iterate through the list and print the error message that's
    # appropriate to each missing Token:
    if len(Difference_List) != 0:

        # If the first Token in the sentence is IF or ELIF Statement, the program will enter this loop:
        if Current_Default_Statement[0] == TKN_IfStatement or Current_Default_Statement[0] == TKN_ELIFStatement:
            for i in range(0, len(Difference_List)):
                if Difference_List[i] == TKN_ParenthesisL:
                    print("Missing Left Parenthesis '('. Line " + str(Current_Line_Number - 1))
                    sys.exit()
                elif Difference_List[i] == TKN_ParenthesisR:
                    print("Missing Right Parenthesis ')'. Line " + str(Current_Line_Number - 1))
                    sys.exit()
                elif Difference_List[i] == TKN_CurlyL:
                    print("Missing Left Curly Bracket '{'. Line " + str(Current_Line_Number))
                    sys.exit()
                elif Difference_List[i] == TKN_CurlyR:
                    print("Missing Right Curly Bracket '}'. Line " + str(Current_Line_Number))
                    sys.exit()

        # If the first Token in the sentence is ELSE Statement, the program will enter this loop:
        else:
            for i in range(0, len(Difference_List)):
                if Difference_List[i] == TKN_CurlyL:
                    print("Missing Left Curly Bracket '{'. Line " + str(Current_Line_Number))
                    sys.exit()
                elif Difference_List[i] == TKN_CurlyR:
                    print("Missing Right Curly Bracket '}'. Line " + str(Current_Line_Number))
                    sys.exit()

    # Create a Temporary List and set it as a copy to the list containing the sentence. This will
    # be used to delete the NewLine Tokens from it so that they won't interfere with the rest of
    # the program:
    Temp = Current_Default_Statement.copy()

    # Create a For Loop which will iterate through the list that contains the sentence. If a Token
    # is found which is a NewLine Token, the program will delete if from the Temporary List created
    # above:
    for i in range(0, len(Current_Default_Statement)):
        if Current_Default_Statement[i] == TKN_NewLine:
            del Temp[i]

    # We then make the list called Current_Default_Statement the same as Temp by assigning them together.
    # This means that the sentence no longer contains NewLine Tokens:
    Current_Default_Statement = Temp



    # If the program reaches here, it means that the sentence contains all the required Tokens. Now, the
    # program will check if the Tokens are in the right order or not. If a Token isn't found at the correct
    # index of the sentence, an error message will be printed, which can be seen from all the else statements
    # at the  end of each loop:

    # The program will enter this loop if the first Token in the sentence is either an IF or ELIF Statement:
    if Current_Default_Statement[0] == TKN_IfStatement or Current_Default_Statement[0] == TKN_ELIFStatement:
        if Current_Default_Statement[1] == TKN_ParenthesisL:
            if Current_Default_Statement[2] in Boolean_Expressions_Parameters:
                if Current_Default_Statement[3] in Boolean_Expressions_Comparisons:
                    if Current_Default_Statement[4] in Boolean_Expressions_Parameters:
                        if Current_Default_Statement[5] == TKN_ParenthesisR:
                            if Current_Default_Statement[6] == TKN_CurlyL:
                                if Current_Default_Statement[7] == TKN_Variable:
                                    if Current_Default_Statement[8] == TKN_Assign:
                                        if Current_Default_Statement[9] in Assignment_Functions_Valid_Initializations:
                                            if Current_Default_Statement[10] == TKN_Semicolon:
                                                if Current_Default_Statement[11] == TKN_CurlyR:

                                                    # If the program has reached here, it means that the IF / ELIF Statement was completely
                                                    # correct. The program will print a success message, increment the current line number,
                                                    # then call the method called Check_Semantics again, however this time the List_Iterator
                                                    # will be set to the index of the value of (NewLine Token + 1). This means that the program
                                                    # will skip the first sentence and perform the same checks starting from the next sentence:
                                                    print("Correct IF/ELIF Statement")
                                                    Current_Line_Number = Increment_Current_Line_Number(Current_Line_Number)
                                                    List_Iterator = Second_NewLine_Index + 1
                                                    Check_Semantics(Tokens_List, List_Iterator, Current_Line_Number)
                                                else:
                                                    print("ERROR: Missing Right Curly Bracket '}'. Line " + str(Current_Line_Number))
                                                    sys.exit()
                                            else:
                                                print("ERROR: Missing Semicolon ';'. Line " + str(Current_Line_Number))
                                                sys.exit()
                                        else:
                                            print("ERROR: Variable Can Only Be Assigned To One Of The Following:")
                                            print("variable, int, float, true, false. Line " + str(Current_Line_Number))
                                            sys.exit()
                                    else:
                                        print("ERROR: Missing Assigning Symbol '='. Line " + str(Current_Line_Number))
                                        sys.exit()
                                else:
                                    print("ERROR: Either Syntax Error Or Missing Variable. Line " + str(Current_Line_Number))
                                    sys.exit()
                            else:
                                print("ERROR: Missing Left Curly Bracket '{'. Line " + str(Current_Line_Number))
                                sys.exit()
                        else:
                            print("ERROR: Missing Right Parenthesis ')'. Line " + str(Current_Line_Number))
                            sys.exit()
                    else:
                        print("ERROR: Boolean Expression Can Only Compare Between One Of The Following:")
                        print("variable, int, float. Line " + str(Current_Line_Number - 1))
                        sys.exit()
                else:
                    print("ERROR: Boolean Expression Can Only Compare Using One Of The Following Mathematical Functions:")
                    print("equals, !=, >, >=, <, <=. Line " + str(Current_Line_Number - 1))
                    sys.exit()
            else:
                print("ERROR: Boolean Expression Can Only Compare Between One Of The Following:")
                print("variable, int, float. Line " + str(Current_Line_Number - 1))
                sys.exit()
        else:
            print("ERROR: Missing Left Parenthesis '('. Line " + str(Current_Line_Number))
            sys.exit()

    # The program will enter this loop if the first Token in the sentence is an ELSE Statement:
    elif Current_Default_Statement[0] == TKN_ElseStatement:
        if Current_Default_Statement[1] == TKN_CurlyL:
            if Current_Default_Statement[2] == TKN_Variable:
                if Current_Default_Statement[3] == TKN_Assign:
                    if Current_Default_Statement[4] in Assignment_Functions_Valid_Initializations:
                        if Current_Default_Statement[5] == TKN_Semicolon:
                            if Current_Default_Statement[6] == TKN_CurlyR:

                                # If the program has reached here, it means that the ELSE Statement was completely
                                # correct. The program will print a success message, increment the current line number,
                                # then call the method called Check_Semantics again, however this time the List_Iterator
                                # will be set to the index of the value of (NewLine Token + 1). This means that the program
                                # will skip the first sentence and perform the same checks starting from the next sentence:
                                print("Correct ELSE Statement")
                                Current_Line_Number = Increment_Current_Line_Number(Current_Line_Number)
                                List_Iterator = Second_NewLine_Index + 1
                                Check_Semantics(Tokens_List, List_Iterator, Current_Line_Number)
                            else:
                                print("ERROR: Missing Right Curly Bracket '}'. Line " + str(Current_Line_Number))
                                sys.exit()
                        else:
                            print("ERROR: Missing Semicolon ';'. Line " + str(Current_Line_Number))
                            sys.exit()
                    else:
                        print("ERROR: Variable Can Only Be Assigned To One Of The Following:")
                        print("variable, int, float, true, false. Line " + str(Current_Line_Number))
                        sys.exit()
                else:
                    print("ERROR: Missing Assigning Symbol '='. Line " + str(Current_Line_Number))
                    sys.exit()
            else:
                print("ERROR: Either Syntax Error Or Missing Variable. Line " + str(Current_Line_Number))
                sys.exit()
        else:
            print("ERROR: Missing Left Curly Bracket '{'. Line " + str(Current_Line_Number))
            sys.exit()
    else:
        print("ERROR: Default Statement Must Start With One Of The Following: ")
        print("if, elif, else. Line " + str(Current_Line_Number))
        sys.exit()


    return





# Create a method which will increment the line number:
def Increment_Current_Line_Number(Line_Number):

    # Add 1 to the line number itself, then return it back to the user:
    Line_Number += 1

    return Line_Number





# Create a method which will get the index of the second NewLine Token from the list:
def Get_Second_NewLine_Index(Tokens_List, List_Iterator, SecondNewLineIndex):

    # The first For Loop will iterate through the list until it finds a NewLine Token:
    for i in range(List_Iterator, len(Tokens_List)):
        if Tokens_List[i] == TKN_NewLine:

        # Once a NewLine Token is found, it means that after it there's another line.
        # We need the index of the NewLine Token that's in the next line, so we create
        # another For Loop however this one starts from the index of the NewLine Token
        # found above + 1:
            for x in range(i + 1, len(Tokens_List)):
                if Tokens_List[x] == TKN_NewLine:

                    # Once the program reaches here, it means that it has found another
                    # NewLine Token. It will save the index in a variable and immediately
                    # break out of the loop, then it will return the index back to the
                    # method:
                    SecondNewLineIndex = x
                    break
            break

    return SecondNewLineIndex




