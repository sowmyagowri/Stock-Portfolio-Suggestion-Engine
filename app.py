from flask import Flask, render_template, request
from decimal import Decimal
import datetime
import requests, json
import sqlite3

sqlite_file = 'my_first_db.sqlite'    # name of the sqlite database file
table_name = 'portfolio_data'
# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()
# 1) Contents of all columns for row that match a certain value in 1 column
c.execute('SELECT * FROM {tn}'.\
        format(tn=table_name))
all_rows = c.fetchall()
print('1):', all_rows)



app = Flask(__name__)


@app.route('/')
def my_form():
    return render_template('my-form.html')


@app.route('/', methods=['POST'])
def my_form_post():

    API_KEY = 'HXMQHG0ZQVA0PXZJ'
    currentDT = datetime.datetime.now()
    date_today = currentDT.strftime("%Y-%m-%d")
    print("date_today" ,date_today)
    day_today = currentDT.strftime("%A")
    strategy = 'Growth'
    budget = 1000
    #Handled Weeked days(last stock update is on Friday of the week)
    if(day_today == 'Monday'):
        date_yesterday = (currentDT - datetime.timedelta(days = 3)).strftime("%Y-%m-%d")
    else:
        date_yesterday = (currentDT - datetime.timedelta(days = 1)).strftime("%Y-%m-%d")

    symbol = request.form["symbol"]
    allotment = int(request.form["allotment"])
    finalSharePrice = float(request.form["finalSharePrice"])
    commission = float(request.form["commission"])
    initialSharePrice = float(request.form["initialSharePrice"])
    buyCommission = float(request.form["buyCommission"])
    capitalGain = float(request.form["capitalGain"])

    # #Proceeds (Allotment x Final share price)
    # proceeds= allotment*finalSharePrice
    # capitalGain1 = ((finalSharePrice * allotment) - commission) - ((initialSharePrice * allotment) + buyCommission)
    # #Cost
    # cost= (allotment*initialSharePrice+(commission+buyCommission)+(capitalGain/100 )*capitalGain1)
    # net = proceeds - cost
    #
    # #Return on investment (in %), Net Profit / Total Investment * 100.
    # roi = round((net / cost *100),2)
    # breakeven= ((allotment *initialSharePrice) + buyCommission +  commission )/100


    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + symbol +'&apikey=' + API_KEY
    r = requests.get(url)
    stock_data = r.json()

    close_today = float(stock_data["Time Series (Daily)"][date_today]["4. close"])
    close_yesterday = float(stock_data["Time Series (Daily)"][date_yesterday]["4. close"])
    close_change = round((close_today - close_yesterday),4)
    if (close_change > 0):
        sign = '+'
    else:
        sign = ''
    #close_change_per = round((close_change/close_yesterday * 100),4)
    #print(close_today , sign, close_change, '(', sign, close_change_per,'%)')
    c.execute("INSERT INTO `portfolio_data` VALUES(?, ?, ?,?,?,?,?)",
            (2,1001,date_today,strategy,symbol,budget,allotment))
    conn.commit()


    return render_template("result_rucha.html",**locals())


if __name__ == "__main__":
    app.run()
