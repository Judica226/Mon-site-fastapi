from fastapi import FastAPI, Form, Response, Cookie, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from banque import Compte, session, Banque
from datetime import datetime, timedelta, timezone  # Correction de la virgule ici
from donnee import hashe, dehashe
import jwt

app = FastAPI()
secret = '1234'

# ==========================================
# 1. ESPACE INSCRIPTION (GET & POST)
# ==========================================

@app.get('/inscription')
def page_inscription():
    html_code = """<!DOCTYPE html>
<html lang="fr"><head><meta charset="UTF-8"><title>Coris Banque - Inscription</title>
<style>
    * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', sans-serif; }
    body { min-height: 100vh; display: flex; justify-content: center; align-items: center; background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); }
    .login-card { background-color: #ffffff; padding: 40px; border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); width: 100%; max-width: 400px; }
    .login-card h2 { color: #1e3c72; text-align: center; margin-bottom: 24px; font-size: 28px; }
    .input-group { margin-bottom: 20px; }
    .input-group label { display: block; margin-bottom: 8px; color: #333; font-weight: 600; font-size: 14px; }
    .input-group input { width: 100%; padding: 12px 16px; border: 2px solid #e1e8f0; border-radius: 8px; font-size: 15px; outline: none; }
    .btn-submit { width: 100%; padding: 12px; background: linear-gradient(135deg, #2a5298 0%, #1e3c72 100%); color: white; border: none; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer; }
    .switch-action { text-align: center; margin-top: 25px; padding-top: 15px; border-top: 1px solid #f0f2f5; font-size: 14px; color: #666; }
    .switch-action a { color: #2a5298; text-decoration: none; font-weight: bold; }
</style>
</head>
<body>
    <div class="login-card">
        <h2>Créer un Compte</h2>
        <form action="/inscription" method="POST">
            <div class="input-group">
                <label for="nom">Nom d'utilisateur</label>
                <input type="text" id="nom" name="nom" placeholder="Choisissez un nom" required>
            </div>
            <div class="input-group">
                <label for="password">Mot de passe</label>
                <input type="password" id="password" name="password" placeholder="Créez un mot de passe" required>
            </div>
            <button type="submit" class="btn-submit">S'inscrire</button>
        </form>
        <div class="switch-action">Déjà client ? <a href="/connexion">Se connecter</a></div>
    </div>
</body></html>"""
    return HTMLResponse(content=html_code)


@app.post('/inscription')
def traitement_inscription(nom: str = Form(...), password: str = Form(...)):
    compte = Compte(proprietaire=nom, password=hashe(password))
    session.add(compte)
    session.commit()
    # Redirection automatique vers la page de connexion après inscription
    return RedirectResponse(url="/connexion", status_code=303)


# ==========================================
# 2. ESPACE CONNEXION (GET & POST)
# ==========================================

@app.get('/connexion')
def page_connexion():
    html_code = """<!DOCTYPE html>
<html lang="fr"><head><meta charset="UTF-8"><title>Coris Banque - Connexion</title>
<style>
    * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', sans-serif; }
    body { min-height: 100vh; display: flex; justify-content: center; align-items: center; background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); }
    .login-card { background-color: #ffffff; padding: 40px; border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); width: 100%; max-width: 400px; }
    .login-card h2 { color: #1e3c72; text-align: center; margin-bottom: 24px; font-size: 28px; }
    .input-group { margin-bottom: 20px; }
    .input-group label { display: block; margin-bottom: 8px; color: #333; font-weight: 600; font-size: 14px; }
    .input-group input { width: 100%; padding: 12px 16px; border: 2px solid #e1e8f0; border-radius: 8px; font-size: 15px; outline: none; }
    .btn-submit { width: 100%; padding: 12px; background: linear-gradient(135deg, #2a5298 0%, #1e3c72 100%); color: white; border: none; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer; }
    .switch-action { text-align: center; margin-top: 25px; padding-top: 15px; border-top: 1px solid #f0f2f5; font-size: 14px; color: #666; }
    .switch-action a { color: #2a5298; text-decoration: none; font-weight: bold; }
</style>
</head>
<body>
    <div class="login-card">
        <h2>Espace Connexion</h2>
        <form action="/connexion" method="POST">
            <div class="input-group">
                <label for="nom">Nom d'utilisateur</label>
                <input type="text" id="nom" name="nom" placeholder="Entrez votre nom" required>
            </div>
            <div class="input-group">
                <label for="password">Mot de passe</label>
                <input type="password" id="password" name="password" placeholder="Entrez votre mot de passe" required>
            </div>
            <button type="submit" class="btn-submit">Se connecter</button>
        </form>
        <div class="switch-action">Nouveau client ? <a href="/inscription">Créer un compte</a></div>
    </div>
</body></html>"""
    return HTMLResponse(content=html_code)


