from flask import Flask, render_template, request,flash, redirect, session, abort

from alpha_vantage.timeseries import TimeSeries
import datetime
import requests
import calendar,math
import os

from flask_bootstrap import Bootstrap
flag = False
message=""

app = Flask(__name__);
Bootstrap(app)


@app.route("/")

def home():
    return render_template("stock_portfolio_homepage.html", **locals())

def fetch_graph_results(strategy_name, investment_per_strategy, stock_symbol_array):
    stock_details = []
    five_days_history = []
    investment_per_company = investment_per_strategy / 3

    for stock_symbol in stock_symbol_array:

        ts = TimeSeries(key='OD5NJODCQXKECCKH')
        data, meta_data = ts.get_daily_adjusted(stock_symbol)

        if meta_data:

            count = 0
            for each_entry in data:
                if count < 5:
                    stock_details.append(
                        [strategy_name, stock_symbol, each_entry, data[each_entry]['5. adjusted close']])
                    five_days_history.append(each_entry)
                    count = count + 1
                else:
                    break

    first_day = []

    first_day_company_stocks = []
    second_day_company_stocks = []
    third_day_company_stocks = []
    forth_day_company_stocks = []
    fifth_day_company_stocks = []

    first_day_investment = 0
    second_day_investment = 0
    third_day_investment = 0
    forth_day_investment = 0
    fifth_day_investment = 0

    graph_results = []
    graph_results_detailed = []

    for entry in stock_details:
        if entry[2] == sorted(set(five_days_history))[0]:
            first_day.append([entry[1], entry[3]])
            no_of_stocks_per_company = math.floor(investment_per_company / float(entry[3]))
            first_day_company_stocks.append([entry[1], round(float(entry[3]), 2), no_of_stocks_per_company])
            first_day_investment += no_of_stocks_per_company * float(entry[3])

    graph_results.append([sorted(set(five_days_history))[0], round(first_day_investment, 2)])

    for entry in stock_details:

        if entry[2] == sorted(set(five_days_history))[1]:
            for company in first_day_company_stocks:
                if company[0] == entry[1]:
                    second_day_company_stocks.append([entry[1], round(float(entry[3]), 2), company[2]])
                    second_day_investment += (float(entry[3]) * company[2])

        elif entry[2] == sorted(set(five_days_history))[2]:
            for company in first_day_company_stocks:
                if company[0] == entry[1]:
                    third_day_company_stocks.append([entry[1], round(float(entry[3]), 2), company[2]])
                    third_day_investment += (float(entry[3]) * company[2])

        elif entry[2] == sorted(set(five_days_history))[3]:
            for company in first_day_company_stocks:
                if company[0] == entry[1]:
                    forth_day_company_stocks.append([entry[1], round(float(entry[3]), 2), company[2]])
                    forth_day_investment += (float(entry[3]) * company[2])

        elif entry[2] == sorted(set(five_days_history))[4]:
            for company in first_day_company_stocks:
                if company[0] == entry[1]:
                    fifth_day_company_stocks.append([entry[1], round(float(entry[3]), 2), company[2]])
                    fifth_day_investment += (float(entry[3]) * company[2])

    graph_results.append([sorted(set(five_days_history))[1], round(second_day_investment, 2)])
    graph_results.append([sorted(set(five_days_history))[2], round(third_day_investment, 2)])
    graph_results.append([sorted(set(five_days_history))[3], round(forth_day_investment, 2)])
    graph_results.append([sorted(set(five_days_history))[4], round(fifth_day_investment, 2)])

    graph_results_detailed.append([sorted(set(five_days_history))[0], first_day_company_stocks])
    graph_results_detailed.append([sorted(set(five_days_history))[1], second_day_company_stocks])
    graph_results_detailed.append([sorted(set(five_days_history))[2], third_day_company_stocks])
    graph_results_detailed.append([sorted(set(five_days_history))[3], forth_day_company_stocks])
    graph_results_detailed.append([sorted(set(five_days_history))[4], fifth_day_company_stocks])

    return graph_results, graph_results_detailed


