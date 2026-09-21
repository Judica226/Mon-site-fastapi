import random
from donnee import session, dehashe
from banque import Compte, Banque
def affichage():
	print('''
__voici le menu__
1: Casino
2: Quitter''')
	choix =input('taper votre choix: ')
	return choix

def casino(nom,password):
	verification= session.query(Compte, Banque).filter_by(proprietaire = nom).join(Banque).first()
	if dehashe(password, verification[0].password) and verification[1].etat:
		while True:
			try:
				print('__Veuiller placer le pari__')
				print('Attention vos perte vont agir sut votre solde')
				nombre = int(input('choisisez un nombre entre 1 et 2 .(5) pour quitter: '))
				if nombre == 5:
					print('retour principal')
					break
				randome = random.randint(1,2)
				cote = int(input('taper le cote que vous voulez: '))
				mise = int(input('taper la somme à miser:  '))
				proprietaire = session.query(Compte).filter_by(proprietaire=nom).first()
				if cote * mise <= proprietaire.solde and proprietaire.dette <=1000:
					print('pari accepter✅')
					if nombre == randome:
						r = mise *cote
						proprietaire.solde += r
						print(f'Felicitation vous avez gagner {r}f au Casino 🎉')
						print(f'votre solde est {proprietaire.solde}')
						mot = f'retrait de {mise}f : gagner LOTO: {r}f || '
						proprietaire.transaction +=mot
						session.commit()
					else:
						r = mise * cote
						print(f'😠malheuresement vous avez perdu >> {r}f')
						print(f'la reponse etait {randome}')
						proprietaire.solde -= r
						print(f'votre solde restant est {proprietaire.solde}')
						mot = f'retrait {mise}f : perte: {r}f'
						proprietaire.transaction +=mot
						session.commit()
				else:
					print('votre solde est insuffisant diminuer le cote ou vous ete endetter')		
			except Exception as e:
				print(f'Nous avons constater une erreur veuiller verifier vos formulaire -----{e}')
	else:
		print('veuller verifier vos identifiant ou banque indisponible')

	
