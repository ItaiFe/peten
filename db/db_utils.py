import cx_Oracle
import config


def do_query(query_string):
    try:
        # create a connection to the Oracle Database
        with cx_Oracle.connect(config.username,
                               config.password,
                               config.dsn) as connection:
            # create a new cursor
            with connection.cursor() as cursor:
                # create a new variable to hold the value of the
                # OUT parameter
                cursor.execute(query_string)
                return cursor.fetchall()
    except cx_Oracle.Error as error:
        print(error)
