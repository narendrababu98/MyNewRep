from sqlalchemy import Column, String, Integer, ForeignKey, Date
from database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    password = Column(String)


class Portfolio(Base):
    __tablename__ = "portfolio"
    id = Column(Integer, primary_key=True, index=True)
    scheme_name = Column(String, nullable=False)
    scheme_code = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    mutual_fund_family = Column(String, nullable=False)
    units = Column(Integer, nullable=False)
    latest_price = Column(Integer, nullable=False)
