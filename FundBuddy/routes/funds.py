from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from fetch_from_rapid_api import ApiData
from oAuth2 import get_current_user
from database import get_db
from models import Portfolio
from insert_database import connect_push_db
from datetime import datetime

import schemas
import json
import os

fund_router = APIRouter(
    tags=['funds']
)
api_obj = ApiData()


@fund_router.get('/funds_schemes', status_code=status.HTTP_200_OK)
async def get_funds(current_user: schemas.User = Depends(get_current_user)):
    pwd = os.getcwd()
    json_file = os.path.join(pwd, r'data\\funddata.json')
    response = api_obj.get_fund_data()
    fund_data = {}
    if response.status_code == 200:
        api_data = json.loads(response.text)
        with open(json_file, 'w') as file:
            json.dump(api_data, file)
    else:
        with open(json_file, 'r') as file:
            api_data = json.load(file)
    # fund_family=list(dict.fromkeys([data["Mutual_Fund_Family"] for data in api_data]))
    for fund_family in api_data:
        if fund_family["Mutual_Fund_Family"] not in fund_data:
            fund_data[fund_family["Mutual_Fund_Family"]] = []
        if fund_family['Scheme_Type'] == "Open Ended Schemes":
            fund_dict ={}
            for key, value in fund_family.items():
                fund_dict.update({key: value})
            fund_data[fund_family["Mutual_Fund_Family"]].append(fund_dict)
            # fund_dict = {"Scheme_Name": "", "Net_Asset_Value": "", "Date": ""}
            # for key in fund_dict:
            #     fund_dict[key] = fund_family[key]
            # fund_data[fund_family["Mutual_Fund_Family"]].append(fund_dict)
    return fund_data


@fund_router.get('/schemes_portfolio', status_code=status.HTTP_200_OK)
async def get_portfolio(db:Session=Depends(get_db),current_user: schemas.User = Depends(get_current_user)):
    pwd = os.getcwd()
    json_file = os.path.join(pwd, r'data\\portfolio.json')
    database_data = db.query(Portfolio).all()
    if len(database_data) == 0:
        connect_push_db(json_file)
    database_data = [{"Scheme_Code": scheme.scheme_code, "Scheme_Name": scheme.scheme_name,
                       "Date": datetime.strftime(scheme.date, "%Y-%m-%d"),
                       "Mutual_Fund_Family": scheme.mutual_fund_family, "Units": scheme.units,
                       "Latest_Price": scheme.latest_price} for scheme in db.query(Portfolio).all()]
    portfolio_data = {}
    for fund_family in database_data:
        portfolio_dict = {}
        for key, value in fund_family.items():
            if key != "Mutual_Fund_Family":
                portfolio_dict.update({key: value})
        portfolio_data[fund_family["Scheme_Name"]] = {}
        portfolio_data[fund_family["Scheme_Name"]].update(portfolio_dict)
    return portfolio_data
