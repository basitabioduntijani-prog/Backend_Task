# from sqlalchemy import create_engine,text
# from sqlalchemy.orm import sessionmaker
# from dotenv import load_dotenv
# from pymysql.constants import CLIENT
# import os

# load_dotenv()

# db_url = f'mysql+pymysql://{os.getenv("dbuser")}:{os.getenv("dbpassword")}@{os.getenv("dbhost")}:{os.getenv("dbport")}/{os.getenv("dbname")}'

# # engine = create_engine(db_url)
# engine = create_engine(
#     db_url,
#     connect_args={"client_flag": CLIENT.MULTI_STATEMENTS}
# )
# session =sessionmaker(bind = engine)

# db = session()

# # Writing sql queries
# query =  text("select * from user")

# users = db.execute(query).fetchall()

# print(users)

# create_table_query = text("""
# CREATE TABLE IF NOT EXISTS users (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     name VARCHAR(100) NOT NULL,
#     email VARCHAR(100) NOT NULL,
#     );

# CREATE TABLE IF NOT EXISTS courses (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     name VARCHAR(100) NOT NULL,
#     email VARCHAR(100) NOT NULL,
#     );
                          
# CREATE TABLE IF NOT EXISTS enrollments (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     userId INT,
#     courseId INT,
#     FOREIGN KEY (userId) REFERENCES user(id),
#     FOREIGN KEY (courseId) REFERENCES course(id),
#     );                        
# """)

# db.execute(create_table_query)
# print("Table created successfully")










from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from pymysql.constants import CLIENT
import os

load_dotenv()

db_url = f'mysql+pymysql://{os.getenv("dbuser")}:{os.getenv("dbpassword")}@{os.getenv("dbhost")}:{os.getenv("dbport")}/{os.getenv("dbname")}'



engine = create_engine(
    db_url,
    connect_args={"client_flag": CLIENT.MULTI_STATEMENTS}
)
session = sessionmaker(bind=engine)
db = session()

# First, create the tables with correct syntax
create_table_query = text("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    instructor_email VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS enrollments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    userId INT,
    courseId INT,
    FOREIGN KEY (userId) REFERENCES users(id),
    FOREIGN KEY (courseId) REFERENCES courses(id)
);
""")
db.execute(create_table_query)
print("Tables created successfully")

# # Now you can query the users table (note: it's 'users' not 'user')
# query = text("SELECT * FROM users")
# users = db.execute(query).fetchall()
# print(users)
















# # Create users table
# users_table = text("""
# CREATE TABLE IF NOT EXISTS users (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     name VARCHAR(100) NOT NULL,
#     email VARCHAR(100) NOT NULL UNIQUE
# )
# """)

# # Create courses table  
# courses_table = text("""
# CREATE TABLE IF NOT EXISTS courses (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     name VARCHAR(100) NOT NULL,
#     instructor_email VARCHAR(100) NOT NULL
# )
# """)

# # Create enrollments table
# enrollments_table = text("""
# CREATE TABLE IF NOT EXISTS enrollments (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     userId INT,
#     courseId INT,
#     FOREIGN KEY (userId) REFERENCES users(id),
#     FOREIGN KEY (courseId) REFERENCES courses(id)
# )
# """)

# # Execute each table creation separately
# db.execute(users_table)
# db.execute(courses_table) 
# db.execute(enrollments_table)
# print("All tables created successfully")


# # # Drop tables in reverse order (due to foreign key constraints)
# # drop_enrollments = text("DROP TABLE IF EXISTS enrollments")
# # drop_courses = text("DROP TABLE IF EXISTS courses")
# # drop_users = text("DROP TABLE IF EXISTS users")

# # db.execute(drop_enrollments)
# # db.execute(drop_courses)
# # db.execute(drop_users)
# # print("All tables dropped successfully")