@app.route('/stockportfolio', methods=['POST'])
def addRegion():
    investment_value = request.form['investment_value']
    investment_strategies = request.form.getlist('strategy')
    investment_per_strategy = int(investment_value) / len(investment_strategies)

    print("investment_value", investment_value)
    print("investment_strategies", investment_strategies)

    ethical_stock_symbol_array = ['AAPL', 'MSFT', 'ADBE']
    growth_stock_symbol_array = ['FIT', 'GPRO', 'NVDA']
    index_stock_symbol_array = ['FB', 'AMZN', 'HMC']
    quality_stock_symbol_array = ['JPM', 'WMT', 'BBY']
    value_stock_symbol_array = ['TSLA', 'TWTR', 'GOOG']

    try:

        final_graph_results = []
        final_graph_results_detailed = []

        for strategy in investment_strategies:

            if strategy == 'Ethical Investing':
                print("RESULT for Ethical Investing:")
                graph_results, graph_results_detailed = fetch_graph_results('Ethical Investing', investment_per_strategy, ethical_stock_symbol_array)

                final_graph_results.append(['Ethical Investing', graph_results])
                final_graph_results_detailed.append(['Ethical Investing', graph_results_detailed])

                print("final_graph_results : ", final_graph_results)
                print("final_graph_results_detailed : ", final_graph_results_detailed)
                print("")

            elif strategy == 'Growth Investing':
                print("RESULT for Growth Investing:")
                graph_results, graph_results_detailed = fetch_graph_results('Growth Investing', investment_per_strategy, growth_stock_symbol_array)

                final_graph_results.append(['Growth Investing', graph_results])
                final_graph_results_detailed.append(['Growth Investing', graph_results_detailed])

                print("final_graph_results : ", final_graph_results)
                print("final_graph_results_detailed : ", final_graph_results_detailed)
                print("")

            elif strategy == 'Index Investing':
                print("RESULT for Index Investing:")
                graph_results, graph_results_detailed = fetch_graph_results('Index Investing', investment_per_strategy, index_stock_symbol_array)

                final_graph_results.append(['Index Investing', graph_results])
                final_graph_results_detailed.append(['Index Investing', graph_results_detailed])

                print("final_graph_results : ", final_graph_results)
                print("final_graph_results_detailed : ", final_graph_results_detailed)
                print("")

            elif strategy == 'Quality Investing':
                print("RESULT for Quality Investing:")
                graph_results, graph_results_detailed = fetch_graph_results('Quality Investing', investment_per_strategy, quality_stock_symbol_array)

                final_graph_results.append(['Quality Investing', graph_results])
                final_graph_results_detailed.append(['Quality Investing', graph_results_detailed])

                print("final_graph_results : ", final_graph_results)
                print("final_graph_results_detailed : ", final_graph_results_detailed)
                print("")

            elif strategy == 'Value Investing':
                print("RESULT for Value Investing:")
                graph_results, graph_results_detailed = fetch_graph_results('Value Investing', investment_per_strategy, value_stock_symbol_array)

                final_graph_results.append(['Value Investing', graph_results])
                final_graph_results_detailed.append(['Value Investing', graph_results_detailed])

                print("final_graph_results : ", final_graph_results)
                print("final_graph_results_detailed : ", final_graph_results_detailed)
                print("")

        print("Length test : ", len(final_graph_results), len(final_graph_results_detailed))

        if len(final_graph_results) == 1 and len(final_graph_results_detailed) == 1:
            return render_template("stock_portfolio_results.html", fgr=final_graph_results, pgrd=final_graph_results_detailed)

        elif len(final_graph_results) == 2 and len(final_graph_results_detailed) == 2:
            return render_template("stock_portfolio_results_2.html", fgr=final_graph_results, pgrd=final_graph_results_detailed)
        else:
            print("Select more than 2 strategies")

    except ValueError:
        print('No Symbol found')

    except requests.ConnectionError:
        print('No Connection')

if __name__=='__main__':
    app.secret_key = os.urandom(12)
    # app.run(host='0.0.0.0',debug=True, port=5000)
    # to run on local machine, use the below app.run
    app.run(debug=True, port=3000)