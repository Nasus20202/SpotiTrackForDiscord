from time import sleep
import spotify
import database
import time_manager

def stats(n):
    bio = f"Time spent listening: {time_manager.get_current_time_spent()} (d:h:m:s)\n"
    songs = database.get_top_song(n)
    i = 1
    totalPlays = 0
    artistsPopularity = {}
    artistsTime = {}
    for song in songs:
        name = spotify.get_track_name_by_id(song[0])
        plays = int(song[1])
        artists = spotify.get_track_artist(song[0])
        time_spent_on_song = spotify.get_track_duration(song[0])*plays // 1000
        bio += f'#{str(i)} {name} by {artists} ({str(plays)}, {time_manager.format_time(time_spent_on_song)})\n'
        i += 1
        for artist in artists.split(', '):
            if artist not in artistsPopularity:
                artistsPopularity[artist] = 0
            artistsPopularity[artist] += plays
            if artist not in artistsTime:
                artistsTime[artist] = 0
            artistsTime[artist] += time_spent_on_song
        totalPlays += plays
    bio += f"\nArtist's tracks play count and time in your top {n} tracks:\n"
    i = 1
    for artists in dict(sorted(artistsPopularity.items(), key=lambda item: item[1], reverse=True)):
        bio += f"#{i} - {artists} {artistsPopularity[artists]} - {time_manager.format_time(artistsTime[artists])}\n"
        i+=1
    sleep(0.05) # just for API rate limit
    bio += f'Total plays: {totalPlays}'
    return bio

print(stats(int(input("How many songs would you like to see? "))))
