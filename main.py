from dotenv import load_dotenv
import spotify
import signal
import sys
import asyncio
import nest_asyncio
import database


def handler(signum, frame):
    res = input("Ctrl-c was pressed. Do you really want to exit? y/n ")
    if res == 'y':
        sys.exit(0)
 
signal.signal(signal.SIGINT, handler)

load_dotenv()
nest_asyncio.apply()

db = database.create_connection()

async def checkIfSongIsOver(id):
    progress = spotify.get_milliseconds()
    duration = spotify.get_duration_milliseconds()
    current_id = spotify.get_track_id()
    if(progress <= 5000):
        id = ""
    if(duration - progress <= 5000 and current_id != id):
        database.new_record(spotify.get_track_id(), db)
        await asyncio.sleep(1)
        return current_id
    await asyncio.sleep(1)
    return id


async def thread():
    i = 0
    id = ""
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
