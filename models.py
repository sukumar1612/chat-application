import sqlite3

class User:
    def __init__(self, _id, username, password):
        self.id=_id
        self.username=username
        self.password=password

    @classmethod
    def find_by_username(cls, username):
        connect = sqlite3.connect('data.db')
        cursor = connect.cursor()

        query="select userid, username, password from users where username=?"
        result = cursor.execute(query, (username,))

        row = result.fetchone()


        if row:
            user = cls(row[0], row[1], row[2])
        else:
            user = None

        connect.close()
        return user

    @classmethod
    def insert_user(cls, username, email, password):
        connect = sqlite3.connect('data.db')
        cursor = connect.cursor()

        query = "INSERT INTO users (username, email, password) VALUES (?, ?, ?)"
        cursor.execute(query, (username,email,password))

        connect.commit()
        connect.close()

    @classmethod
    def find_by_id(cls, userid):
        connect = sqlite3.connect('data.db')
        cursor = connect.cursor()

        query = "select userid, username, password from users where userid=?"
        result = cursor.execute(query, (userid,))

        row = result.fetchone()

        if row:
            user = cls(row[0], row[1], row[2])
        else:
            user = None

        connect.close()
        return user

    @classmethod
    def return_all_users(cls):
        connect = sqlite3.connect('data.db')
        cursor = connect.cursor()

        query = "select userid, username from users"
        result = cursor.execute(query)

        row = result.fetchall()

        lst=[]
        if row:
            for i in row:
                lst.append([i[0], i[1]])
        else:
            lst = None

        connect.close()
        return lst

