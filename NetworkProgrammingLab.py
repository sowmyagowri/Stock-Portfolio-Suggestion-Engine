import urllib, json, pandas as pd, datetime

try:
    while True:

        print("")
        print("Enter the stock symbol:",)
        stock_symbol = raw_input()
        df = pd.read_csv('secwiki_tickers.csv')

        url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + stock_symbol + "&outputsize=full&apikey=4T3YNOER9C4JI9BA"
        response = urllib.urlopen(url)
        data = json.loads(response.read())

        test = df[df.Ticker == stock_symbol]

        if not test.empty:
            print(datetime.datetime.now().strftime("%a %b %d %H:%M:%S PDT %Y"))

            print(list(test.Name.values)[0], '(' + stock_symbol + ')')

            todayRate = data.get('Time Series (Daily)').get(datetime.datetime.now().strftime('%Y-%m-%d')).get('2. high')
            lastRate = data.get('Time Series (Daily)').get(
                (datetime.datetime.now() - datetime.timedelta(days=3)).strftime('%Y-%m-%d')).get('2. high')

            profit = float(todayRate) - float(lastRate)
            if profit > 0:
                profit = '+' + str("{0:.2f}".format(profit))
            else:
                profit = str("{0:.2f}".format(profit))

            per_profit = (float(todayRate) - float(lastRate)) / float(todayRate) * 100
            if per_profit >= 0:
                per_profit = '+' + str("{0:.2f}".format(per_profit))
            else:
                per_profit = str("{0:.2f}".format(per_profit))

            print(todayRate, profit, '(' + per_profit + '%)')

        else:
            print("Invalid symbol")

except Exception:
    print("No internet connection. Kindly establish a secure connection and try again ...")
