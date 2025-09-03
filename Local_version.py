import mysql.connector
from mysql.connector import Error
import random
def server_connection(host, user, pwd):
    connection = None
    try:
        connection = mysql.connector.connect(
            host = host,
            user = user, 
            passwd = pwd
        ) 
        print("Your server is running")    
    except Error as err:
        print(f"Error :{err}")


    return connection

#connection = server_connection("localhost", "root", "Ahamed@@122")

def create_database(query, connection):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created Successfully")
    except Error as err:
        print(f"Error :{err}")

#create_database("CREATE Database quiz", connection)

def database_connection(host, user, pwd, db):
    connection = None
    try:
        connection = mysql.connector.connect(
            host = host,
            user = user,
            passwd = pwd,
            database = db
        )

        print("Database connection Successful")

    except Error as err:
        print("Error :{err}")
    return connection

# db_connection = database_connection('localhost', 'root', "Ahamed@@122", "quiz")

def execute_query(query, connection):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully")

    except Error as err:
        print("Error {err}")

query1 = '''CREATE TABLE all_questions(
qn_id INT AUTO_INCREMENT primary key,
questions VARCHAR(1000) not null,
option1 VARCHAR(100) not null,
option2 VARCHAR(100) not null,
option3 VARCHAR(100) not null,
option4 VARCHAR(100) not null,
answer VARCHAR not null
)'''

query2 = """
CREATE Table user_details(
user_id INT primary key,
name VARCHAR(50) not null,
Score INT not null
)
"""

query3 = """
ALTER TABLE all_questions MODIFY answer VARCHAR(100) NOT NULL;
"""

# execute_query(query1, db_connection)
# execute_query(query2, db_connection)
# execute_query(query3, db_connection)

def Question():
    key = "Y"

    while key == "Y" or key == "y":
        print("Add Questions and their options with answer:")
        print("--------------------------------------------")
        question = input("Enter the Question: ")
        option1 = input("Enter the option 1: ")
        option2 = input("Enter the option 2: ")
        option3 = input("Enter the option 3: ")
        option4 = input("Enter the option 4: ")
        answer = 0

        while answer == 0:
            option = int(input("Enter the option as number 1,2,3 or 4: "))
            if option == 1:
                answer = option1
            elif option == 2:
                answer = option2
            elif option == 3:
                answer = option3
            elif option == 4:
                answer = option4

            else:
                print("Give the correct option number.")

        mycursor.execute("SELECT * from all_questions")
        data = mycursor.fetchall()
        mycursor.execute("INSERT into all_questions(questions, option1, option2, option3, option4, answer) VALUES(%s, %s, %s, %s, %s, %s)", 
                            (question, option1, option2, option3, option4, answer))

        mydb.commit()
        key = input("Question added successfully, Do you want to add more(y/n): ")
    Home()


def quiz():
    print("Welcome to Quiz Portal")
    mycursor.execute("SELECT * from all_questions")
    data = mycursor.fetchall()
    
    name = input("Enter your Name: ")
    total_questions = mycursor.rowcount

    to_attempt = int(input(f"Please input the total Number of question you want to attempt (Maximum {total_questions})"))
    question_id = [i for i in range(1, total_questions+1)]
    question_id = random.sample(question_id, to_attempt)

    c = 1
    score = 0
    wrong = {}
    for i in range(len(question_id)):
        mycursor.execute("SELECT * from all_questions WHERE qn_id = %s", (question_id[i],))
        qn = mycursor.fetchone()

        print("------------------------------------------")
        print("Q", c, ":", qn[1], "\n a.", qn[2], '\t \tb.', qn[3], '\n c.', qn[4], "\t \td.", qn[5])
        print("------------------------------------------")
        c += 1
        answer = None

        while answer == None:
            choice = input("Please choose the option beween a,b,c and d: ").strip().lower()

            if choice == "a":
                answer = qn[2]
                print("Moving on to next question")
            elif choice == "b":
                answer = qn[3]
                print("Moving on to next question")
            elif choice == "c":
                answer = qn[4]
                print("Moving on to next question")
            elif choice == "d":
                answer = qn[5]
                print("Moving on to next question")
            else:
                print("Only input choice between a to d")
        if answer == qn[6]:
            score += 1
        else:
            wrong[qn[1]] = qn[6]

    print("The quiz has ended")
    print(f"Your score is {score}")
    if score != len(question_id):
        see_answer = input("Do you want to see the correct answers for your incorrect attempts (y/n); ")
        if see_answer == "y" or see_answer == "Y":
            for q, ans in wrong.items():
                print(f"Question: {q} \n Correct Answer {ans}")

    mycursor.execute("Select * from user_details")
    data = mycursor.fetchall()
    user_id = mycursor.rowcount + 1

    mycursor.execute("INSERT into user_details VALUES(%s,%s,%s)",(user_id, name, score))
    mydb.commit()
    key = input("Press any key to continue:")
    Home()

def Home():
    opt = 1
    
    while opt != 3:
        print("Welcome To Quiz")
        print("=================")
        print("What do you want to do:\n1.Enter Questions \n2.Take Quiz \n3.Exit")
        opt = int(input("Enter the choice:"))
        if opt == 1:
            Question()
        elif opt==2:
            quiz()
        elif opt ==3:
            print("Exiting the quiz")
            mycursor.close()
            mydb.close()
        else:
            Home()

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root", 
    passwd = "Ahamed@@122",
    database = "quiz"
)

mycursor =mydb.cursor()

execute_query(query2, mydb)
Home()






            
            
            




     


    


