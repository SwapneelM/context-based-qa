from datetime import datetime

class Sector:

    def __init__(self, name):
        self.name = name
        self.companies = list()
        self.rising = list()
        self.falling = list()
        self.news = list()
        self.highest_price = None
        self.lowest_price = None

    def add_company(self, company):
        self.companies.append(company)
        if "+" in company.stock.per_diff:
            self.rising.append(company)
            self.rising.sort(key=lambda x: float(x.stock.per_diff[1:]), reverse=True)
        else:
            self.falling.append(company)
            self.falling.sort(key=lambda x: float(x.stock.per_diff[1:]), reverse=True)
        for n in company.news:
            self.news.append(n)
        self.news.sort(key=lambda x: datetime.strptime(x.date, '%H:%M %d-%b-%Y'), reverse=True) #latest article first
        if self.highest_price == None:
            self.highest_price = company
        else:
            if float(company.stock.price.replace(",","")) > float(self.highest_price.stock.price.replace(",","")):
                self.highest_price = company
        if self.lowest_price == None:
            self.lowest_price = company
        else:
            if float(company.stock.price.replace(",","")) < float(self.lowest_price.stock.price.replace(",","")):
                self.lowest_price = company