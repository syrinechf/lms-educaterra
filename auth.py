import bcrypt
from database import get_connection

# Hacher un mot de passe
def hacher_mot_de_passe(mot_de_passe):
    sel = bcrypt.gensalt()
    hache = bcrypt.hashpw(mot_de_passe.encode('utf-8'), sel)
    return hache

# Vérifier un mot de passe au login
def verifier_mot_de_passe(mot_de_passe, hache):
    return bcrypt.checkpw(mot_de_passe.encode('utf-8'), hache)

# Connexion d'un utilisateur
def connecter_utilisateur(email, mot_de_passe):
    conn = get_connection()
    curseur = conn.cursor(dictionary=True)

    # On cherche l'utilisateur par email
    curseur.execute(
        "SELECT * FROM utilisateurs WHERE email = %s",
        (email,)
    )
    utilisateur = curseur.fetchone()
    conn.close()

    # Si l'utilisateur existe et le mot de passe est correct
    if utilisateur and verifier_mot_de_passe(mot_de_passe, utilisateur['mot_de_passe'].encode('utf-8')):
        return utilisateur  # On retourne toutes les infos de l'utilisateur
    return None  # Échec de connexion