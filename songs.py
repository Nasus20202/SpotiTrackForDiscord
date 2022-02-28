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
    for song in songs:
        name = spotify.get_track_name_by_id(song[0])
        plays = song[1]
        artists = spotify.get_track_artist(song[0])
        bio += f'#{str(i)} {name} by {artists} ({str(plays)})\n'
        i += 1
        for artist in artists.split(', '):
            if artist not in artistsPopularity:
                artistsPopularity[artist] = 0
            artistsPopularity[artist] += plays
        totalPlays += plays
    bio += f"\nArtists popularity in your top {n} tracks:\n"
    i = 1
    for artists in dict(sorted(artistsPopularity.items(), key=lambda item: item[1], reverse=True)):
        bio += f"#{i} {artists} {artistsPopularity[artists]}\n"
        i+=1
    sleep(0.05) # just for API rate limit
    bio += f'Total plays: {totalPlays}'
    return bio

print(stats(int(input("How many songs would you like to see? "))))
