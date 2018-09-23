#!/usr/bin/env python


import requests
from bs4 import BeautifulSoup


cookies_2 = {'bdshare_firstime': '1451638559248',
             'fp': '001150915704198038',
             'Hm_lvt_eca85e284f8b74d1200a42c9faa85464': '1529129746',
             '__utma': '172984700.2043759916.1514459896.1531391135.1531493518.120',
             '__utmz': '172984700.1514459896.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
             'ASP.NET_SessionId': 'aox31obbjre4o543ik20i2df',
             'Hm_lpvt_eca85e284f8b74d1200a42c9faa85464': '1531493517',
             '__utmc': '172984700',
             'BIGipServercn': '2241287690.20480.0000'}


class Downloader(object):
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'
            }

    def get_fee(self, fcid):
        try:
            url = 'https://cn.morningstar.com/handler/quicktake.ashx?command=fee&fcid=%s&randomid=0.6564773440355611' % fcid
            r = requests.get(url, headers = self.headers)
            if (r.status_code != 200):
                print("Response status code: %d" % r.status_code)
                exit(0)

            return r.json()
        except Exception as e:
            print("Open url fail: %s" % format(e))
            exit(0)


