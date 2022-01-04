from dotenv import load_dotenv
import spotify
import signal
import sys
import asyncio
import nest_asyncio
import database
import discord_bio
import time_manager


def handler(signum, frame):
    res = input("Ctrl-c was pressed. Do you really want to exit? y/n ")
    if res == 'y':
        sys.exit(0)
 
signal.signal(signal.SIGINT, handler)

load_dotenv()
nest_asyncio.apply()

db = database.create_connection()

async def checkIfSongIsOver(id):
    current_id = spotify.get_track_id()
    progress = spotify.get_milliseconds()
    duration = spotify.get_duration_milliseconds()
    if(progress <= 7500):
        id = ""
    if(duration - progress <= 7500 and current_id != id):
        database.new_record(spotify.get_track_id(), db)
        time_manager.add_millis(duration)
        discord_bio.set(generate_bio())
        await asyncio.sleep(1)
        return current_id
    await asyncio.sleep(1)
    return id



def generate_bio():
    bio = "Time spent listening: " + time_manager.get_current_time_spent() + " (d/h/m/s)\\n"
    songs = database.get_top_song(5)
    i = 1
    for song in songs:
        name = spotify.get_track_name_by_id(song[0])
        plays = song[1]
        bio += '#' + str(i) + " " + name + ' (' + str(plays) + ')\\n'
        i += 1
    return bio

async def thread():
    i = 0
    id = spotify.get_track_id()
    while True:
        id = await checkIfSongIsOver(id)
        if(i == 1000):
            spotify.refresh_access_token()
            i = 0
        i = i + 1

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
task = loop.create_task(thread())
try:
    loop.run_until_complete(task)
except asyncio.CancelledError:
    pass
