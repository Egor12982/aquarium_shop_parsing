# Aquarium_shop_parsing
This project is for parsing latest notifications from the aquarium store.
It will extract  ***product_name, link, topic and date*** of each
product that appeared in the notifications and put them into MySQL DataBase. 
So, using this, you will be up to date about the latest deliveries to the 
store and will always be able to quickly find what you need.

# Before you start
You need add in code some parameters, that I mentioned below.
For example: Add your DB hostname. Find this part of code
it looks like this: 
```
aqua_df = pd.DataFrame(aqua_dict, columns=["product_name", "link", "topic", "date"])
        pd.set_option('display.max_columns', None)
        hostname = "Your hostname here"
```
And, instead of the phrase, add your hostname, it will look like this:
```
aqua_df = pd.DataFrame(aqua_dict, columns=["product_name", "link", "topic", "date"])
        pd.set_option('display.max_columns', None)
        hostname = "root"
```
That's all, just put your credentials instead of phrases.

# Quick start
In order to start, you have to add your personal information to some
of the below-mentioned parameters of the code:
```
headers = {
    "User-Agent": "Your User-Agent here",
}

proxies = {
    'http': 'Your proxy here',
}
```
After adjusting these parameters you need to prepare your DataBase:

1. Make a DataBase named "aquarium_store_news"

2. Create a table named "news" with 4 columns and name them
product_name, link, topic, date. All of them needs to be
not null and two of them, link and date, must be primary keys.

Lastly, add your DB hostname, DB username and DB password here:
```
aqua_df = pd.DataFrame(aqua_dict, columns=["product_name", "link", "topic", "date"])
        pd.set_option('display.max_columns', None)
        hostname = "Your hostname here"
        dbname = "aquarium_store_news"
        uname = "Your username here"
        pwd = "Your password here"
        engine = create_engine(
            "mysql+pymysql://{user}:{pw}@{host}/{db}".format(host=hostname, db=dbname, user=uname, pw=pwd))
        new_info = pd.DataFrame()
```
After all the above-mentioned steps have been completed, the code is
ready to be used.

# Option description:
On the first run you need to choose the answer "y" for the question
"Do you want to load the latest version of site? [y,n]". After the
first run you may use "n" option to work with previous page snapshot.
So, option "y" will change your snapshot to the latest version, option
"n" give you an opportunity to work with previously parsed information.
