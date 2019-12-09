#Packages
import requests
import json
import plotly.graph_objects as go
import sqlite3
import os.path
import chardet
import unittest
import secrets_final
from secrets_final import API_key
from secrets_final import STORIES_API

print("What places do you want to search for? Example: Chicago/Detroit/Ann Arbor")
user_loc=input()

print("What term do you want to search? (Example: food, restaurant, Starbucks)")
user_term=input()

print("What pricing level do you wish to see? (You can pick from 1-4. 1 is the least expensive, and 4 is the most expensive)")
user_price=input()

print("How many results do you want to see? Please enter an integer from 1-50.")
user_num=input()


#######Part 1 starts here
CACHE_FNAME="Yelp.json"

try:
    cache_file=open(CACHE_FNAME,"r")
    cache_contents=cache_file.read()
    CACHE_DICTION=json.loads(cache_contents)
    cache_file.close()

except:
    CACHE_DICTION={}

# A helper function that accepts 2 parameters
# and returns a string that uniquely represents the request
# that could be made with this info (url + params)
def params_unique_combination(url, params):
    try:
        alphabetized_keys = sorted(params.keys())
        res = []
        for k in alphabetized_keys:
            res.append("{}-{}".format(k, params[k]))
        return url + "_" + "_".join(res)
    except:
        return url


def make_request_using_cache(url,params,headers):
    unique_ident=params_unique_combination(url, params)

    ## first, look in the cache to see if we already have this data
    if unique_ident in CACHE_DICTION:
        # print("Getting cached data...")
        #CACHE_DICTION[unique_ident]=json.loads(CACHE_DICTION[unique_ident])
        return CACHE_DICTION[unique_ident]

    ## if not, fetch the data afresh, add it to the cache,
    ## then write the cache to file
    else:
        # print("Making a request for new data...")
        # Make the request and cache the new data
        resp = requests.get(url, params, headers=headers)
        CACHE_DICTION[unique_ident] = json.loads(resp.text)
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]


baseurl="https://api.yelp.com/v3/businesses/search"
#API_KEY="KxSDI47u9kJNQeQwecvs0TcH1nxS8miCUp4kUKn1MtqkuE0aopqwaw8q4SA2L49Mj9D9izPp6YUfZ8jIQRl04GJzaBGc7eGjHUczdzEyep_KKX0D1ysFeDEO-PXnXXYx"

class Yelp_result(object):
    def __init__(self, name=None, rating=None, review_count=None, address=None, zip_code=None, url=None, json_dict=None):
        if json_dict is None:
            self.name=name
            self.rating=rating
            self.review_count=review_count
            self.address=address
            self.zip_code=zip_code
            self.url=url
        else:
            self.process_json_dict(json_dict)

            
    def process_json_dict(self, json_dict):
        self.name=json_dict["name"]
        self.rating=json_dict["rating"]
        self.review_count=json_dict["review_count"]
        self.address=json_dict["location"]["address1"]
        self.zip_code=json_dict["location"]["zip_code"]
        self.url=json_dict["url"]
        
    def __str__(self):
        info = "{} is located in {}. (Zip code: {}) Based on {} number of reviews, rating is {}. For more info, please go to {}".format(self.name,self.address,self.zip_code,self.review_count,self.rating,self.url)
        return info
        
if user_loc==" " or user_loc=="":
    print("No results were entered")

if user_loc != "exit":
    diction_of_params={}
    diction_of_params["location"]=user_loc
    diction_of_params["term"]=user_term
    diction_of_params["price"]=user_price
    diction_of_params["limit"]=user_num
    headers={"Authorization":"Bearer KxSDI47u9kJNQeQwecvs0TcH1nxS8miCUp4kUKn1MtqkuE0aopqwaw8q4SA2L49Mj9D9izPp6YUfZ8jIQRl04GJzaBGc7eGjHUczdzEyep_KKX0D1ysFeDEO-PXnXXYx"}
    response=make_request_using_cache(baseurl,params=diction_of_params,headers=headers)
    results=response["businesses"]
    #print(results)
    all_names=[]
    all_ratings=[]
    all_alt=[]
    all_lon=[]
    for info in results:
        all_names.append(info["name"])
        all_ratings.append(info["rating"])
        all_alt.append(info["coordinates"]["latitude"])
        all_lon.append(info["coordinates"]["longitude"])
    num=1
    for info in results:
        complete_info=Yelp_result(json_dict=info)
        print("["+str(num)+"]",complete_info)
        num=num+1
else:
    pass
        
#print(all_alt)
#print(all_lon)

#Google API KEY
print("Want to know more about the location of a place? Please enter an integer. Do not enter an integer out of the range!")
user_dec=input()

