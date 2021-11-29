![NUSe](https://i.imgur.com/1bJTVAQ.png)
## A Passion Project brought to you by Team GEQ19C.

## Our Mission
NUSe is an Telegram Bot to help develop a culture of reusing and reducing waste generation within the National University of Singapore, through the process of mutual exchange. 

We link people of common needs together as a means to communicate directly, so as to tackle the issue of sustainability.

## Visit Us
Have something to share or give away? Looking for any items? Communicate with NUSebot to create a post in the Channel!
Talk to the bot @TheNUSeBot, or visit the Channel https://t.me/GEQ19C.

## What can NUSebot do?
 - Make and send automatically-crafted posts to the channel
 - Adds photos to your posts to better suit your needs
 - Edit, Delete or Change the Photo of your previous posts
 - Uses inline keyboard functionality to ensure seamless transitions through the process
 - Update any changes to the status of posts
 - [Admin function] Using a separate admin channel, track changes in statuses and deletions, hence
 measuring number of transactions.

Note: Photos shown are not from the final product.
<p align="middle">
 <img src="https://i.imgur.com/2J2MXnC.jpg" height=450>
 <img src="https://i.imgur.com/SS4tZl2.jpg" height=450>
 <img src="https://i.imgur.com/AvRoeb6.jpg" height=370>
 <img src="https://i.imgur.com/6EyK3Sl.jpg" height=370>
</p>
 
## Usage

This bot is uploaded to Heroku using the Heroku CLI & Github Desktop

### Getting API Token
Using Telegram's in-app bot Botfather, generate a key to set up your bot, and set it up in GEQBot.py main():
 ``` 
 updater = Updater(token = TOKEN, use_context = True)
 ```
 Create 2 new channels: 1 for the Administrative Logs, and the other for the bot to send the posts to. Get the Channel IDs (From the web URL) and paste it into the fields in globals.py.
 
 It is recommended to also create a Group chat at link it as a Discussion Chat on the main Channel.

 The bot also uses Amazon's AWS S3 bucket to store its data (as a pickle), since Heroku doesn't store it for more than 24 Hours.
 Find out more here: https://devcenter.heroku.com/articles/s3
 
 Start GEQbot.py and click /start on the bot to start interacting with the bot. :D
 
## Possible Future Features
Suggest some here :)

 

## Credits
This bot was designed by Koh Jia Xian, as part of a GEQ1917 project, Group 19C, from the National University of Singapore, Ridge View Residential College.

This bot is hosted by Telegram, and uses the Telegram Bot API, and the Python-Telegram-Bot library (python-telegram-bot.org)
