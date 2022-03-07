# Voting

This is my CS50x 2021 Final Project.

### What it does
This is a website that facilitates easy anonymous voting, while also allowing users to keep a record of all past poll results. 

### How to use it
#### Video Demo: https://www.youtube.com/watch?v=4ShpKT9As2w 

**Creating a poll:** 
1)	Register for an account
2)	Set all the candidates for the poll
3)	Get the room key
4)	Share the room key with relevant parties

**Voting on a poll:**
The room key can be used by anyone to vote on a poll.

1)	Enter the room key into the front page of the website
2)	Click on choice
3)	Submit

**Closing a poll:**

1)	Log into account
2)	Click on the “close” button beside the active poll you want to close

Note: Once a poll is closed, it can no longer be opened again.

### How I built it
Python, Flask and SQLAlchemy was used for the backend, and Javascript, HTML and CSS was used for the frontend. Heroku was used to deploy the website. 

### Challenges I ran into
When building a website for CS50’s problem set, the helper library had automated a significant portion of the backend, including integration with sqlite3 as well as authenticating logins. 

Problem sets were also done in the CS50 IDE, with all the required libraries already pre-installed.

Hence, the challenges I faced were:
1)  Setting up the correct environment in my local computer with all the relevant libraries and dependencies
2)	Figuring out how to authenticate logins
3)	Figuring out how to integrate SQL with python and flask
4)	Figuring out how to deploy a website onto the internet
5)	Designing the schema for databases for efficient data storage
6)	Designing user-friendly website layout

### Accomplishments I’m proud of
I learnt SQLAlchemy and Flask-login from reading the documentation and managed to integrate both technologies successfully into the website. I also learnt Heroku specifically to deploy this website. 

By continuously testing my website and trying to use it in a way that it was not intended for, I managed to think of multiple edge cases, and was thus able to modify my code to account for them. For example, in an older version, users clicking away before setting all the candidates would lead to the poll being lost forever, and any user with an account typing the room key directly into the URL would be able to see the results of the poll regardless of whether they created that specific poll or not. 

### What I’ve learnt
Minimum viable product.
Initially, I came up with an idea that was too complex and was at a loss at how to begin. I only began to make progress once I aimed to create a minimum viable product, and then broke the project down into smaller pieces to be worked on separately, implementing one feature at a time. 
