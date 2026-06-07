# script_hash.py — à lancer une seule fois puis supprimer
import bcrypt
from database import get_connection

comptes = [
    ("admin@educaterra.fr", "admin123"),
    ("formateur@educaterra.fr", "form123"),
    ("apprenant@educaterra.fr", "app123"),
]

conn = get_connection()
curseur = conn.cursor()

for email, mdp in comptes:
    hache = bcrypt.hashpw(mdp.encode('utf-8'), bcrypt.gensalt())
    curseur.execute("UPDATE utilisateurs SET mot_de_passe = %s WHERE email = %s", (hache, email))

conn.commit()
conn.close()
print("Mots de passe hachés avec succès !")