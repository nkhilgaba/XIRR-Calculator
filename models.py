import quandl
import datetime
import pandas as pd

from formulae import xirr

quandl.ApiConfig.api_key = "#PutYourQuandlAPIKeyHere#"

class FundRequest:

    def __init__(self, scode, startDate, endDate, sipAmount):
        self.qcode = 'AMFI/' + scode
        self.startDate = startDate
        self.endDate = endDate
        self.sipAmount = sipAmount
        self.fundName = quandl.Dataset(self.qcode).name

        self.create_date_nav_df()
        self.add_quantity_to_df()


    xirr = None
    df = None
    totalQuantity = 0 


    def get_sip_dates(self):
        day = self.startDate.day
        month = self.startDate.month
        year = self.startDate.year
        
        dates = []
        
        dates.append(self.startDate)
        
        date = self.startDate
        
        while date < self.endDate:
            if month == 12:
                year += 1

            month = month  % 12 + 1
            
            try:
                nextDate = datetime.date(year, month, day)
            except:
                nextDate = datetime.date(year,month+1,1)

            dates.append(nextDate)
            date = nextDate
        
        return dates



    def get_nav_df(self, date):
        if date < datetime.date.today():
            res = quandl.get(self.qcode, start_date=date, end_date=date)
            if res.empty:
                incDate = date + datetime.timedelta(days = 1)
                return self.get_nav_df(incDate)
            return res
        
        else:
            print("I can't predict future!")



    def create_date_nav_df(self):
        sipDates = self.get_sip_dates()
        if sipDates:
        
            dfList = []

            for tentativeDate in sipDates:
                ls = []

                navDf = self.get_nav_df(tentativeDate)
                actualDateTimeStamp = navDf['Net Asset Value'].index[0]
                
                actualDate = datetime.date(actualDateTimeStamp.year, actualDateTimeStamp.month, actualDateTimeStamp.day)
                ls.append(actualDate)
            
                nav = float(navDf['Net Asset Value'][0])
                ls.append(nav)

                dfList.append(ls)


            df = pd.DataFrame(dfList, columns = ['Date', 'NAV'])
            df = df.set_index('Date')

            self.df = df
            return df

        else:
            print('Error!')



    def add_quantity_to_df(self):
        modDf = self.df
        modDf['Quantity'] = float(self.sipAmount) / modDf['NAV']
        modDf['Quantity'] = modDf['Quantity'].round(decimals=4)
        modDf['Cash-Flow'] = - self.sipAmount
        print(modDf)
        self.df = modDf
        return modDf



    def add_lump_sum(self, date, amount):
        df = self.df

        navDf = self.get_nav_df(date)
        if not navDf.empty:
            dateTimeStamp = navDf['Net Asset Value'].index[0]
            actualDate = datetime.date(dateTimeStamp.year, dateTimeStamp.month, dateTimeStamp.day)
            nav = float(navDf['Net Asset Value'][0])
            quantity = round(float(amount) / nav, 4)

            row = pd.Series({'NAV':nav, 'Cash-Flow':-amount, 'Quantity':quantity},name=actualDate)

            df = df.append(row)

            self.df = df
            return df
        
        else:
            print('Error: Check the dates!')



    def get_latest_nav_df(self, date):
        if date <= datetime.date.today():
    #         print(date)
            res = quandl.get(self.qcode, start_date=date, end_date=date)
            if res.empty:
                decDate = date - datetime.timedelta(days = 1)
                return self.get_latest_nav_df(decDate)
            return res




    def calculate_xirr(self):
        df = self.df
        df.sort_index(inplace=True)

        quantitySum = float(df['Quantity'].sum())
        self.totalQuantity = round(quantitySum, 4)

        latestNAVdf = self.get_latest_nav_df(datetime.date.today())
        latestNAV = float(latestNAVdf['Net Asset Value'][0])
        latestDateTimestamp = latestNAVdf['Net Asset Value'].index[0]
        latestDate = datetime.date(latestDateTimestamp.year, latestDateTimestamp.month, latestDateTimestamp.day)

        
        redemptionAmount = round(quantitySum * latestNAV, 4)

        row = pd.Series({'NAV':latestNAV,'Cash-Flow':redemptionAmount},name=latestDate)
        df = df.append(row)
        row = pd.Series({'Quantity':quantitySum},name='Total')
        df = df.append(row)
        
    #     print(df)
        
        dateList = list(df.index[:-1])
        cashFlowList = list(df['Cash-Flow'][:-1])
        dateAndCashFlowList = list(zip(dateList, cashFlowList))

        xirrValue = float(xirr(dateAndCashFlowList) * 100)
        xirrValue = round(xirrValue, 2)  
        xirrValue = str(xirrValue) + ' %'
        row = pd.Series({'Cash-Flow':xirrValue},name='XIRR')
        df = df.append(row)
        
        self.df = df
        self.xirr = xirrValue
        return xirrValue




























