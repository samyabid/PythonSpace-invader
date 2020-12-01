#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 20:08:50 2019

@author: toto
Version utilisée PYTHON 2.7
Samy ABID CHAREF
Thomas VERNOUX 

Voici le script dédié aux classes, méthodes et fonctions nécessaires au Space Invader. 


Note : Lorsque rien n'est mentionné à propos des paramètres d'entrée ou de sortie d'une méthode, celle-ci prend en paramètre d'entrée self et ne retourne rien.
"""

from Tkinter import Label,Canvas,PhotoImage,Tk,Button


class fenetre:
    # classe fenêtre, elle permet de créer une fenetre sur l'ecran de l'ordinateur. L'objet fenêtre contiendra tous les elements de notre programme comme les bouttons ou la zone de jeu
    def __init__(self):
        
        self.MaFenetre = None
        self.largeur = 400 # largeur du canevas
        self.hauteur = 400 # hauteur du canevas
        self.MonCanvas = None
        self.V1 = None
        self.A1 = None # alien 1
        self.A2 = None #alien 2
        self.A3 = None #alien 3
        self.A4 = None #alien 4
        self.T1 = None# tir
        self.TA1 = None #tir alien 1

    def creation_de_la_fenetre(self):
        # Cette methode crée la fenetre tkinter ainsi le le canvas et les widget associés
        
        self.MaFenetre = Tk()
        self.MaFenetre.title('-- Space Invader --')
        self.MaFenetre.geometry("500x600") 
        self.creation_canvas()
        self.creation_boutons()
        self.MaFenetre.mainloop()
    
    def creation_boutons(self):
        # cette methode est appelée par creation_de_la_fenetre pour créer les bouttons
        
        B1 = Button(text = "Quitter", relief = "flat" , command = self.MaFenetre.destroy)
        accueil = Label(text = "You must destroy all aliens ")
        accueil.pack()
        B1.pack()
       
    
    def creation_canvas(self):
         # cette methode crée les objets : tir,vaisseau et alien
        
        photo = PhotoImage(file = "photofunky.gif")
        self.MonCanvas = Canvas(self.MaFenetre, width = self.largeur, height = self.hauteur, bg = 'grey')# creation du canvas
        self.MonCanvas.create_image(200,200,image = photo)
        self.creation_vaisseau()
        self.creation_alien()
        self.MonCanvas.bind('<Key>',self.gestion_des_touches) # ici on ne met pas de () à V1.bouger
        self.MonCanvas.focus_set() # hyper important pour event
        self.MonCanvas.pack(pady = 30) # on pack avec une marge en haut et en bas de 30 px
        self.boucle_temps()
        
    def gestion_des_touches(self,event):
        # cette methode est appelee lorsqu'une touche du clavier est préssée, elle va choisir la méthode à appeler en fonction de la touche préssée
        
        touche = event.keysym
        if touche == 'd':
            self.V1.bouger_d()
        if touche == 'q':
            self.V1.bouger_g()
        if touche == "space":
            self.creation_tir()
            
    def creation_vaisseau(self):
        # Cette méthode contient les outils pour créer le vaisseau
        
        self.V1 = Vaisseau(self.MonCanvas) # on commande la creation du vaisseau
        self.V1.creer()
        
    def creation_alien(self):
        # Cette méthode contient les outils pour créer les aliens.
        
        self.A1 = Alien(self.MonCanvas,50)
        self.A2 = Alien(self.MonCanvas,100)
        self.A3 = Alien(self.MonCanvas,150)
        self.A4 = Alien(self.MonCanvas,200)
        self.A1.creer()
        self.creation_tir_alien()
        self.A2.creer()
        self.A3.creer()
        self.A4.creer()
    
    def creation_tir(self):
        #Cette methode a pour objectif de créer les tirs.
        
        self.T1 = Tir(self.MonCanvas,self.V1.posX)
    
    def creation_tir_alien(self):
        #Cette methode a pour objectif de créer les tirs aliens.
        
        self.TA1 = Tir_alien(self.MonCanvas,self.A1.posX,self.A1.posY)
            
    def destruction_tir(self):
        #Cette methode a pour objectif de detruire les tirs lorsque ces derniers on depasse le cadre de la fenetre.
        
        if self.T1 != None:
            if self.T1.posY < -20:
                self.MonCanvas.delete(self.MaFenetre,self.T1._tir) # on detruit le tir
    
    def boucle_temps(self):
        #Cette methode a pour objectif de definir les temps de d'enclanchement des methodes. 
        
        self.A1.bouger()
        self.A2.bouger()
        self.A3.bouger()
        self.A4.bouger()
        
        if self.T1 != None:
            self.T1.bouger()
            self.destruction_tir()
       
        self.TA1.bouger()
        self.MonCanvas.after(10,self.boucle_temps)


class Vaisseau:
    # cette classe vaisseau contient toutes les méthodes concernant le vaisseau (celles pour le créer, le déplacer)
    
    def __init__(self,MonCanvas_):
        self.posX = 400/2 # position initiale en x
        self.posY = 380 # position initiale en y
        self.MonCanvas = MonCanvas_ # on prend le canvas dans la classe
        self.l = 10 # largeur/hauteur du vaisseau
        self.vaisseau = None # c'est le ovale du vaisseau, cet objet est un canvas

    def creer(self):
        # Cette methode permet créer le vaisseau (l'ajoute au canvas)
        
        self.vaisseau = self.MonCanvas.create_oval(self.posX-self.l,self.posY-self.l,self.posX+self.l,self.posY+self.l, width = 2, outline = 'black') # creation du vaisseau
    
    def bouger_d(self):
        # Cette methode permet de déplacer le vaisseau vers la droite.
        
        if self.posX < 380:
            self.posX += 20
        self.MonCanvas.coords(self.vaisseau,self.posX-self.l,self.posY-self.l,self.posX+self.l,self.posY+self.l) # ici ya un probleme !!!
    
    def bouger_g(self):
        # Cette methode permet de déplacer le vaisseau vers la gauche.
        
        if self.posX > 20:
            self.posX -= 20
        self.MonCanvas.coords(self.vaisseau,self.posX-self.l,self.posY-self.l,self.posX+self.l,self.posY+self.l) # ici ya un probleme !!!


class Tir:
    # Cette classe contient tout ce qu'il faut pour gérer les tirs.
    
    def __init__(self,MonCanvas_,VposX):
        self.posX = 0
        self.posY = 340 # position initiale en y
        self.MonCanvas = MonCanvas_ # on prend le canvas dans la classe
        self.l = 6 # dimention du tir
        self._tir = None # c'est le tir
        self.posX = VposX # position initiale en x
        self._tir = self.MonCanvas.create_rectangle(self.posX,self.posY,self.posX+self.l,self.posY+self.l,fill = 'green') # creation du tir de couleur rouge
        
    def bouger(self):
        #Cette methode permet de faire bouger les tirs du vaisseau
        
        self.posY -= 1
        self.MonCanvas.coords(self._tir,self.posX,self.posY,self.posX+self.l,self.posY+self.l)

class Alien:
    # Cette classe contient les informations necessaires a la creation des aliens. 
    
    def __init__(self,MonCanvas_,posX):
        self.posX = posX# position initiale en x
        self.posY = 30 # position initiale en y
        self.MonCanvas = MonCanvas_ # on prend le canvas dans la classe
        self.l = 10 # largeur/hauteur de l'alien
        self.alien = None # contient le canvas de l'alien
        self.sens = "d" # sens de deplacement de l alien, d ou g

    def creer(self):
        #Cette methode permet de creer un alien 
        
        self.alien = self.MonCanvas.create_rectangle(self.posX-self.l,self.posY-self.l,self.posX+self.l,self.posY+self.l, width = 2, outline = 'black') # creation du vaisseau
 
    def bouger(self):
        #Cette methode permet de faire bouger les aliens de maniere automatique
        
        if self.posX > 370 :
            self.sens = "g"
            self.posY += 30
        if self.posX < 30 :
            self.sens = "d"
            self.posY += 30
        if self.sens == "g":
            self.posX -= 1
        if self.sens == "d":
            self.posX += 1
            
        self.MonCanvas.coords(self.alien,self.posX-self.l,self.posY-self.l,self.posX+self.l,self.posY+self.l) # ici ya un probleme !!!

class Tir_alien:
    # Cette classe contient tout ce qu'il faut pour gérer les tirs d'aliens.
    
    def __init__(self,MonCanvas_,AposX,AposY):
        self.MonCanvas = MonCanvas_ # on prend le canvas dans la classe
        self.posX = 0
        self.posY = 0 # position initiale en y
        self.l = 6 # dimention du tir
        self._tir_alien = self.MonCanvas.create_rectangle(self.posX,self.posY,self.posX+self.l,self.posY+self.l,fill = 'red') # creation du tir de couleur rouge
    
    def bouger(self):
        #Cette methode permet de faire bouger les tirs des aliens 
        self.posY += 1
        
        self.MonCanvas.coords(self._tir_alien,self.posX-self.l,self.posY-self.l,self.posX+self.l,self.posY+self.l)
       

def jouer():
    #Cette fonction permet d'ouvrir une fenetre de jeu. 
    
    a = fenetre()
    a.creation_de_la_fenetre()
    

















