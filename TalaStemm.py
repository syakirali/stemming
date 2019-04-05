
class TalaStemmFactory:
    def __init__(self):
        stopword = [line.rstrip('\n') for line in open('stopword.txt')]
        self.stopword = stopword

    def getTalaStemmer(self):
        return TalaStemmer(self.stopword)

class TalaStemmer:
    awalan1 = [
        ['meng',  ''],  ['menya', 's'], ['menyi', 's'], ['menyu', 's'], ['menye', 's'],
        ['menyo', 's'], ['meny',  's'], ['men',   ''],  ['mema',  'p'], ['memi',  'p'],
        ['memu',  'p'], ['meme',  'p'], ['memo',  'p'], ['mem',   ''],  ['me',    ''],
        ['peng',  ''],  ['penya', 's'], ['penyi', 's'], ['penyu', 's'], ['penye', 's'],
        ['penyo', 's'], ['peny',  's'], ['pen',   ''],  ['pema',  'p'], ['pemi',  'p'],
        ['pemu',  'p'], ['peme',  'p'], ['pemo',  'p'], ['pem',   ''],  ['di',    ''],
        ['ter',   ''],  ['ke',   '']
    ]
    awalan2 = [
        ['ber', ''],    ['bel', ''],    ['be', ''],     ['per', ''],    ['pel', ''],    ['pe', '']
    ]

    akhiran1 = ['lah', 'kah',   'pun']
    akhiran2 = ['nya', 'ku',    'mu']
    akhiran3 = ['kan', 'an',    'i']

    def __init__(self, stopword):
        self.stopword = stopword

    def stem(self, word):
        word, success = self.hilangkanAwalan(self.awalan1, word)
        if (success):
            word, success = self.hilangAkhiran(self.akhiran1, word)
            if not success:
                return word
            word, success = self.hilangAkhiran(self.akhiran2, word)
            if not success:
                return word
            word, success = self.hilangAkhiran(self.akhiran3, word)
            if not success:
                return word
            word, success = self.hilangkanAwalan(self.awalan2, word)
        else:
            word, success = self.hilangkanAwalan(self.awalan2, word)
            word, success = self.hilangAkhiran(self.akhiran1, word)
            word, success = self.hilangAkhiran(self.akhiran2, word)
            word, success = self.hilangAkhiran(self.akhiran3, word)
        return word

    def hilangAkhiran(self, akhiran, word):
        success = False
        for i in akhiran:
            ind = len(i) * -1
            if (word[ind:] == i):
                result = word[:ind]
                if (len(result) > 2):
                    word = result
                    success = True
                    break
        return word, success

    def hilangkanAwalan(self, awalan, word):
        success = False
        for i in awalan:
            ind = len(i[0])
            if (word[:ind] == i[0]):
                result = word[ind:]
                if (len(result) > 2):
                    word = result
                    success = True
                    break
        return word, success
