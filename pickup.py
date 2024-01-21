import boto3
import json
import tkinter as tk
from tkinter import ttk

class SondajFom(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Formulaire Sondaj ESIH")
        self.geometry("600x400")

        # Kreye ekran pral kontni fòmilè a
        self.frame = ttk.Frame(self, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Kreye label ak entri pou chak kesyon nan fòmilè a
        self.create_form()

        # Bouton pou anrejistre done yo
        self.submit_button = ttk.Button(self.frame, text="Anrejistre", command=self.save_data)
        self.submit_button.grid(row=10, column=0, columnspan=2, pady=(10, 0))

    def create_form(self):
        # Diksyonè ki reprezante kesyon yo nan fòmilè a
        self.questions = {
            "Quitter le pays après études universitaires": tk.StringVar(),
            "Tranche d'âge": tk.StringVar(),
            "Niveau d'études": tk.StringVar(),
            "Pays visé": tk.StringVar(),
            "Raison du départ": tk.StringVar(),
            "Objectif du départ": tk.StringVar(),
            "Durée prévue à l'étranger": tk.StringVar(),
            "Intention de retour": tk.StringVar()
        }

        # Kreye label ak entri pou chak kesyon
        row_num = 0
        for question, var in self.questions.items():
            label = ttk.Label(self.frame, text=question)
            label.grid(row=row_num, column=0, padx=(0, 10), pady=(5, 5))

            if "Oui" in question or "Non" in question or "Incertain" in question:
                # Pou kesyon ki gen opsyon Oui/Non/Incertain, kreye meni (Combobox)
                options = ["Oui", "Non", "Incertain"]
                entry = ttk.Combobox(self.frame, textvariable=var, values=options, state="readonly")
            else:
                # Pou lòt kesyon, kreye yon zòn tekst
                entry = ttk.Entry(self.frame, textvariable=var)

            entry.grid(row=row_num, column=1, padx=(0, 10), pady=(5, 5))
            row_num += 1

    def save_data(self):
        # Récupérer les clés d'accès
        aws_access_key_id = 'AKIAXCJJH3O3U76C5TUC'  # Remplacez par votre Access Key ID
        aws_secret_access_key = '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'  # Remplacez par votre Secret Access Key

        # Créer une session AWS
        session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )

        # Créer un client S3
        s3 = session.client('s3')

        # Créer un dictionnaire avec les informations saisies
        data = {question: var.get() for question, var in self.questions.items()}

        # Convertir le dictionnaire en format JSON avec indentation
        json_data = json.dumps(data, indent=2)

        # Nom du fichier à vérifier et mettre à jour
        bucket_name = 'esihbucketl4'  # Remplacez par votre nom de bucket
        file_name = 'sondaj_esih.json'

        # Écrire le JSON dans un fichier temporaire
        with open('sondaj_esih.json', 'a') as f:  # 'a' pour append (ajouter à la fin du fichier)
            f.write(json_data + '\n')  # Ajoutez un saut de ligne après chaque utilisateur

        # Envoyer le fichier vers le bucket S3
        s3.upload_file('sondaj_esih.json', bucket_name, file_name)
        print(f"Le fichier {file_name} a été mis à jour avec succès dans le bucket {bucket_name}.")


if __name__ == "__main__":
    app = SondajFom()
    app.mainloop()
