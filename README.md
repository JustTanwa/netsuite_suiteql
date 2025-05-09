# Netsuite SuiteQL

Netsuite SuiteQL an interactive learning application that highlights and teaches SuiteQL query langauge. Learn through practice by running SuiteQL command directly in the application. Login required.

## Description

This is a CS50 Final Project that I have decided to build, using Flask, Sqlite and Tailwind CSS. I have already some experience with Bootstrap so I wanted to try Tailwind just to see how to work with it and if it would be much different from Bootstrap.

I work with Netsuite on a daily basis and I wanted to incorporate it into this final project, which is why I decided to take what I have learnt in this course to build something connected to Netsuite.

The goal of the application is to do two things:
1. Demonstrate how a third party application could integrate with Netsuite using OAuth2.0 Code Grant Flow for authorization.
2. Share some knowledge around Netsuite to anyone who would be interested, specific how SuiteQL is similar enough to other SQL language for other databases that it is beneficial to learn as it is a transferable skill.

In order to achieve this, I need to do two things, set up some environment variable to hide my credentials on the server for security reasons and to store permanent and persistence lesson data on Sqlite database. Of course, I need a Netsuite instance to make the integration with, and luckily I have access to a demo account to use.

Since I have not opt for a user management database, I will be storing the access token on the server session and using them to make requests to Netsuite.

I have also spent a bit of time, looking at ways to host this project, deploying application developed is something I wanted to explore and have this application available outside of local environment. Luckily, [Pythonanywhere](https://www.pythonanywhere.com/) provides free hosting for python based project, which is perfect to show case and allow me to learn a bit about WSGI configuration.

### File structure and purpose

As part of the CS50 final project requirement, here is a breakdown of the files in this project and my decision and choices throughout.

#### app.py 
This is the main entry point of my application that Flask will serve up and handle incoming requests and routing. I wanted to keep the application small so I did not implement any user login access, since the goal to demonstrate OAuth2.0 Code Grant Flow, I had set up only 1 environment variable for my Netsuite instance and showcase the login with my own access. The file contains various routes with the index page being the home page where user (me) can login via Netsuite or go to dashboard directly to view the lessons.

The dashboard route, fetches lessons from the sqlite database and display them, each link will route the user to a specific lesson page.

The lesson page, is a dynamic parameterized route which accepts the internal id of the lesson and it will fetch the lesson data from the databse to display to the user.

If the user is logged in, an editor is shown to allow for the user to write and send SuiteQL statements to Netsuite for fetching data. The button will send a post request with the SuiteQL statment captured from the editor to the server. The resulting response data is transform to a table like format to display to the user what Netsuite as returned. In the event of an error, the error message is shown.

There's no persistent user information, the access token obtained through authorization is stored in the server session and is deleted when the browser is closed.

#### auth.py 
This is contains the helper function for making a request to Netsuite to start the OAuth2.0 Code Grant flow, it will send request to login endpoint and also token endpoint when it gets a code response back. The OAuth2.0 Code Grant Flow with Netsuie has a good documentation, the first step requires a GET request to be sent to Netsuite, if there is a logged in session then user will be asked to authorized the access, if not, they will be asked to log in. Afterwards, the authorized code is returned and the application process the authorized code to get an access token. This file formats the request to the correct format for Netsuite and making use of the request module to make the resquest to Netsuite.

#### config.py 
This is for setting up some API endpoint and environment variables for the OAuth2.0 requests, this is what I will adjust if I need to change some information regarding scope or URI.

#### create_lesson.py and setup_db.py

This is for me to use to create and update lessons to the database, instead of manually using sqlite3 in the command line, I created these python scripts to help with setup the database table initially and maintain the lesson contents.

#### database.py 
This file contains helper functions to interact with the sqlite table

#### templates/* and static/* 
These are folders that contains various jinja2 HTML template to be served up when requested or static image files.
- base.html is the base template used in all pages, it provides nav bar and header for the page.
- 404.html is for when user visit a non-existing page
- dashboard.html shows a list of lesson as card with title and description where use can navigate to a specific lesson.
- home.html is for displaying the home page, it will redirect to dashboard if there is a logged in user in the session
- lesson.html give standard layout for a lesson. I have opt to use some third part text editor called ACE for text highlighting to give some styling than just a regular text area element.


#### Video Demo:  [SuiteQL Learn YouTube](https://youtu.be/gOyiXoNTCqU)

#### Live demo: [SuiteQL Learn](https://ts2025dev.pythonanywhere.com/)

## Run it locally

### Pre-req

- Python 3.13+
- Flask (pip install flask)
- Requests (pip install requests)
- Python Dotenv (pip install python-dotenv)

### Steps
1. Clone the repository
2. Set up Integration Record in Netsuite
3. Create .env file for the Netsuite variables
4. flask run

## Improvement
If I were to continue this project, I could implement user management so people could sign up and set up their own Netsuie instance credentials. 