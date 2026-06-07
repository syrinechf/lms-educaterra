import customtkinter as ctk
from database import get_connection
from datetime import date
from modules.quiz import ModuleQuiz

BLEU = "#014562"
OR = "#D0A42D"
BLANC = "#FFFFFF"
FOND = "#F5F6F8"
TEXTE_GRIS = "#888888"
BORDURE = "#E5E7EB"

class VueFormateur(ctk.CTk):
    def __init__(self, utilisateur):
        super().__init__()
        self.utilisateur = utilisateur

        self.title("LMS Educaterra — Formateur")
        self.geometry("1000x620")
        self.resizable(True, True)
        self.configure(fg_color=FOND)
        ctk.set_appearance_mode("light")
        self.lift()
        self.focus_force()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.creer_sidebar()
        self.creer_zone_principale()
        self.afficher_dashboard()

    # ═══════════════════════════════════════════════════════════════════
    # SIDEBAR
    # ═══════════════════════════════════════════════════════════════════
    def creer_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=200, fg_color=BLEU, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)
        self.sidebar.grid_rowconfigure(6, weight=1)

        frame_logo = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        frame_logo.grid(row=0, column=0, padx=16, pady=(20,16), sticky="ew")

        ctk.CTkLabel(frame_logo, text="Educaterra",
                     font=ctk.CTkFont(size=18, weight="bold"),
                     text_color=OR).pack(anchor="w")
        ctk.CTkLabel(frame_logo, text="Espace formateur",
                     font=ctk.CTkFont(size=11),
                     text_color="gray60").pack(anchor="w")

        ctk.CTkFrame(self.sidebar, height=1, fg_color="gray30").grid(
            row=1, column=0, sticky="ew")

        self.boutons_nav = {}
        nav_items = [
            ("dashboard",  "⊞  Tableau de bord"),
            ("fiches",     "📋  Fiches journalières"),
            ("cours",      "📚  Mes cours"),
            ("creer_cours","➕  Créer un cours"),
            ("quiz",       "📝  Gérer les quiz"),
            ("apprenants", "👥  Mes apprenants"),
        ]

        for i, (cle, label) in enumerate(nav_items):
            btn = ctk.CTkButton(
                self.sidebar, text=label, anchor="w",
                fg_color="transparent", text_color="gray70",
                hover_color="#0a3a52",
                font=ctk.CTkFont(size=13),
                corner_radius=0, height=42,
                command=lambda c=cle: self.changer_vue(c)
            )
            btn.grid(row=i+2, column=0, sticky="ew")
            self.boutons_nav[cle] = btn

        ctk.CTkFrame(self.sidebar, height=1, fg_color="gray30").grid(
            row=9, column=0, sticky="ew")

        frame_user = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        frame_user.grid(row=10, column=0, padx=16, pady=14, sticky="ew")

        initiales = (self.utilisateur['prenom'][0] + self.utilisateur['nom'][0]).upper()
        ctk.CTkLabel(frame_user, text=initiales, width=36, height=36,
                     fg_color=OR, corner_radius=18,
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=BLEU).pack(side="left", padx=(0,10))

        frame_infos = ctk.CTkFrame(frame_user, fg_color="transparent")
        frame_infos.pack(side="left")
        ctk.CTkLabel(frame_infos,
                     text=f"{self.utilisateur['prenom']} {self.utilisateur['nom']}",
                     font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=BLANC).pack(anchor="w")
        ctk.CTkLabel(frame_infos, text="Formateur",
                     font=ctk.CTkFont(size=10),
                     text_color="gray60").pack(anchor="w")

    # ═══════════════════════════════════════════════════════════════════
    # ZONE PRINCIPALE
    # ═══════════════════════════════════════════════════════════════════
    def creer_zone_principale(self):
        self.zone_main = ctk.CTkFrame(self, fg_color=FOND, corner_radius=0)
        self.zone_main.grid(row=0, column=1, sticky="nsew")
        self.zone_main.grid_rowconfigure(1, weight=1)
        self.zone_main.grid_columnconfigure(0, weight=1)

        self.topbar = ctk.CTkFrame(self.zone_main, fg_color=BLANC,
                                    height=52, corner_radius=0)
        self.topbar.grid(row=0, column=0, sticky="ew")
        self.topbar.grid_propagate(False)
        self.topbar.grid_columnconfigure(0, weight=1)

        self.label_titre_page = ctk.CTkLabel(
            self.topbar, text="Tableau de bord",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=BLEU)
        self.label_titre_page.grid(row=0, column=0, padx=20, sticky="w")

        ctk.CTkLabel(self.topbar,
                     text=f"Bonjour {self.utilisateur['prenom']} 👋",
                     font=ctk.CTkFont(size=13),
                     text_color=TEXTE_GRIS).grid(row=0, column=1, padx=20, sticky="e")

        self.contenu = ctk.CTkScrollableFrame(
            self.zone_main, fg_color=FOND, corner_radius=0)
        self.contenu.grid(row=1, column=0, sticky="nsew")
        self.contenu.grid_columnconfigure(0, weight=1)

    def vider_contenu(self):
        for widget in self.contenu.winfo_children():
            widget.destroy()

    def changer_vue(self, cle):
        for k, btn in self.boutons_nav.items():
            btn.configure(fg_color="transparent", text_color="gray70")
        self.boutons_nav[cle].configure(fg_color="#0a3a52", text_color=BLANC)

        titres = {
            "dashboard":   "Tableau de bord",
            "fiches":      "Fiches journalières",
            "cours":       "Mes cours",
            "creer_cours": "Créer un cours",
            "quiz":        "Gérer les quiz",
            "apprenants":  "Mes apprenants",
        }
        self.label_titre_page.configure(text=titres[cle])
        self.vider_contenu()

        vues = {
            "dashboard":   self.afficher_dashboard,
            "fiches":      self.afficher_fiches,
            "cours":       self.afficher_cours,
            "creer_cours": self.afficher_creer_cours,
            "quiz":        self.afficher_quiz,
            "apprenants":  self.afficher_apprenants,
        }
        vues[cle]()

    # ═══════════════════════════════════════════════════════════════════
    # DASHBOARD
    # ═══════════════════════════════════════════════════════════════════
    def afficher_dashboard(self):
        self.boutons_nav["dashboard"].configure(fg_color="#0a3a52", text_color=BLANC)

        conn = get_connection()
        curseur = conn.cursor(dictionary=True)

        curseur.execute(
            "SELECT COUNT(*) as nb FROM cours WHERE id_formateur = %s",
            (self.utilisateur['id'],))
        nb_cours = curseur.fetchone()['nb']

        curseur.execute(
            "SELECT COUNT(*) as nb FROM fiches_journalieres WHERE id_formateur = %s",
            (self.utilisateur['id'],))
        nb_fiches = curseur.fetchone()['nb']

        curseur.execute(
            "SELECT COUNT(*) as nb FROM utilisateurs WHERE role = 'apprenant'")
        nb_apprenants = curseur.fetchone()['nb']

        curseur.execute(
            "SELECT titre, date_creation FROM cours WHERE id_formateur = %s ORDER BY date_creation DESC LIMIT 3",
            (self.utilisateur['id'],))
        derniers_cours = curseur.fetchall()

        curseur.execute(
            "SELECT date, contenu FROM fiches_journalieres WHERE id_formateur = %s ORDER BY date DESC LIMIT 3",
            (self.utilisateur['id'],))
        dernieres_fiches = curseur.fetchall()
        conn.close()

        # Stats
        ctk.CTkLabel(self.contenu, text="VUE D'ENSEMBLE",
                     font=ctk.CTkFont(size=11, weight="bold"),
                     text_color=TEXTE_GRIS).grid(
            row=0, column=0, sticky="w", padx=20, pady=(16,8))

        frame_stats = ctk.CTkFrame(self.contenu, fg_color="transparent")
        frame_stats.grid(row=1, column=0, sticky="ew", padx=20, pady=(0,0))
        frame_stats.grid_columnconfigure((0,1,2), weight=1)

        for i, (label, valeur, couleur) in enumerate([
            ("Cours créés", str(nb_cours), BLEU),
            ("Fiches journalières", str(nb_fiches), OR),
            ("Apprenants suivis", str(nb_apprenants), "#2e7d32"),
        ]):
            card = ctk.CTkFrame(frame_stats, fg_color=BLANC,
                                corner_radius=10, border_width=1,
                                border_color=BORDURE)
            card.grid(row=0, column=i, padx=(0,10) if i < 2 else 0, sticky="ew")
            ctk.CTkLabel(card, text=label,
                         font=ctk.CTkFont(size=11),
                         text_color=TEXTE_GRIS).pack(anchor="w", padx=16, pady=(12,2))
            ctk.CTkLabel(card, text=valeur,
                         font=ctk.CTkFont(size=26, weight="bold"),
                         text_color=couleur).pack(anchor="w", padx=16, pady=(0,12))

        # Derniers cours
        ctk.CTkLabel(self.contenu, text="DERNIERS COURS",
                     font=ctk.CTkFont(size=11, weight="bold"),
                     text_color=TEXTE_GRIS).grid(
            row=2, column=0, sticky="w", padx=20, pady=(20,8))

        if derniers_cours:
            for c in derniers_cours:
                card = ctk.CTkFrame(self.contenu, fg_color=BLANC,
                                    corner_radius=10, border_width=1,
                                    border_color=BORDURE)
                card.grid(sticky="ew", padx=20, pady=(0,6))
                card.grid_columnconfigure(0, weight=1)

                ctk.CTkLabel(card, text=c['titre'],
                             font=ctk.CTkFont(size=13, weight="bold"),
                             text_color=BLEU).grid(sticky="w", padx=16, pady=(12,4))
                ctk.CTkLabel(card, text=str(c['date_creation']),
                             font=ctk.CTkFont(size=11),
                             text_color=TEXTE_GRIS).grid(sticky="w", padx=16, pady=(0,12))
        else:
            ctk.CTkLabel(self.contenu, text="Aucun cours créé pour l'instant.",
                         text_color=TEXTE_GRIS,
                         font=ctk.CTkFont(size=13)).grid(padx=20, pady=8, sticky="w")

        # Dernières fiches
        ctk.CTkLabel(self.contenu, text="DERNIÈRES FICHES",
                     font=ctk.CTkFont(size=11, weight="bold"),
                     text_color=TEXTE_GRIS).grid(
            sticky="w", padx=20, pady=(20,8))

        if dernieres_fiches:
            for f in dernieres_fiches:
                card = ctk.CTkFrame(self.contenu, fg_color=BLANC,
                                    corner_radius=10, border_width=1,
                                    border_color=BORDURE)
                card.grid(sticky="ew", padx=20, pady=(0,6))
                card.grid_columnconfigure(0, weight=1)

                ctk.CTkLabel(card, text=f"📅  {f['date']}",
                             font=ctk.CTkFont(size=13, weight="bold"),
                             text_color=BLEU).grid(sticky="w", padx=16, pady=(12,4))
                ctk.CTkLabel(card,
                             text=f['contenu'][:100] + "..." if len(f['contenu']) > 100 else f['contenu'],
                             font=ctk.CTkFont(size=11),
                             text_color=TEXTE_GRIS,
                             wraplength=600).grid(sticky="w", padx=16, pady=(0,12))
        else:
            ctk.CTkLabel(self.contenu, text="Aucune fiche créée pour l'instant.",
                         text_color=TEXTE_GRIS,
                         font=ctk.CTkFont(size=13)).grid(padx=20, pady=8, sticky="w")

    # ═══════════════════════════════════════════════════════════════════
    # FICHES JOURNALIÈRES
    # ═══════════════════════════════════════════════════════════════════
    def afficher_fiches(self):
        # Formulaire ajout
        card = ctk.CTkFrame(self.contenu, fg_color=BLANC,
                            corner_radius=10, border_width=1,
                            border_color=BORDURE)
        card.grid(sticky="ew", padx=20, pady=(16,12))
        card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(card, text="Nouvelle fiche du jour",
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color=BLEU).grid(sticky="w", padx=16, pady=(14,8))

        self.zone_fiche = ctk.CTkTextbox(card, width=700, height=120,
                                          font=ctk.CTkFont(size=13))
        self.zone_fiche.grid(padx=16, pady=(0,8), sticky="ew")

        self.label_fiche = ctk.CTkLabel(card, text="", font=ctk.CTkFont(size=12))
        self.label_fiche.grid(pady=(0,4))

        ctk.CTkButton(card, text="Enregistrer la fiche",
                      fg_color=BLEU, hover_color="#0a3a52",
                      text_color=BLANC, height=38,
                      font=ctk.CTkFont(size=13, weight="bold"),
                      corner_radius=8,
                      command=self.enregistrer_fiche).grid(
            sticky="w", padx=16, pady=(0,14))

        # Liste des fiches
        ctk.CTkLabel(self.contenu, text="MES FICHES",
                     font=ctk.CTkFont(size=11, weight="bold"),
                     text_color=TEXTE_GRIS).grid(sticky="w", padx=20, pady=(8,8))

        self.frame_liste_fiches = ctk.CTkFrame(self.contenu, fg_color="transparent")
        self.frame_liste_fiches.grid(sticky="ew", padx=20)
        self.frame_liste_fiches.grid_columnconfigure(0, weight=1)

        self.charger_fiches()

    def enregistrer_fiche(self):
        contenu = self.zone_fiche.get("1.0", "end").strip()
        if not contenu:
            self.label_fiche.configure(text="Le contenu est vide.", text_color="red")
            return
        try:
            conn = get_connection()
            curseur = conn.cursor()
            curseur.execute(
                "INSERT INTO fiches_journalieres (id_formateur, date, contenu) VALUES (%s,%s,%s)",
                (self.utilisateur['id'], date.today(), contenu))
            conn.commit()
            conn.close()
            self.label_fiche.configure(text="Fiche enregistrée !", text_color="green")
            self.zone_fiche.delete("1.0", "end")
            self.charger_fiches()
        except Exception as e:
            self.label_fiche.configure(text=f"Erreur : {e}", text_color="red")

    def charger_fiches(self):
        for widget in self.frame_liste_fiches.winfo_children():
            widget.destroy()

        conn = get_connection()
        curseur = conn.cursor(dictionary=True)
        curseur.execute(
            "SELECT date, contenu FROM fiches_journalieres WHERE id_formateur = %s ORDER BY date DESC",
            (self.utilisateur['id'],))
        fiches = curseur.fetchall()
        conn.close()

        if not fiches:
            ctk.CTkLabel(self.frame_liste_fiches,
                         text="Aucune fiche pour l'instant.",
                         text_color=TEXTE_GRIS,
                         font=ctk.CTkFont(size=13)).grid(pady=8)
            return

        for f in fiches:
            card = ctk.CTkFrame(self.frame_liste_fiches, fg_color=BLANC,
                                corner_radius=10, border_width=1,
                                border_color=BORDURE)
            card.grid(sticky="ew", pady=(0,6))
            card.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(card, text=f"📅  {f['date']}",
                         font=ctk.CTkFont(size=13, weight="bold"),
                         text_color=BLEU).grid(sticky="w", padx=16, pady=(12,4))
            ctk.CTkLabel(card, text=f['contenu'],
                         font=ctk.CTkFont(size=12),
                         text_color=TEXTE_GRIS,
                         wraplength=650).grid(sticky="w", padx=16, pady=(0,12))

    # ═══════════════════════════════════════════════════════════════════
    # MES COURS
    # ═══════════════════════════════════════════════════════════════════
    def afficher_cours(self):
        conn = get_connection()
        curseur = conn.cursor(dictionary=True)
        curseur.execute(
            "SELECT * FROM cours WHERE id_formateur = %s ORDER BY date_creation DESC",
            (self.utilisateur['id'],))
        cours = curseur.fetchall()
        conn.close()

        if not cours:
            ctk.CTkLabel(self.contenu, text="Aucun cours créé pour l'instant.",
                         text_color=TEXTE_GRIS,
                         font=ctk.CTkFont(size=13)).grid(padx=20, pady=20, sticky="w")
            return

        for c in cours:
            card = ctk.CTkFrame(self.contenu, fg_color=BLANC,
                                corner_radius=10, border_width=1,
                                border_color=BORDURE)
            card.grid(sticky="ew", padx=20, pady=(12,0))
            card.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(card, text="COURS",
                         font=ctk.CTkFont(size=10, weight="bold"),
                         fg_color=BLEU, text_color=BLANC,
                         corner_radius=4, padx=8, pady=2).grid(
                sticky="w", padx=14, pady=(12,4))

            ctk.CTkLabel(card, text=c['titre'],
                         font=ctk.CTkFont(size=14, weight="bold"),
                         text_color=BLEU).grid(sticky="w", padx=14)

            ctk.CTkLabel(card,
                         text=c['contenu'][:120] + "..." if len(c['contenu']) > 120 else c['contenu'],
                         font=ctk.CTkFont(size=12),
                         text_color=TEXTE_GRIS,
                         wraplength=600).grid(sticky="w", padx=14, pady=(4,0))

            ctk.CTkLabel(card, text=str(c['date_creation']),
                         font=ctk.CTkFont(size=11),
                         text_color=TEXTE_GRIS).grid(sticky="w", padx=14, pady=(4,12))

    # ═══════════════════════════════════════════════════════════════════
    # CRÉER UN COURS
    # ═══════════════════════════════════════════════════════════════════
    def afficher_creer_cours(self):
        card = ctk.CTkFrame(self.contenu, fg_color=BLANC,
                            corner_radius=10, border_width=1,
                            border_color=BORDURE)
        card.grid(sticky="ew", padx=20, pady=20)
        card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(card, text="Nouveau cours",
                     font=ctk.CTkFont(size=15, weight="bold"),
                     text_color=BLEU).grid(padx=20, pady=(16,12), sticky="w")

        ctk.CTkLabel(card, text="Titre du cours",
                     font=ctk.CTkFont(size=12),
                     text_color=TEXTE_GRIS).grid(sticky="w", padx=20, pady=(8,2))
        self.champ_titre = ctk.CTkEntry(card, width=600, height=36)
        self.champ_titre.grid(sticky="w", padx=20)

        ctk.CTkLabel(card, text="Contenu",
                     font=ctk.CTkFont(size=12),
                     text_color=TEXTE_GRIS).grid(sticky="w", padx=20, pady=(12,2))
        self.zone_contenu = ctk.CTkTextbox(card, width=600, height=200,
                                            font=ctk.CTkFont(size=13))
        self.zone_contenu.grid(sticky="w", padx=20)

        self.label_cours = ctk.CTkLabel(card, text="", font=ctk.CTkFont(size=12))
        self.label_cours.grid(pady=(8,0))

        ctk.CTkButton(card, text="Publier le cours",
                      fg_color=BLEU, hover_color="#0a3a52",
                      text_color=BLANC, height=40,
                      font=ctk.CTkFont(size=13, weight="bold"),
                      corner_radius=8,
                      command=self.creer_cours).grid(padx=20, pady=(8,20), sticky="w")

    def creer_cours(self):
        titre = self.champ_titre.get()
        contenu = self.zone_contenu.get("1.0", "end").strip()

        if not titre or not contenu:
            self.label_cours.configure(text="Remplissez tous les champs.", text_color="red")
            return

        try:
            conn = get_connection()
            curseur = conn.cursor()
            curseur.execute(
                "INSERT INTO cours (titre, contenu, id_formateur, date_creation) VALUES (%s,%s,%s,%s)",
                (titre, contenu, self.utilisateur['id'], date.today()))
            conn.commit()
            conn.close()
            self.label_cours.configure(text="Cours publié !", text_color="green")
            self.champ_titre.delete(0, "end")
            self.zone_contenu.delete("1.0", "end")
        except Exception as e:
            self.label_cours.configure(text=f"Erreur : {e}", text_color="red")

    # ═══════════════════════════════════════════════════════════════════
    # QUIZ
    # ═══════════════════════════════════════════════════════════════════
    def afficher_quiz(self):
        ctk.CTkButton(
            self.contenu,
            text="Ouvrir le gestionnaire de quiz",
            fg_color=BLEU, hover_color="#0a3a52",
            text_color=BLANC, height=40,
            font=ctk.CTkFont(size=13, weight="bold"),
            corner_radius=8,
            command=lambda: ModuleQuiz(self, self.utilisateur)
        ).grid(padx=20, pady=20, sticky="w")

    # ═══════════════════════════════════════════════════════════════════
    # APPRENANTS
    # ═══════════════════════════════════════════════════════════════════
    def afficher_apprenants(self):
        conn = get_connection()
        curseur = conn.cursor(dictionary=True)
        curseur.execute(
            "SELECT id, nom, prenom, email FROM utilisateurs WHERE role = 'apprenant'")
        apprenants = curseur.fetchall()
        conn.close()

        ctk.CTkLabel(self.contenu, text="LISTE DES APPRENANTS",
                     font=ctk.CTkFont(size=11, weight="bold"),
                     text_color=TEXTE_GRIS).grid(sticky="w", padx=20, pady=(16,8))

        if not apprenants:
            ctk.CTkLabel(self.contenu, text="Aucun apprenant enregistré.",
                         text_color=TEXTE_GRIS,
                         font=ctk.CTkFont(size=13)).grid(padx=20, pady=8, sticky="w")
            return

        for a in apprenants:
            card = ctk.CTkFrame(self.contenu, fg_color=BLANC,
                                corner_radius=10, border_width=1,
                                border_color=BORDURE)
            card.grid(sticky="ew", padx=20, pady=(0,6))
            card.grid_columnconfigure(0, weight=1)

            initiales = (a['prenom'][0] + a['nom'][0]).upper()

            frame_row = ctk.CTkFrame(card, fg_color="transparent")
            frame_row.grid(sticky="ew", padx=14, pady=12)
            frame_row.grid_columnconfigure(1, weight=1)

            ctk.CTkLabel(frame_row, text=initiales,
                         width=38, height=38,
                         fg_color=BLEU, corner_radius=19,
                         font=ctk.CTkFont(size=13, weight="bold"),
                         text_color=OR).grid(row=0, column=0, rowspan=2)

            ctk.CTkLabel(frame_row,
                         text=f"{a['prenom']} {a['nom']}",
                         font=ctk.CTkFont(size=13, weight="bold"),
                         text_color="#1a1a1a").grid(row=0, column=1, sticky="w", padx=12)
            ctk.CTkLabel(frame_row, text=a['email'],
                         font=ctk.CTkFont(size=11),
                         text_color=TEXTE_GRIS).grid(row=1, column=1, sticky="w", padx=12)