import customtkinter as ctk
from database import get_connection
from datetime import date

class ModuleActivites(ctk.CTkToplevel):
    def __init__(self, parent, utilisateur):
        super().__init__(parent)
        self.utilisateur = utilisateur
        self.title("Activités sportives")
        self.geometry("650x500")

        self.onglets = ctk.CTkTabview(self, width=620, height=450)
        self.onglets.pack(padx=15, pady=10)
        self.onglets.add("Ajouter une activité")
        self.onglets.add("Mes activités")

        self.construire_ajout()
        self.construire_liste()

    def construire_ajout(self):
        onglet = self.onglets.tab("Ajouter une activité")

        ctk.CTkLabel(onglet, text="Sport pratiqué").pack(pady=5)
        self.champ_sport = ctk.CTkEntry(onglet, width=400,
                                         placeholder_text="Ex: Football, Natation...")
        self.champ_sport.pack(pady=5)

        ctk.CTkLabel(onglet, text="Évaluation").pack(pady=5)
        self.choix_eval = ctk.CTkOptionMenu(
            onglet,
            values=["Excellent", "Bien", "Satisfaisant", "À améliorer"]
        )
        self.choix_eval.pack(pady=5)

        self.label_activite = ctk.CTkLabel(onglet, text="")
        self.label_activite.pack(pady=5)

        ctk.CTkButton(onglet, text="Enregistrer l'activité",
                      command=self.ajouter_activite).pack(pady=10)

    def ajouter_activite(self):
        sport = self.champ_sport.get().strip()
        evaluation = self.choix_eval.get()

        if not sport:
            self.label_activite.configure(
                text="Saisissez un sport.", text_color="red")
            return

        try:
            conn = get_connection()
            curseur = conn.cursor()
            curseur.execute(
                "INSERT INTO activites (id_apprenant, sport, date_pratique, evaluation) VALUES (%s, %s, %s, %s)",
                (self.utilisateur['id'], sport, date.today(), evaluation)
            )
            conn.commit()
            conn.close()
            self.label_activite.configure(
                text="Activité enregistrée !", text_color="green")
            self.champ_sport.delete(0, "end")
            self.charger_activites()
        except Exception as e:
            self.label_activite.configure(text=f"Erreur : {e}", text_color="red")

    def construire_liste(self):
        onglet = self.onglets.tab("Mes activités")

        ctk.CTkButton(onglet, text="Rafraîchir",
                      command=self.charger_activites).pack(pady=8)

        self.zone_activites = ctk.CTkTextbox(onglet, width=580, height=350)
        self.zone_activites.pack()
        self.zone_activites.configure(state="disabled")

        self.charger_activites()

    def charger_activites(self):
        conn = get_connection()
        curseur = conn.cursor(dictionary=True)
        curseur.execute(
            "SELECT sport, date_pratique, evaluation FROM activites WHERE id_apprenant = %s ORDER BY date_pratique DESC",
            (self.utilisateur['id'],)
        )
        activites = curseur.fetchall()
        conn.close()

        self.zone_activites.configure(state="normal")
        self.zone_activites.delete("1.0", "end")
        for a in activites:
            self.zone_activites.insert(
                "end",
                f"🏃 {a['sport']} — {a['date_pratique']} — {a['evaluation']}\n"
            )
        self.zone_activites.configure(state="disabled")