import pymysql
from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import OpenAI
import re
import Syllabi_Read as sr

# Generate initial descriptive information for the database
def concatenate():
    syllabus_info_set = []
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

            # Collect information from syllabus information table
            cursor.execute("SELECT * FROM syllabus_info")
            result = cursor.fetchall()
            for row in result:
                syllabus_info = ["The course is called " + row.__getitem__("COURSE_NAME") + ". "]
                syllabus_info.append("This course's instructor is called " + row.__getitem__("COURSE_INSTRUCTOR") + ". ")
                course_location = "The course location is not defined"
                if row.__getitem__("COURSE_LOCATION") != "":
                    course_location = "This course is held " + row.__getitem__("COURSE_LOCATION") + ". "
                syllabus_info.append(course_location)
                course_period = "The course period is not defined"
                if row.__getitem__("COURSE_START_DATE") != "" and row.__getitem__("COURSE_END_DATE") != "":
                    course_period = "This course starts from " + (row.__getitem__("COURSE_START_DATE")) + " to " + (row.__getitem__("COURSE_END_DATE")) + ". "
                syllabus_info.append(course_period)
                course_info = ""
                if row.__getitem__("COURSE_INFO") != "":
                    course_info = row.__getitem__("COURSE_INFO")
                syllabus_info.append(course_info)
                result = "".join(syllabus_info)
                print(result)
                syllabus_info_set.append(result)

    except Exception as e:
        print("Error while connecting to MySQL:", e)

    finally:
        # Close connection
        connection.close()
        print("MySQL connection is closed")

    db_description = "\n".join(syllabus_info_set)
    return db_description

# Extract useful course information
def extract(file_path):
    standardize_str = "Please extract the file information using line breaks as separators, providing only the answers for each item: course name, course instructor, course brief description, course location, course start date, course end date. Keep the same item name and colon in the answer. Please do not add any additional words but keep the colons."
    documents = sr.handle_file(file_path)

    # Use text spliter to extract information from tge document
    # In fact, not really use spliter. Just transfer the information from document to string
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=100,
        separators=["\n\n", ".", " "]
    )

    # Divided the whole file into different sections
    split_documents = text_splitter.split_documents(documents)
    documents_list = []
    for s in split_documents:
        documents_list.append(s.page_content)
    input_document = "\n".join(documents_list)

    # Use ChatGPT to extract information from document
    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "system", "content": input_document},
            {"role": "user", "content": standardize_str}
        ]
    )

    # Collect response from OpenAI API
    course_info = response.choices[0].message.content
    print(course_info)

    # Extract information from the standardized response
    course_name = re.search(r'course name:\s*(.*)', course_info, re.IGNORECASE)
    course_name = course_name.group(1).strip() if course_name else ''

    course_instructor = re.search(r'course instructor:\s*(.*)', course_info, re.IGNORECASE)
    course_instructor = course_instructor.group(1).strip() if course_instructor else ''

    course_description = re.search(r'course brief description:\s*(.*)', course_info, re.IGNORECASE)
    course_description = course_description.group(1).strip() if course_description else ''

    course_location = re.search(r'course location:\s*(.*)', course_info, re.IGNORECASE)
    course_location = course_location.group(1).strip() if course_location else ''

    course_start_date = re.search(r'course start date:\s*(.*)', course_info, re.IGNORECASE)
    course_start_date = course_start_date.group(1).strip() if course_start_date else ''

    course_end_date = re.search(r'course end date:\s*(.*)', course_info, re.IGNORECASE)
    course_end_date = course_end_date.group(1).strip() if course_end_date else ''

    result = [course_name,course_instructor,course_description,course_location,course_start_date,course_end_date, (str)(file_path)]
    return result

def update(index_list):
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

            # Collect information from syllabus information table
            sql_query = """
                            INSERT INTO syllabus_info 
                            (COURSE_NAME, COURSE_INSTRUCTOR,COURSE_INFO, COURSE_LOCATION, COURSE_START_DATE, COURSE_END_DATE, COURSE_LINK) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s);
                        """
            cursor.execute(sql_query, (index_list[0], index_list[1], index_list[2], index_list[3], index_list[4], index_list[5], index_list[6]))
            connection.commit()
            print("Data inserted successfully")

    except Exception as e:
        print("Error while connecting to MySQL:", e)

    finally:
        # Close connection
        connection.close()
        print("MySQL connection is closed")


# concatenate("syllabus_info", "user", "password")
# update(extract("Syllabus/Syllabi/Gould MASY1-GC1230-201, Strategic Marketing Fall 2022_Final.pdf"))
