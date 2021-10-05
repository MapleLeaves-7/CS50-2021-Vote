# Voting
#### Video Demo:  <URL HERE>
#### Description:

This is a website that allows users to create polls, vote on them, as well as keep a record of past polls they have created. 

Users have to register for an account to create polls, and set all the candidates of the poll to activate it. Once a poll has been activated, the user will be given a unique room key for that particular poll. Anyone can use a room key they have been given to vote on a poll. All they have to do is go to the website, enter the room key, and vote on the poll. Since voting is anonymous, users do not have to log in to vote on polls, they only need a poll's room key. The creator of the poll can monitor each poll's progress as well as latest results by logging into their account, and their homepage should a summary of all the active polls a user has. To view the details of each poll, users can click on the poll name, and they will be redirected to a page that shows them the current vote count, as well as the number of votes each candidate currently has. From the homepage, users can also close any active polls by clicking "close". This is non-reversible and once a poll has been closed, it can no longer be open again. Furthermore, if users enter the room key of a closed poll into the front page of the website, they would be given a warning informing them they the poll is closed and they would not be allowed to vote. 

Each poll is allowed a maximum of 15 candidates. I had to set a limit on the number of candidates each user could set so that would not enter an arbituarily big number and crash the entire system. I put 15 as I thought it was neither too big nor too small, and good polls should not have too many choices anyway. 

All of the logic for the website lies inside the folder called "website". Outside, the main.py file is used to execute the program. It refers to a function called create_app() in the __init__.py file in the website folder.  
