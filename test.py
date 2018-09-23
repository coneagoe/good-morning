#!/usr/bin/env python


from download import Downloader
from fee import Fee


if __name__ == '__main__':
    dl = Downloader()
    data = dl.get_fee('0P0000YXTA')
    fee = Fee(data)
    print(fee.front)
    print(fee.defer)
    print(fee.redemption)


