import csv
from _datetime import datetime as dt

custormers = list()
products = list()
purch_dates = list()
prices = list()


def get_data_from_file(path: str):
    with open(path) as file:
        file_reader = csv.reader(file, delimiter=";")
        count = 0

        for row in file_reader:
            if count != 0:
                custormers.append(row[0])
                products.append(row[1])
                prices.append(row[2])
                purch_dates.append(dt.strptime(row[3], '%Y-%m-%d %H:%M'))
            else:
                count += 1


def get_stats_for3days(cust: list, prod: list, dates: list, price: list):
    countOfcustPerHour, countOfpurchase, totalProfitPerHour = 0, 0, 0
    totalCust, totalPurch, totalProfit, counterOfTime = list(), list(), list(), list()

    if len(cust) > 1:
        for i in range(0, len(dates) - 1, 1):
            if dates[i].day - dates[0].day < 3:    # ограничение в 3 дня
                if ((dates[i + 1].day == dates[i].day) and (dates[i + 1].hour - dates[i].hour) >= 1 or \
                        (dates[i + 1].day - dates[i].day) == 1 and (dates[i + 1].hour - dates[i].hour + 24) >= 1\
                        or (dates[i + 1].day - dates[i].day) == 2 and (dates[i + 1].hour - dates[i].hour + 24) >= 1):
                    # если уже следующий час

                    countOfcustPerHour += 1
                    countOfpurchase += 1
                    totalProfitPerHour += int(price[i])

                    totalCust.append(countOfcustPerHour)
                    totalPurch.append(countOfpurchase)
                    totalProfit.append(totalProfitPerHour)
                    counterOfTime.append(dates[i])

                    countOfcustPerHour = countOfpurchase = totalProfitPerHour = 0

                elif ((dates[i + 1].day == dates[i].day) and (dates[i + 1].hour - dates[i].hour) < 1 or \
                      (dates[i + 1].day - dates[i].day) == 1 and (dates[i + 1].hour - dates[i].hour + 24) < 1\
                      or (dates[i + 1].day - dates[i].day) == 2 and (dates[i + 1].hour - dates[i].hour + 24) < 1):
                    # если еще тот же час

                    countOfcustPerHour += 1
                    countOfpurchase += 1
                    totalProfitPerHour += int(price[i])

            else:   # завершение цикла, когда начинаеться 4-ый день
                break
        return [totalCust, totalPurch, totalProfit, counterOfTime]

    elif len(cust) == 1:    # если имеем только одно значение
        return [1, 1, int(price[0]), dates[0]]
    else:   # если значений нет
        return "No data!"


def show_stats_for3days(stats: list):
    tmp = stats[3][0]
    print('{:#^100}'.format(' DATE %s.%s.%s ') % (stats[3][0].day, stats[3][0].month, stats[3][0].year), '\n')
    print('Hour ' + '{:*^30}'.format(' Total Customers ') + '{:*^30}'.format(' Total Purchase ') + \
          '{:*^30}'.format(' Total Profit ') + '\n')

    for i in range(0, len(stats[0]), 1):
        if stats[3][i].day > tmp.day:   # смена дня
            print('{:#^100}'.format(' DAY %s.%s.%s ') % (stats[3][i].day, stats[3][i].month, stats[3][i].year), '\n')
            print('Hour ' + '{:*^30}'.format(' Total Customers ') + '{:*^30}'.format(' Total Purchase ') + \
                '{:*^30}'.format(' Total Profit ') + '\n')
            tmp = stats[3][i]

        print('%s' % (stats[3][i].hour) + ' ' + '{: ^30}'.format('%s' % (stats[0][i])) + \
              '{: ^30}'.format('%s' % (stats[1][i])) + '{: ^30}'.format('%s' % (stats[2][i])) + '\n')


get_data_from_file("C:/Users/Lenovo/Desktop/data.csv")
show_stats_for3days(get_stats_for3days(custormers, products, purch_dates, prices))
