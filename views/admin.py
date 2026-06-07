import customtkinter as ctk
from database import get_connection
import bcrypt

BLEU = "#014562"
OR = "#D0A42D"
BLANC = "#FFFFFF"
FOND = "#F5F6F8"
TEXTE_GRIS = "#888888"
BORDURE = "#E5E7EB"

class VueAdmin(ctk.CTk):
    def __init__(self, utilisateur):
        super().__init__()
        self.utilisateur = utilisateur

        self.title("LMS Educaterra — Administration")
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
        self.afficher_utilisateurs()

    # ═══════════════════════════════════════════════════════════════════
    # SIDEBAR
    # ═══════════════════════════════════════════════════════════════════
    def creer_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=200, fg_color=BLEU, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)
        self.sidebar.grid_rowconfigure(5, weight=1)

        frame_logo = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        frame_logo.grid(row=0, column=0, padx=16, pady=(20, 16), sticky="ew")

        ctk.CTkLabel(frame_logo, text="Educaterra",
                     font=ctk.CTkFont(size=18, weight="bold"),
                     text_color=OR).pack(anchor="w")
        ctk.CTkLabel(frame_logo, text="Administration",
                     font=ctk.CTkFont(size=11),
                     text_color="gray60").pack(anchor="w")

        ctk.CTkFrame(self.sidebar, height=1, fg_color="gray30").grid(
            row=1, column=0, sticky="ew")

        self.boutons_nav = {}
        nav_items = [
            ("utilisateurs", "👥  Utilisateurs"),
            ("creer",        "➕  Créer un compte"),
            ("parcours",     "🎓  Parcours"),
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
            row=6, column=0, sticky="ew")

        frame_user = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        frame_user.grid(row=7, column=0, padx=16, pady=14, sticky="ew")

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
        ctk.CTkLabel(frame_infos, text="Administrateur",
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
            self.topbar, text="Utilisateurs",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=BLEU)
        self.label_titre_page.grid(row=0, column=0, padx=20, sticky="w")

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
            "utilisateurs": "Utilisateurs",
            "creer": "Créer un compte",
            "parcours": "Parcours de formation",
        }
        self.label_titre_page.configure(text=titres[cle])
        self.vider_contenu()

        vues = {
            "utilisateurs": self.afficher_utilisateurs,
            "creer": self.afficher_creer_compte,
            "parcours": self.afficher_parcours,
        }
        vues[cle]()

    # ═══════════════════════════════════════════════════════════════════
    # VUE UTILISATEURS
    # ═══════════════════════════════════════════════════════════════════
    def afficher_utilisateurs(self):
        self.boutons_nav["utilisateurs"].configure(
            fg_color="#0a3a52", text_color=BLANC)

        conn = get_connection()
        curseur = conn.cursor(dictionary=True)
        curseur.execute(
            "SELECT id, nom, prenom, email, role FROM utilisateurs ORDER BY role")
        utilisateurs = curseur.fetchall()
        conn.close()

        # Stats en haut
        admins = sum(1 for u in utilisateurs if u['role'] == 'administrateur')
        formateurs = sum(1 for u in utilisateurs if u['role'] == 'formateur')
        apprenants = sum(1 for u in utilisateurs if u['role'] == 'apprenant')

        frame_stats = ctk.CTkFrame(self.contenu, fg_color="transparent")
        frame_stats.grid(row=0, column=0, sticky="ew", padx=20, pady=(16, 0))
        frame_stats.grid_columnconfigure((0,1,2), weight=1)

        for i, (label, valeur, couleur) in enumerate([
            ("Administrateurs", str(admins), BLEU),
            ("Formateurs", str(formateurs), OR),
            ("Apprenants", str(apprenants), "#2e7d32"),
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

        # Liste utilisateurs
        ctk.CTkLabel(self.contenu, text="LISTE DES UTILISATEURS",
                     font=ctk.CTkFont(size=11, weight="bold"),
                     text_color=TEXTE_GRIS).grid(
            row=1, column=0, sticky="w", padx=20, pady=(20, 8))

        couleurs_role = {
            'administrateur': (BLEU, BLANC),
            'formateur': (OR, BLEU),
            'apprenant': ("#e8f5e9", "#2e7d32"),
        }

        for u in utilisateurs:
            card = ctk.CTkFrame(self.contenu, fg_color=BLANC,
                                corner_radius=10, border_width=1,
                                border_color=BORDURE)
            card.grid(sticky="ew", padx=20, pady=(0, 6))
            card.grid_columnconfigure(0, weight=1)

            initiales = (u['prenom'][0] + u['nom'][0]).upper()
            fg, tc = couleurs_role.get(u['role'], (BLEU, BLANC))

            frame_row = ctk.CTkFrame(card, fg_color="transparent")
            frame_row.grid(row=0, column=0, sticky="ew", padx=14, pady=12)
            frame_row.grid_columnconfigure(1, weight=1)

            ctk.CTkLabel(frame_row, text=initiales,
                         width=38, height=38,
                         fg_color=fg, corner_radius=19,
                         font=ctk.CTkFont(size=13, weight="bold"),
                         text_color=tc).grid(row=0, column=0, rowspan=2)

            ctk.CTkLabel(frame_row,
                         text=f"{u['prenom']} {u['nom']}",
                         font=ctk.CTkFont(size=13, weight="bold"),
                         text_color="#1a1a1a").grid(
                row=0, column=1, sticky="w", padx=12)
            ctk.CTkLabel(frame_row, text=u['email'],
                         font=ctk.CTkFont(size=11),
                         text_color=TEXTE_GRIS).grid(
                row=1, column=1, sticky="w", padx=12)

            ctk.CTkLabel(frame_row, text=u['role'].capitalize(),
                         font=ctk.CTkFont(size=11, weight="bold"),
                         fg_color=fg, text_color=tc,
                         corner_radius=6, padx=10, pady=3).grid(
                row=0, column=2, rowspan=2, padx=(0, 4))

    # ═══════════════════════════════════════════════════════════════════
    # VUE CRÉER UN COMPTE
    # ═══════════════════════════════════════════════════════════════════
    def afficher_creer_compte(self):
        card = ctk.CTkFrame(self.contenu, fg_color=BLANC,
                            corner_radius=10, border_width=1,
                            border_color=BORDURE)
        card.grid(sticky="ew", padx=20, pady=20)
        card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(card, text="Nouveau compte",
                     font=ctk.CTkFont(size=15, weight="bold"),
                     text_color=BLEU).grid(padx=20, pady=(16,12), sticky="w")

        champs = [
            ("Nom", "nom"), ("Prénom", "prenom"),
            ("Email", "email"), ("Mot de passe", "mdp"),
        ]
        self.champs_creation = {}

        for i, (label, cle) in enumerate(champs):
            ctk.CTkLabel(card, text=label,
                         font=ctk.CTkFont(size=12),
                         text_color=TEXTE_GRIS).grid(
                sticky="w", padx=20, pady=(8,2))
            entry = ctk.CTkEntry(card, width=500, height=36,
                                  show="*" if cle == "mdp" else "")
            entry.grid(sticky="w", padx=20)
            self.champs_creation[cle] = entry

        ctk.CTkLabel(card, text="Rôle",
                     font=ctk.CTkFont(size=12),
                     text_color=TEXTE_GRIS).grid(sticky="w", padx=20, pady=(8,2))
        self.choix_role = ctk.CTkOptionMenu(
            card, width=500,
            values=["apprenant", "formateur", "administrateur"],
            fg_color=BLANC, button_color=BLEU,
            text_color="#1a1a1a")
        self.choix_role.grid(sticky="w", padx=20)

        self.label_message = ctk.CTkLabel(card, text="",
                                           font=ctk.CTkFont(size=12))
        self.label_message.grid(pady=(10,0))

        ctk.CTkButton(card, text="Créer le compte",
                      fg_color=BLEU, hover_color="#0a3a52",
                      text_color=BLANC, height=40,
                      font=ctk.CTkFont(size=13, weight="bold"),
                      corner_radius=8,
                      command=self.creer_compte).grid(padx=20, pady=(8,20), sticky="w")

    def creer_compte(self):
        nom = self.champs_creation['nom'].get()
        prenom = self.champs_creation['prenom'].get()
        email = self.champs_creation['email'].get()
        mdp = self.champs_creation['mdp'].get()
        role = self.choix_role.get()

        if not all([nom, prenom, email, mdp]):
            self.label_message.configure(
                text="Tous les champs sont obligatoires.", text_color="red")
            return

        mdp_hache = bcrypt.hashpw(mdp.encode('utf-8'), bcrypt.gensalt())

        try:
            conn = get_connection()
            curseur = conn.cursor()
            curseur.execute(
                "INSERT INTO utilisateurs (nom, prenom, email, mot_de_passe, role) VALUES (%s,%s,%s,%s,%s)",
                (nom, prenom, email, mdp_hache, role)
            )
            conn.commit()
            conn.close()
            self.label_message.configure(
                text="Compte créé avec succès !", text_color="green")
            for entry in self.champs_creation.values():
                entry.delete(0, "end")
        except Exception as e:
            self.label_message.configure(text=f"Erreur : {e}", text_color="red")

    # ═══════════════════════════════════════════════════════════════════
    # VUE PARCOURS
    # ═══════════════════════════════════════════════════════════════════
    def afficher_parcours(self):
        conn = get_connection()
        curseur = conn.cursor(dictionary=True)
        curseur.execute("SELECT * FROM parcours")
        parcours = curseur.fetchall()
        conn.close()

        ctk.CTkLabel(self.contenu, text="PARCOURS DE FORMATION",
                     font=ctk.CTkFont(size=11, weight="bold"),
                     text_color=TEXTE_GRIS).grid(
            sticky="w", padx=20, pady=(16,8))

        couleurs = [BLEU, OR, "#2e7d32", "#993556"]

        for i, p in enumerate(parcours):
            card = ctk.CTkFrame(self.contenu, fg_color=BLANC,
                                corner_radius=10, border_width=1,
                                border_color=BORDURE)
            card.grid(sticky="ew", padx=20, pady=(0,8))
            card.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(card, text=p['intitule'],
                         font=ctk.CTkFont(size=14, weight="bold"),
                         text_color=couleurs[i % len(couleurs)]).grid(
                sticky="w", padx=16, pady=(14,4))
            ctk.CTkLabel(card, text=p['description'],
                         font=ctk.CTkFont(size=12),
                         text_color=TEXTE_GRIS,
                         wraplength=600).grid(
                sticky="w", padx=16, pady=(0,14))