import customtkinter as ctk

app = ctk.CTk()
app.title("Test")
app.geometry("300x200")
ctk.CTkLabel(app, text="Ca marche !").pack(pady=20)
app.lift()
app.focus_force()
app.mainloop()