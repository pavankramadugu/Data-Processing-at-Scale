#!/usr/bin/python2.7

import psycopg2
import os
import sys

output_range_file = 'RangeQueryOut.txt'
output_point_file = 'PointQueryOut.txt'


def RangeQuery(ratingsTableName, ratingMinValue, ratingMaxValue, openconnection):
    if ratingMinValue < 0.0 or ratingMaxValue > 5.0:
        return

    output_list = []

    with openconnection.cursor() as cursor:
        select_query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
        cursor.execute(select_query)
        tables = cursor.fetchall()

        for table in tables:
            if not (table[0] == 'rangeratingsmetadata' or table[0] == 'roundrobinratingsmetadata'):
                select_query = "SELECT * FROM {} WHERE Rating >= {} AND Rating <= {}".format(table[0],
                                                                                             ratingMinValue,
                                                                                             ratingMaxValue)
                cursor.execute(select_query)
                ratings = cursor.fetchall()

                for rating in ratings:
                    row = "{},{},{},{}".format(table[0], rating[0], rating[1], rating[2])
                    output_list.append(row)

        writeToFile(output_range_file, output_list)
        cursor.close()


def PointQuery(ratingsTableName, ratingValue, openconnection):
    if ratingValue > 5.0 or ratingValue < 0.0:
        return

    output_list = []

    with openconnection.cursor() as cursor:
        select_query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
        cursor.execute(select_query)
        tables = cursor.fetchall()

        for table in tables:
            if not (table[0] == 'rangeratingsmetadata' or table[0] == 'roundrobinratingsmetadata'):
                select_query = "SELECT * FROM {} WHERE Rating = {}".format(table[0], ratingValue)
                cursor.execute(select_query)
                ratings = cursor.fetchall()

                for rating in ratings:
                    newRow = "{},{},{},{}".format(table[0], rating[0], rating[1], rating[2])
                    output_list.append(newRow)
        writeToFile(output_point_file, output_list)
        cursor.close()


def writeToFile(filename, rows):
    f = open(filename, 'w')
    for line in rows:
        f.write(line)
        f.write('\n')
    f.close()
