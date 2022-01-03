import database

# I am saving this one variable in the database as a song, cause why not. I am too lazy, and noone will ever see this :)

time = 0

if(database.check_if_exists("time_spent")):
    time = database.get_song_plays("time_spent")
else:
    database.new_song("time_spent", time)

def get_current_raw_time_spent():
    return database.get_song_plays("time_spent")

def add_seconds(sec):
    global time
    database.update_song("time_spent", time + sec)
    time += sec

def add_millis(millis):
    add_seconds(millis // 1000)

def add_minutes(minutes):
    add_seconds(60 * minutes)

def get_current_time_spent():
    seconds = get_current_raw_time_spent()
    days = seconds // (24 * 3600)
    seconds -= days * 24 * 3600
    hours = seconds // 3600
    seconds -= hours * 3600
    minutes = seconds // 60
    seconds -= minutes * 60
    return str(days) + ":" + f"{hours:02d}" + ":" + f"{minutes:02d}" + ":" + f"{seconds:02d}"



