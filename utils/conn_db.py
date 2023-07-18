#!/usr/bin/python
import psycopg2
from utils.config import config

def connect_open():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        #retorna conexão
        return conn


def connect_close(conn):

    try:
        #Encerraconexão com servidor PostgreSQL
        if conn is not None:
            conn.close()
            print('Database connection closed.')

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

