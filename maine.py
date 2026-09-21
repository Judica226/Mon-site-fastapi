from fastapi import FastAPI, Request, Form, Cookie, Depends, status
import jwt
from fastapi.responses import RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from banque import Compte, Banque, session
from datetime import datetime , timezone, timedelta
import bcrypt
secret='i8x0sks5l1l8'

app = FastAPI()
@app.get("/")
def read_root():
    # Cela redirigera automatiquement l'utilisateur vers /connexion
    return RedirectResponse(url="/connexion")

templates = Jinja2Templates(directory='templates')

@app.get('/inscription')
def inscription(request:Request):
	return templates.TemplateResponse(request, name='inscription.html') #context={'request':request})
	
@app.post('/inscription')
def inscription(nom:str=Form(...), password:str=Form(...)):
	banques = session.query(Banque).first()
	if not banques:
		banques= Banque(nom='Coris_banque', solde=100000, etat=True)
	session.add(banques)
	passworde = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
	compte = Compte(proprietaire=nom, solde=10000,password=passworde, banques=banques)
	session.add(compte)
	session.commit()
	return RedirectResponse('/connexion', status_code=status.HTTP_302_FOUND)

@app.get('/connexion')
def connexion(request:Request):
	print(request.cookies)
	return templates.TemplateResponse(request, name='connexion.html')

@app.post('/connexion')
def connextion(response:Response,nom:str=Form(...), password:str=Form(...)):
	compte = session.query(Compte).filter_by(proprietaire=nom).first()
	if not compte:
		return RedirectResponse('/inscription',status_code=status.HTTP_302_FOUND)
	passworde = bcrypt.checkpw(password.encode(), compte.password)
	if passworde:
		expiration=datetime.now(timezone.utc) + timedelta(minutes=30)
		payload = {'id':compte.id, 'exp':expiration}
		token = jwt.encode(payload,secret, algorithm='HS256')
		response=RedirectResponse('/home', status_code=status.HTTP_302_FOUND)
		response.set_cookie(key='acces', value=token, httponly=True)
		return response
	return RedirectResponse('/connexion', status_code=status.HTTP_302_FOUND)

def get_current_user(acces:str=Cookie(None)):
	print('cookie=',acces)
	if not acces:
		return None
	token= jwt.decode(acces, secret, algorithms=['HS256'])
	print("PAYLOAD :", token)
	utilisateur = session.query(Compte).filter_by(id=token['id']).first()
	print("UTILISATEUR :", utilisateur)
	if not utilisateur:
		return 'compte inexistant'
	return utilisateur
	
#@app.get('/home')
#def home(request:Request):
#	return templates.TemplateResponse(request, name='home.html')
@app.get('/home')	
def home(request:Request, utilisateur=Depends(get_current_user)):
	if not utilisateur:
		return RedirectResponse('/connexion',status_code=302)
	return templates.TemplateResponse(request, name='home.html', context={'nom':utilisateur.proprietaire})
	
@app.get('/solde')
def solde(request:Request, utilisateur=Depends(get_current_user)):
	if not utilisateur:
		return RedirectResponse('/connexion',status_code=302)
	return templates.TemplateResponse(request, name='solde.html', context={'solde':utilisateur.solde})

@app.get('/deconnexion')
def deconnexion():
	response = RedirectResponse('/connexion', status_code=302)
	response.delete_cookie('acces')
	return response
	
@app.get('/profil')
def profil(request:Request,utilisateur=Depends(get_current_user)):
	if not utilisateur:
		return RedirectResponse('/connexion',status_code=302)
	return templates.TemplateResponse(request, name='profil.html', context={'nom':utilisateur.proprietaire,'solde':utilisateur.solde})
	
@app.get('/users')
def utilisateur(request:Request):
	compte = session.query(Compte).all()
	return templates.TemplateResponse(request, name='utilisateur.html',context={'utilisateurs':compte})
	
@app.get('/utilisateur/{id}')
def profil(id:int, request:Request):
	utilisateur = session.query(Compte).filter_by(id=id).first()
	return templates.TemplateResponse(request, name='profil_utilisateur.html', context={'utilisateur':utilisateur})