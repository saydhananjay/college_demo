from flask import Flask, request, render_template, redirect, make_response
import mysql.connector

config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'wbut',
    # 'port': 23329
}

app = Flask("WBUT")


@app.route("/")
def home():
    return render_template('student.html')

@app.route("/submit", methods=["GET", "POST"])
def submit():
    if request.method == "GET":
        return render_template('submit.html')
    elif request.method == "POST":
        try:
            # Establish a connection to the MySQL database
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
            name = request.form["name"]
            roll_no = request.form["roll_no"]
            joining_year = request.form["joining_year"]
            college = request.form["college"]
            stream = request.form["stream"]
            print(joining_year)
            # SQL query to fetch student names
            query = f"insert into students (name,roll_no,joining_year,college,stream) values ('{name}',{roll_no},{joining_year},'{college}','{stream}');"
            cursor.execute(query)
            conn.commit()
            # Fetch all student names
            return make_response(redirect("/students"))

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()



@app.route("/students")
def students():
    try:
        # Establish a connection to the MySQL database
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # SQL query to fetch student names
        query = "SELECT name,roll_no, joining_year FROM students;"
        cursor.execute(query)

        # Fetch all student names
        student_names = cursor.fetchall()
        x = []
        for i in student_names:
            x.append({"name": i[0], "roll_no": i[1],"joining_year": i[2]})
        return x

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@app.route("/subjects")
def sub():
    try:
        # Establish a connection to the MySQL database
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # SQL query to fetch student names
        query = "SELECT id, name, total_marks FROM subjects;"
        cursor.execute(query)

        # Fetch all student names
        student_names = cursor.fetchall()
        x = []
        for i in student_names:
            x.append({"id": i[0],"name": i[1], "total_marks": i[2]})
        return x

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@app.route("/enrollments")
def enroll():
    try:
        # Establish a connection to the MySQL database
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # SQL query to fetch student names
        query = "SELECT  id, student_id, subject_id, year, semester FROM enrollments;"
        cursor.execute(query)

        # Fetch all student names
        student_names = cursor.fetchall()
        x = []
        for i in student_names:
            x.append({"id": i[0], "student_id": i[1],"subject_id": i[2],"year": i[3],"semester": i[4]})
        return x

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# @app.route("/students/Avik")
# def s_avik():
#     # Database connection configuration
#     config = {
#         'user': 'root',
#         'password': '',
#         'host': 'localhost',
#         'database': 'wbut'
#     }
#
#     try:
#         # Establish a connection to the MySQL database
#         conn = mysql.connector.connect(**config)
#         cursor = conn.cursor()
#
#         # SQL query to fetch student names
#         query = "SELECT * FROM students where name = 'Avik';"
#         cursor.execute(query)
#
#         # Fetch all student names
#         student_names = cursor.fetchall()
#
#         x = []
#         for i in student_names:
#             x.append({"name" : i[0], "roll_no" : i[1], "joining_year" : i[2], "college" : i[3], "stream" : i[4]})
#         return x
#     except mysql.connector.Error as err:
#         print(f"Error: {err}")
#
#     finally:
#         if conn.is_connected():
#             cursor.close()
#             conn.close()

@app.route("/students/<name>")
def stu_details(name):
    try:
        # Establish a connection to the MySQL database
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        # SQL query to fetch student names
        query = f"SELECT * FROM students where name = '{name}';"
        cursor.execute(query)
        # Fetch all student names
        student_names = cursor.fetchall()
        x = []
        for i in student_names:
            x.append(
                {
                    "name": i[0],
                    "roll_no": i[1],
                    "joining_year": i[2],
                    "college": i[3],
                    "stream": i[4]
                }
            )
        return x
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


@app.route("/students/<name>/semester/<semester>/subjects", methods=['GET', 'POST'])
def stu_sem_1(name, semester):
    if request.method == "GET":
        try:
            # Establish a connection to the MySQL database
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
            # SQL query to fetch student names
            query = f"select subjects.id as id, subjects.name as subject  from students join enrollments on enrollments.student_id = students.roll_no join subjects on subjects.id = enrollments.subject_id where students.name = '{name}'and enrollments.semester = '{semester}';"
            cursor.execute(query)
            # Fetch all student names
            student_names = cursor.fetchall()
            x = {"subjects": []}

            for i in student_names:
                x["subjects"].append({
                    "id": i[0],
                    "name": i[1]
                })
            return x

        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    else:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        subject_id = request.form[
            "subject_id"]  # form dictionary hai jo ki request ke ander hai.aur params(body) ka value le raha hai
        querry = f"insert into enrollments (student_id,subject_id,year,semester) values (123,{subject_id},2011,{semester});"
        cursor.execute(querry)
        conn.commit()
        print(subject_id)
        print(querry)
        return "successfully added"


@app.route("/students/add/", methods=['POST'])
def add_stu():
    if request.method == "POST":
        try:
            # Establish a connection to the MySQL database
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
            name = request.form["name"]
            roll_no = request.form["roll_no"]
            joining_year = request.form["joining_year"]
            college = request.form["college"]
            stream = request.form["stream"]
            print(joining_year)
            # SQL query to fetch student names
            query = f"insert into students (name,roll_no,joining_year,college,stream) values ('{name}',{roll_no},{joining_year},'{college}','{stream}');"
            cursor.execute(query)
            conn.commit()
            # Fetch all student names
            upda = cursor.fetchall()

            return "successfully updated"

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()


@app.route("/subjects/add/", methods=['POST'])
def add_sub():
    if request.method == "POST":
        try:
            # Establish a connection to the MySQL database
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
            # idd = request.form["id"]
            name = request.form["name"]
            practical = request.form["practical"]
            total_marks = request.form["total_marks"]

            # SQL query to fetch student names
            query = f"insert into subjects (name,practical,total_marks) values ('{name}',{practical},{total_marks});"
            cursor.execute(query)
            conn.commit()
            # Fetch all student names
            upda = cursor.fetchall()

            return "successfully updated"

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

@app.route("/enrollments/add/", methods=['POST'])
def add_enroll():
    if request.method == "POST":
        try:
            # Establish a connection to the MySQL database
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
            # idd = request.form["id"]
            student_id = request.form["student_id"]
            subject_id = request.form["subject_id"]
            year = request.form["year"]
            semester = request.form["semester"]

            # SQL query to fetch student names
            query = f"insert into enrollments (student_id, subject_id, year, semester) values ({student_id},{subject_id},{year},{semester});"
            cursor.execute(query)
            conn.commit()
            # Fetch all student names
            upda = cursor.fetchall()

            return "Enrollments updated successfully"

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

if __name__ == "__main__":
    app.run(debug=True, port=5000,host="0.0.0.0")
