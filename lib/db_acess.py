#! /usr/bin/env python

__author__ = 'andresantos'

import MySQLdb

class DBConnect:

    __instance = None

    @staticmethod
    def instance():
        if DBConnect.__instance is None:
            DBConnect.__instance = DBConnect()
        return DBConnect.__instance

    def open(self, params):
        self.__db = MySQLdb.connect(
            host= params['host'],
            port= params['port'],
            user= params['user'],
            passwd= params['passwd'],
            db= params['db'])
        self.__cursor = self.__db.cursor()

    def query(self, query, args):
        self.__cursor.execute(query, tuple(args))
        return self.__cursor.fetchall()

    def close(self):
        self.__db.close()