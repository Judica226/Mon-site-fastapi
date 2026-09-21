from donnee import engine , base , session, Column, Integer, String, ForeignKey, Float, relationship, Boolean
from donnee import hashe, dehashe
import bcrypt
class solde_insufisant(Exception):
	pass

def ransomware(fonction):
	def modifier(*args,**kwargs):
		print('___Ransomaware____')
		print('veuiller paye le rancon 20f > oui/non')
		choix=input('veuiller taper votre choix: ')
		if choix == 'oui':
			hacker = 20
			resultat= fonction(*args,**kwargs)
			print('exelent choix')
			return f'votre solde est: {resultat - hacker}'
		else:
			print('mauvais choix')
			return 'votre solde est 00f'
	return modifier

class Banque(base):
	__tablename__='banque'
	id = Column(Integer, primary_key=True)
	nom=Column(String)
	solde=Column(Float)
	etat = Column(Boolean)
	
class Compte(base):
	__tablename__='compte'
	id = Column(Integer, primary_key=True)
	proprietaire=Column(String)
	solde=Column(Float)
	dette = Column(Float)
	transaction=Column(String)
	password=Column(String)
	id_banque=Column(Integer, ForeignKey('banque.id'))
	
	banques= relationship('Banque', backref='compte')

#base.metadata.drop_all(engine)
base.metadata.create_all(engine)

#@ransomware
def consulter(nom):
	compte = session.query(Compte).filter_by(proprietaire=nom).first()
	print(f'Votre solde est {compte.solde}')
	print(f'_____________________________')


def dette(nom):
	somme = int(input('taper la.somme a emprunter: : '))
	compte = session.query(Compte, Banque).filter_by(proprietaire=nom).join(Banque).first()
	if somme >0 and compte[1].solde >= somme and compte[1].etat == True:
		compte[0].solde += somme
		compte[0].dette +=somme
		compte[1].solde -=somme
		print('reussi avec succes')
		print('_________________________')
		mot = f'emprunt: de {nom} somme {somme} | '
		compte[0].transaction +=mot
		session.commit()
	else:
		print('saisie incorect ou banque refus')

def transfert(nom):
	compte = input('taper le nom du compte a transferer: ')
	somme = int(input('taper la somme a transferer: '))
	comptes= session.query(Compte).all()
	me = session.query(Compte).filter_by(proprietaire=nom).first()
	for compt in comptes:
		if compt.proprietaire == compte and me.solde >= somme:
			passworde = input('taper votre mot de passe pour confirmer:  ')
			if  dehashe(passworde,me.password) and somme >0 and me.banques.etat == True:
				compt.solde +=somme
				me.solde -=somme
				mot = f'{me.proprietaire} a transferer {somme} a {compt.proprietaire} || '
				me.transaction +=mot
				compt.transaction +=mot
				session.commit()
				return f'vous avez transfere {somme} a {compt.proprietaire}'
			return 'mot de passe incorect ou somme invalide ou verifier letat de la banque'
		print(f'proprietaire: {compt.proprietaire} etranger: {compte}')
	return 'le compte nexiste pas ou verifier votre solde'
		

def savoir_plus(choi):
	resultat= session.query(Banque,Compte).join(Compte).filter_by(proprietaire=choi).first()
	print(f'nom: {resultat[1].proprietaire} solde: {resultat[1].solde}f dette: {resultat[1].dette}f >> banque: {resultat[0].nom} {resultat[0].solde}')
	print(f''''_______Transaction_______
{resultat[1].transaction} ||  ''')

def afficher():
	tous = session.query(Compte).all()
	for e in tous:
		print(e.proprietaire, e.password)
		
def suprimer():
	compte = input('taper le nom du compte a suprimer: ')
	recupere = session.query(Compte).filter_by(proprietaire=compte).first()
	if recupere:
		session.delete(recupere)
		print('suprimer avec suces')
		session.commit()
	else:
		print('compte introuvable')

def savoir_tous():
	resultate= session.query(Banque,Compte).join(Compte).all()
	for resultat in resultate:
		print(f'nom: {resultat[1].proprietaire} solde: {resultat[1].solde}f dette: {resultat[1].dette}f >> banque: {resultat[0].nom} {resultat[0].solde}')
		print(f''''_______Transaction_______
{resultat[1].transaction}''')

def verifier():
	banque = session.query(Banque).first()
	if banque.etat == True:
		return 'votre Banque est disponible'
	return "banque n'est pas disponible"

def savoir_banque():
	banque = session.query(Banque).first()
	nombre = banque.compte
	print(f'nom: {banque.nom} > solde: {banque.solde} > Etat: {banque.etat} >> nombre de comptes >> {len(nombre)}')

def controller():
	print('''
1: Allumer 
2: etteindre 
3: rien''')
	banque = session.query(Banque).first()
	choix = input('taper votre choix: ')
	if choix == '1':
		banque.etat = True
		return 'Banque allumer'
		session.commit()
	elif choix == '2':
		banque.etat = False
		return 'Banque etteint'
		session.commit()
	else:
		print()
session.commit()

def payer_dette(nom,somme):
	me = session.query(Compte,Banque).filter_by(proprietaire=nom).join(Banque).first()
	if somme > 0 and somme <= me[0].dette :
		me[0].solde -=somme
		me[0].dette -=somme
		me[1].solde += somme
		print(f'dette paye avec succes il reste {me[0].dette} dette')
		mot = f'|| dette de {somme} rembourser || '
		me[0].transaction +=mot
		session.commit()
	else:
		print('solde negatif ou verifier bien votre dette')

#compte = session.query(Compte).all()
#for c in compte:
#	print(c.proprietaire, c.password)