# QCI-Robinhood-Bot 
## Learn More  
Visit https://quikfo.com to learn more about Quikfo and its proprietary systems.  
## Info 
This bot leverages a metric called the **Quikfo Confidence Index** with the goal of maintaining long exposure to the SP500 and many key sectors (Health Care, Info Tech, etc.) on days where investor confidence looks positive.  It does this by moving a portfolio's money around between ETFs.  
_Please note_: this bot is _not_ designed to work in a portfolio containing other positions. 
## Setup
In order to run this bot simply:  
* edit the `username`, `password`, and `key` fields with your Robinhood credentials and Quikfo API key.  *If you don't have a Quikfo API key then please email admin@quikfo.com in order to get one!*  
* set up a cron job to execute the `bot.py` file each weekday at some point towards the market open.