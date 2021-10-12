import sqlite3, hashlib
from sqlite3.dbapi2 import Cursor # squlite pour base de données
from tkinter import *
from tkinter import simpledialog # ca permet de creer les pop-up
from functools import partial
import tkinter
from typing import Collection, Match # pour que l'app pop up

# Création de la base de données
with sqlite3.connect("Chambre_de_mot_de_passe.db") as db: # j'ainnommé ma base de données
    cursor = db.cursor() # ca permet de controler ma base de données

cursor.execute("""CREATE TABLE IF NOT EXISTS masterpassword(
id INTEGER PRIMARY KEY,
password TEXT NO NULL);
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS chambreforte(
id INTEGER PRIMARY KEY,
siteweb TEXT NOT NULL,
nom_d_utilisateur TEXT NOT NULL,
mot_de_passe TEXT NOT NULL);
""")

#Creer les pop-up
def popUp(text):
    reponse = simpledialog.askstring("chaîne de caractéres", text) # ca crée un popUp puis demande une saisie
    print(reponse)
    return reponse

####################################################################################

fenetre = Tk() 

# fond beige
fenetre.config(background = "#E5E3D6")

fenetre.title("Chambre forte pour les mots de passe")

def hashpassword(input):
    hash = hashlib.md5(input) # ca prend le texte et le met en md5
    hash = hash.hexdigest() # on prend le md5 et on le remet en text pour pouvoir le lire
    return hash

def premiereConnexion():
    fenetre.geometry("350x150")

    étiquette = Label(fenetre, text = "Créer votre mot de passe")
    étiquette.config(anchor =  CENTER)
    étiquette.pack()

    texte = Entry(fenetre, width = 35, show = "*") 
    texte.pack()
    texte.focus() 

    étiquette2 = Label(fenetre, text = "Confirmer votre mot de passe") 
    étiquette2.pack()

    texte2 = Entry(fenetre, width = 35, show = "*") 
    texte2.pack()
    texte2.focus() 

    étiquette3 = Label(fenetre) # ca me permet de faire apparaitre un message "Mdp non similaires"
    étiquette3.pack()

    def enregistrerMotDePasse():
        if texte.get() == texte2.get() :
            hashedpassword = hashpassword(texte.get().encode("utf-8"))
            insérer_mdp = """INSERT INTO masterpassword(password)
            VALUES(?) """
            cursor.execute(insérer_mdp, [(hashedpassword)]) 
            db.commit() #ca permet d'enreigster dans la base de données

            coffre() # quand j'enregistre le mdp, ca m'ammene à l'écran du coffre 

        else:
            étiquette.config(text = "Mot de passe non similaires")


    bouton2 = Button(fenetre, text = "Enregistrez", command = enregistrerMotDePasse)
    bouton2.pack(pady = 7)

def ecranDeConnexion():
    fenetre.geometry("350x150")

    étiquette = Label(fenetre, text = "Entrez le mot de passe")
    étiquette.config(anchor =  CENTER)
    étiquette.pack()

    texte = Entry(fenetre, width = 35, show = "*") # The Entry widget is used to accept single-line text strings from a user. (Pour plus d'info : https://www.tutorialspoint.com/python/tk_entry.htm)
    texte.pack()
    texte.focus() # ca permet que la barre de mdp soit préalablement selecitonné

    étiquette2 = Label(fenetre) # en gros, je code la ligne qui me permet d'identifier si le code est faux
    étiquette2.pack()

    def obtenirMasterPassword():
        vérifHashedPassword =  hashpassword(texte.get().encode("utf-8"))
        cursor.execute("SELECT * FROM masterpassword WHERE id = 1 AND password = ?", [(vérifHashedPassword)]) # tracution : selectionner TOUT de la TABLE "masterpassword" où id = 1 /// le "?" est toujours remplacé par la variable qui le suit
        print(vérifHashedPassword)
        return cursor.fetchall()

    
    def vérifMotDePasse():
        mot_de_passe = obtenirMasterPassword()
        print(mot_de_passe)
        

        if mot_de_passe:
            coffre()
        
        else :
            texte.delete(0,"fin") # ca permet d'effacer le texte ecris aprés chaque "mot de passe incorrecte"
            étiquette2.config(text = "Mot de passe incorrecte")


    bouton = Button(fenetre, text=  "Soumettre", command = vérifMotDePasse)
    bouton.pack(pady = 7) # ca me créer un esapce entre le bouton "soumettre" et la barre du mdp

