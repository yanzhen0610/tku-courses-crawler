import catalogs
import departments
import categories
from database import Database


if __name__ == '__main__':
    with Database('courses.db') as db:
        db.drop_and_create_raw_course_data_table()
        courses = set()

        for i in range(7):
            for j in range(14):
                print((i + 1, j + 1))
                data = catalogs.get_courses_of_week(i + 1, j + 1)
                parsed_data = catalogs.parse(data)
                courses.update(parsed_data)

        departs = departments.get_departments()
        for college in departs.values():
            for department in college:
                print(department)
                data = catalogs.get_courses_of_departments(department[0])
                parsed_data = catalogs.parse(data)
                courses.update(parsed_data)

        cats = categories.get_categories()
        for programs in cats.values():
            for program in programs:
                print(program)
                data = catalogs.get_courses_of_programs(program[0])
                parsed_data = catalogs.parse(data)
                courses.update(parsed_data)

        print('found', len(courses), 'courses')
        db.insert_raw_courses_data(courses)
