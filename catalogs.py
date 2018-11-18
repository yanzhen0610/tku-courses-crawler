from bs4 import BeautifulSoup as Soup
import re
import itertools
import utils
from contract import RawCourseData


def parse(page) -> set:
    try:

        result = set()

        soup = Soup(page, 'html5lib')
        table = soup.select('table')[-1]
        department = 'unknown'
        for row in table.select('tr'):
            td = row.select('td')
            if len(td) == 16:
                course_info = (
                    td[1].string.strip(),  # grade
                    ''.join(td[2].stripped_strings).strip(),  # control_number
                    td[3].string.strip(),  # course_number
                    td[4].string.strip(),  # trade
                    td[5].string.strip(),  # section
                    td[6].string.strip(),  # class
                    td[7].string.strip(),  # group
                    td[8].string.strip(),  # required_or_selective
                    td[9].string.strip(),  # credits
                    td[10].string.strip(),  # field
                    td[11].font.string.strip(),  # course_name
                    td[11].p.contents[-1].string.strip(),  # course_remark
                    td[12].string.strip(),  # enrollment_maximum
                    ''.join(td[13].p.stripped_strings).strip(),  # instructor
                    tuple(itertools.chain(
                        td[14].stripped_strings,
                        td[15].stripped_strings
                    )),  # day_hour_classroom
                    department,  # department
                )
                result.add(RawCourseData(course_info))
            elif len(td) == 1:
                department = td[0].b.string.strip()
                match = re.search('.*Department.*?([A-za-z0-9]+).', department)
                if match:
                    department = match.group(1)
            elif len(td) == 3 or 15:
                pass
            else:
                print('structure changed?')

        return result

    except Exception as exception:
        print('The structure of the catalogs changed?')
        raise exception


def get_courses_of_week(week: int, period: int) -> str:
    return utils.http_post('esquery.tku.edu.tw',
                           '/acad/query_result.asp',
                           {
                               'func': 'go',
                               'R1': 4,
                               'weekdepts': 'ALL',
                               'weekdept': 'ALL',
                               'week': week,
                               'o1': period,
                               'o2': period,
                               'weekcheck2': 'yes'
                           },
                           False)


def get_courses_of_departments(department) -> str:
    return utils.http_post('esquery.tku.edu.tw',
                           '/acad/query_result.asp',
                           {
                               'func': 'go',
                               'R1': 1,
                               'sgn1': '-',
                               'dept': department,
                               'level': 999,
                           },
                           False)


def get_courses_of_programs(program) -> str:
    return utils.http_post('esquery.tku.edu.tw',
                           '/acad/query_result.asp',
                           {
                               'func': 'go',
                               'R1': 5,
                               'sgn2': '-',
                               'others': program,
                           },
                           False)
