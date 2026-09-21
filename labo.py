from sqlalchemy import create_engine, Column , String , Float, Integer
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from fastapi import FastAPI, Response, Cookie
from pydantic import BaseModel
import bcrypt
import jwt
from datetime import datetime, timezone, timedelta

app = FastAPI()

secret = '201caf45bd9c982fc68dbd9c801e5588288db75f4d2a51c08bc4dc05fd0e873286f122'

engine = create_engine('sqlite:///mon_banque.db')
base = declarative_base()
Session = sessionmaker(engine)
session = Session()

class Mon_compte(base):
	__tablename__='Mon_compte'
	id=Column(Integer, primary_key=True)
	nom=Column(String)
	password=Column(String)
	Solde=Column(Float)

#base.metadata.drop_all(engine)		
base.metadata.create_all(engine)


class personne(BaseModel):
	nom:str
	password:str
	solde:int
	
@app.post('/inscription')
def inscription(response:Response, donnee:personne):
	if not donnee:
		return "veullez vous s'inscrire"
	password = bcrypt.hashpw(donnee.password.encode(), bcrypt.gensalt())
	compte = Mon_compte(nom=donnee.nom, password=password,Solde=10000)
	session.add(compte)
	session.commit()
	return 'compte cree avec succes'

class personne(BaseModel):
	nom:str
	password:str
	solde:int
	
@app.post('/connextion')
def connextion(response:Response, donnee:personne):
	if not donnee:
		return 'veuiller vous idendifier'
	compte = session.query(Mon_compte).filter_by(nom=donnee.nom).first()
	password = bcrypt.checkpw(donnee.password.encode(), compte.password)
	if not compte and not password:
		return 'identifiant incorect'
	expiration = datetime.now(timezone.utc) + timedelta(minutes=30)
	payload= {'id':compte.id, 'exp':expiration}
	token = jwt.encode(payload, secret, algorithm='HS256')
	response.set_cookie(key='token', value=token, httponly=True)	
	return 'bienvenue'
	
@app.post('/deconnextion')
def connextion(response:Response,token:str=Cookie(None)):
	if not token:
		return "vous n'avez pas de token"
	response.delete_cookie(key='cookie')
	return 'cookie suprimer'
	
@app.get('/Mon_compte')
def compte(token:str=Cookie(None)):
	if not token:
		return 'vous navez pas de token'
	payload = jwt.decode(token, secret, algorithms=['HS256'])
	id = payload['id']
	compte = session.query(Mon_compte).filter_by(id = id).first()
	if not compte:
		return 'veuillez vous inscrire'	
	return {'nom':compte.nom, 'id':compte.id, 'solde':compte.Solde}

class montant(BaseModel):
	montant:int	
	
@app.post('/retrait')
def retrait(montant:montant,token:str=Cookie(None)):
	if not token:
		return 'token invalide'
	if montant < 0:
		return 'solde negatig'
	payload = jwt.decode(token, secret, algorithms=['HS256'])
	id = payload['id']
	compte = session.query(Mon_compte).filter_by(id=id).first()
	if compte.solde > montant.montant:
		compte.solde -=montant.montant
		session.commit()
		return 'succes'
	return 'solde negatif'

class montant(BaseModel):
	montant:int
	nom_destinataire:str
	
@app.post('/transfert')
def transfert(donnee:montant, token:str=Cookie(None), ):
	if not token :
		return 'pas de token'
	if donnee.montant < 0:
		return 'solde negatif'
	payload = jwt.decode(token,secret,algorithms=['HS256'])
	id = payload['id']
	compte = session.query(Mon_compte).filter_by(id=id).first()
	destinataire = session.query(Mon_compte).filter_by(nom=donnee.nom_destinataire).first()
	if not destinataire:
		return 'destinataire introuvable'
	try:
		compte.solde -=donnee.montant
		destinataire.solde +=donnee.montant
		session.commit()
		return 'succes'
	except:
		session.Rollback()
		return 'erreur'
