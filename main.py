import subprocess
import sys
import os

if __name__ == "__main__":
    # Force l'affichage de la fenêtre sur Mac
    os.environ['TK_SILENCE_DEPRECATION'] = '1'
    
    from views.login import FenetreLogin
    
    app = FenetreLogin()
    app.after(200, lambda: app.lift())
    app.after(200, lambda: app.focus_force())
    app.mainloop()