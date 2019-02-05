import pymongo
import random

try:
    conn = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = conn['MusicBox-v1']
    users_collection = mydb['users']
    artists_collection = mydb['artists']
    songs_collection = mydb['songs']
    print('SUCCESS: Connected to MongoDB')
except Exception as e:
    print('ERR: Connection Error - MongoDB\n', e)


def show_collection(collection):
    for x in collection.find():
        print(x)


def add_users(file):
    users_file = open(file, 'r')
    data = []
    gender = ['m', 'f']
    while True:
        t = users_file.readline().split('\t')
        if len(t) <= 1:
            break

        rand = random.randint(0, 1)
        g = gender[rand]

        try:
            data.append({
                '_id': t[0],
                'gender': g if len(t[1]) == 0 else t[1],
                'age': random.randint(18, 30) if len(t[2]) == 0 else t[2],
                'country': 'Ethopia' if len(t[3]) == 0 else t[3]
            })
        except:
            continue

        if len(data) == 500:
            del data[0]
            # users_collection.insert_many(data)
            for i in data:
                users_collection.insert_one(i)
            data = []

    if len(data) > 0: del data[0]
    users_collection.insert_many(data)


def add_music(file):
    users_file = open(file, 'r', encoding="utf8")
    artists = {}
    songs = {}
    while True:
        t = users_file.readline().split('\t')
        if len(t) <= 1:
            break

        try:
            print(t[0])

            if t[2] in artists:
                if t[4] not in artists[t[2]]['songs']:
                    artists[t[2]]['songs'].append(t[4])
            else:
                artists[t[2]] = {
                    '_id': t[2],
                    'name': t[3],
                    'songs': [t[4]]
                }
            if t[4] in songs:
                if t[0] not in songs[t[4]]['users']:
                    songs[t[4]]['users'].append(t[0])
                    songs[t[4]]['count'] += 1
            else:
                songs[t[4]] = {
                    '_id': t[4],
                    'name': t[5],
                    'artist_id': t[2],
                    'users': [t[0]],
                    'count': 1
                }
            users_collection.find_one_and_update({'_id': t[0]},{'$push': {'songs': t[4]}})

        except Exception as e:
            print('ERR', e, '\n', t)

    for key in artists.values():
        artists_collection.insert_one(key)
    for key in songs.values():
        songs_collection.insert_one(key)


def main():
    add_users('lastfm-dataset/userid-profile.tsv')
    # show_collection(artists_collection)
    add_music('lastfm-dataset/songs.tsv')


if __name__ == '__main__':
    main()
