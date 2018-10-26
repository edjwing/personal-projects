import sqlite3
from time import strftime, localtime


class DictionaryWord:

    text = None
    fr_article = None
    fr_word = None
    korean = None
    english = None
    mp3_file = None
    mp3_file_slow = None
    etc = None
    date = None

    def set_input_text(self, input_text):
        self.text = str(input_text).strip().lower()
        token = self.text.split()
        print('[analyze_input_text] token =', token)
        self.fr_word = self.text
        if len(token) > 1:
            if token[0] in Constant.article:
                self.fr_article = token[0]
                delimiter = ' '
                self.fr_word = delimiter.join(token[1:])

    def set_from_db_record(self, record):
        self.text = record[0]
        self.fr_article = record[1]
        self.fr_word = record[2]
        self.korean = record[3]
        self.english = record[4]
        self.mp3_file = record[5]
        self.mp3_file_slow = record[6]
        self.etc = record[7]
        self.date = record[8]

    def set_time(self):
        if self.date is None or self.date == '':
            self.date = strftime("%Y-%m-%d %H:%M:%S", localtime())

    def get_record(self):
        result = (self.text, self.fr_article, self.fr_word, self.korean, self.english,
                  self.mp3_file, self.mp3_file_slow, self.etc, self.date)
        return result

    def __str__(self):
        return self.text + '\t' + self.korean + '\t'\
               + self.english + '\t' + self.date


class DictionaryDB:

    table_name = 'dictionary'

    col_french = 'french'
    col_fr_article = 'fr_article'
    col_fr_word = 'fr_word'
    col_korean = 'korean'
    col_english = 'english'
    col_mp3_file = 'mp3_file'
    col_mp3_file_slow = 'mp3_file_slow'
    col_etc = 'etc'
    col_date = 'date'

    conn = None

    def is_db_connected(self):
        if self.conn is not None:
            return True
        else:
            return False

    def connect_db(self, name='mydic_v2.db'):
        self.conn = sqlite3.connect(name)
        cur = self.conn.cursor()
        cmd = 'CREATE TABLE IF NOT EXISTS ' + self.table_name + '(' \
              + self.col_french + ' TEXT, ' + self.col_fr_article + ' TEXT, ' + self.col_fr_word + ' TEXT, '\
              + self.col_korean + ' TEXT, ' + self.col_english + ' TEXT, ' + self.col_mp3_file + ' TEXT, ' \
              + self.col_mp3_file_slow + ' TEXT, ' + self.col_etc + ' TEXT, ' + self.col_date + ' TEXT)'
        print('connect_db =', cmd)
        cur.execute(cmd)
        self.conn.commit()
        cur.close()

    def disconnect_db(self):
        self.conn.commit()
        self.conn.close()

    def read_all(self):
        if self.conn is not None:
            cur = self.conn.cursor()
            cmd = 'SELECT * FROM ' + self.table_name + ' ORDER BY ' + self.col_fr_word
            print('read_all :', cmd)
            cur.execute(cmd)
            if cur is not None:
                result = list()
                for record in cur:
                    print(record)
                    cur_word = DictionaryWord()
                    cur_word.set_from_db_record(record)
                    result.append(cur_word)
                cur.close()
                return result
            else:
                return None
        else:
            return None

    def insert_record(self, record):
        if self.conn is not None:
            cur = self.conn.cursor()
            cmd = 'INSERT INTO ' + self.table_name + '(' \
                  + self.col_french + ', ' + self.col_fr_article + ', ' + self.col_fr_word + ', '\
                  + self.col_korean + ', ' + self.col_english + ', ' + self.col_mp3_file + ', ' \
                  + self.col_mp3_file_slow + ', ' + self.col_etc + ', ' + self.col_date\
                  + ') VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
            print('insert_record :', cmd)
            cur.execute(cmd, record)
            self.conn.commit()
            cur.close()

    def insert_record_by_word(self, dic_word):
        self.insert_record(dic_word.get_record())

    def find_record(self, word):
        if self.conn is not None:
            cur = self.conn.cursor()
            cmd = 'SELECT * FROM ' + self.table_name + ' WHERE ' + self.col_fr_word + ' = \'' + word + '\''
            print('find_record :', cmd)
            cur.execute(cmd)
            for record in cur:
                return record
        else:
            return None


class Constant:
    article = ('un', 'une', 'la', 'le', 'les')
