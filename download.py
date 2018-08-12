#!/usr/bin/env python


import requests
import json
from bs4 import BeautifulSoup
import json
import re


#url = 'https://cn.morningstar.com/quicktake/assetchart.html?key1=11.3,93.61,0,-4.91&key2=10.45,84.51,0,5.04&width=300&height=100'
#url = 'https://cn.morningstar.com/quicktake/sectorchart.html?key1=&key2=&width=190&height=420'
#url = 'https://cn.morningstar.com/handler/home.ashx?q=distributors&randomid=0.5595053435107059'

#output_html = 'test.html'
#output_html = 'test0.html'
#output_html = 'test1.html'

cookies_2 = {'bdshare_firstime': '1451638559248',
             'fp': '001150915704198038',
             'Hm_lvt_eca85e284f8b74d1200a42c9faa85464': '1529129746',
             '__utma': '172984700.2043759916.1514459896.1531391135.1531493518.120',
             '__utmz': '172984700.1514459896.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
             'ASP.NET_SessionId': 'aox31obbjre4o543ik20i2df',
             'Hm_lpvt_eca85e284f8b74d1200a42c9faa85464': '1531493517',
             '__utmc': '172984700',
             'BIGipServercn': '2241287690.20480.0000'}



def download(outputFile, url, cookies = None):
    try:
        if cookies is not None:
            response = requests.get(url, cookies = cookies)
        else:
            response = requests.get(url)
    except Exception as e:
        print("Open url fail: %s" % format(e))
        exit(0)

    if response.status_code != 200:
        print("Status: %d" % response.status_code)
        exit(0)

    #print(response.headers)

    bs = BeautifulSoup(response.content, "lxml")
    #print(bs.prettify())

    with open(outputFile, 'wb') as f:
        f.write(bs.prettify().encode('utf-8', 'ignore'))


class Downloader(object):
    def get_fee(self, fcid):
        try:
            url = 'https://cn.morningstar.com/handler/quicktake.ashx?command=fee&fcid=%s&randomid=0.6564773440355611' % fcid
            headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'
                    }
            #r = requests.get(url, cookies = cookies_2, headers = headers)
            r = requests.get(url, headers = headers)
            #r = requests.get(url)
            if (r.status_code != 200):
                print("Response status code: %d" % r.status_code)
                exit(0)

            return r.json()
        except Exception as e:
            print("Open url fail: %s" % format(e))
            exit(0)


class Fee(object):
    vol_threshold_re_0 = re.compile('([\d.]+)万')
    vol_threshold_re_1 = re.compile('([\d.]+)')
    rate_re_0 = re.compile('([\d.]+)%')
    rate_re_1 = re.compile('([\d.,]+)元')
    span_threshold_re_0 = re.compile('([\d.]+)年')


    def __init__(self, data):
        self.management = float(data["Management"])
        self.custodial = float(data["Custodial"])
        if data["Distribution"] == "":
            self.distributors = 0
        else:
            self.distribution = float(data["Distribution"])
        self.front = {}
        self.__extractFrontOrDefer(data["Front"], self.front)
        self.defer = {}
        self.__extractFrontOrDefer(data["Defer"], self.defer)
        self.__extractRedemption(data["Redemption"])


    def __extractFrontOrDefer(self, data, frontOrDefer = {}):
        if len(data) == 0:
            frontOrDefer[0] = 0
            return

        for item in data:
            threshold, rate = None, None
            m_obj = self.vol_threshold_re_0.search(item["Key"])
            if m_obj:
                threshold = float(m_obj.group(1)) * 10000
            else:
                m_obj = self.vol_threshold_re_1.search(item["Key"])
                if m_obj:
                    threshold = float(m_obj.group(1))

            m_obj = self.rate_re_0.search(item["Value"])
            if m_obj:
                rate = float(m_obj.group(1))
            else:
                m_obj = self.rate_re_1.search(item["Value"])
                if m_obj:
                    continue

            if threshold and rate:
                frontOrDefer[threshold] = rate


    def __extractRedemption(self, data):
        self.redemption = {}

        if len(data) == 0:
            self.redemption[0] = 0
            return

        for item in data:
            threshold, rate = None, None
            m_obj = self.span_threshold_re_0.search(item["Key"])
            if m_obj:
                threshold = float(m_obj.group(1)) * 365
            else:
                raise ValueError("Can't handle %s" % item["Key"])

            m_obj = self.rate_re_0.search(item["Value"])
            if m_obj:
                rate = float(m_obj.group(1))

            if threshold and rate:
                self.redemption[threshold] = rate


if __name__ == '__main__':
    dl = Downloader()
    data = dl.get_fee('0P0000YXTA')
    fee = Fee(data)
    print(fee.front)
    print(fee.defer)
    print(fee.redemption)
    #print(type(fee["Front"]))

#     url_0 = 'https://cn.morningstar.com/quicktake/0P0000YXTA'
    # download('test0.html', url_0)

    # url_2 = 'https://cn.morningstar.com/quicktake/sectorchart.html?key1=0,0,0,0,0,0,0,0,0,0&key2=0,0,0,0,0,0,0,0,0,0&width=190&height=227'
    # cookies_2 = {'bdshare_firstime': '1451638559248',
                 # 'fp': '001150915704198038',
                 # 'Hm_lvt_eca85e284f8b74d1200a42c9faa85464': '1529129746',
                 # '__utma': '172984700.2043759916.1514459896.1531391135.1531493518.120',
                 # '__utmz': '172984700.1514459896.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
                 # 'ASP.NET_SessionId': 'aox31obbjre4o543ik20i2df',
                 # 'Hm_lpvt_eca85e284f8b74d1200a42c9faa85464': '1531493517',
                 # '__utmc': '172984700',
                 # 'BIGipServercn': '2241287690.20480.0000'}
#     download('test2.html', url_2, cookies_2)


