#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 15:29:06 2023

@author: leenasamant
"""
#Question 1
#Go to https://api.github.com Links to an external site. and familiarize yourself with the API.


import pandas as pd
import pymysql
import requests
import json
import warnings
from prettytable import PrettyTable
import textwrap
warnings.filterwarnings("ignore")

#Question 2
# 2. Go to https://api.github.com/repos/apache/hadoop/contributors Links to an external site. . 
#This is the Apache Hadoop Github Repo's contributors’ endpoint. Extract the JSON corresponding
# to the first 100 contributors from this API. (Hint: the API request is a GET request and the 
#variable name that handles the items per page is "per_page").  Write Java or Python code that does all this.
token = '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'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36', 
    'Authorization': 'token ' + token
}
url = 'https://api.github.com/repos/apache/hadoop/contributors'
params = {'per_page': 100}
response = requests.get(url = url, headers = headers, params= params)

# Extract 100 contributors from this API
contributors_json = response.json() 


# confirming 100 contributors extracted
print("Succesfully extract %s contributors extract from Github API." % len(contributors_json))

#Question 3
# For each of the 100 contributors extracted in (2), write code that accesses their user 
#information and extracts "login", "id", "location", "email", "hireable", "bio", "twitter_username",
# "public_repos", "public_gists", "followers", "following", "created_at" (and print those to screen)

for contributor in contributors_json:
    print(type(contributors_json))
    contributor_url = contributor['url']
    user_info_response = requests.get(url = contributor_url, headers = headers)
    user_info_json = user_info_response.json() 
    print("Login:", user_info_json['login'])
    print("ID:", user_info_json['id'])
    print("Location:", user_info_json['location'])
    print("Email:", user_info_json['email'])
    print("Hireable:", user_info_json['hireable'])
    print("Bio:", user_info_json['bio'])
    print("Twitter Username:", user_info_json['twitter_username'])
    print("Public Repos:", user_info_json['public_repos'])
    print("Public Gists:", user_info_json['public_gists'])
    print("Followers:", user_info_json['followers'])
    print("Following:", user_info_json['following'])
    print("Created At:", user_info_json['created_at'])
    print("--------------------------------------------------------------------------------------")
    

#Question 4
#Write code that creates an SQL database + table, and stores all the information obtained in (3)
#in it.  Please be cautious of the data type you choose for each collumn and briefly justify 
#your decisions.  What do you choose as Primary Key and why?
DBHOST = 'localhost'
DBUSER = 'root'
DBPASS = '########'
DBPORT = 3306


db = pymysql.connect(host = DBHOST, user = DBUSER, password = DBPASS, port = DBPORT)
cursor = db.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS db_contributors")
cursor.close() # close cursor
db.close() 

# Connecting to mysql and creating database
try:
    db = pymysql.connect(host = DBHOST, user = DBUSER, password = DBPASS, database = 'db_contributors', port = DBPORT)
    print('connect successfully')
    cursor = db.cursor()
    cursor.execute('DROP TABLE IF EXISTS Contributors')
    sql = "CREATE TABLE Contributors ( \
        Id INT(30) NOT NULL PRIMARY KEY, \
        Login VARCHAR(255), \
        Location VARCHAR(255), \
        Email VARCHAR(255), \
        Hireable BOOLEAN, \
        Bio VARCHAR(500), \
        Twitter_Username VARCHAR(255), \
        Public_repos INT(30), \
        Public_gists INT(30), \
        Followers INT(30), \
        Following INT(30), \
        Created_at VARCHAR(255))"
    cursor.execute(sql)
    print('table created successfully')
    
    
# Insert data
    for contributor in contributors_json:
        contributor_url = contributor['url'] # Get each contributor's url 
        user_info_response = requests.get(url = contributor_url, headers = headers)
        if user_info_response.status_code == 200: # to check if each contributor's url can be reached
            try:
                user_info_json = user_info_response.json() # type(info_json) = dict
                # Retrive required info
                login = user_info_json['login']
                id_value = user_info_json['id']
                location = user_info_json['location']
                email = user_info_json['email']
                hireable = user_info_json['hireable']
                bio = user_info_json['bio']
                twitter_username = user_info_json['twitter_username']
                public_repos = user_info_json['public_repos']
                public_gists = user_info_json['public_gists']
                followers = user_info_json['followers']
                following = user_info_json['following']
                created_at = user_info_json['created_at']
                # Insert data
                sql = "INSERT INTO Contributors (Login, Id, Location, Email, Hireable, Bio, Twitter_Username, Public_repos, Public_gists, Followers, Following, Created_at) VALUE (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                values = (login, id_value, location, email, hireable, bio, twitter_username, public_repos, public_gists, followers, following, created_at)
                cursor.execute(sql, values)
                db.commit() ### submit database
                print(f"Successfully inserted user data for contributor id: {contributor['id']}")
            except pymysql.Error as e:
                print(f"Error: failed to insert user data for contributor id:{contributor['id']}" + str(e))
                db.rollback() # if errors occur, rollback database 
    
        else: 
            print(f"Error: failed to retrieve url for contributor id: {contributor['id']}")      

    sql = 'select * from Contributors'
    cursor.execute(sql)
    result = cursor.fetchall() 
    table = PrettyTable()
    table.field_names = ["Id", "Login", "Location", "Email", "Hireable", "Bio", "Twitter_Username", "Public_repos", "Public_gists", "Followers", "Following", "Created_at"]
    table.max_width = 30
    for row in result: # iterate each row of the result 
        id_value = row[0]
        login = row[1]
        location = row[2]
        email = row[3]
        hireable = row[4]
        bio = row[5]
        twitter_username = row[6]
        public_repos = row[7]
        public_gists = row[8]
        followers = row[9]
        following = row[10]
        created_at = row[11]
        if bio is not None: #truncate bio to a certain length
            bio = textwrap.shorten(bio, width=20, placeholder="...")
        list = [id_value, login, location, email, hireable, bio, twitter_username, public_repos, 
                public_gists, followers, following, created_at]
        # add each row into the table
        table.add_row(list) 
    print(table)
    cursor.close() # close cursor
    db.close() # close database
    
except pymysql.Error as e:
    print('failed to create table' + str(e))

print("I have selected 'id' as the primary key. It is a unique identifier for each user, ensuring that each row in the table represents a distinct user.  Secondly, the 'id' attribute is of the integer data type, which is ideal for use as a primary key. Also, 'id' as the primary key will make it more convenient to join with other tables in the future when new tables are added to the database.")

#Question 5. Optimize your code in (4) to allow for quick look-ups of "login", "location", 
#and "hireable".  I.e., I would like, for example, to run the command  <<  SELECT * FROM table
# WHERE location = "Tokyo"  >>  fast.  What choices do you make and why?


def get_rows_with_login_location_hireable(login = None, location = None, hireable = None):
    db = pymysql.connect(host = DBHOST, user = DBUSER, password = DBPASS, database = 'db_contributors', port = DBPORT)
    cursor = db.cursor()
    # Check index with the name 'idx' exists
    cursor.execute("SHOW INDEX FROM Contributors WHERE Key_name = 'idx'")
    result = cursor.fetchone()
    if result:
    # drop idx if exists
        cursor.execute("DROP INDEX idx ON Contributors")
    else:
        pass
    # Create index for the columns of Login, Location, Hireable
    cursor.execute('CREATE INDEX idx ON Contributors (Login, Location, Hireable)')
    
    where_clauses = []
    if login:
        where_clauses.append(f"Login LIKE '%{login}%'")
    if location:
        where_clauses.append(f"Location LIKE '%{location}%'")
    if hireable:
         where_clauses.append(f"Hireable = '{hireable}'")

    if where_clauses:
        sql = "SELECT * FROM Contributors WHERE " + " AND ".join(where_clauses)
    else:
        sql = "SELECT * FROM Contributors"
    cursor.execute(sql)
    # adding result in dataframe in pandas
    df = pd.DataFrame(cursor.fetchall(), columns=['Id', 'Login', 'Location', 'Email', 'Hireable', 'Bio', 
                                                  'Twitter_Username', 'Public_repos', 'Public_gists', 'Followers',
                                                  'Following', 'Created_at'])
    cursor.close()
    db.close() # close database
    return df

df_tokyo = get_rows_with_login_location_hireable(location = 'Tokyo')
df_tokyo


























    
