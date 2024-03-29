from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker
from app import Owner,Company,db


def owners(count):
    fake = Faker()
    i = 0
    while i < count:
        owner = Owner(
            firstName = fake.first_name(),
            lastName = fake.last_name(),
            prefix = fake.prefix())
        db.session.add(owner)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()

def company(count):
    fake = Faker()
    i = 0
    while i < count:
        company = Company(
            company = fake.company(),
            motto = fake.catch_phrase(),
            owner_id = randint(0, count))
        db.session.add(company)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()
