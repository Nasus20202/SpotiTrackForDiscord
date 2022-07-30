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

old_time = time_manager.get_current_raw_time_spent()
load_dotenv()
nest_asyncio.apply()

db = database.create_connection()

async def checkIfSongIsOver(id):
    sleep_time = 3
    data = spotify.get_current_spotify_info();
    current_id = spotify.get_track_id(data)
    progress = spotify.get_milliseconds(data)
    duration = spotify.get_duration_milliseconds(data)
    global old_time
    if(progress <= 7500):
        id = ""
    if(duration - progress <= 7500 and current_id != id):
        database.new_record(spotify.get_track_id(), db)
        time_manager.add_millis(duration)
        new_time = time_manager.get_current_raw_time_spent()
        if(new_time != old_time):
            discord_bio.set(generate_bio())
            old_time  = new_time
        await asyncio.sleep(sleep_time)
        return current_id
    await asyncio.sleep(sleep_time)
    return id



def generate_bio():
    bio = "Time spent listening: **" + time_manager.get_current_time_spent() + "** (d:h:m\\\:s)\\n"
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
            await spotify.refresh_access_token()
            i = 0
        i = i + 1

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
task = loop.create_task(thread())
try:
    loop.run_until_complete(task)
except asyncio.CancelledError:
    pass
