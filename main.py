import pandas as pd
from datetime import datetime
import faker
import random
import string
#try:
#    a = int("1")
#    print(a.isdigit())
#except:
#    print("caught")
#exit()

#validates user input for the appropriate situation
def input_check(user_input):
    try:
        user_input = int(user_input)
        while(len(str(abs(int(user_input)))) != 6):
            user_input = input("Please enter a valid response: ")
        return user_input
    except:
        while(not user_input.isalpha()):
            user_input = input("Please enter a valid response: ")
        return user_input
    #if datatype == int:
    #    while(not user_input.isdigit() or len(str(abs(int(user_input)))) != 6):
    #        user_input = input("Please enter a valid response: ")
    #    return user_input
    #elif datatype == str:
    #    while(not user_input.isalpha()):
    #        user_input = input("Please enter a valid response: ")
    #    return user_input
    
# if the employee is already in the table, the record's date is updated to today
def update_date(PERNR, DF):    
    record = DF.loc[DF["PERNR NUMBER"] == int(PERNR)]
    index = record.index[0]
    DF.loc[index, "DATE AGREEMENT SIGNED"] = datetime.today()
    print("Date updated!")

#if the employee does not exist yet, a new record is created
def new_entry(PERNR, DF):
    first_name = input_check(input("First Name: "))
    last_name = input_check(input("Last Name: "))
    initial = input_check(input("Supervisor first name initial: "))
    while(len(initial) != 1):
        print("Initial can only be one letter")
        initial = input_check(input("Supervisor first name initial: "))
    supervisor_lname = input_check(input("Supervisor last name: "))
    supervisor_entry = initial + "." + " " + supervisor_lname
    print(f"You entered: {first_name},{last_name},{supervisor_entry}")
    confirmation = input("Enter 'y' to confirm, any other input implies a mistake: ")
    while(confirmation.upper() != "Y"):
        first_name = input("First Name: ")
        last_name = input("Last Name: ")
        initial = input("Supervisor first name initial: ")
        supervisor_lname = input("Supervisor last name: ")
        supervisor_entry = initial + "." + " " + supervisor_lname
        print(f"You entered: {first_name},{last_name},{supervisor_entry}")
        confirmation = input("Enter 'y' to confirm, any other input implies a mistake: ")
    DF.loc[len(DF)] = [int(PERNR), last_name, first_name, datetime.today(), supervisor_entry]
    print("Added!")

#this function searches for the employee in the data using the PERNR number
def search(PERNR):
    for i in range(len(DF)):
        if DF.loc[i, "PERNR NUMBER"] == int(PERNR):
            return True
    return False


#Reading the provided Excel sheet, and specifying the column datatypes
DF = pd.read_excel("log.xlsx")
DF = DF.astype({"PERNR NUMBER":'Int64', "EMPLOYEE LAST NAME":str, "EMPLOYEE FIRST NAME":str, "SUPERVISOR":str})


#PSUEDO DATA generation, this code may be commented out if the provided Excel sheet already has data ---------------------------------------------------------------------------------------------
faker = faker.Faker()
for i in range(len(DF)):
    DF.loc[i, "PERNR NUMBER"] = random.randint(100000, 999999)
    DF.loc[i, "EMPLOYEE FIRST NAME"] = faker.first_name()
    DF.loc[i, "EMPLOYEE LAST NAME"] = faker.last_name()
    DF.loc[i, "SUPERVISOR"] = string.ascii_uppercase[random.randint(0, 25)] + " " + faker.last_name()

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
# Brief data clean, PERNR numbers are a unique employee identifier so duplicates may not exist
df = DF.drop_duplicates(subset = ["PERNR NUMBER"])
#The sheet is to be sorted by last name
df = df.sort_values(["EMPLOYEE LAST NAME"])

#use the head() and tail() methods too see the amount of data desired at any point during the program
#   print(df.head())
#   print(df.tail())

#WORKFLOW
print("Let's get to work updating our log.")
while(True):
    num = input_check(input("Enter the six-digit PERNR: "))
    if search(num):
        print("Found")
        update_date(num, df)
    else:
        print("Not found")
        new_entry(num, df)
        #dataframe must be resorted by last name after a new record entered
        df = df.sort_values(["EMPLOYEE LAST NAME"])
    continue_working = input("Continue working? Enter 'a' for yes, any other key implies no: ")
    if continue_working.upper() == "A":
        continue
    else:
        output = input("Export the new Excel file? Enter 'a' for yes, any other key implies no: ")
        if output.upper() == "A":
            df.to_excel("output.xlsx")
            print("Exported! Note: you'll have to expand the columns.")
            break
        else:
            break
print("Thank you for using this program. Great work.")
