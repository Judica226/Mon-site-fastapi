from banque import solde_insufisant, ransomware, Banque , Compte, consulter,suprimer, dette, transfert, session, savoir_plus, afficher,savoir_tous, verifier, savoir_banque, controller, payer_dette
from donnee import hashe, dehashe
from loisir import affichage, casino
import bcrypt

print('''____voici le Menu____
1: s'inscrire
2: Se connecter ''')

choix = input('___Taper votre choix___: ')
if choix == '1':
	print('Veuiller vous inscrire')
	nom = input('taper votre nom: ')
	passworde= input('taper votre mot de passe: ')
	banque_exist = session.query(Banque).first()
	if banque_exist:
		Banque_n= banque_exist
	else:
		Banque_n= Banque(nom='Coris Banque', solde=150000, etat=True)
		session.add(Banque_n)
		session.commit()
	passe = hashe(passworde)
	compte =Compte(proprietaire=nom,solde=1000, dette=0, transaction='',password = passe, banques=Banque_n)
	session.add(compte)
	session.commit()
	print('Compte cree avec succes')
	print('_________________________')
	
	
	while True:
		print('''1: consulter solde
2: prendre une dete
3: transfert d'argent
4: verifier l'etat de la banque
5: en savoir plus sur mon compte:
6: Jouer au casino
7: payer votre dette
8: Quitter ''')

		choix = input('taper votre choix: ')
		try:
			if choix == '1':
				consulter(nom)
			elif choix == '2':
				dette(nom)
			elif choix == '3':
				transfert(nom)
			elif choix == '4':
				print(verifier())
				print('______________________')
			elif choix == '5':
				savoir_plus(nom)
			elif choix == '6':
				while True:
					resultat = affichage()
					if resultat == '1':
						casino(nome, passworde)
					elif resultat == '2':
						print('retour au menu principal')
			elif choix == '7':
				somme = int(input('taper somme a rembourser: '))
				payer_dette(nom, somme)
			elif choix == '8':
				print('Compte deconnecter...')
				break
			else:
				print('choix indisponible')
		except :
			print('Erreur de formulaire')
elif choix == '2':
	nome= input('taper le nom: ')
	passworde= input('taper le mot de passe: ')
	comptes = session.query(Compte).all()
	for compte in comptes:
		if nome == 'admin' and passworde == '2020':
			print('____________________')
			print('vous ete connecter en tant que administrateur')
			print('________________________')
			while True:
				print('''
____Voici le menu____
1: voir tous les compte 
2: suprimer un compte 
3: savoir plus sur tous les comptes
4: savoir plus sur la banque
5: Controler la banque
6: Quitter''')
				choix = input('taper votre choix: ')
				if choix == '1':
					afficher()
				elif choix == '2':
					suprimer()
				elif choix == '3':
					print(savoir_tous())
				elif choix == '4':
					savoir_banque()
				elif choix == '5':
					print(controller())
					session.commit()
				elif choix == '6':
					print('retour au programme principal')
					break
		elif compte.proprietaire == nome and dehashe(passworde,compte.password) == True:
			print('connection reussi')
			print('____________________')
			while True:
				print()
				print('''1: consulter solde
2: prendre un dette
3: transfert d'argent
4: verifier l'etat de la banque
5: en savoir plus sur mon compte:
6: Jouer au Casino
7 : payer votre dette
8: Quitter ''')
				choix = input('taper votre choix: ')
				try:
					if choix == '1':
						consulter(nome)
					elif choix == '2':
						dette(nome)
					elif choix == '3':
						print(transfert(nome))
					elif choix == '4':
						print(verifier())
						print('__________')
					elif choix == '5':
						savoir_plus(nome)
					elif choix == '6':
						while True:
							resultat = affichage()
							if resultat == '1':
								casino(nome, passworde)
							elif resultat == '2':
								print('retour au menu principal')
								break
					elif choix == '7':
						somme = int(input('taper somme a rembourser: '))
						payer_dette(nome, somme)
					elif choix == '8':
						print('Compte deconnecter...')
						break
					else:
						print('choix indisponible')
				except Exception as e :
					print(f'nous avons rencontrer une erreur {e}')
	print('compe introuvable')
else:
	print('Choix invalide')
			
				

