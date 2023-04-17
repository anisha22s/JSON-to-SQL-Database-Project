# **JSON to SQL Database Project**

This project extracts data from the GitHub API in JSON format, and stores it in a MySQL database in the form of a table.

## **Description**

This project aims to extract data from the Apache Hadoop Github Repository's contributors endpoint, retrieve specific information about the contributors using the API and store it in a SQL database. This project uses Python and its packages like Pandas, pymysql, requests, json, and PrettyTable.

This projects code fetches information about the first 100 contributors to the Apache Hadoop GitHub repository, such as their login ID, location, email, hireable status, bio, Twitter username, public repositories, public gists, followers, following, and creation date. It then creates a MySQL database and a table. The data retrieved in the earlier step is then inserted into the table.


## **Installation**

To run this project, you will need to have the following libraries installed:

pandas
pymysql  
requests  
json  
warnings  
prettytable  
textwrap 

## **Usage**

To use this project, simply run the Python code in your preferred IDE or text editor. Make sure you have your MySQL database set up and configured correctly, and update the DBHOST, DBUSER, DBPASS, and DBPORT variables with your own database connection details.

Once the code is executed, you will see the extracted information for each contributor printed to the console. The information will also be stored in a table in your MySQL database.


