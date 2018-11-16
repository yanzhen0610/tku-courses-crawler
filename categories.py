import utils
from bs4 import BeautifulSoup as Soup


def get_categories() -> dict:
    def get_page(category=''):
        return utils.http_post('esquery.tku.edu.tw',
                               '/acad/query.asp',
                               {'other': category},
                               False)

    def get_cats(page) -> set:
        categories = set()
        soup = Soup(page, 'html5lib')
        table = soup.select('table')[5]
        second_row = table.select('tr')[1]
        categories_select = second_row.select('select')[0]
        categories_options = categories_select.select('option')
        for option in categories_options:
            categories.add(tuple((
                option['value'],
                option.string,
            )))
        return categories

    def get_programs(page) -> set:
        programs = set()
        soup = Soup(page, 'html5lib')
        table = soup.select('table')[5]
        second_row = table.select('tr')[1]
        programs_select = second_row.select('select')[2]
        programs_options = programs_select.select('option')
        for option in programs_options:
            programs.add(tuple((
                option['value'],
                option.string,
            )))
        return programs

    try:

        result = dict()

        for category in get_cats(get_page()):
            result[category] = None

        for key in result.keys():
            result[key] = get_programs(get_page(key[0]))

        return result

    except Exception as exception:
        print('Seems like the structure of this page has changed [http://esquery.tku.edu.tw/acad/query/result.asp]')
        raise exception


if __name__ == '__main__':
    import pprint
    pprint.PrettyPrinter(indent=4).pprint(get_categories())
