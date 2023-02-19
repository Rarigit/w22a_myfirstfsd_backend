import mariadb
import dbcreds

def connect_db():
    try: 
        conn=mariadb.connect(
        host =dbcreds.host,
        port=dbcreds.port,
        user=dbcreds.user,
        password=dbcreds.password,
        database=dbcreds.database,
        autocommit=True 
        )
        cursor = conn.cursor()
        return cursor
    except mariadb.OperationalError as e:
        print("Could not connect to the database",e)
    except Exception as e:
        print("Something went very wrong:",e)


def disconnect_db(cursor):
    try:
        conn = cursor.connection
        cursor.close()
        conn.close
    except mariadb.OperationalError as e:
        print("OPERATIONAL ERROR", e)
    except mariadb.InternalError as e:
        print("INTERNAL ERROR:", e)
    except Exception as e:
        print("UNEXPECTED ERROR", e)


def execute_statement(cursor, statement, args=[]):
    try:
        cursor.execute(statement, args)
        result = cursor.fetchall()
        return result
    except mariadb.ProgrammingError as e:
        if "doesn't have a result set" in e.msg:
            return None
        print("Syntax error in your SQL statement:", e)
        return str(e)
    except mariadb.IntegrityError as e:
        print("Statement failed to execute due to integrity error",e)
        return str(e)
    except mariadb.DataError as e:
        print("DATA ERROR", e)
        return str(e)
    except Exception as e:
        print("Unexpected error", e)
        return str(e)

def run_statement(statement : str, args=[]):
    """
    This function expects a valid SQL statement and an optional list of arguments. It connects to the DB,
    executes the statement and closes the connection.
    If the connection to the DB fails, it returns None without running the statement
    
    Args:
        statement (str:) A valid SQL query
        args (list, optional): The list of arguments. Defaults to []

    """
    cursor = connect_db()
    if (cursor == None):
        print("Failed to connect to the DB, statement will not run")
        return None
    result = execute_statement(cursor, statement, args)
    disconnect_db(cursor)
    return result

# dbhelpers is suitable for copy and paste. You can now edit and add as you develop in your career/pursuits