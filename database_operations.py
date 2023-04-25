import pymysql

# connect to the database
conn = pymysql.connect(
    host='localhost',
    user='Pratham',
    password='1234',
    db='chatbotdatabase'
)

# create a cursor object to execute SQL queries
c = conn.cursor()

# create a table
c.execute('''CREATE TABLE IF NOT EXISTS users 
             (id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255), email VARCHAR(255))''')

# insert data into the table
c.execute("INSERT INTO users (name, email) VALUES (%s, %s)", ('John Doe', 'john@example.com'))

# commit changes to the database
conn.commit()

# fetch data from the table
c.execute("SELECT * FROM users")
result = c.fetchall()

# print the results
for row in result:
    print(row)

# close the connection
conn.close()
