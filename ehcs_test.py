from EHCS import EHCS

stemmer = EHCS()
terms = [line.rstrip('\n') for line in open('term.txt')]
for t in terms:
    print(t)
    print(stemmer.process(t)['stem'])