#API_key="AIzaSyDWrFMiyV5QLyrsARx2s9d6npdBNgzA97Y"
find_places_url="https://maps.googleapis.com/maps/api/place/findplacefromtext/json?"
NEW_CACHE="Google.json"


if user_dec== " " or "":
    print("No results were entered")

if user_dec != 'exit':
    try:
        dict_places={}
        posit=int(user_dec)-1
        search_name=all_names[posit]
        dict_places["input"]=search_name
        dict_places["inputtype"]="textquery"
        dict_places["fields"]="geometry"
        dict_places["key"]=API_key
        resp_places=requests.get(url=find_places_url, params=dict_places)
        resp=resp_places.json()
        json_content=json.loads(resp_places.text)
        dumped_json_cache = json.dumps(json_content)
        f_w = open(NEW_CACHE,"w")
        f_w.write(dumped_json_cache)
        f_w.close()
        
        
    except:
        print("You did not enter an integer or the number you put in is out of range")
else:
    pass

##New York Times
class Stories_result(object):
    def __init__(self, title=None,author=None,created_date=None,updated_date=None,published_date=None, json_dict=None):
        if json_dict is None:
            self.title=title
            self.author=author
            self.created_date=created_date
            self.updated_date=updated_date
            self.published_date=published_date
        else:
            self.process_json(json_dict)

    def process_json(self,json_dict):
        self.title=json_dict["title"]
        name=json_dict["byline"]
        try:
            self.author=name[-2]+" "+name[-1]
        except:
            self.author="Missing"
        self.updated_date=json_dict["updated_date"]
        self.created_date=json_dict["created_date"]
        self.published_date=json_dict["published_date"]
    def __str__(self):
        info="{} is written by {} and published on {}".format(self.title,self.author,self.published_date)
        return info

all_categories=["automobiles", "books", "business", "fashion", "food"]
#STORIES_API="oT846e8NF7dEEoVHojsDftSXfHrtvVFu"
stories_url="https://api.nytimes.com/svc/topstories/v2/"
LAST_CACHE="Stories.json"

if user_term in all_categories:
    print("Do you want to see top stories of the term you search? Press 'Y' to continue")
    user_stories=input()

    if user_stories.upper()=="Y":
        complete_url=stories_url+user_term+".json?"+"api-key="+STORIES_API

        resp_stories=requests.get(complete_url).json()
        dumped_json_cache_new=json.dumps(resp_stories)
        fw_n=open(LAST_CACHE,"w")
        fw_n.write(dumped_json_cache_new)
        fw_n.close()
        
        all_stories=resp_stories["results"]
        num=1
        for info in all_stories:
            complete_info=Stories_result(json_dict=info)
            print("["+str(num)+"]",complete_info)
            num=num+1




#######Part 2 starts here: Build a database to store your data

DBNAME = 'Final_Proj.db'
YELPJSON = 'Yelp.json'
LOCATIONJSON="Google.json"
STORIES="Stories.json"

conn=sqlite3.connect("Final_Proj.db")
cur=conn.cursor()

statement= '''
DROP TABLE IF EXISTS 'SearchYelp';
'''

conn=sqlite3.connect("Final_Proj.db")
cur=conn.cursor()

cur.execute(statement)

conn.commit()

statement= '''
CREATE TABLE "SearchYelp" (
	"ID"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"Name"	TEXT,
	"Address"	TEXT,
	"Zip Code"	TEXT,
	"Price Level"	INTEGER,
	"Rating"	REAL,
	FOREIGN KEY("NAME") REFERENCES "Location"("NAME")
);
'''

cur.execute(statement)
conn.commit()

statement= '''
DROP TABLE IF EXISTS 'Location';
'''

cur.execute(statement)

conn.commit()

statement= '''
CREATE TABLE "Location" (
	"ID"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"Longtitude"	NUMERIC,
	"Lattitude"	NUMERIC,
	"Name"	TEXT
);
'''
cur.execute(statement)
conn.commit()
conn.close()


conn=sqlite3.connect("Final_Proj.db")
cur=conn.cursor()

statement= '''
DROP TABLE IF EXISTS 'Stories';
'''

conn=sqlite3.connect("Final_Proj.db")
cur=conn.cursor()

cur.execute(statement)

conn.commit()

statement= '''
CREATE TABLE "Stories" (
	"ID"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"Title"	TEXT,
	"Author"	TEXT,
	"Updated date"	TEXT,
	"Created date"	TEXT,
	"Published date"	TEXT
);
'''

cur.execute(statement)
conn.commit()


#######insert data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "Final_Proj.db")

web_url="https://api.yelp.com/v3/businesses/search_limit-"+user_num+"_location-"+user_loc+"_price-"+user_price+"_term-"+user_term


enc=chardet.detect(open(YELPJSON,"rb").read())["encoding"]

with open(YELPJSON,"r",encoding=enc) as file:
    data=json.load(file)
    file.close()


