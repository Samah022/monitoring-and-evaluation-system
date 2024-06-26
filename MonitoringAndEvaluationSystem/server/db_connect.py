# Method-1: use sqllite3
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import sqlite3

db = sqlite3.connect("monitoring-and-evaluation.db")
cr = db.cursor()


engine = create_engine("sqlite:///monitoring-and-evaluation.db")
Session = sessionmaker(bind=engine)
session = Session()
