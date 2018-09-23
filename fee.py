#!/usr/bin/env python

import re


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
            self.distribution = 0
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
                if threshold in frontOrDefer:
                    threshold += 1
            else:
                m_obj = self.vol_threshold_re_1.search(item["Key"])
                if m_obj:
                    threshold = float(m_obj.group(1))
                    if threshold in frontOrDefer:
                        threshold += 1

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
                if threshold in self.redemption:
                    threshold += 1
            else:
                raise ValueError("Can't handle %s" % item["Key"])

            m_obj = self.rate_re_0.search(item["Value"])
            if m_obj:
                rate = float(m_obj.group(1))

            if threshold and rate:
                self.redemption[threshold] = rate



