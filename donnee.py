from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float,Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import bcrypt, hashlib

engine = create_engine('sqlite:///Banque.db')
base = declarative_base()
Session = sessionmaker(engine)
session = Session()

def hashe(mot):
    encode = mot.encode()
    hasher = bcrypt.hashpw(encode, bcrypt.gensalt())
    return hasher.decode() 

def dehashe(mot_saisi, hash_stocke_en_base):
    return bcrypt.checkpw(mot_saisi.encode('utf-8'), hash_stocke_en_base.encode('utf-8'))


#ha = hashe('salut')
#print(ha)
#m = 'salut'
#de = dehashe(m.encode(),ha)
#print(de)
	

