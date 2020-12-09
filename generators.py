import random


class BaseGenerator:

    def reset(self):
        raise NotImplementedError

    def generate(self):
        raise NotImplementedError

class RandomStringGenerator(BaseGenerator):
    letters_alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    digits_alphabet = '0123456789'
    specsymbols_alphabet = '.,/?!@#$%^&*():;\'"|\\'

    def __init__(self, length=16, use_letters=True,
                 use_digits=True, use_specsymbols=False):
        self.length = length
        self.use_letters = use_letters
        self.use_digits = use_digits
        self.use_specsymbols = use_specsymbols
        print('Init:', length, use_letters, use_digits, use_specsymbols)

    def reset(self):
        pass

    def generate(self):
        alphabet = ''
        if self.use_letters:
            alphabet += self.letters_alphabet
        if self.use_digits:
            alphabet += self.digits_alphabet
        if self.use_specsymbols:
            alphabet += self.specsymbols_alphabet
        if not alphabet:
            print('Empty alphabet')
            return

        s = ''
        for i in range(self.length):
            s += random.choice(alphabet)
        return s


class PopularStringGenerator(BaseGenerator):

    def __init__(self, filepath='popular.txt', limit=1000):
        self.counter = 0
        self.filepath = filepath
        self.limit = limit
        with open(filepath) as f:
            self.passwords = f.read().split('\n')[:limit]
        print('Init PopularStringGenerator:', filepath, limit)

    def reset(self):
        self.counter = 0

    def generate(self):
       if self.counter >= self.limit:
           return
       password = self.passwords[self.counter]
       self.counter += 1
       return password

class BruteForceGenerator(BaseGenerator):

    def __init__(self, alphabet='0123456789abcdefghijklmnopqrstuvwxyz', length=0):
        self.counter = 0
        self.length = length
        self.start_length = length
        self.alphabet = alphabet
        self.base = len(alphabet)
        print('Init BruteForceGenerator:', length, alphabet)

    def reset(self):
        self.counter = 0
        self.length = self.start_length

    def generate(self):
        # counter -> str at base -> password
        # 1000 == 62 * 16 + 8 == (3 * 16 + 14) * 16 + 8 -> 3(14)8 == 3E8
        password = ''
        number = self.counter
        while number > 0:
            # counter = x * base + rest
            x = number // self.base
            rest = number % self.base
            password = self.alphabet[rest] + password
            number = x
        while len(password) < self.length:
            password = self.alphabet[0] + password
        # check password
        print(self.length, self.counter, password)

        if self.alphabet[-1] * self.length == password:
            self.length += 1
            self.counter = 0
        else:
            self.counter += 1

        return password

class LoginGenerator(BaseGenerator):
    default_logins = ['admin', 'jack', 'cat']

    def __init__(self, logins=None):
        self.counter = 0
        if logins is None:
            self.logins = self.default_logins
        else:
            self.logins = logins
        print('Init LoginGenerator:', self.logins)

    def reset(self):
        self.counter = 0

    def generate(self):
       if self.counter >= len(self.logins):
           return
       login = self.logins[self.counter]
       self.counter += 1
       return login