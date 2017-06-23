import random
import faker

FAKE = faker.Faker()
MALE = 'male'
FEMALE = 'female'

class Person:

    @staticmethod
    def boy():
        return Person(MALE)

    @staticmethod
    def girl():
        return Person(FEMALE)

    @staticmethod
    def make():
        return Person(random.choice([MALE, FEMALE]))

    def __init__(self, gender):
        self.gender = gender
        self.name = FAKE.name_male() if self.gender == MALE else FAKE.name_female()

    def is_male(self):
        return self.gender == MALE

    def is_female(self):
        return self.gender == FEMALE

    def __hash__(self):
        return hash((self.gender, self.name))

    def __repr__(self):
        return f'Person({self.gender}, {self.name})'
