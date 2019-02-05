from subprocess import call
from setup import songs_collection, users_collection, artists_collection
import math
import random


def init_pop(size):
    cmd = 'shuf -n {size} ./lastfm-dataset/songs.tsv > gen_pop.tsv'.format(size=size)
    call(cmd, shell=True)
    population = []
    users_file = open('gen_pop.tsv', 'r')
    for _ in range(100):
        t = users_file.readline().split('\t')
        population.append(t[4])
    users_file.close()
    return population


def generate_score(population, size):
    return None


def main():
    init_pop(100)
    pass


main()
