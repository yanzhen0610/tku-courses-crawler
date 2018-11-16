from bs4 import BeautifulSoup as Soup
import re


def parse(page) -> set:
    """
    :param page:
    :return:
    (
        grade,
        control_number,
        course_number,
        trade,
        section,
        class,
        group,
        required_or_selective,
        credits,
        field,
        course_name,
        course_remark,
        enrollment_maximum,
        instructor,
        day_hour_classroom1,
        day_hour_classroom2,
        department,
    )
    """
    try:

        result = set()

        soup = Soup(page, 'html5lib')
        table = soup.select('table')[1]
        department = 'unknown'
        for row in table.select('tr'):
            td = row.select('td')
            if len(td) == 16:
                course_info = (
                    td[1].string.strip(),  # grade
                    td[2].font.string.strip(),  # control_number
                    td[3].string.strip(),  # course_number
                    td[4].string.strip(),  # trade
                    td[5].string.strip(),  # section
                    td[6].string.strip(),  # class
                    td[7].string.strip(),  # group
                    td[8].string.strip(),  # required_or_selective
                    td[9].string.strip(),  # credits
                    td[10].string.strip(),  # field
                    td[11].font.string.strip(),  # course_name
                    td[11].p.contents[2].string.strip(),  # course_remark
                    td[12].string.strip(),  # enrollment_maximum
                    (td[13].a if td[13].a else td[13].p).string.strip(),  # instructor
                    td[14].string.strip(),  # day_hour_classroom1
                    td[15].string.strip(),  # day_hour_classroom2
                    department,  # department
                )
                result.add(course_info)
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