result_list=data[web_url]["businesses"]


def insert_yelp():
    with sqlite3.connect(db_path) as db:
        cur=db.cursor()

        for i in result_list:
            name=i["name"]
            address=i["location"]["address1"]
            zip_code=i["location"]["zip_code"]
            price_level=len(i["price"])
            rating=i["rating"]

            insertion=(None,name,address,zip_code,price_level,rating)
            statement="INSERT INTO 'SearchYelp'"
            statement += 'VALUES(?,?,?,?,?,?)'
            cur.execute(statement,insertion)

    db.commit()
    db.close()

insert_yelp()


with open(LOCATIONJSON,"r",encoding=enc) as file_n:
    data_n=json.load(file_n)
    file_n.close()


def insert_google():
    with sqlite3.connect(db_path) as db:
        cur=db.cursor()
        lat=data_n["candidates"][0]["geometry"]["location"]["lat"]
        lon=data_n["candidates"][0]["geometry"]["location"]["lng"]
        name=search_name

        insertion=(None,lat,lon,name)
        statement="INSERT INTO 'Location'"
        statement += 'VALUES(?,?,?,?)'
        cur.execute(statement,insertion)
    db.commit()
    db.close()
    
insert_google()


with open(STORIES,"r") as file_l:
    data_l=json.load(file_l)
    file_l.close()


def insert_stories():
    with sqlite3.connect(db_path) as db:
        cur=db.cursor()
        all_results=data_l["results"]
        for info in all_results:
            title=info["title"]
            name=info["byline"].split(" ")
            try:
                author=name[-2]+" "+name[-1]
            except:
                author="missing"
            updated_date=info["updated_date"]
            created_date=info["created_date"]
            published_date=info["published_date"]
            insertion=(None,title,author,updated_date,created_date,published_date)
            statement="INSERT INTO 'Stories'"
            statement += 'VALUES(?,?,?,?,?,?)'
            cur.execute(statement,insertion)
    db.commit()
    db.close()
    
insert_stories()


print("We have saved your search to a database. Please check!")
        
#######part 3: data processing

def process_rating():
    with sqlite3.connect(db_path) as db:
        cur=db.cursor()
    statement="SELECT s.Rating, s.name FROM SearchYelp as s WHERE s.Rating >= 4 ORDER BY s.Rating DESC"
    cur.execute(statement)
    name_list=[]
    rating_list=[]
    for row in cur:
        name_list.append(row[0])
        rating_list.append(row[1])
        print(row[0],row[1])
    #print(name_list)
    #print(rating_list)
    return name_list,rating_list


def max_rating():
    with sqlite3.connect(db_path) as db:
        cur=db.cursor()
    statement="SELECT s.name, MAX(s.Rating) FROM SearchYelp as s"
    cur.execute(statement)
    max_rating_list=[]
    for row in cur:
     max_rating_list.append(row[0])
     max_rating_list.append(row[1])
     print(row[0],row[1])
    return max_rating_list


def min_rating():
    with sqlite3.connect(db_path) as db:
        cur=db.cursor()
    statement="SELECT s.name, MIN(s.Rating) FROM SearchYelp as s"
    cur.execute(statement)
    min_rating_list=[]
    for row in cur:
        min_rating_list.append(row[0])
        min_rating_list.append(row[1])
        print(row[0],row[1])
    return min_rating_list

#######Part 4 Unittest starts here
class TestYelpSearch(unittest.TestCase):

    def test_rating(self):
        results=process_rating()
        self.assertEqual(results[0][0], 5.0)
        self.assertEqual(results[0][1], 5.0)
        self.assertEqual(results[0][2], 4.5)
        self.assertEqual(results[0][3], 4.5)
        self.assertEqual(results[0][4], 4.5)
        self.assertEqual(results[0][5], 4.5)
        self.assertEqual(results[0][6], 4.5)
        self.assertEqual(results[1][0], "Oriole")
        self.assertEqual(results[1][2],"Alinea")
        self.assertEqual(results[1][3],"Crab Cellar")
        self.assertEqual(results[1][4],"Temporis")
        self.assertEqual(len(results), 2)


    def test_max_rating(self):
        results=max_rating()
        self.assertEqual(results[0], "Oriole")
        self.assertEqual(results[1], 5.0)

    def test_min_rating(self):
        results=min_rating()
        self.assertEqual(results[0], "Starbucks")       
        self.assertEqual(results[1], 1.5)

    



#######Part 5 Presentation starts here
        
def show_all_rating():
    rating_list,name_list=process_rating()
    fig=go.Figure()
    fig.add_trace(go.Bar(
        x=name_list,
        y=rating_list,
    ))

    fig.update_layout(
        title="Figure 1: Ratings of Places",
        autosize=False,
        width=800,
        height=600,
        xaxis_title="Name of places you search",
        yaxis_title="Ratings",
        font=dict(
            family="Courier New, monospace",
            size=12,
            color="#7f7f7f"
            )
        )
    fig.show()

