import customtkinter as ctk
from database import get_connection

class Dashboard(ctk.CTkToplevel):
    def __init__(self, parent, utilisateur):
        super().__init__(parent)
        self.utilisateur = utilisateur
        self.title("Mon tableau de bord")
        self.geometry("650x500")

        ctk.CTkLabel(self, text="Mon tableau de bord",
                     font=ctk.CTkFont(size=18, weight="bold")).pack(pady=15)

        self.zone = ctk.CTkTextbox(self, width=600, height=400)
        self.zone.pack(padx=20, pady=10)
        self.zone.configure(state="disabled")

        self.charger_dashboard()

    def charger_dashboard(self):
        conn = get_connection()
        curseur = conn.cursor(dictionary=True)

        # Nombre de quiz passés et score moyen
        curseur.execute(
            "SELECT COUNT(*) as nb, AVG(score) as moyenne FROM resultats_quizz WHERE id_apprenant = %s",
            (self.utilisateur['id'],)
        )
        stats_quiz = curseur.fetchone()

        # Activités pratiquées
        curseur.execute(
            "SELECT sport, evaluation FROM activites WHERE id_apprenant = %s ORDER BY date_pratique DESC LIMIT 5",
            (self.utilisateur['id'],)
        )
        activites = curseur.fetchall()

        # Nombre de cours disponibles
        curseur.execute("SELECT COUNT(*) as nb FROM cours")
        nb_cours = curseur.fetchone()

        conn.close()

        self.zone.configure(state="normal")
        self.zone.delete("1.0", "end")

        self.zone.insert("end", "═══ STATISTIQUES ═══\n\n")

        nb_quiz = stats_quiz['nb'] or 0
        moyenne = round(stats_quiz['moyenne'], 1) if stats_quiz['moyenne'] else 0
        self.zone.insert("end", f"📝 Quiz passés : {nb_quiz}\n")
        self.zone.insert("end", f"📊 Score moyen : {moyenne}%\n")
        self.zone.insert("end", f"📚 Cours disponibles : {nb_cours['nb']}\n\n")

        self.zone.insert("end", "═══ DERNIÈRES ACTIVITÉS ═══\n\n")
        if activites:
            for a in activites:
                self.zone.insert("end", f"🏃 {a['sport']} — {a['evaluation']}\n")
        else:
            self.zone.insert("end", "Aucune activité enregistrée.\n")

        self.zone.configure(state="disabled")