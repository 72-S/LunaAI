import tkinter as tk
import customtkinter as ctk


def confirm_city():
    # Ausgabe des eingegebenen Wertes
    print(cityinput.get())

    # Erste Seite ausblenden
    main_page.pack_forget()

    # Zweite Seite anzeigen
    second_page.pack()

def confirm_api():
    # Ausgabe des eingegebenen Wertes
    print(apiinput.get())

    # Zweite Seite ausblenden
    second_page.pack_forget()

    # Dritte Seite anzeigen



ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("480x340")
app.title("LunaAi - Setup")

# Hauptseite
main_page = tk.Frame(app)
main_page.pack()
main_page.configure(bg="#242424")

cityinput = tk.StringVar()
title = ctk.CTkLabel(main_page, text="Enter your city", font=("Helvetica", 18))
title.pack(padx=10, pady=10)

city = ctk.CTkEntry(main_page, width=350, height=50, textvariable=cityinput)
city.pack(padx=10, pady=10)

city_confirm = ctk.CTkButton(main_page, text="Confirm", width=350, height=50, command=confirm_city)
city_confirm.pack(padx=10, pady=10)

# Zweite Seite
apiinput = tk.StringVar()
second_page = tk.Frame(app)
second_page.configure(bg="#242424")
title2 = ctk.CTkLabel(second_page, text="Enter your OpenWheaterMapAPI", font=("Helvetica", 18))
title2.pack(padx=10, pady=10)

api = ctk.CTkEntry(second_page, width=350, height=50, textvariable=apiinput)
api.pack(padx=10, pady=10)

confirm = ctk.CTkButton(second_page, text="Confirm", width=350, height=50, command=confirm_api)
confirm.pack(padx=10, pady=10)

back_button = ctk.CTkButton(second_page, text="Zurück", width=350, height=50,
                            command=lambda: [second_page.pack_forget(), main_page.pack()])
back_button.pack(padx=10, pady=10)

app.mainloop()
