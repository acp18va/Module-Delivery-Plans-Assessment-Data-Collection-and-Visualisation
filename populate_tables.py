from datetime import datetime
from adc.application import *

import drop_tables
import create_tables

# users.
users = [User(name="John Cena", usertype=UserType.LTM, email="john.cena@sheffield.ac.uk"),
         User(name="User1", usertype=UserType.ACADEMIC, email="user.1@sheffield.ac.uk"),
         User(name="User2", usertype=UserType.TUTOR, email="user.2@sheffield.ac.uk")]

# modules.
modules = [Module(code="COM1", name="Module1", semester=Semester.BOTH, academic=1)]

# assessments.
Assessment(format=AssessmentFormat.MOLE_QUIZ, name="Assessment1/2", marks=50, release_date=datetime.strptime("01/03/19 10:00","%d/%m/%y %H:%M"), submission_date=datetime.strptime("01/04/19 23:59","%d/%m/%y %H:%M"), module=modules[0])
Assessment(format=AssessmentFormat.MOLE_QUIZ, name="Assessment2/2", marks=50, release_date=datetime.strptime("01/05/19 10:00","%d/%m/%y %H:%M"), submission_date=datetime.strptime("01/06/19 23:59","%d/%m/%y %H:%M"), module=modules[0])

# add to session.
for user in users:
    db.session.add(user)
for module in modules:
    db.session.add(module)

db.session.commit()
