# Sparky-Bot (Beta)

A Discord bot for Codechef

## Key Features
1. Identify users based on their Codechef handles.
2. Check recent submissions by a user
3. Check upcoming contests.
4. Plot Rating Graph
5. Get useful insights about a user instantly
6. Get random unsolved problem by difficulty

## Images

#### Identify people by Codechef Handles
<img src="https://i.ibb.co/5xhYtBy/xcgxc.png" alt="xcgxc" border="0">

#### Check recent submissions by users
<img src="https://i.ibb.co/4m4M0zT/subs.png" alt="subs" border="0">

#### Plot Rating Graphs
<img src="https://i.ibb.co/SKkQVJz/ratinggraph.png" alt="ratinggraph" border="0">

#### Check upcoming contests
<img src="https://i.ibb.co/TMVnwyg/cont.png" alt="cont" border="0">

#### Get useful insights about a user instantly
![](https://i.ibb.co/23kzXBS/sssss.png)

#### Get random unsolved problem by difficulty
![](https://i.ibb.co/7nGGYMb/Capture.png)

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
0. Create an Enviroment Variable `DEBUG` and set it to '1'
1. In `cogs\Utils\constants.py` replace `TOKEN` line 30, with your bot token.
2. In `cogs\Utils\constants.py` replace `OWNER` with your Discord User ID
3. In `cogs\Utils\constants.py` set `DEBUG` to `True`
4. In `cogs\Utils\cc_api.py` set `CLIENT_ID` and `CLIENT_SECRET` with your API Credentials respectively.


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
2. To run bot commands, use prefix (`=`) , e.g `=contest future`
3. Bot should have Admin privileges.


## Footer

This bot is in Beta, and have only basic functionality.
All contributions are welcome.

## Thanks

- [imjohnzakkam](https://github.com/imjohnzakkam) for developing and testing the bot in development and giving valuable feedback.
- [SayangitBIT](https://github.com/SayangitBIT) for testing the bot in development and giving valuable feedback.
