# SpotiTrack for Discord

Nice Spotify stats, display your favourite songs and your total time spent listening. All this in your Discord bio section.

Works best with https://github.com/Nasus20202/SpotifyDiscordActivity

### How does it look?
![Demo](https://github.com/Nasus20202/SpotiTrackForDiscord/blob/master/img/demo.gif)
## How to use it?

1. You will need a Spotify App. You can register one here: https://developer.spotify.com/dashboard/. 
You can use the same app as for SpotifyDiscordActivity or create a new one.
If you are using development mode, you will have to add your account in "Users and access" tab.
2. Create a .env file in ./TokenGenrator. It should look like this:
```
CLIENT_ID=YOUR_APP_CLIENT_ID
CLIENT_SECRET=YOUR_APP_CLIENT_SECRET
REDIRECT_URI=http://localhost:9999/callback
```
Your Client ID and Secret can be accessed at your devloper dashboard.
3. Now start the Node.js server
```
cd ./TokenGenerator
node ./app.js
```
4. You also need your Discord user token. Here is how to obtain it: https://pcstrike.com/how-to-get-discord-token/
5. Now create and .env file in project main folder. It should look like this:
```
TOKEN=YOUR_DISCORD_TOKEN
SPOTIFY_REFRESH_TOKEN=SPOTIFY_REFRESH_TOKEN
TOKEN_GENERATOR_SERVER=http://localhost:9999/refresh_token
```
6. Go to http://localhost:9999/ and log in to Spotify. Now you should receive your Spotify Refresh Token. Copy it to the .env file.
7. Start the Python script
```
python ./main.py
```

### Required libraries

Python: 
- python-dotenv
- nest-asyncio
```
pip install python-dotenv
pip install nest-asyncio
```

Node:
- express
- request
- cors
- cookie-parser
- query-string

Node.js packages should be installed automatically. If not, install them with npm. (npm install *package name*)
