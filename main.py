import matplotlib.pyplot as plt
import requests
from datetime import datetime as dt
import json
import statistics as st
import calendar

#function that returns dictionary containing average prices for each month when given an API data containing daily product prices
def get_average_monthly_price(daily, date_key, price_key, comp=False, additional_key=""):
    try:
        if comp:
            iter=json.loads(daily)[additional_key]
        else:
            iter=json.loads(daily)
        monthly = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[], 10:[], 11:[], 12:[]}
        for dailydata in iter:
            date=dt.strptime(dailydata[date_key], "%Y-%m-%d")
            month=date.month
            monthly[month].append(dailydata[price_key])
        average_monthly_price = {i:round(st.mean(monthly[i]),2) for i in range(1,13)}
        return average_monthly_price
    except json.decoder.JSONDecodeError:
        print("Your average monthly price cant be established")

def try_getting_url(url):
    try:
        returnal = requests.get(url).text
        return returnal
    except requests.exceptions.ConnectionError:
        print("There was a problem with internet connection")
        return False
    except requests.exceptions.HTTPError:
        print("There was an HTTP issue with getting your data")
        return False
    except requests.exceptions.URLRequired:
        print(f"Url: {url} given is invalid")
        return False
    except requests.exceptions.TooManyRedirects:
        print("There was too many redirects")
        return False
    except requests.exceptions.InvalidSchema:
        print(f"Url: {url} given is invalid")
        return False

fig, axs = plt.subplots(2,3, figsize=(25,10))

#gold prices from NBP API in years 2021-2022
gold2021daily = try_getting_url("http://api.nbp.pl/api/cenyzlota/2021-01-01/2021-12-31")
gold2022daily = try_getting_url("http://api.nbp.pl/api/cenyzlota/2022-01-01/2022-12-31")
if gold2021daily!=False and gold2022daily!=False:
    gold2021monthly = get_average_monthly_price(gold2021daily, 'data', 'cena')

    axs[0,0].bar(gold2021monthly.keys(), gold2021monthly.values(), color = "#11f3af")
    axs[0,0].set_title("Gold Prices from NBP in months of 2021")
    axs[0,0].set_ylim(int(min(gold2021monthly.values()))-10, int(max(gold2021monthly.values()))+10)
    axs[0,0].set_xticks(range(1,13), [calendar.month_abbr[i] for i in range(1,13)])
    axs[0,0].set_xlabel("Months")
    axs[0,0].set_ylabel("Average monthly 1g gold price in PLN")
    rects = axs[0,0].patches
    for rect, label in zip(rects, gold2021monthly.values()):
        height = rect.get_height()
        axs[0,0].text(rect.get_x() + rect.get_width() / 2, height + 1, label, ha="center", va="bottom")



    gold2022monthly = get_average_monthly_price(gold2022daily, 'data', 'cena')

    axs[0,1].bar(gold2022monthly.keys(), gold2022monthly.values(), color = "#e25372")
    axs[0,1].set_title("Gold Prices from NBP in months of 2022")
    axs[0,1].set_ylim(int(min(gold2022monthly.values()))-10, int(max(gold2022monthly.values()))+10)
    axs[0,1].set_xticks(range(1,13), [calendar.month_abbr[i] for i in range(1,13)])
    axs[0,1].set_xlabel("Months")
    axs[0,1].set_ylabel("Average monthly 1g gold price in PLN")
    rects = axs[0,1].patches
    for rect, label in zip(rects, gold2022monthly.values()):
        height = rect.get_height()
        axs[0,1].text(rect.get_x() + rect.get_width() / 2, height + 1, label, ha="center", va="bottom")


    #extremely simple algorithm that 'predicts' gold prices for next year
    predict_gold_monthly2023 = {i+1:round(2*list(gold2022monthly.values())[i]-list(gold2021monthly.values())[i],2) for i in range(12)}
    axs[0,2].bar(predict_gold_monthly2023.keys(), predict_gold_monthly2023.values(), color = "#ffa500")
    axs[0,2].set_title("Predicted Gold Prices from NBP in months of 2023")
    axs[0,2].set_ylim(int(min(predict_gold_monthly2023.values()))-10, int(max(predict_gold_monthly2023.values()))+10)
    axs[0,2].set_xticks(range(1,13), [calendar.month_abbr[i] for i in range(1,13)])
    axs[0,2].set_xlabel("Months")
    axs[0,2].set_ylabel("Average monthly 1g gold price in PLN")
    rects = axs[0,2].patches
    for rect, label in zip(rects, predict_gold_monthly2023.values()):
        height = rect.get_height()
        axs[0,2].text(rect.get_x() + rect.get_width() / 2, height + 1, label, ha="center", va="bottom")


