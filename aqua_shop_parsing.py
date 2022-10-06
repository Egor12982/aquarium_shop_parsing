import pickle
from bs4 import BeautifulSoup as bs
import re
import cfscrape
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import exc


url = "https://aquapiter.com/"

headers = {
    "User-Agent": "Your User-Agent here",
}

proxies = {
    'http': 'Your proxy here',
}


def save_pickle(o, path):
    with open(path, 'wb') as f:
        pickle.dump(o, f)


def load_pickle(path):
    with open(path, 'rb') as f:
        return pickle.load(f)


def get_site(url, headers, proxies):
    scraper = cfscrape.create_scraper()
    r = scraper.get(url, headers=headers, proxies=proxies)
    print(r)
    path = "fish.rsp"
    save_pickle(r, path)
    return bs(r.text, "html.parser")


def user_answer():
    user = input("Do you want to load the latest version of site? [y,n] ")
    if user == 'y':
        soup = get_site(url, headers, proxies)
    elif user == 'n':
        print("Loading last saved fish.rsp")
    else:
        print("You entered an unexpected answer, please try again.")
        user_answer()
    return


def get_info():
    dated = []
    topic = []
    name = []
    link = []
    l = 0
    counter = 0
    user_answer()
    path = "fish.rsp"
    r = load_pickle(path)
    soup = bs(r.text, "html.parser")
    while True:
        items = soup.find_all('div', attrs={"class": "block block-block block-even region-even clearfix"})
        for p in items:
            pp = p.find_all("p")
            for i in pp:
                one = i.find("span")
                date = one.getText()
                pre_dates = re.search(r'\d{2}.\d{2}.\d{4}', date)
                if pre_dates:
                    dates = datetime.strptime(pre_dates.group(0), '%d.%m.%Y').date()
                    dates = str(dates)
                    # stopper
                    two = i.find_next("span").find_next().find_next()
                    two = str(two)
                    result = re.findall('>.*?<', two)[0]
                    result = result.replace(">", "").replace("<", "")
                    result = result.replace(":", "").replace("-", "")
                    result = result.strip()
                    l = l + 1
                    href = i.find_all("a")
                    for x in href:
                        name.append(x.getText())
                        if "https" in x.attrs["href"]:
                            link.append(x.attrs["href"])
                        else:
                            link.append("https://aquapiter.com" + x.attrs["href"])
                        dated.append(dates)
                        topic.append(result)
                        counter = counter + 1
        aqua_dict = {
            "date": dated,
            "topic": topic,
            "product_name": name,
            "link": link
        }
        aqua_df = pd.DataFrame(aqua_dict, columns=["product_name", "link", "topic", "date"])
        pd.set_option('display.max_columns', None)
        hostname = "Your hostname here"
        dbname = "aquarium_store_news"
        uname = "Your username here"
        pwd = "Your password here"
        engine = create_engine(
            "mysql+pymysql://{user}:{pw}@{host}/{db}".format(host=hostname, db=dbname, user=uname, pw=pwd))
        new_info = pd.DataFrame()
        for i in range(len(aqua_df)):
            try:
                aqua_df.iloc[i:i + 1].to_sql("news", engine, index=False, if_exists='append')
                new_info = new_info.append(aqua_df.iloc[i:i + 1], ignore_index=True)
            except exc.IntegrityError:
                pass
        pd.options.display.expand_frame_repr = False
        if not new_info.empty:
            print('New information added to the database: ')
            print(new_info)
        else:
            print("Data already exists in the database")
        print("Close database successfully")
        return


get_info()
