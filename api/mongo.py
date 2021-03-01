from pymongo import MongoClient
from pprint import pprint
from Lesson2 import hh

client = MongoClient('127.0.0.1', 27017)
db = client['jobs_database']
jobs_data = db.jobs_data


# dicts = hh('C++', 1)

# jobs_data.insert_many(dicts)

# for job in jobs_data.find({}):
#     pprint(job)


def find_min_salary(min_salary):
    for job in jobs_data.find({'$or': [{'salary_min': {'$gte': min_salary},
                                       'salary_max': {'$gte': min_salary}}]}):
        pprint(job)


def new_jobs_to_db(jobs):
    c = 0
    for job in jobs:
        if jobs_data.count_documents({'link': job['link']}) == 0:
            db.jobs_data.insert_one(job)
            c += 1
    print(f"{c} ваканий добавлено в базу данных")


find_min_salary(100000)
new_jobs_to_db(hh('html', 1))
