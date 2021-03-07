
import sys

# !-- LEXER --! #
# This class will take the source code from the user as input and
# produce tokens. Each step is explained in details!

# Create strings and store the valid characters which can be used
# in the source code. Any other character, digit, or alphabet will
# be considered as an illegal character and a message will be
# printed showing the illegal character and the line where it is
# located, then the program will exit.



# All the numbers:
Valid_Integers = '0123456789.'

# All the alphabets including small and capital, as well as the other
# characters such as (=, <, >, !):
Valid_Characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ=<>!.'



# Create a class to define the current character's position in the source code.
# We will use this class to control the index in order to increment it whenever 
# we want to:
class Current_Character_Position:

    # Define an initialization method to create the variable which will
    # hold the current character index:
    def __init__(self, Current_Character_Index):
        self.Current_Character_Index = Current_Character_Index

    # Define a method to increment the current character index by 1. This is
    # the method we will call every time to increment move to the next character:
    def Increment_Current_Character_Index(self):
        self.Current_Character_Index += 1

        return




# Create all the necessary token types for our "Boolean" statement:
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



# Create a class which will initialize tokens. Each token will have a type
# which was set from the tokens above, and will also have a value depending
# on  whether it's an integer, float, variable or anything else. because
# some tokens will not have a value, we will set is to "None" from the beginning:
class Token:

    # Define an initialization method to create variables which will hold the
    # token type and value:
    def __init__(self, TKN_TYPE, TKN_VALUE = None):
        self.Token_Type = TKN_TYPE
        self.Token_Value = TKN_VALUE

    # Define a representation method which will be used to print (represent) the
    # tokens to the user:
    def __repr__(self):

        # If a token has a value set to it, print both the type and value:
        if self.Token_Value is not None:
            return f'{self.Token_Type}:{self.Token_Value}'
        # If a token doesn't have a value set to it, print only the type:
        else:
            return f'{self.Token_Type}'



