import sqlite3
from contract import RawCourseData


class Database:
    RAW_COURSE_DATA_TABLE = 'raw_course_data'

    def __init__(self, path):
        self.__path = path

    def __enter__(self):
        self.__connection = sqlite3.connect(self.__path)
        self.__connection.execute(
            '''
            CREATE TABLE IF NOT EXISTS {table_name}
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                grade TEXT,
                control_number TEXT,
                course_number TEXT,
                trade TEXT,
                section TEXT,
                class_ TEXT,
                group_ TEXT,
                required_or_selective TEXT,
                credits TEXT,
                field TEXT,
                course_name TEXT,
                course_remark TEXT,
                enrollment_maximum TEXT,
                instructor TEXT,
                day_hour_classroom TEXT,
                department TEXT
            );
            '''.format(
                table_name=Database.RAW_COURSE_DATA_TABLE
            ))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__connection.commit()
        self.__connection.close()

    def insert_raw_course_data(self, row: RawCourseData):
        query = '''
        INSERT INTO {table_name}
        (
            grade,
            control_number,
            course_number,
            trade,
            section,
            class_,
            group_,
            required_or_selective,
            credits,
            field,
            course_name,
            course_remark,
            enrollment_maximum,
            instructor,
            day_hour_classroom,
            department
        )
        VALUES
        (
            {0},
            {1},
            {2},
            {3},
            {4},
            {5},
            {6},
            {7},
            {8},
            {9},
            {10},
            {11},
            {12},
            {13},
            {14},
            {15}
        );
        '''.format(
            *(repr(str(col)) for col in row.data),
            table_name=Database.RAW_COURSE_DATA_TABLE
        )
        print(query)
        self.__connection.execute(query)

    def insert_raw_courses_data(self, data: iter):
        for row in data:
            self.insert_raw_course_data(row)

    def commit(self):
        self.__connection.commit()
        
    def get_connection(self):
        return self.__connection
