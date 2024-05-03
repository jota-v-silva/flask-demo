import logging
import sqlite3
import re

class SQLiteHandler(logging.Handler):
    def __init__(self, db_name, table_name):
        logging.Handler.__init__(self)
        self.db_name = db_name
        self.table_name = table_name
        self.create_table()

    def create_table(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute(f'''
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                messageId INTEGER PRIMARY KEY AUTOINCREMENT,
                time TEXT,
                level TEXT,
                message TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def __format_log(self, record: logging.LogRecord):
        ''' Formats time stamp from werkzeug messages
        '''
        message = record.getMessage()
        pattern = r'\[\d{2}/[A-Za-z]{3}/\d{4} \d{2}:\d{2}:\d{2}\]'
        match = re.search(pattern, message)
        if match:
            t_stamp = match.group(0)[1:-1]
            message = message.replace(f"- - [{t_stamp}] ","")
        else:
            t_stamp = 'empty'

        return t_stamp, message

    def __format_msg(self, record: logging.LogRecord):
        ''' Formats log message from werkzeug messages
        '''
        return record.getMessage()

    def emit(self, record):
        try:
            t_stamp, message = self.__format_log(record)
            print(f'''Level: {record.levelname}, Time: {t_stamp}, Message: {message}''')
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute(f'''
                INSERT INTO {self.table_name} (time, level, message)
                VALUES (?, ?, ?)
            ''', (t_stamp, record.levelname, message))
            conn.commit()
            conn.close()
        except Exception as e:
            print("Error occurred while logging to SQLite:", e)