def coffre():
        for widget in fenetre.winfo_children():
            widget.destroy() # quand on passe de l'écran de connexion au coffre, cela va detruire tout ke texte, car si on ne fait pas ca, ca va empiler tout le texte
        fenetre.geometry("700x350")

        def ajoutEntrée():
            texte = "Siteweb"
            texte2 = "Nom d'utilisateur"
            texte3 = "Mot de passe"

            siteweb = popUp(texte)
            nom_d_utilisateur = popUp(texte2)
            mot_de_passe = popUp(texte3)

            insérer_le_champs = """INSERT INTO chambreforte(siteweb, nom_d_utilisateur, mot_de_passe)
            VALUES (?, ?, ?)"""
            cursor.execute(insérer_le_champs, (siteweb, nom_d_utilisateur, mot_de_passe))
            db.commit()
            
            coffre()

        def suppressionEntrée(input):
            cursor.execute("DELETE FROM chambreforte WHERE id = ?", (input,)) # la "," apres le "(input)" permet d'avoir la bonne id
            db.commit()

            coffre()

        étiquette = Label(fenetre, text = "Coffre-fort")
        étiquette.config(anchor =  CENTER) 
        étiquette.grid()  # j'aurai pu faire "étiquette.pack()" mais j'aurai du le faire pour tous les autres elements contenant "grid" donc les remplacer par pack. Mais je n'aurai pas pu faire mes rangées avec siteweb, nom utilisateur et mdp

        bouton2 = Button(fenetre, text = "+", command = ajoutEntrée)
        bouton2.grid(column = 1, pady = 10)

        étiquettebis = Label(fenetre, text = "Siteweb")
        étiquettebis.grid(row = 2, column = 0, padx = 80)
        étiquettebis = Label(fenetre, text = "Nom d'utilisateur")
        étiquettebis.grid(row = 2, column = 1, padx = 80)
        étiquettebis = Label(fenetre, text = "Mot de passe")
        étiquettebis.grid(row = 2, column = 2, padx = 80)

        cursor.execute("SELECT * FROM chambreforte") 
        if(cursor.fetchall() != None):
            i = 0

            while True:
                cursor.execute("SELECT * FROM chambreforte")
                array = cursor.fetchall()

                # if(len(array) == 0): ca marche sans cette ligne aussi
                #   break

                etiquette = Label(fenetre, text = (array[i][1]), font = ("Helvetica", 12))
                etiquette.grid(row = (i + 3), column = 0) 
                etiquettebis2 = Label(fenetre, text = (array[i][2]), font = ("Helvetica", 12))
                etiquettebis2.grid(row = (i + 3), column = 1) 
                etiquettebis3 = Label(fenetre, text = (array[i][3]), font = ("Helvetica", 12))
                etiquettebis3.grid(row = (i + 3), column = 2) 

                bouttonSupr = Button(fenetre, text = "Effacer", command = partial(suppressionEntrée, array[i][0])) # "partial" me permet de prendre la fonction avec l'"aaray" actuelle et l'id, si on n'utilise pas "partial" la fonction aurait pris le dernier item et l'aurai effacé et c'est pour ca on met "array[0][1]"
                bouttonSupr.grid(row = (i + 3), column = 5, pady = 20)

                i +=1 # a chaque fois que la fonction tourne, le i augmente

                cursor.execute("SELECT * FROM chambreforte")
                if (len(cursor.fetchall()) <= i): # ca permet de stopper le boucle While et ne pas tourner infiniment
                    break




cursor.execute("SELECT * FROM masterpassword")
if cursor.fetchall(): # si il y a qlqch dans la TABLE "masterpassword" -> va direct à l'écran de connexion.....
    ecranDeConnexion()

else :                #....sinon va à l'écran de premiere connexion
    premiereConnexion()
fenetre.mainloop() # elle affiche la fenêtre principale à l'écran puis elle attend que l'usager pose une action.


