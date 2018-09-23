#!/usr/bin/env python


from sqlalchemy import create_engine, Column, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session


engine = create_engine('mysql+mysqlconnector://fund:1234@localhost/fund')
Base = declarative_base()


class Fund(Base):
    __tablename__ = 'fund'
    id = Column(String, primary_key = True)
    fcid = Column(String)
    name = Column(String)
    management = Column(Float)
    custodial = Column(Float)
    distribution = Column(Float)

    def __repr__(self):
        return "id = %s\n" \
               "fcid = %s\n" \
               "name = %s\n" \
               "管理费 = %f%\n" \
               "托管费 = %f% \n" \
               "销售服务费 = %f% \n" \
                % (self.id,
                   self.fcid,
                   self.name,
                   self.management,
                   self.custodial,
                   self.distribution)


class Front(Base):
    __tablename__ = 'front'
    id = Column(Integer, primary_key = True)
    fund_id = Column(String) # Fund.id
    vol_threshold = Column(Float)
    rate = Column(Float)


class Defer(Base):
    __tablename__ = 'defer'
    id = Column(Integer, primary_key = True)
    fund_id = Column(String) # Fund.id
    vol_threshold = Column(Float)
    rate = Column(Float)


class Redemption(Base):
    __tablename__ = 'redemption'
    id = Column(Integer, primary_key = True)
    fund_id = Column(String) # Fund.id
    span_threshold = Column(Float)
    rate = Column(Float)


session = Session(bind = engine)
