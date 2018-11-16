import utils
from bs4 import BeautifulSoup as Soup


def get_departments() -> dict:
    def get_page(college=''):
        return utils.http_post('esquery.tku.edu.tw',
                               '/acad/query.asp',
                               {'depts': college},
                               False)

    def parse_to_get_colleges(page) -> set:
        colleges = set()
        soup = Soup(page, 'html5lib')
        table = soup.select('table')[5]
        first_row = table.select('tr')[0]
        colleges_select = first_row.select('select')[0]
        colleges_options = colleges_select.select('option')
        for option in colleges_options:
            colleges.add(tuple((
                option['value'],
                option.string,
            )))
        return colleges

    def parse_to_get_departments(page) -> set:
        departments = set()
        soup = Soup(page, 'html5lib')
        table = soup.select('table')[5]
        first_row = table.select('tr')[0]
        departments_select = first_row.select('select')[2]
        departments_options = departments_select.select('option')
        for option in departments_options:
            departments.add(tuple((
                option['value'],
                option.string,
            )))
        return departments

    try:

        result = dict()

        for college in parse_to_get_colleges(get_page()):
            result[college] = None

        for key in result.keys():
            result[key] = parse_to_get_departments(get_page(key[0]))

        return result

    except Exception as exception:
        print('Seems like the structure of this page has changed [http://esquery.tku.edu.tw/acad/query/result.asp]')
        raise exception


if __name__ == '__main__':
    import pprint
    pprint.PrettyPrinter(indent=4).pprint(get_departments())