#usd to pln rates from NDP API years 2021-2022

usd_daily2021 = try_getting_url("http://api.nbp.pl/api/exchangerates/rates/a/usd/2021-01-01/2021-12-31/")
usd_daily2022 = try_getting_url("http://api.nbp.pl/api/exchangerates/rates/a/usd/2022-01-01/2022-12-31/")

if usd_daily2021!=False and usd_daily2022!=False:
    usd_monthly2021 = get_average_monthly_price(usd_daily2021, "effectiveDate", 'mid', comp=True, additional_key='rates')

    axs[1,0].plot(usd_monthly2021.keys(), usd_monthly2021.values(), color = "#800080", lw=5)
    axs[1,0].set_title("USD to PLN prices in months of 2021")
    axs[1,0].set_ylim((min(usd_monthly2021.values()))-0.2, (max(usd_monthly2021.values()))+0.2)
    axs[1,0].set_xticks(range(1,13), [calendar.month_abbr[i] for i in range(1,13)])
    axs[1,0].set_xlabel("Months")
    axs[1,0].set_ylabel("Average USD to PLN price")
    i=1
    for label in usd_monthly2021.values():
        axs[1,0].text(i, label+0.03, label, ha="center", va="bottom")
        i+=1

    usd_monthly2022 = get_average_monthly_price(usd_daily2022, "effectiveDate", 'mid', comp=True, additional_key='rates')

    axs[1,1].plot(usd_monthly2022.keys(), usd_monthly2022.values(), color = "#ffc0cb", lw=5)
    axs[1,1].set_title("USD to PLN prices in months of 2022")
    axs[1,1].set_ylim(min(usd_monthly2022.values())-0.2, max(usd_monthly2022.values())+0.2)
    axs[1,1].set_xticks(range(1,13), [calendar.month_abbr[i] for i in range(1,13)])
    axs[1,1].set_xlabel("Months")
    axs[1,1].set_ylabel("Average USD to PLN price")
    i=1
    for label in usd_monthly2022.values():
        axs[1,1].text(i, label+0.03, label, ha="center", va="bottom")
        i+=1



    #extremely simple algorithm that 'predicts' next year USD to PLN price
    predict_usd_monthly2023 = {i+1:round(2*list(usd_monthly2022.values())[i]-list(usd_monthly2021.values())[i],2) for i in range(12)}
    axs[1,2].plot(predict_usd_monthly2023.keys(), predict_usd_monthly2023.values(), color = "#916782", lw=5)
    axs[1,2].set_title("USD to PLN predicted prices for 2023")
    axs[1,2].set_ylim(min(predict_usd_monthly2023.values())-0.2, max(predict_usd_monthly2023.values())+0.2)
    axs[1,2].set_xticks(range(1,13), [calendar.month_abbr[i] for i in range(1,13)])
    axs[1,2].set_xlabel("Months")
    axs[1,2].set_ylabel("Average USD to PLN price")
    i=1
    for label in predict_usd_monthly2023.values():
        axs[1,2].text(i, label+0.05, label, ha="center", va="bottom")
        i+=1

plt.subplots_adjust(left=0.04,
                    bottom=0.1,
                    right=0.96,
                    top=0.9,
                    wspace=0.1,
                    hspace=0.4)
plt.show()
