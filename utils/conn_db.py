#!/usr/bin/python
import psycopg2
from utils.config import config


def connect_open():
    """Connect to the PostgreSQL database server"""
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        # print("Connecting to the PostgreSQL database...")
        conn = psycopg2.connect(**params)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        # retorna conexão
        return conn


def connect_close(conn):
    try:
        # Encerraconexão com servidor PostgreSQL
        if conn is not None:
            conn.close()
            # print("Database connection closed.")

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


# Função para executar querys
def execute_query(conn, query):
    """Execute a single query"""
    ret = None
    try:
        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute(query)

        # Execute query
        ret = cur.fetchall()

        # close the communication with the PostgreSQL
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        # retorna conexão
        return ret


# funcao para inserir registros em uma tabela do banco
def insert_table(conn, table, columns, values):
    """insert a new vendor into the vendors table"""
    ret = None
    try:
        # create a cursor
        cur = conn.cursor()

        # validate if columns parameter is a list and return exceptio if not
        if not isinstance(columns, list):
            raise Exception("Columns parameter must be a list")

        # validate if values parameter is a list and return exceptio if not
        if not isinstance(values, list):
            raise Exception("Columns parameter must be a list")

        columns = (
            str(columns).replace("[", "").replace("]", "").replace("'", "")
        )
        values = (
            str(values).replace("[", "").replace("]", "").replace('"', "'")
        )

        # print(
        #     "INSERT INTO "
        #     + table
        #     + " ("
        #     + columns
        #     + ") VALUES ("
        #     + values
        #     + ") ;"
        # )

        # execute a statement
        cur.execute(
            "INSERT INTO "
            + table
            + " ("
            + columns
            + ") VALUES ("
            + values
            + ") ;"
        )

        # display the PostgreSQL database server version
        ret = cur.fetchone()[0]

        # commit the changes to the database
        conn.commit()

        # close communication with the database
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        # retorna conexão
        return ret
