import sqlite3

conn = sqlite3.connect('user.db')
c = conn.cursor()

"""c.execute('''CREATE TABLE users (
                id integer,
                username text,
                mail text,
                pass text,
                v_mail integer,
                v_pass integer,
                status text,
                join_date text,
                join_time text
                count int
                )''')"""


def dbConn():
    global conn, c
    conn = sqlite3.connect('user.db')
    c = conn.cursor()


def newUser(idn, uname, mail,
            passw, vmail, vpass,
            status, join_date,
            join_time):
    dbConn()
    with conn:
        try:
            c.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
                      (idn, uname, mail, passw, vmail, vpass, status, join_date, join_time))
            return 0
        except Exception as e:
            print(e)
            return e


# returns status of verified passcode
def vPass(umail):
    dbConn()
    with conn:
        c.execute("SELECT v_pass FROM users WHERE mail =?", (umail,))
        return c.fetchone()


def last_id():
    dbConn()
    with conn:
        c.execute("SELECT id FROM users ORDER BY id DESC LIMIT 1")
        return c.fetchone()


def uMail(uname):
    dbConn()
    with conn:
        c.execute("SELECT mail FROM users WHERE username =?", (uname,))
        return c.fetchone()


def getPass(uname):
    dbConn()
    with conn:
        c.execute("SELECT pass FROM users where username =?", (uname,))
        return c.fetchone()


def updateMail(uname, newmail):
    dbConn()
    with conn:
        try:
            c.execute("UPDATE users SET mail =? where username =?", (newmail, uname))
            return "db updated"
        except Exception as e:
            return e


# verified status
def vStat(uname):
    dbConn()
    with conn:
        try:
            c.execute("UPDATE users SET v_pass = 1 where username =?", (uname,))
            return "code verified"
        except Exception as e:
            return e


conn.commit()

conn.close()
