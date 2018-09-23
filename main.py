#!/usr/bin/env python


from download import Downloader
from fee import Fee
from database import Fund
import database


if __name__ == '__main__':
    dl = Downloader()
    data = dl.get_fee('0P0000YXTA')
    fee = Fee(data)
    fund = Fund(management = fee.management, custodial = fee.custodial,
            distribution = fee.distribution)
    database.session.add(fund)
    database.session.commit()


