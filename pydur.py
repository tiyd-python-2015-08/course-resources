import random

students = '''Robert Amand
Ryan Burton
William Butts
Jonathan Frederick
Adam Hartz
Glenn Hurley
Karthik Kasala
Jermaine Kee
Michael Krawiec
Tyler Kotkin
Andrew Pierce
Kathleen Rauh'''

# turn into a list
students = students.split('\n')


def get_pairings(students):
    return list({
        frozenset((s1, s2))
        for s1 in students
        for s2 in students
        if s1 != s2
    })


def get_random_pairs(students):
    ret = []
    pairings = get_pairings(students)
    while len(pairings) > 0:
        this_pair = random.choice(pairings)
        ret.append(this_pair)
        for pair in pairings[:]:
            if not this_pair.isdisjoint(pair):
                pairings.remove(pair)
    return ret
