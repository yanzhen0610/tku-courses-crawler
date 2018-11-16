import http.client
import urllib.parse


def http_post(host, path, kv: dict, https: bool):
    headers = {
        'Host': host,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'close',
    }
    body = urllib.parse.urlencode(kv)
    re_state = False
    re_reason = False
    try:
        C = http.client.HTTPSConnection if https else http.client.HTTPConnection
        connection = C(host, 80, timeout=10)
        connection.request(
            'POST',
            path,
            headers=headers,
            body=body
        )
        with connection.getresponse() as response:
            re_state, re_reason = response.status, response.reason
            print(response.status, response.reason)
            print(response.headers)
            return response.read().decode('utf-8')
    except Exception as exception:
        print('failed to fetch [http://' + host + path + ']')
        if re_state:
            print(re_state)
        if re_reason:
            print(re_reason)
        print('Method:', 'POST')
        print('Headers:', headers)
        print('Body:', body)
        raise exception
