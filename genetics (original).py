from subprocess import call
from setup import songs_collection, users_collection, artists_collection
import math
import random


def init_pop(size):
    # call('shuf -n 30 /home/shivam/Desktop/MusicBot/lastfm-dataset/songs.tsv > init-pop.tsv')
    if size == 100:
        file = 'lastfm-dataset/init-pop.tsv'
    else:
        file = 'lastfm-dataset/gen.tsv'
    population = []
    users_file = open(file, 'r')
    for _ in range(100):
        t = users_file.readline().split('\t')
        population.append(t[4])
    return population


def generate_score(population, size):
    score = [0] * size
    i = 0
    for song_id in population:
        song = songs_collection.find_one({"_id": song_id})
        artist = artists_collection.find_one({"songs": song_id})
        if song is None or artist is None:
            continue

        score[i] += math.log10(math.pi * len(song['users'])) * 2.5
        score[i] += math.log10(math.pi * len(artist['songs'])) * 1.3
        score[i] = score[i] ** 2 * random.randrange(10, 90)
        while score[i] > 100:
            score[i] /= 10
        i += 1

    return score


def get_avg_score(score, count):
    score.sort()
    return sum(score[:count])/count


def genetics(population, score, avg):
    pop = []
    for i in range(len(score)):
        if score[i] > (3*avg/2) or score[i] > 45:
            pop.append(population[i])
        if score[i] > (2*avg/3):
            song = songs_collection.find_one({'id': population[i]})
            j = 0
            user_cutoff = 60
            if song is None:
                user_cutoff -= 5
                continue
            for user in song['users']:
                if random.randrange(0, 100) > user_cutoff:
                    j += 1
                    u = users_collection.find_one({'id': user})
                    song_cutoff = 40
                    if u is None:
                        continue
                    for s in u['songs']:
                        if s in None:
                            song_cutoff -= 5
                            continue
                        if random.randrange(0, 100) > song_cutoff:
                            pop.append(s)
                if j == 10:
                    break

    population = pop[:]
    population.extend(init_pop(100 - len(population)))

    return population[int(len(population)/2):int(len(population)/2) + 50]


def main():
    # user_id = 'user_000019'
    population = init_pop(100)  # Contains trackid of 100 songs
    print(population)
    # population = ['3f92576c-4465-49de-8518-ad244857018b', 'f7c1f8f8-b935-45ed-8fc8-7def69d92a10', '340d9a0b-9a43-4098-b116-9f79811bd508', '0b04407b-f517-4e00-9e6a-494795efc73e', 'b79e44f0-2a27-4f50-8a08-ce959a48c9c0', 'f2a38e8c-2eb1-4f47-b3be-bf613153631e', '2f550569-8859-4345-a554-ff698eef3ffe']
    songs_generated = 10
    best_score_avg = 0   # Avg of top songs_generated songs
    score_cutoff = 80
    i = 0
    while best_score_avg < score_cutoff or i <15:
        i += 1
        print("\n-------------------------------\nGeneration Count: ", i)

        print("Generating Score")
        score = generate_score(population, len(population))
        #print("Score Generated: ", score)

        best_score_avg = get_avg_score(score, len(score)) ** score_cutoff % 100
        print("Score Avg: ", best_score_avg)

        print("Generating New Population By Genetics")
        population = genetics(population, score, best_score_avg)
        print("New Population: ", population)

    print("\n\n - | - | - | - | - | - | - | - | - |\n\n")
    for track_id in population[:songs_generated]:
        song = songs_collection.find_one({"_id":track_id})
        if song is not None:
            print(song['name'])

    return population[:songs_generated]
    # Returns top 10 song suggestions


main()

