import mutagen
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC, error
from mutagen.mp3 import MP3
from yandex_music import Client
import os

path = 'E://music/'

dont_need_replace = False

client = Client('AQAAAAAW_bnzAAG8XsHO3Y6QDkvyrcotC8zgqKM')
client.init()

for i in range(201, 500):
    print(i)
    track = client.users_likes_tracks()[i]
    print(track.id)
    title = client.tracks(track.id)[0].title
    album = client.tracks(track.id)[0].albums[0].title
    year = client.tracks(track.id)[0].albums[0].year
    artist = ''
    i = 0
    for ar in client.tracks(track.id)[0].artists:
        artist += ar.name + ', '
        i+=1
    #artist = artist.replace(', ', '', -1)
    artist = artist.rstrip(", ")
    print(f'\tTITLE: {title}\n\tALBUM: {album}\n\tARTIST: {artist}\n\t{year}')
    f = path + f'{artist}/{album}/{title}.mp3'
    vr_album = album
    if f.find('*')>0:
        f = f.replace('*', '')
    if album.find(':') > 0:
        vr_album = vr_album.replace(':', '')
        f = path + f'{artist}/{vr_album}/{title}.mp3'
    if title.find('/')>0:
        vr_title = title.replace('/',' ')
        f = path + f'{artist}/{album}/{vr_title}.mp3'
    if album.find('/')>0:
        vr_album = vr_album.replace('/', '')
        f = path + f'{artist}/{vr_album}/{title}.mp3'
    if album.find('?')>0:
        vr_album = vr_album.replace('?', '')
        f = path + f'{artist}/{vr_album}/{title}.mp3'
    if title.find('?')>0:
        vr_title = title.replace('?', '')
        f = path + f'{artist}/{vr_album}/{vr_title}.mp3'
    if f.find('"')>0:
        f = f.replace('"', '')
    if os.path.isdir(path + f'{artist}/{vr_album}/'):
        track.fetch_track().download(f)
        if os.path.isfile(f) and dont_need_replace:
            print('Exist!')
        else:
            client.tracks(track.id)[0].download_cover(path + f'{artist}/{vr_album}/cover.jpeg', '1000x1000')
            try:
                tags = EasyID3(f)
            except mutagen.id3.ID3NoHeaderError:
                tags = mutagen.File(f, easy=True)
                tags.add_tags()
            tags['title'] = title
            tags['album'] = album
            tags['artist'] = artist
            tags['date'] = year.__str__()
            tags.save()

            audio = MP3(f, ID3=ID3)
            audio.tags.add(
                APIC(
                    encoding=0,
                    mime='image/jpeg',
                    type=3,
                    desc=u'Cover',
                    data=open(path + f'{artist}/{vr_album}/cover.jpeg', 'rb').read()
                )
            )
            audio.save()

            print('Succes!')
    else:
        os.makedirs(path + f'{artist}/{vr_album}/')
        client.tracks(track.id)[0].download_cover(path + f'{artist}/{vr_album}/cover.jpeg', '1000x1000')

        track.fetch_track().download(f)
        try:
            tags = EasyID3(f)
        except mutagen.id3.ID3NoHeaderError:
            tags = mutagen.File(f, easy=True)
            tags.add_tags()
        tags['title'] = title
        tags['album'] = album
        tags['artist'] = artist
        tags['date'] = year.__str__()
        tags.save()

        audio = MP3(f, ID3=ID3)
        audio.tags.add(
            APIC(
                encoding = 0,
                mime = 'image/jpeg',
                type=3,
                desc=u'Cover',
                data=open(path + f'{artist}/{vr_album}/cover.jpeg', 'rb').read()
            )
        )
        audio.save()

        print('Succes!')
print('THE END!!!')