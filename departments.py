import http.client
import urllib.parse
from bs4 import BeautifulSoup as Soup


def get_departments() -> dict:
    def get_page(college=''):
        headers = {
            'Host': 'esquery.tku.edu.tw',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'close',
        }
        body = urllib.parse.urlencode({
            'depts': college,
        })
        re_state = False
        re_reason = False
        try:
            connection = http.client.HTTPConnection('esquery.tku.edu.tw', 80, timeout=10)
            connection.request(
                'POST',
                '/acad/query.asp',
                headers=headers,
                body=body
            )
            with connection.getresponse() as response:
                re_state, re_reason = response.status, response.reason
                print(response.status, response.reason)
                print(response.headers)
                return response.read().decode('utf-8')
        except Exception as exception:
            print('failed to fetch [http://esquery.tku.edu.tw:80/acad/query/result.asp]')
            if re_state:
                print(re_state)
            if re_reason:
                print(re_reason)
            print('Method:', 'POST')
            print('Headers:', headers)
            print('Body:', body)
            raise exception

    def get_colleges(page) -> set:
        colleges = set()
        first = Soup(page, 'html5lib')
        table = first.select('table')[5]
        first_row = table.select('tr')[0]
        colleges_select = first_row.select('select')[0]
        colleges_options = colleges_select.select('option')
        for option in colleges_options:
            colleges.add(tuple((
                option['value'],
                option.string,
            )))
        return colleges

    def get_departs(page) -> set:
        departments = set()
        first = Soup(page, 'html5lib')
        table = first.select('table')[5]
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

        for college in get_colleges(get_page()):
            result[college] = None

        for key in result.keys():
            result[key] = get_departs(get_page(key[0]))

        return result

    except Exception as exception:
        print('Seems like the structure of this page has changed [http://esquery.tku.edu.tw/acad/query/result.asp]')
        raise exception


if __name__ == '__main__':
    print(get_departments())
