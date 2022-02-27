
# Steps to run 
This is build on python 3.8.12. Recommend python version: 3.7 and beyond

0. make sure: 
\n(a)you have pip installed, which manages python libraries for you; 
\n(b)this is built on 3.8.12, so I recommind python version 3.7 and beyond
\n(c) main.py make connection to a cloud mongo db, so make sure you have internet connection as well
LET ME KNOW if you cannot connect to the cloud db, I will have to fix the config for this db

1. install all dependencies
pip install -r requirements.txt

2. Run main.py on the first terminal
python main.py

3. Poppulate Data into MongoDB
use this on a new terminal: 
http POST http://127.0.0.1:5000/api/db_populate

4. test get api_books()
you should see the address of Jason Bourne's residency
http GET http://127.0.0.1:5000/api/address


MAKE SURE: you test these API call on the second terminal/cmd while running main.py on the first terminal/cmd. 