#show_all_rating()


#accesstoken="pk.eyJ1IjoicHJpbmNpcGxleiIsImEiOiJjam1taTE3dGowamRjM3FqcG50MGp0anEwIn0.XuaFZy4Tff6aTfjiQUdd9Q"

def show_minmax_rating():
    max_rate=max_rating()
    min_rate=min_rating()
    fig=go.Figure()
    fig.add_trace(go.Bar(
        x=[max_rate[0],min_rate[0]],
        y=[max_rate[1],min_rate[1]],
    ))

    fig.update_layout(
        title="Figure 2: Rating of the best and worst place",
        autosize=False,
        width=800,
        height=600,
        xaxis_title="Name of places you search",
        yaxis_title="Ratings",
        font=dict(
            family="Courier New, monospace",
            size=12,
            color="#7f7f7f"
            )
        )
    fig.show()


#show_minmax_rating()

def map_location():
    data = [
    go.Scattermapbox(
        lat=[data_n["candidates"][0]["geometry"]["location"]["lat"]],
        lon=[data_n["candidates"][0]["geometry"]["location"]["lng"]],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=9
        ),
    )
    ]
    layout = go.Layout(
    autosize=True,
    hovermode='closest',
    mapbox=go.layout.Mapbox(
        accesstoken="pk.eyJ1IjoicHJpbmNpcGxleiIsImEiOiJjam1taTE3dGowamRjM3FqcG50MGp0anEwIn0.XuaFZy4Tff6aTfjiQUdd9Q",
        bearing=0,
        center=go.layout.mapbox.Center(
            lat=data_n["candidates"][0]["geometry"]["location"]["lat"],
            lon=data_n["candidates"][0]["geometry"]["location"]["lng"]
        ),
        pitch=0,
        zoom=13
    ),
    )
    fig = go.Figure(data=data, layout=layout)
    fig.show()

#map_location()

def all_location():
    data = [
    go.Scattermapbox(
        lat=all_alt,
        lon=all_lon,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=9,
            symbol="star",
            color="MediumPurple",
        ),
       text=all_names
    )
     ]
    layout = go.Layout(
    autosize=True,
    hovermode='closest',
    mapbox=go.layout.Mapbox(
        accesstoken="pk.eyJ1IjoicHJpbmNpcGxleiIsImEiOiJjam1taTE3dGowamRjM3FqcG50MGp0anEwIn0.XuaFZy4Tff6aTfjiQUdd9Q",
        bearing=0,
        center=go.layout.mapbox.Center(
            lat=(min(all_alt)+max(all_alt))/2,
            lon=(min(all_lon)+max(all_lon))/2
        ),
        pitch=0,
        zoom=10
    ),
    )
    fig = go.Figure(data=data, layout=layout)
    fig.show()
    
#all_location()

def interactive_funct():
    response=""
    while response != "exit":
        response = input("Do you want to see what place has ratings higher than 4.0? Press Y to continue and exit to quit ")
        if response=="exit":
            pass
        elif response=="":
            continue
        elif response.upper()=="Y":
            process_rating()
            
        else:
            print("Your input is invalid")
            continue
        response_one=input("Do you want to see what place has the best rating? Press Y to continue and exit to quit ")

        if response_one=="exit":
            pass
        elif response_one=="":
            continue
        elif response_one.upper()=="Y":
            max_rating()
        else:
            print("Your input is invalid")
            continue

        response_two=input("Do you want to see what place has the worst rating? Press Y to continue and exit to quit ")

        if response_two=="exit":
            pass
        elif response_two=="":
            continue
        elif response_two.upper()=="Y":
            min_rating()
        else:
            print("Your input is invalid")
            continue

#interactive_funct()

def interactive_graph():
    response=""
    while response!="exit":
        print("We have Four graph options. Please pick one!")
        print("[1] A map that shows all the result")
        print("[2] A map that shows the result you previously picked")
        print("[3] A bar graph that shows placs of rating greater than 4.0")
        print("[3] A bar graph that shows the best and worst rating")
        
        response=input("Enter an integer or a list of integers(example: 1,2 OR 1,2,3,4):")
        
        if response=="exit":
            pass
        elif response=="":
            continue
        else:
            try:
                ind_command=response.split(",")
                if "1" in ind_command:
                    all_location()
                if "2" in ind_command:
                    map_location()
                if "3" in ind_command:
                    show_all_rating()
                if "4" in ind_command:
                    show_minmax_rating()
            except:
                print("Your input is invalid")
                continue
                    
interactive_graph()

            
unittest.main()