@app.post('/connexion')
def traitement_connexion(nom: str = Form(...), password: str = Form(...)):
    resultat = session.query(Compte).filter_by(proprietaire=nom).first()
    
    if resultat and dehashe(password, resultat.password):
        expiration = datetime.now(timezone.utc) + timedelta(hours=1)
        donnee = {'nom': nom, 'exp': expiration}
        token = jwt.encode(donnee, secret, algorithm='HS256')
        
        # On redirige directement vers le tableau de bord (/home) en injectant le cookie
        reponse_finale = RedirectResponse(url="/home", status_code=303)
        reponse_finale.set_cookie(key="badge_banque", value=token, httponly=True)
        return reponse_finale
        
    return HTMLResponse("<h2>Identifiants incorrects. <a href='/connexion'>Réessayer</a></h2>", status_code=401)


# ==========================================
# 3. NOUVEL ESPACE : TABLEAU DE BORD (HOME)
# ==========================================

@app.get('/home')
def page_home(badge_banque: str = Cookie(None)):
    # 1. Vérifier si le cookie existe
    if not badge_banque:
        return RedirectResponse(url="/connexion", status_code=303)
    
    try:
        # 2. Décoder le token JWT pour récupérer le nom de l'utilisateur
        donnee = jwt.decode(badge_banque, secret, algorithms=['HS256'])
        nom_utilisateur = donnee['nom']
        
        # 3. Récupérer les informations du compte dans la base de données
        compte = session.query(Compte).filter_by(proprietaire=nom_utilisateur).first()
        if not compte:
            return RedirectResponse(url="/connexion", status_code=303)
            
        # On suppose que ton modèle 'Compte' possède un attribut 'solde' (ex: compte.solde)
        # S'il n'existe pas, remplace par une valeur fictive ou gère-le selon ta BDD
        solde_actuel = getattr(compte, 'solde', 0.0)

    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        # Si le token a expiré ou est corrompu, on redirige vers la connexion
        return RedirectResponse(url="/connexion", status_code=303)

    # 4. Code HTML propre pour le Tableau de Bord
    html_dashboard = f"""<!DOCTYPE html>
<html lang="fr"><head><meta charset="UTF-8"><title>Coris Banque - Tableau de bord</title>
<style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', sans-serif; }}
    body {{ background-color: #f4f6f9; color: #333; }}
    .navbar {{ background: #1e3c72; padding: 15px 30px; color: white; display: flex; justify-content: space-between; align-items: center; }}
    .navbar h1 {{ font-size: 22px; }}
    .navbar .logout-btn {{ background: #e74c3c; color: white; padding: 8px 16px; border-radius: 6px; text-decoration: none; font-weight: bold; }}
    .container {{ max-width: 800px; margin: 50px auto; padding: 20px; }}
    .welcome-card {{ background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
    .welcome-card h2 {{ color: #1e3c72; margin-bottom: 10px; }}
    .solde-box {{ margin-top: 20px; background: #eef2f7; padding: 20px; border-radius: 8px; border-left: 5px solid #2a5298; }}
    .solde-box span {{ font-size: 24px; font-weight: bold; color: #2a5298; }}
</style>
</head>
<body>
    <div class="navbar">
        <h1>Coris Banque E-Space</h1>
        <a href="/deconnexion" class="logout-btn">Se déconnecter</a>
    </div>
    <div class="container">
        <div class="welcome-card">
            <h2>Ravi de vous revoir, {nom_utilisateur} ! 👋</h2>
            <p>Bienvenue sur votre espace bancaire sécurisé.</p>
            
            <div class="solde-box">
                <p>Solde disponible :</p>
                <span>{solde_actuel} FCFA</span>
            </div>
        </div>
    </div>
</body></html>"""
    
    return HTMLResponse(content=html_dashboard)


# ==========================================
# 4. ROUTE FACULTATIVE : DÉCONNEXION
# ==========================================

@app.get('/deconnexion')
def deconnexion():
    # Pour déconnecter, on supprime le cookie en le surchargeant avec une date expirée
    reponse = RedirectResponse(url="/connexion", status_code=303)
    reponse.delete_cookie(key="badge_banque")
    return reponse
