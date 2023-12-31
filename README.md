Я создала базу данных в jupyter-notebook с помощью следующего кода: cur.execute(""" CREATE TABLE IF NOT EXISTS answers ( answer_id INTEGER PRIMARY_KEY, q1 TEXT, q2 TEXT, q3 TEXT, q4 TEXT, q5 TEXT, q6 TEXT, q7 TEXT, q8 TEXT, q9 TEXT )""")

cur.execute(""" CREATE TABLE IF NOT EXISTS users ( user_id INTEGER PRIMARY_KEY AUTO_INCREMENT, name TEXT, surname TEXT, age INTEGER, gender TEXT, city TEXT )""")

База данных лежит в папке instance.
