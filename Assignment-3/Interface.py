#!/usr/bin/python2.7
#
# Interface for the assignement
#

import psycopg2
import math


def getopenConnection(user='postgres', password='1234', dbname='postgres'):
    return psycopg2.connect("dbname='" + dbname + "' user='" + user + "' host='localhost' password='" + password + "'")


def loadRatings(ratingstablename, ratingsfilepath, openconnection):
    cursor = openconnection.cursor()
    drop_query = "DROP TABLE IF EXISTS {}".format(ratingstablename)
    create_query = ''' CREATE TABLE {} (
        userid INT NOT NULL,
        movieid INT,
        rating NUMERIC(2,1),
        PRIMARY KEY(userid, movieid, rating))'''.format(ratingstablename)
    cursor.execute(drop_query)
    cursor.execute(create_query)
    ratings_file = open(ratingsfilepath, "r")
    data = ratings_file.readlines()
    i = 0
    for l in data:
        params = l.split("::")
        if i == 20:
            break
        insert_query = "INSERT INTO " + ratingstablename + "(userid, movieid, rating) VALUES ({}, {}, {})".format(
            str(params[0]), str(params[1]), str(params[2]))
        cursor.execute(insert_query)
        i += 1

    ratings_file.close()
    cursor.close()


def rangePartition(ratingstablename, numberofpartitions, openconnection):
    cursor = openconnection.cursor()
    rule = float(5.0 / numberofpartitions)

    for i in range(0, numberofpartitions):
        drop_query = "DROP TABLE IF EXISTS range_part{};".format(str(i))
        cursor.execute(drop_query)
        flag = float(i)

        if i == 0:
            create_query = "CREATE TABLE range_part{} AS SELECT * FROM {} WHERE Rating >= {} AND Rating <= {} ;".format(
                str(i), ratingstablename, str(flag * rule), str((flag + 1) * rule))
            cursor.execute(create_query)
        else:
            create_query = "CREATE TABLE range_part{} AS SELECT * FROM {} WHERE Rating > {} AND Rating <= {} ;".format(
                str(i), ratingstablename, str(flag * rule), str((flag + 1) * rule))
            cursor.execute(create_query)

    cursor.close()


def roundRobinPartition(ratingstablename, numberofpartitions, openconnection):
    if math.floor(numberofpartitions) != math.ceil(numberofpartitions):
        return
    if numberofpartitions <= 0:
        return
    partition_list = []
    cursor = openconnection.cursor()
    for i in range(0, numberofpartitions):
        partition_list.append(('rrobin_part' + str(i)))
    for i in range(0, numberofpartitions):
        cursor.execute("Create table " + partition_list[i] + " (userid INT, movieid INT, rating REAL)")
        openconnection.commit()
        if i == numberofpartitions - 1:
            cursor.execute("insert into " + partition_list[
                i] + " select userid, movieid, rating from (select row_number() over() as row_id, * from " + ratingstablename + ") as imp where row_id%" + str(
                numberofpartitions) + "=" + str(0))
            openconnection.commit()
        else:
            cursor.execute("insert into " + partition_list[
                i] + " select userid, movieid, rating from (select row_number() over() as row_id, * from " + ratingstablename + ") as imp where row_id%" + str(
                numberofpartitions) + "=" + str(i + 1))
            openconnection.commit()
    cursor.close()


def roundrobininsert(ratingstablename, userid, itemid, rating, openconnection):
    cursor = openconnection.cursor()
    if rating < 0 or rating > 5:
        return
    cursor.execute(
        "SELECT count(*) FROM (SELECT tablename FROM pg_catalog.pg_tables where tablename like 'rrobin_part%') AS temp")
    partition_count = int(cursor.fetchone()[0])
    cursor.execute('SELECT COUNT(*) FROM {}'.format(ratingstablename))
    count = int(cursor.fetchone()[0])
    statement = 'rrobin_part' + str((count % partition_count))
    insert_query1 = "INSERT INTO " + ratingstablename + " (userid,movieid,rating) values (" + str(userid) + "," + str(
        itemid) + "," + str(rating) + ")"
    cursor.execute(insert_query1)
    insert_query2 = "INSERT INTO " + statement + " (userid,movieid,rating) values (" + str(userid) + "," + str(
        itemid) + "," + str(rating) + ")"
    cursor.execute(insert_query2)
    cursor.close()


def rangeinsert(ratingstablename, userid, itemid, rating, openconnection):
    cursor = openconnection.cursor()
    low = partition_count = 0
    high = 1.0

    while low < 5.0:
        if low == 0:
            if low <= rating <= high:
                break
        else:
            if low < rating <= high:
                break

        partition_count = partition_count + 1
        low = low + 1.0
        high = high + 1.0

    insert_query = "INSERT INTO range_part{} (userid, movieid, rating) VALUES ({}, {}, {})".format(
        partition_count, userid, itemid, rating)
    cursor.execute(insert_query)
    cursor.close()

def createDB(dbname='dds_assignment'):
    """
    We create a DB by connecting to the default user and database of Postgres
    The function first checks if an existing database exists for a given name, else creates it.
    :return:None
    """
    # Connect to the default database
    con = getopenConnection(dbname='postgres')
    con.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()

    # Check if an existing database with the same name exists
    cur.execute('SELECT COUNT(*) FROM pg_catalog.pg_database WHERE datname=\'%s\'' % (dbname,))
    count = cur.fetchone()[0]
    if count == 0:
        cur.execute('CREATE DATABASE %s' % (dbname,))  # Create the database
    else:
        print
        'A database named {0} already exists'.format(dbname)

    # Clean up
    cur.close()
    con.close()


def deletepartitionsandexit(openconnection):
    cur = openconnection.cursor()
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    l = []
    for row in cur:
        l.append(row[0])
    for tablename in l:
        cur.execute("drop table if exists {0} CASCADE".format(tablename))

    cur.close()


def deleteTables(ratingstablename, openconnection):
    try:
        cursor = openconnection.cursor()
        if ratingstablename.upper() == 'ALL':
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
            tables = cursor.fetchall()
            for table_name in tables:
                cursor.execute('DROP TABLE %s CASCADE' % (table_name[0]))
        else:
            cursor.execute('DROP TABLE %s CASCADE' % (ratingstablename))
        openconnection.commit()
    except psycopg2.DatabaseError, e:
        if openconnection:
            openconnection.rollback()
        print
        'Error %s' % e
    except IOError, e:
        if openconnection:
            openconnection.rollback()
        print
        'Error %s' % e
    finally:
        if cursor:
            cursor.close()
