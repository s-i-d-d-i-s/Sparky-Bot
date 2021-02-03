# Sparky-Bot (Beta)

A Discord bot for Codechef

## Key Features
1. Identify users based on their Codechef handles.
2. Check recent submissions by a user
3. Check upcoming contests.
4. Plot Rating Graph

## Images

#### Identify people by Codechef Handles
<img src="https://i.ibb.co/5xhYtBy/xcgxc.png" alt="xcgxc" border="0">

#### Check recent submissions by users
<img src="https://i.ibb.co/PGJqMnN/sss.png" alt="subs" border="0">

#### Plot Rating Graphs
<img src="https://i.ibb.co/SKkQVJz/ratinggraph.png" alt="ratinggraph" border="0">

#### Check upcoming contests
![](https://i.ibb.co/RCs7Js8/ss.png)

#### Get useful insights about a user instantly
![](https://i.ibb.co/23kzXBS/sssss.png)

## Installation

#### Clone the repository

```bash
git clone https://github.com/s-i-d-d-i-s/Sparky-Bot
```
#### Install Dependencies

```bash
pip install -r requirements.txt
```

#### Create a Bot

Create a bot on your server. Here is a [tutorial](https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token) on that

#### Add Bot Token

In `main.py` replace  `"YOUR BOT TOKEN"` with your bot token.
In `Utils\constants.py` replace `OWNER` with your Discord User ID
In `Utils\constants.py` set `DEBUG` to `True`


#### Final Steps 

```bash
python main.py
```

## Note

1. Make sure you have the following roles present on your server
 - Admin
 - 1★
 - 2★
 - 3★
 - 4★
 - 5★
 - 6★
 - 7★
2. To run bot commands, use prefix (`=`) , e.g `=handles`

## Footer

This bot is in Beta, and have only basic functionality.
All contributions are welcome.

## Thanks

- [imjohnzakkam](https://github.com/imjohnzakkam) for testing the bot in development and giving valuable feedback.
- [SayangitBIT](https://github.com/SayangitBIT) for testing the bot in development and giving valuable feedback.
