import psycopg2
from psycopg2 import pool

try:

    postgreSQL_pool = psycopg2.pool.SimpleConnectionPool(1, 20,user = "postgres",
                                                password = "1234",
                                                host = "localhost",
                                                database = "sea_ice")

    if(postgreSQL_pool):
        print("Connection pool created successfully")
    
    ice_connection = postgreSQL_pool.getconn()

    if(ice_connection):
        print("successfully recived connection from connection pool ")
        ice_cursor = ice_connection.cursor()
        ice_cursor.execute("select * from masie")
        ice_data = ice_cursor.fetchall()
        ice_cursor.close()

        print("Put away a PostgreSQL connection")
        postgreSQL_pool.putconn(ice_connection)

except (Exception, psycopg2.DatabaseError) as error :
    print ("Error while connecting to PostgreSQL", error)

finally:
    #closing database connection.
    # use closeall method to close all the active connection if you want to turn of the application
    if (postgreSQL_pool):
        postgreSQL_pool.closeall
    print("PostgreSQL connection pool is closed")