# This is the main Lexer Class. This class will be used to iterate through every
# single character in the source code and extract the known variables and terms 
# in order to create the tokens. 
class Lexer:

    # Define an initialization method to create the variables which will contain 
    # the Source Code, Current Character Position, and Current Character value. 
    # Because we need to begin from the very first character, we will set the 
    # Current_Character_Position to -1, then use the method to increment. We have
    # tried to begin with 0 however it didn't work as expected. We will also set
    # the value of the Current Character to None:
    def __init__(self, User_Input):
        self.Source_Code = User_Input
        self.current_char = None
        self.CC_Position = Current_Character_Position(-1)   # CC = Current Character
        self.Increment_Current_Character_Index()
        self.Current_Line_Counter = 1

    def Increment_Current_Line_counter(self):
        self.Current_Line_Counter += 1

    # Define a method that will increment the index of the current character by calling the previous
    # method we created above. After incrementing the index, we will update the current character to
    # contain the value of the next character (Current_character[i + 1]):
    def Increment_Current_Character_Index(self):
        self.CC_Position.Increment_Current_Character_Index()

        # After incrementing the index, we assign the current character to the new index. But before
        # doing so, we check if the new incremented index is less than the length of the Source Code.
        # If the index was less that the length of the Source Code, we can proceed to assign the current
        # character to the new index, however if it is equal to the length then it means there is no next
        # character so we set it to "None" in order for the program to finish execution:
        if self.CC_Position.Current_Character_Index < len(self.Source_Code):
            self.current_char = self.Source_Code[self.CC_Position.Current_Character_Index]
        else:
            self.current_char = None



    # Define a method to create the actual tokens. We will create an array then keep checking
    # for every single character and word in the Source Code to match with the appropriate
    # token. After finding the and matching the tokens, we will append them to the array we
    # created:
    def Create_And_Match_Tokens(self):

        # Create a list to store the found tokens in it:
        List_Of_Tokens = []

        # Check for each character that isn't an alphabet or number and match with the correct
        # token then append the token to the list. the first "if" statement check to see if the
        # current character is a space, tab, or a new line, and if found so the program will
        # ignore it:
        while self.current_char is not None:
            if self.current_char in ' \t':
                self.Increment_Current_Character_Index()
            elif self.current_char in '\n':
                List_Of_Tokens.append(Token(TKN_NewLine))
                self.Increment_Current_Line_counter()
                self.Increment_Current_Character_Index()
            elif self.current_char == '(':
                List_Of_Tokens.append(Token(TKN_ParenthesisL))
                self.Increment_Current_Character_Index()
            elif self.current_char == ')':
                List_Of_Tokens.append(Token(TKN_ParenthesisR))
                self.Increment_Current_Character_Index()
            elif self.current_char == '{':
                List_Of_Tokens.append(Token(TKN_CurlyL))
                self.Increment_Current_Character_Index()
            elif self.current_char == '}':
                List_Of_Tokens.append(Token(TKN_CurlyR))
                self.Increment_Current_Character_Index()
            elif self.current_char == ';':
                List_Of_Tokens.append(Token(TKN_Semicolon))
                self.Increment_Current_Character_Index()
            # If the current character isn't from the ones above, it means it is either a String or
            # an Integer, So we will check so by calling another method:
            elif self.current_char in Valid_Characters:
                List_Of_Tokens.append(self.Make_String(self.Current_Line_Counter))
            # If the current character is none of the above, then it must be an Illegal Character. We
            # will assign it to a variable and print an error message. Then we will increment the index
            # to continue the program:
            else:
                Illegal_Character = self.current_char
                self.Increment_Current_Character_Index()
                return Error_Message(Illegal_Character, self.Current_Line_Counter)

        # After finishing all the characters in the Source Code and appending the tokens to the list, we
        # return the list to the user in order to be used in the parser:
        return List_Of_Tokens



    # Define a method to iterate through as many characters as possible that might resemble a String.
    #  We have limited the inputs that will be given to this method to 2 which are either a String or
    # an Integer. First it will take all the characters and store them in a string until a space is
    # found where the program will stop. Then it will check the formulated string such that is if is
    # all numbers then it is an Integer, else it must be a string. Then we check for the strings whether
    # it is a variable or an already defined word such as "boolean" or "if" or "else":
    def Make_String(self, Current_Line_Counter):

        # This variable will hold all the characters initially:
        String = ''

        # This variable will be the final string which will be returned to the program as a token to be
        # appended to the List_Of_Tokens:
        FinalWord = ''

        # check if the current character isn't the last one and if it's valid and not illegal:
        while self.current_char is not None and (self.current_char in Valid_Characters):

            # If the character passes the inspection above, it will be added to the initial String:
            String = String + self.current_char

            # We will increment the index so that the current character will be updated to the next one.
            # The process is repeated until a space is found where the program will stop collecting
            # characters and will continue below with the String it generated:
            self.Increment_Current_Character_Index()

            # Call a method to check if the generated string is all numbers which if it was, we will
            # append it to the list as an Integer and exit the loop and method. If it wasn't all numbers,
            # the program will enter the else statement where it will begin comparing the string with the
            # required defined words of the program:
            if CheckIfNumber(String) == True:
                # Send it to another method which determines whether it is an Integer or a Float and then
                # append it with its respective token:
                FinalWord = Set_Int_Or_Float(String, Current_Line_Counter)
            else:
                if String == 'equals':
                    FinalWord = Token(TKN_Equals)
                elif String == 'boolean':
                    FinalWord = Token(TKN_Boolean, str(String))
                elif String == 'true':
                    FinalWord = Token(TKN_BooleanT, str(String))
                elif String == 'false':
                    FinalWord = Token(TKN_BooleanF, str(String))
                elif String == 'if':
                    FinalWord = Token(TKN_IfStatement, str(String))
                elif String == 'elif':
                    FinalWord = Token(TKN_ELIFStatement, str(String))
                elif String == 'else':
                    FinalWord = Token(TKN_ElseStatement, str(String))
                elif String == ';':
                    FinalWord = Token(TKN_Semicolon, str(String))
                elif String == '<':
                    FinalWord = Token(TKN_LT, str(String))
                elif String == '>':
                    FinalWord = Token(TKN_GT, str(String))
                elif String == '<=':
                    FinalWord = Token(TKN_LTEQ, str(String))
                elif String == '>=':
                    FinalWord = Token(TKN_GTEQ, str(String))
                elif String == '!=':
                    FinalWord = Token(TKN_NOTEQ, str(String))
                elif String == '=':
                    FinalWord = Token(TKN_Assign, str(String))
                elif String == '!':
                    FinalWord = Token(TKN_NOT, str(String))
                    #If the String didn't match any of the above statements, it would certainly mean
                    # that it is a variable and the program will append it respectively:
                else:
                    FinalWord = Token(TKN_Variable, str(String))

        # Return the FinalWord variable to the Create_And_Match_Tokens method where it will be
        # appended to the List_Of_Tokens:
        return FinalWord



# Define a method to check whether the String is an Integer or not:
def CheckIfNumber(GeneratedString):

    # Create a boolean variable and set it to True:
    Flag = True

    # Iterate over every single number in the string, if no character is spotted and everything was
    # a number, it will be sent to another method which will determine whether it's an Integer or Float:
    for i in range (0, len(GeneratedString)):
        if GeneratedString[i] in Valid_Integers:
            continue
        else:
            Flag = False

    return Flag



# Define a method that would check whether the number is an Integer or a Float:
def Set_Int_Or_Float(GeneratedInteger, Current_Line_Number):

    # Variable to hold the number of points fount in the number. Set it initially to 0:
    Number_Of_Points = 0

    # Iterate over every element and check whether it is a number or a point using a for loop:
    for i in range (0, len(GeneratedInteger)):
        # If the current character was a point, the program will increment the variable and continue:
        if GeneratedInteger[i] == ".":
            Number_Of_Points += 1
        else:
            continue

    # if the counter of points was more than 0, it means the number is a float, else it is an Integer:
    if Number_Of_Points == 1:
        return Token(TKN_Float, float(GeneratedInteger))
    elif Number_Of_Points > 1:
        print("Float must contain only one point, Found " + str(Number_Of_Points) + ".")
        print("Error at line " + str(Current_Line_Number))
        sys.exit()
    else:
        return Token(TKN_Integer, int(GeneratedInteger))


# Define a method to display an error message whenever an illegal character is fount:
def Error_Message(Illegal_Character, Current_Line_Number):

    print("ILLEGAL CHARACTER FOUND " + "--{" + Illegal_Character + "}--" " AT LINE " + str(Current_Line_Number))
    sys.exit()

    return

