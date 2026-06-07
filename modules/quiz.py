import customtkinter as ctk
from database import get_connection
from datetime import date

class ModuleQuiz(ctk.CTkToplevel):
    def __init__(self, parent, utilisateur):
        super().__init__(parent)
        self.utilisateur = utilisateur
        self.title("Module Quiz")
        self.geometry("750x550")

        self.onglets = ctk.CTkTabview(self, width=720, height=500)
        self.onglets.pack(padx=15, pady=10)

        # Onglets selon le rôle
        if utilisateur['role'] == 'formateur':
            self.onglets.add("Créer un quiz")
        self.onglets.add("Passer un quiz")

        if utilisateur['role'] == 'formateur':
            self.construire_creation_quiz()
        self.construire_passage_quiz()

    # ─── Formateur : créer un quiz ─────────────────────────────────────
    def construire_creation_quiz(self):
        onglet = self.onglets.tab("Créer un quiz")

        ctk.CTkLabel(onglet, text="Choisir le cours associé").pack(pady=5)
        self.cours_ids = []
        self.choix_cours = ctk.CTkOptionMenu(onglet, values=["Chargement..."])
        self.choix_cours.pack(pady=5)
        self.charger_cours_formateur()

        ctk.CTkLabel(onglet, text="Question").pack()
        self.champ_question = ctk.CTkEntry(onglet, width=600)
        self.champ_question.pack(pady=5)

        ctk.CTkLabel(onglet, text="Réponse correcte").pack()
        self.champ_reponse = ctk.CTkEntry(onglet, width=600)
        self.champ_reponse.pack(pady=5)

        self.label_quiz = ctk.CTkLabel(onglet, text="")
        self.label_quiz.pack(pady=5)

        ctk.CTkButton(onglet, text="Ajouter la question",
                      command=self.ajouter_question).pack(pady=8)

    def charger_cours_formateur(self):
        conn = get_connection()
        curseur = conn.cursor(dictionary=True)
        curseur.execute(
            "SELECT id, titre FROM cours WHERE id_formateur = %s",
            (self.utilisateur['id'],)
        )
        cours = curseur.fetchall()
        conn.close()

        if cours:
            self.cours_ids = {c['titre']: c['id'] for c in cours}
            self.choix_cours.configure(values=list(self.cours_ids.keys()))
            self.choix_cours.set(list(self.cours_ids.keys())[0])
        else:
            self.choix_cours.configure(values=["Aucun cours disponible"])

    def ajouter_question(self):
        titre_cours = self.choix_cours.get()
        question = self.champ_question.get()
        reponse = self.champ_reponse.get()

        if not question or not reponse:
            self.label_quiz.configure(text="Remplissez tous les champs.", text_color="red")
            return

        id_cours = self.cours_ids.get(titre_cours)
        if not id_cours:
            self.label_quiz.configure(text="Sélectionnez un cours valide.", text_color="red")
            return

        try:
            conn = get_connection()
            curseur = conn.cursor()
            curseur.execute(
                "INSERT INTO quizz (id_cours, question, reponse_correcte) VALUES (%s, %s, %s)",
                (id_cours, question, reponse)
            )
            conn.commit()
            conn.close()
            self.label_quiz.configure(text="Question ajoutée !", text_color="green")
            self.champ_question.delete(0, "end")
            self.champ_reponse.delete(0, "end")
        except Exception as e:
            self.label_quiz.configure(text=f"Erreur : {e}", text_color="red")

    # ─── Apprenant : passer un quiz ────────────────────────────────────
    def construire_passage_quiz(self):
        onglet = self.onglets.tab("Passer un quiz")

        ctk.CTkLabel(onglet, text="Choisir un cours").pack(pady=5)
        self.cours_ids_apprenant = {}
        self.choix_cours_apprenant = ctk.CTkOptionMenu(
            onglet, values=["Chargement..."],
            command=self.charger_questions
        )
        self.choix_cours_apprenant.pack(pady=5)

        self.zone_quiz = ctk.CTkScrollableFrame(onglet, width=680, height=320)
        self.zone_quiz.pack(pady=5)

        self.label_score = ctk.CTkLabel(onglet, text="",
                                         font=ctk.CTkFont(size=15, weight="bold"))
        self.label_score.pack(pady=5)

        ctk.CTkButton(onglet, text="Valider mes réponses",
                      command=self.corriger_quiz).pack(pady=5)

        self.charger_tous_cours()

    def charger_tous_cours(self):
        conn = get_connection()
        curseur = conn.cursor(dictionary=True)
        curseur.execute("SELECT id, titre FROM cours")
        cours = curseur.fetchall()
        conn.close()

        if cours:
            self.cours_ids_apprenant = {c['titre']: c['id'] for c in cours}
            self.choix_cours_apprenant.configure(
                values=list(self.cours_ids_apprenant.keys())
            )
            self.choix_cours_apprenant.set(list(self.cours_ids_apprenant.keys())[0])
            self.charger_questions(list(self.cours_ids_apprenant.keys())[0])

    def charger_questions(self, titre_cours):
        # Vide la zone
        for widget in self.zone_quiz.winfo_children():
            widget.destroy()

        self.questions = []
        self.champs_reponses = []

        id_cours = self.cours_ids_apprenant.get(titre_cours)
        if not id_cours:
            return

        conn = get_connection()
        curseur = conn.cursor(dictionary=True)
        curseur.execute(
            "SELECT id, question, reponse_correcte FROM quizz WHERE id_cours = %s",
            (id_cours,)
        )
        self.questions = curseur.fetchall()
        conn.close()

        if not self.questions:
            ctk.CTkLabel(self.zone_quiz,
                         text="Aucune question pour ce cours.").pack(pady=10)
            return

        for i, q in enumerate(self.questions):
            ctk.CTkLabel(self.zone_quiz,
                         text=f"Q{i+1} : {q['question']}",
                         wraplength=640,
                         anchor="w").pack(anchor="w", pady=(8, 2))
            champ = ctk.CTkEntry(self.zone_quiz, width=640,
                                  placeholder_text="Ta réponse...")
            champ.pack(anchor="w", pady=(0, 5))
            self.champs_reponses.append(champ)

    def corriger_quiz(self):
        if not self.questions:
            self.label_score.configure(text="Aucune question chargée.", text_color="red")
            return

        bonnes = 0
        for i, q in enumerate(self.questions):
            reponse_utilisateur = self.champs_reponses[i].get().strip().lower()
            reponse_correcte = q['reponse_correcte'].strip().lower()
            if reponse_utilisateur == reponse_correcte:
                bonnes += 1

        total = len(self.questions)
        score = round((bonnes / total) * 100)

        # Enregistrement du score
        try:
            conn = get_connection()
            curseur = conn.cursor()
            curseur.execute(
                "INSERT INTO resultats_quizz (id_apprenant, id_quizz, score, date_passage) VALUES (%s, %s, %s, %s)",
                (self.utilisateur['id'], self.questions[0]['id'], score, date.today())
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Erreur enregistrement score : {e}")

        self.label_score.configure(
            text=f"Score : {bonnes}/{total} ({score}%)",
            text_color="green" if score >= 50 else "red"
        )