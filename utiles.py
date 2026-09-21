class Hero:
	def __init__(self, nom):
		self.nom=nom
		self.pv=100
	def afficher_profil(self):
		print(f'nom >> {self.nom} : vie >> {self.pv}' )