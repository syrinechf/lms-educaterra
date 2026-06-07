import customtkinter as ctk
from auth import connecter_utilisateur

BLEU = "#014562"
OR = "#D0A42D"
BLANC = "#FFFFFF"
FOND = "#F5F6F8"
TEXTE_GRIS = "#888888"
BORDURE = "#E5E7EB"

class FenetreLogin(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("LMS Educaterra")
        self.geometry("900x560")
        self.resizable(False, False)
        self.configure(fg_color=BLANC)
        ctk.set_appearance_mode("light")
        self.lift()
        self.focus_force()

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.creer_panneau_gauche()
        self.creer_panneau_droit()

    # ═══════════════════════════════════════════════════════════════════
    # PANNEAU GAUCHE — Visuel bleu
    # ═══════════════════════════════════════════════════════════════════
    def creer_panneau_gauche(self):
        panneau = ctk.CTkFrame(self, fg_color=BLEU, corner_radius=0)
        panneau.grid(row=0, column=0, sticky="nsew")
        panneau.grid_rowconfigure(0, weight=1)
        panneau.grid_columnconfigure(0, weight=1)

        frame_centre = ctk.CTkFrame(panneau, fg_color="transparent")
        frame_centre.grid(row=0, column=0)

        # Logo / Nom
        ctk.CTkLabel(
            frame_centre,
            text="Educaterra",
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color=OR
        ).pack(pady=(0, 8))

        ctk.CTkLabel(
            frame_centre,
            text="Learning Management System",
            font=ctk.CTkFont(size=14),
            text_color="gray60"
        ).pack()

        # Séparateur doré
        ctk.CTkFrame(
            frame_centre,
            width=60, height=3,
            fg_color=OR, corner_radius=2
        ).pack(pady=24)

        # Description
        ctk.CTkLabel(
            frame_centre,
            text="Gérez vos formations,\nvos apprenants et vos\ncontenus pédagogiques.",
            font=ctk.CTkFont(size=14),
            text_color="gray70",
            justify="center"
        ).pack()

        # Fonctionnalités
        features = ["✓  Gestion des cours", "✓  Suivi des apprenants", "✓  Quiz interactifs"]
        for f in features:
            ctk.CTkLabel(
                frame_centre,
                text=f,
                font=ctk.CTkFont(size=12),
                text_color=OR
            ).pack(pady=3)

    # ═══════════════════════════════════════════════════════════════════
    # PANNEAU DROIT — Formulaire
    # ═══════════════════════════════════════════════════════════════════
    def creer_panneau_droit(self):
        panneau = ctk.CTkFrame(self, fg_color=BLANC, corner_radius=0)
        panneau.grid(row=0, column=1, sticky="nsew")
        panneau.grid_rowconfigure(0, weight=1)
        panneau.grid_columnconfigure(0, weight=1)

        frame_form = ctk.CTkFrame(panneau, fg_color="transparent")
        frame_form.grid(row=0, column=0, padx=50)

        ctk.CTkLabel(
            frame_form,
            text="Connexion",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color=BLEU
        ).pack(anchor="w", pady=(0, 4))

        ctk.CTkLabel(
            frame_form,
            text="Entrez vos identifiants pour accéder à votre espace.",
            font=ctk.CTkFont(size=12),
            text_color=TEXTE_GRIS
        ).pack(anchor="w", pady=(0, 28))

        # Email
        ctk.CTkLabel(
            frame_form, text="Adresse email",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=BLEU
        ).pack(anchor="w")

        self.champ_email = ctk.CTkEntry(
            frame_form, width=320, height=42,
            placeholder_text="exemple@educaterra.fr",
            border_color=BORDURE,
            fg_color=FOND
        )
        self.champ_email.pack(pady=(4, 16))

        # Mot de passe
        ctk.CTkLabel(
            frame_form, text="Mot de passe",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=BLEU
        ).pack(anchor="w")

        self.champ_mdp = ctk.CTkEntry(
            frame_form, width=320, height=42,
            show="*",
            placeholder_text="••••••••",
            border_color=BORDURE,
            fg_color=FOND
        )
        self.champ_mdp.pack(pady=(4, 8))

        # Erreur
        self.label_erreur = ctk.CTkLabel(
            frame_form, text="",
            font=ctk.CTkFont(size=12),
            text_color="red"
        )
        self.label_erreur.pack(pady=(0, 8))

        # Bouton connexion
        ctk.CTkButton(
            frame_form,
            text="Se connecter →",
            width=320, height=44,
            fg_color=BLEU,
            hover_color="#0a3a52",
            text_color=BLANC,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=8,
            command=self.se_connecter
        ).pack(pady=(0, 16))

        # Séparateur
        ctk.CTkFrame(
            frame_form,
            width=320, height=1,
            fg_color=BORDURE
        ).pack(pady=(0, 16))

        # Comptes de test
        ctk.CTkLabel(
            frame_form,
            text="Comptes de test",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=TEXTE_GRIS
        ).pack(anchor="w")

        comptes = [
            ("Admin", "admin@educaterra.fr", "admin123"),
            ("Formateur", "formateur@educaterra.fr", "form123"),
            ("Apprenant", "apprenant@educaterra.fr", "app123"),
        ]

        for role, email, mdp in comptes:
            btn = ctk.CTkButton(
                frame_form,
                text=f"{role} — {email}",
                width=320, height=32,
                fg_color=FOND,
                hover_color="#e8f0f5",
                text_color=BLEU,
                font=ctk.CTkFont(size=11),
                corner_radius=6,
                border_width=1,
                border_color=BORDURE,
                command=lambda e=email, m=mdp: self.remplir_et_connecter(e, m)
            ).pack(pady=3)

    def remplir_et_connecter(self, email, mdp):
        self.champ_email.delete(0, "end")
        self.champ_email.insert(0, email)
        self.champ_mdp.delete(0, "end")
        self.champ_mdp.insert(0, mdp)
        self.se_connecter()

    def se_connecter(self):
        email = self.champ_email.get()
        mdp = self.champ_mdp.get()

        if not email or not mdp:
            self.label_erreur.configure(text="Veuillez remplir tous les champs.")
            return

        utilisateur = connecter_utilisateur(email, mdp)

        if utilisateur:
            self.destroy()
            self.ouvrir_bonne_vue(utilisateur)
        else:
            self.label_erreur.configure(text="Email ou mot de passe incorrect.")

    def ouvrir_bonne_vue(self, utilisateur):
        role = utilisateur['role']
        if role == 'administrateur':
            from views.admin import VueAdmin
            app = VueAdmin(utilisateur)
            app.mainloop()
        elif role == 'formateur':
            from views.formateur import VueFormateur
            app = VueFormateur(utilisateur)
            app.mainloop()
        elif role == 'apprenant':
            from views.apprenant import VueApprenant
            app = VueApprenant(utilisateur)
            app.mainloop()