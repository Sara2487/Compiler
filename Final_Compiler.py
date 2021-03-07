import Final_Lexer
import Final_Parser

# Open the SourceCode.txt file as "r" which stands for read, and save it in
# a variable called Text_File:
Text_File = open("SourceCode.txt", "r")

# Check if the Text_File was opened as read mode only, then proceed:
if Text_File.mode == 'r':

    # Read the contents of the Text_File and save them in a variable called
    # Source_Code:
    Source_Code = Text_File.read()

    # Send the Source_Code to the Lexer to the class called Lexer from the file
    # called Final_Lexer in order to initialize the required variables:
    Test = Final_Lexer.Lexer(Source_Code)

    # Create a variable named Source_Code_Tokens which will contain all the Tokens
    # of the entire Source Code:
    Source_Code_Tokens = Test.Create_And_Match_Tokens()
    #print(Source_Code_Tokens)

    # Send the Source_Code_Tokens list to the Parser class called Final_Parser in
    # order to check the semantics and determine whether the Source Code is correct
    # or not:
    Final_Parser.Perform_Parsing(Source_Code_Tokens)



# This is the correct Source Code we will be testing:

# boolean OpenGate = false;
# if (P89099 equals P89099)
# {OpenGate = true;}
# elif (F952 != A5876)
# {OpenGate = false;}
# else
# {OpenGate = false;}
# DodgeRam = P89099;
