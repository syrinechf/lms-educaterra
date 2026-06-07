import customtkinter as ctk
from database import get_connection
from datetime import date
from modules.quiz import ModuleQuiz
from modules.activites import ModuleActivites

# ─── Couleurs Educaterra ───────────────────────────────────────────────
BLEU = "#014562"
OR = "#D0A42D"
BLANC = "#FFFFFF"
FOND = "#F5F6F8"
TEXTE_GRIS = "#888888"
BORDURE = "#E5E7EB"

class VueApprenant(ctk.CTk):
    def __init__(self, utilisateur):
        super().__init__()
        self.utilisateur = utilisateur
        self.vue_active = None

        self.title("LMS Educaterra — Espace Apprenant")
        self.geometry("1000x620")
        self.resizable(True, True)
        self.configure(fg_color=FOND)
        ctk.set_appearance_mode("light")
        self.lift()
        self.focus_force()

        # ─── Layout principal ──────────────────────────────────────────
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

        # Logo
        frame_logo = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        frame_logo.grid(row=0, column=0, padx=16, pady=(20, 16), sticky="ew")

        ctk.CTkLabel(
            frame_logo,
            text="Educaterra",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=OR
        ).pack(anchor="w")

        ctk.CTkLabel(
            frame_logo,
            text="Espace apprenant",
            font=ctk.CTkFont(size=11),
            text_color="gray60"
        ).pack(anchor="w")

        # Séparateur
        ctk.CTkFrame(self.sidebar, height=1, fg_color="gray30").grid(
            row=1, column=0, sticky="ew", padx=0)

        # Navigation
        self.boutons_nav = {}
        nav_items = [
            ("dashboard", "⊞  Tableau de bord"),
            ("cours",     "📚  Mes cours"),
            ("quiz",      "📝  Quiz"),
            ("activites", "🏃  Activités"),
            ("dossier",   "📁  Mon dossier"),
        ]

        for i, (cle, label) in enumerate(nav_items):
            btn = ctk.CTkButton(
                self.sidebar,
                text=label,
                anchor="w",
                fg_color="transparent",
                text_color="gray70",
                hover_color="#0a3a52",
                font=ctk.CTkFont(size=13),
                corner_radius=0,
                height=42,
                command=lambda c=cle: self.changer_vue(c)
            )
            btn.grid(row=i+2, column=0, sticky="ew", padx=0)
            self.boutons_nav[cle] = btn

        # Séparateur bas
        ctk.CTkFrame(self.sidebar, height=1, fg_color="gray30").grid(
            row=8, column=0, sticky="ew")

        # Utilisateur en bas
        frame_user = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        frame_user.grid(row=9, column=0, padx=16, pady=14, sticky="ew")

        initiales = (self.utilisateur['prenom'][0] + self.utilisateur['nom'][0]).upper()

        avatar = ctk.CTkLabel(
            frame_user,
            text=initiales,
            width=36, height=36,
            fg_color=OR,
            corner_radius=18,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=BLEU
        )
        avatar.pack(side="left", padx=(0, 10))

        frame_infos = ctk.CTkFrame(frame_user, fg_color="transparent")
        frame_infos.pack(side="left")

        ctk.CTkLabel(
            frame_infos,
            text=f"{self.utilisateur['prenom']} {self.utilisateur['nom']}",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=BLANC
        ).pack(anchor="w")

        ctk.CTkLabel(
            frame_infos,
            text=self.utilisateur['role'].capitalize(),
            font=ctk.CTkFont(size=10),
            text_color="gray60"
        ).pack(anchor="w")

    # ═══════════════════════════════════════════════════════════════════
    # ZONE PRINCIPALE
    # ═══════════════════════════════════════════════════════════════════
    def creer_zone_principale(self):
        self.zone_main = ctk.CTkFrame(self, fg_color=FOND, corner_radius=0)
        self.zone_main.grid(row=0, column=1, sticky="nsew")
        self.zone_main.grid_rowconfigure(1, weight=1)
        self.zone_main.grid_columnconfigure(0, weight=1)

        # Topbar
        self.topbar = ctk.CTkFrame(self.zone_main, fg_color=BLANC,
                                    height=52, corner_radius=0)
        self.topbar.grid(row=0, column=0, sticky="ew")
        self.topbar.grid_propagate(False)
        self.topbar.grid_columnconfigure(0, weight=1)

        self.label_titre_page = ctk.CTkLabel(
            self.topbar,
            text="Tableau de bord",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=BLEU
        )
        self.label_titre_page.grid(row=0, column=0, padx=20, sticky="w")

        ctk.CTkLabel(
            self.topbar,
            text=f"Bonjour {self.utilisateur['prenom']} 👋",
            font=ctk.CTkFont(size=13),
            text_color=TEXTE_GRIS
        ).grid(row=0, column=1, padx=20, sticky="e")

        # Contenu scrollable
        self.contenu = ctk.CTkScrollableFrame(
            self.zone_main, fg_color=FOND, corner_radius=0)
        self.contenu.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        self.contenu.grid_columnconfigure(0, weight=1)

    def vider_contenu(self):
        for widget in self.contenu.winfo_children():
            widget.destroy()

    def changer_vue(self, cle):
        # Reset tous les boutons
        for k, btn in self.boutons_nav.items():
            btn.configure(fg_color="transparent", text_color="gray70")

        # Active le bouton cliqué
        self.boutons_nav[cle].configure(fg_color="#0a3a52", text_color=BLANC)

        titres = {
            "dashboard": "Tableau de bord",
            "cours": "Mes cours",
            "quiz": "Quiz",
            "activites": "Activités sportives",
            "dossier": "Mon dossier",
        }
        self.label_titre_page.configure(text=titres[cle])

        vues = {
            "dashboard": self.afficher_dashboard,
            "cours": self.afficher_cours,
            "quiz": self.afficher_quiz,
            "activites": self.afficher_activites,
            "dossier": self.afficher_dossier,
        }
        self.vider_contenu()
        vues[cle]()

    # ═══════════════════════════════════════════════════════════════════
    # VUE DASHBOARD
    # ═══════════════════════════════════════════════════════════════════
    def afficher_dashboard(self):
        self.boutons_nav["dashboard"].configure(fg_color="#0a3a52", text_color=BLANC)

        # Récupération stats BDD
        conn = get_connection()
        curseur = conn.cursor(dictionary=True)

        curseur.execute("SELECT COUNT(*) as nb FROM cours")
        nb_cours = curseur.fetchone()['nb']

        curseur.execute(
            "SELECT COUNT(*) as nb, AVG(score) as moyenne FROM resultats_quizz WHERE id_apprenant = %s",
            (self.utilisateur['id'],)
        )
        stats = curseur.fetchone()
        nb_quiz = stats['nb'] or 0
        moyenne = round(stats['moyenne'], 0) if stats['moyenne'] else 0

        curseur.execute(
            "SELECT COUNT(*) as nb FROM activites WHERE id_apprenant = %s",
            (self.utilisateur['id'],)
        )
        nb_activites = curseur.fetchone()['nb']

        curseur.execute(
            "SELECT titre, date_creation FROM cours ORDER BY date_creation DESC LIMIT 3"
        )
        derniers_cours = curseur.fetchall()

        curseur.execute(
            "SELECT score, date_passage FROM resultats_quizz WHERE id_apprenant = %s ORDER BY date_passage DESC LIMIT 3",
            (self.utilisateur['id'],)
        )
        derniers_quiz = curseur.fetchall()
        conn.close()

        pad = {"padx": 20, "pady": (16, 0)}

        # ── Cartes statistiques ────────────────────────────────────────
        ctk.CTkLabel(
            self.contenu, text="VUE D'ENSEMBLE",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=TEXTE_GRIS
        ).grid(row=0, column=0, sticky="w", **pad)

        frame_stats = ctk.CTkFrame(self.contenu, fg_color="transparent")
        frame_stats.grid(row=1, column=0, sticky="ew", padx=20, pady=(8, 0))
        frame_stats.grid_columnconfigure((0,1,2), weight=1)

        stats_data = [
            ("Cours disponibles", str(nb_cours), "cette semaine"),
            ("Quiz passés", str(nb_quiz), f"Score moyen : {int(moyenne)}%"),
            ("Activités sportives", str(nb_activites), "ce mois-ci"),
        ]

        for i, (label, valeur, sous) in enumerate(stats_data):
            card = ctk.CTkFrame(frame_stats, fg_color=BLANC,
                                corner_radius=10, border_width=1,
                                border_color=BORDURE)
            card.grid(row=0, column=i, padx=(0, 10) if i < 2 else 0, sticky="ew")

            ctk.CTkLabel(card, text=label,
                         font=ctk.CTkFont(size=11),
                         text_color=TEXTE_GRIS).pack(anchor="w", padx=16, pady=(14,2))
            ctk.CTkLabel(card, text=valeur,
                         font=ctk.CTkFont(size=28, weight="bold"),
                         text_color=BLEU).pack(anchor="w", padx=16)
            ctk.CTkLabel(card, text=sous,
                         font=ctk.CTkFont(size=11),
                         text_color=OR).pack(anchor="w", padx=16, pady=(0,14))

        # ── Derniers cours ─────────────────────────────────────────────
        ctk.CTkLabel(
            self.contenu, text="COURS RÉCENTS",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=TEXTE_GRIS
        ).grid(row=2, column=0, sticky="w", padx=20, pady=(20, 8))

        for cours in derniers_cours:
            card = ctk.CTkFrame(self.contenu, fg_color=BLANC,
                                corner_radius=10, border_width=1,
                                border_color=BORDURE)
            card.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 8))
            card.grid_columnconfigure(0, weight=1)

            badge = ctk.CTkLabel(card, text="BPJEPS",
                                  font=ctk.CTkFont(size=10, weight="bold"),
                                  fg_color=BLEU, text_color=BLANC,
                                  corner_radius=4, padx=8, pady=2)
            badge.grid(row=0, column=0, sticky="w", padx=14, pady=(12,4))

            ctk.CTkLabel(card, text=cours['titre'],
                         font=ctk.CTkFont(size=13, weight="bold"),
                         text_color="#1a1a1a").grid(row=1, column=0, sticky="w", padx=14)

            ctk.CTkLabel(card, text=str(cours['date_creation']),
                         font=ctk.CTkFont(size=11),
                         text_color=TEXTE_GRIS).grid(row=2, column=0, sticky="w",
                                                      padx=14, pady=(2,12))

        # ── Derniers quiz ──────────────────────────────────────────────
        ctk.CTkLabel(
            self.contenu, text="DERNIERS RÉSULTATS QUIZ",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=TEXTE_GRIS
        ).grid(row=4, column=0, sticky="w", padx=20, pady=(16, 8))

        if derniers_quiz:
            for qz in derniers_quiz:
                score = int(qz['score'])
                couleur_score = "#2e7d32" if score >= 70 else OR
                fond_score = "#e8f5e9" if score >= 70 else "#fff8e1"

                row = ctk.CTkFrame(self.contenu, fg_color=BLANC,
                                   corner_radius=10, border_width=1,
                                   border_color=BORDURE)
                row.grid(row=5, column=0, sticky="ew", padx=20, pady=(0,6))
                row.grid_columnconfigure(0, weight=1)

                ctk.CTkLabel(row, text=f"Quiz du {qz['date_passage']}",
                             font=ctk.CTkFont(size=13),
                             text_color="#1a1a1a").grid(row=0, column=0,
                                                         sticky="w", padx=14, pady=12)

                ctk.CTkLabel(row, text=f"{score}%",
                             font=ctk.CTkFont(size=13, weight="bold"),
                             fg_color=fond_score,
                             text_color=couleur_score,
                             corner_radius=20, padx=12, pady=4
                             ).grid(row=0, column=1, padx=14, pady=12)
        else:
            ctk.CTkLabel(self.contenu,
                         text="Aucun quiz passé pour l'instant.",
                         text_color=TEXTE_GRIS,
                         font=ctk.CTkFont(size=13)
                         ).grid(row=5, column=0, padx=20, pady=8, sticky="w")

    # ═══════════════════════════════════════════════════════════════════
    # VUE COURS
    # ═══════════════════════════════════════════════════════════════════
    def afficher_cours(self):
        conn = get_connection()
        curseur = conn.cursor(dictionary=True)
        curseur.execute("SELECT * FROM cours ORDER BY date_creation DESC")
        cours = curseur.fetchall()
        conn.close()

        if not cours:
            ctk.CTkLabel(self.contenu, text="Aucun cours disponible.",
                         text_color=TEXTE_GRIS).grid(padx=20, pady=20)
            return

        for c in cours:
            card = ctk.CTkFrame(self.contenu, fg_color=BLANC,
                                corner_radius=10, border_width=1,
                                border_color=BORDURE)
            card.grid(sticky="ew", padx=20, pady=(12, 0))
            card.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(card, text="BPJEPS",
                         font=ctk.CTkFont(size=10, weight="bold"),
                         fg_color=BLEU, text_color=BLANC,
                         corner_radius=4, padx=8, pady=2
                         ).grid(row=0, column=0, sticky="w", padx=14, pady=(12,4))

            ctk.CTkLabel(card, text=c['titre'],
                         font=ctk.CTkFont(size=14, weight="bold"),
                         text_color=BLEU).grid(row=1, column=0, sticky="w", padx=14)

            ctk.CTkLabel(card, text=c['contenu'][:120] + "..." if len(c['contenu']) > 120 else c['contenu'],
                         font=ctk.CTkFont(size=12),
                         text_color=TEXTE_GRIS,
                         wraplength=600).grid(row=2, column=0, sticky="w", padx=14, pady=(4,0))

            ctk.CTkLabel(card, text=str(c['date_creation']),
                         font=ctk.CTkFont(size=11),
                         text_color=TEXTE_GRIS).grid(row=3, column=0,
                                                      sticky="w", padx=14, pady=(4,12))

    # ═══════════════════════════════════════════════════════════════════
    # VUE QUIZ
    # ═══════════════════════════════════════════════════════════════════
    def afficher_quiz(self):
        ctk.CTkButton(
            self.contenu,
            text="Passer un quiz",
            fg_color=BLEU, hover_color="#0a3a52",
            text_color=BLANC,
            font=ctk.CTkFont(size=13, weight="bold"),
            height=40, corner_radius=8,
            command=lambda: ModuleQuiz(self, self.utilisateur)
        ).grid(padx=20, pady=20, sticky="w")

        # Historique des résultats
        conn = get_connection()
        curseur = conn.cursor(dictionary=True)
        curseur.execute(
            "SELECT score, date_passage FROM resultats_quizz WHERE id_apprenant = %s ORDER BY date_passage DESC",
            (self.utilisateur['id'],)
        )
        resultats = curseur.fetchall()
        conn.close()

        ctk.CTkLabel(self.contenu, text="HISTORIQUE",
                     font=ctk.CTkFont(size=11, weight="bold"),
                     text_color=TEXTE_GRIS).grid(sticky="w", padx=20, pady=(0, 8))

        if resultats:
            for r in resultats:
                score = int(r['score'])
                couleur = "#2e7d32" if score >= 70 else OR
                fond = "#e8f5e9" if score >= 70 else "#fff8e1"

                row = ctk.CTkFrame(self.contenu, fg_color=BLANC,
                                   corner_radius=10, border_width=1,
                                   border_color=BORDURE)
                row.grid(sticky="ew", padx=20, pady=(0, 6))
                row.grid_columnconfigure(0, weight=1)

                ctk.CTkLabel(row, text=f"Quiz du {r['date_passage']}",
                             font=ctk.CTkFont(size=13),
                             text_color="#1a1a1a").grid(row=0, column=0,
                                                         sticky="w", padx=14, pady=12)
                ctk.CTkLabel(row, text=f"{score}%",
                             font=ctk.CTkFont(size=13, weight="bold"),
                             fg_color=fond, text_color=couleur,
                             corner_radius=20, padx=12, pady=4
                             ).grid(row=0, column=1, padx=14, pady=12)
        else:
            ctk.CTkLabel(self.contenu, text="Aucun quiz passé pour l'instant.",
                         text_color=TEXTE_GRIS,
                         font=ctk.CTkFont(size=13)).grid(padx=20, pady=8, sticky="w")

    # ═══════════════════════════════════════════════════════════════════
    # VUE ACTIVITÉS
    # ═══════════════════════════════════════════════════════════════════
    def afficher_activites(self):
        ctk.CTkButton(
            self.contenu,
            text="Ajouter une activité",
            fg_color=OR, hover_color="#b8891f",
            text_color=BLEU,
            font=ctk.CTkFont(size=13, weight="bold"),
            height=40, corner_radius=8,
            command=lambda: ModuleActivites(self, self.utilisateur)
        ).grid(padx=20, pady=20, sticky="w")

        conn = get_connection()
        curseur = conn.cursor(dictionary=True)
        curseur.execute(
            "SELECT sport, date_pratique, evaluation FROM activites WHERE id_apprenant = %s ORDER BY date_pratique DESC",
            (self.utilisateur['id'],)
        )
        activites = curseur.fetchall()
        conn.close()

        ctk.CTkLabel(self.contenu, text="MES ACTIVITÉS",
                     font=ctk.CTkFont(size=11, weight="bold"),
                     text_color=TEXTE_GRIS).grid(sticky="w", padx=20, pady=(0,8))

        if activites:
            for a in activites:
                row = ctk.CTkFrame(self.contenu, fg_color=BLANC,
                                   corner_radius=10, border_width=1,
                                   border_color=BORDURE)
                row.grid(sticky="ew", padx=20, pady=(0, 6))
                row.grid_columnconfigure(0, weight=1)

                ctk.CTkLabel(row, text=f"🏃  {a['sport']}",
                             font=ctk.CTkFont(size=13, weight="bold"),
                             text_color=BLEU).grid(row=0, column=0,
                                                    sticky="w", padx=14, pady=(12,2))
                ctk.CTkLabel(row, text=f"{a['date_pratique']}  ·  {a['evaluation']}",
                             font=ctk.CTkFont(size=11),
                             text_color=TEXTE_GRIS).grid(row=1, column=0,
                                                          sticky="w", padx=14, pady=(0,12))
        else:
            ctk.CTkLabel(self.contenu, text="Aucune activité enregistrée.",
                         text_color=TEXTE_GRIS,
                         font=ctk.CTkFont(size=13)).grid(padx=20, pady=8, sticky="w")

    # ═══════════════════════════════════════════════════════════════════
    # VUE DOSSIER
    # ═══════════════════════════════════════════════════════════════════
    def afficher_dossier(self):
        card = ctk.CTkFrame(self.contenu, fg_color=BLANC,
                            corner_radius=10, border_width=1,
                            border_color=BORDURE)
        card.grid(sticky="ew", padx=20, pady=20)
        card.grid_columnconfigure(0, weight=1)

        # Avatar
        initiales = (self.utilisateur['prenom'][0] + self.utilisateur['nom'][0]).upper()
        ctk.CTkLabel(card, text=initiales,
                     width=64, height=64,
                     fg_color=BLEU,
                     corner_radius=32,
                     font=ctk.CTkFont(size=22, weight="bold"),
                     text_color=OR).grid(row=0, column=0, pady=(20,8))

        ctk.CTkLabel(card,
                     text=f"{self.utilisateur['prenom']} {self.utilisateur['nom']}",
                     font=ctk.CTkFont(size=16, weight="bold"),
                     text_color=BLEU).grid(row=1, column=0)

        ctk.CTkLabel(card,
                     text=self.utilisateur['role'].capitalize(),
                     font=ctk.CTkFont(size=12),
                     text_color=TEXTE_GRIS).grid(row=2, column=0, pady=(2,16))

        # Séparateur
        ctk.CTkFrame(card, height=1, fg_color=BORDURE).grid(
            row=3, column=0, sticky="ew", padx=20)

        infos = [
            ("Email", self.utilisateur['email']),
            ("Rôle", self.utilisateur['role'].capitalize()),
        ]

        for i, (label, valeur) in enumerate(infos):
            ctk.CTkLabel(card, text=label,
                         font=ctk.CTkFont(size=11),
                         text_color=TEXTE_GRIS).grid(
                row=4+i*2, column=0, sticky="w", padx=20, pady=(12,0))
            ctk.CTkLabel(card, text=valeur,
                         font=ctk.CTkFont(size=13, weight="bold"),
                         text_color="#1a1a1a").grid(
                row=5+i*2, column=0, sticky="w", padx=20, pady=(0,4))

        ctk.CTkFrame(card, height=1, fg_color=BORDURE).grid(
            row=8, column=0, sticky="ew", padx=20, pady=(12,0))

        ctk.CTkLabel(card, text="",
                     font=ctk.CTkFont(size=11)).grid(row=9, column=0, pady=8)