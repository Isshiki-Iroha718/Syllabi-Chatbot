import pymysql

# Generate initial descriptive information for the database
def concatenate(database_name, user, password):
    try:
        # Start database connection
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='010624-aaA',
            database='syllabi_database',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        print("Successfully connected to the database")

        with connection.cursor() as cursor:
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()
            print("You're connected to database:", record)

            professor_info_set = []
            syllabus_info_set = []

            # Collect information from syllabus information table
            cursor.execute("SELECT * FROM syllabus_info")
            result = cursor.fetchall()
            for row in result:
                syllabus_info = ["The course is called " + row.__getitem__("COURSE_NAME") + " and its code is " + row.__getitem__("COURSE_CODE") + ". "]
                syllabus_info.append("This course's instructor is called " + row.__getitem__("COURSE_INSTRUCTOR") + ". ")
                course_location = "The course location is not defined"
                if row.__getitem__("COURSE_LOCATION") != "":
                    course_location = "This course is held " + row.__getitem__("COURSE_LOCATION") + ". "
                syllabus_info.append(course_location)
                course_period = "The course period is not defined"
                if row.__getitem__("COURSE_START_DATE") is not None and row.__getitem__("COURSE_END_DATE") is not None:
                    course_period = "This course starts from " + (str)(row.__getitem__("COURSE_START_DATE")) + " to " + (str)(row.__getitem__("COURSE_END_DATE")) + ". "
                syllabus_info.append(course_period)
                course_info = ""
                if row.__getitem__("COURSE_INFO") != "":
                    course_info = row.__getitem__("COURSE_INFO")
                syllabus_info.append(course_info)
                course_link = ""
                if row.__getitem__("COURSE_LINK") != "":
                    course_link = "You can access to the course link through " + row.__getitem__("COURSE_LINK") + ". "
                syllabus_info.append(course_link)
                result = "".join(syllabus_info)
                print(result)
                syllabus_info_set.append(result)


            # Collect information from professor information table
            cursor.execute("SELECT * FROM professor_info")
            result = cursor.fetchall()
            for row in result:
                professor_info = ["The professor name is " + row.__getitem__("PROFESSOR_NAME") + ". "]
                professor_phone = ""
                if row.__getitem__("PROFESSOR_PHONE") is not None:
                    professor_phone = "His/Her phone number is " + str(row.__getitem__("PROFESSOR_PHONE")) + ". "
                professor_info.append(professor_phone)
                professor_email = ""
                if row.__getitem__("PROFESSOR_EMAIL") != "":
                    professor_email = "His/Her email address is " + row.__getitem__("PROFESSOR_EMAIL") + ". "
                professor_info.append(professor_email)
                professor_link = ""
                if row.__getitem__("PROFESSOR_LINK") != "":
                    professor_link = "His/Her personal link is " + row.__getitem__("PROFESSOR_LINK") + ". "
                professor_info.append(professor_link)
                result = "".join(professor_info)
                print(result)
                professor_info_set.append(result)


    except Exception as e:
        print("Error while connecting to MySQL:", e)

    finally:
        # Close connection
        connection.close()
        print("MySQL connection is closed")

concatenate("syllabus_info", "user", "password")