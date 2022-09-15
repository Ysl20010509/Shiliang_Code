from getpass import getpass
from xml.dom.expatbuilder import parseString
from mysql.connector import connect, Error
# from Send_email import daily_report

def Create_database():
    try:
        with connect(
            host="staging.cejhgoi6hssq.us-west-2.rds.amazonaws.com",
            user="indeed",
            password="indeed1357"
        ) as connection:
            create_db_query = "CREATE DATABASE indeed_jobs"
            with connection.cursor() as cursor:
                cursor.execute(create_db_query)
    except Error as e:
        print(e)
    

def Connect_database(database_name):
    try:
        with connect(
            host="staging.cejhgoi6hssq.us-west-2.rds.amazonaws.com",
            user="indeed",
            password="indeed1357",
            # host = "localhost",
            # user = "root",
            # password = "Ysl20010509",
            database=database_name
        ) as connection:
            return connection
    except Error as e:
        print(e)


def Create_table(connection):
    create_job_table_query = """
    CREATE TABLE jobs(
        JobID VARCHAR(50) PRIMARY KEY,
        Search_Word VARCHAR(50),
        Post_Date Varchar(30),
        TimeStamp datetime,
        Job_Title VARCHAR(100),
        Company VARCHAR(100),
        Location VARCHAR(100),
        City VARCHAR(50),
        State VARCHAR(3),
        Salary VARCHAR(100),
        JobType VARCHAR(30),
        Description VARCHAR(1000),
        JobURL VARCHAR(3000),
        Experience_Level VARCHAR(50)
    )
    """
    connection.reconnect()
    try:
        with connection.cursor() as cursor:
            cursor.execute(create_job_table_query)
            connection.commit()
    except Error as e:
        print(e)

def show_table(connection, search_word):
    show_table_query1 = "SELECT JobID FROM jobs WHERE Search_Word = '" + search_word + "'" + " AND Experience_Level LIKE '%entry%'" + " ORDER BY TIMESTAMP ASC LIMIT 50"
    show_table_query2 = "SELECT JobID FROM jobs WHERE Search_Word = '" + search_word + "'" + " AND Experience_Level LIKE '%mid%'" + " ORDER BY TIMESTAMP ASC LIMIT 50"
    show_table_query3 = "SELECT JobID FROM jobs WHERE Search_Word = '" + search_word + "'" + " AND Experience_Level LIKE '%senior%'" + " ORDER BY TIMESTAMP ASC LIMIT 50"
    connection.reconnect()
    with connection.cursor() as cursor:
        cursor.execute(show_table_query1)
    # Fetch rows from last executed query
        result1 = cursor.fetchall()
        cursor.execute(show_table_query2)
        result2 = cursor.fetchall()
        cursor.execute(show_table_query3)
        result3 = cursor.fetchall()
        output = [row[0] for row in result1]
        output2 = [row[0] for row in result2]
        output3 = [row[0] for row in result3]
    #  print(output)
        return set(output + output2 + output3)
         

def insert_data(connection, records):
    insert_jobs_query = ("INSERT INTO jobs(JobID, Search_Word, Post_Date, TimeStamp, Job_Title, Company, Location, City, State, Salary, JobType, Description, JobURL, Experience_Level)"
    "VALUES (%s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s)")
    
    
    connection.reconnect()
    # with connection.cursor() as cursor:
    #     cursor.executemany(insert_jobs_query, records)
    #     connection.commit()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM `jobs`")
        cursor.fetchall()
        if cursor.rowcount == 0:
            records = reversed(records)

        for i in records:
            try:
                cursor.execute(insert_jobs_query, i)
                connection.commit()
            except Error as e:
                print(e)
    connection.disconnect()



'''
Alter Table
'''
# alter_table_query = """
# ALTER TABLE jobs
# MODIFY COLUMN Experience_Level VARCHAR(200)
# """
# con = Connect_database("indeed_jobs")
# con.reconnect()
# with con.cursor() as cursor:
#     cursor.execute(alter_table_query)

'''
To view the database
'''
# con = Connect_database("indeed_jobs")
# show_table(con, "Software Engineer")


# '''
# Delete all entries
# '''
# con = Connect_database("indeed_jobs")
# con.reconnect()
# # count_query = "SELECT ROW_COUNT()"
# truncate_query = "TRUNCATE jobs"
# with con.cursor(buffered=True) as cursor:
#     cursor.execute(truncate_query)
#     con.commit()
# delete_query = "DELETE FROM jobs WHERE State = ''"
# with con.cursor() as cursor:
#     cursor.execute(delete_query)
#     con.commit()

# show_table_query = "SELECT JobID FROM jobs WHERE Search_Word = '" + "Software Engineer" + "'" + " ORDER BY TIMESTAMP DESC LIMIT 20"
# connection = Connect_database("indeed_jobs")
# connection.reconnect()
# with connection.cursor() as cursor:
#         cursor.execute(show_table_query)
#     # Fetch rows from last executed query
#         result = cursor.fetchall()
#         output = [row[0] for row in result]
#         print(output)
# con = Connect_database("indeed_jobs")
# # Create_table(con)
# con.close()