import tkinter as tk
from tkinter import messagebox

class JocSahTkinter:
    def __init__(self, master):
        self.master = master
        self.master.title("Joc de Sah - Tkinter")

        #Configurez tabla de sah initiala
        self.tabla = [
            ["♜", "♞", "♝", "♛", "♚", "♝", "♞", "♜"],  #Turnuri, cai, nebuni, regina, rege
            ["♟", "♟", "♟", "♟", "♟", "♟", "♟", "♟"],  #Pioni
            [".", ".", ".", ".", ".", ".", ".", "."],  #Locuri goale
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            ["♙", "♙", "♙", "♙", "♙", "♙", "♙", "♙"],   #Pioni albi
            ["♖", "♘", "♗", "♕", "♔", "♗", "♘", "♖"]   #Turnuri, cai, nebuni, regina, rege albi
        ]

        self.selectie = None
        self.jucator = "Alb"  #Incepem cu jucatorul alb
        self.creeaza_tabla()

    def creeaza_tabla(self):
        """Fac tabla de sah si pun butoanele corespunzatoare"""
        self.frame_tabla = tk.Frame(self.master)
        self.frame_tabla.pack()



        
        self.butoane = []  #Lista in care tin butoanele
        for i in range(8):  #Parcurg randurile
            rand = []  #Lista pentru fiecare rand
            for j in range(8):  #Parcurg coloanele
                culoare = "#DDB88C" if (i + j) % 2 == 0 else "#A66D4F"  #Alternarea culorilor
                buton = tk.Button(self.frame_tabla, width=4, height=2, bg=culoare,
                                  command=lambda x=i, y=j: self.selecteaza_casuta(x, y))  #Apelam functie la apasare
                buton.grid(row=i, column=j)
                rand.append(buton)  #Adaug butonul in rand
            self.butoane.append(rand)  #Adaug randul la lista de butoane
        
        self.afiseaza_tabla()

    def afiseaza_tabla(self):
        #Actualizez tabla si pun piesele pe ea
        for i in range(8):  # Parcurg randurile
            for j in range(8):  #Parcurg coloanele
                piesa = self.tabla[i][j]  #Preiau piesa de pe tabla
                culoare = "#DDB88C" if (i + j) % 2 == 0 else "#A66D4F"  #Alege culoarea
                self.butoane[i][j].config(text=piesa if piesa != "." else "", bg=culoare)  #Actualizez butonul

    def selecteaza_casuta(self, x, y):
        #Gestionez selectie si mutare piesa
        if self.selectie is None:  # Daca nu e nicio selectie anterioara
            if self.tabla[x][y] == ".":  #Daca selectez o casuta goala, nu se intampla nimic
                return

            # Verific daca piesa apartine jucatorului curent
            if (self.jucator == "Alb" and self.tabla[x][y].islower()) or (self.jucator == "Negru" and self.tabla[x][y].isupper()):
                messagebox.showwarning("Eroare", "Este randul celuilalt jucator")  #eroare daca piesa apartine altui jucator
                return

            self.selectie = (x, y)  #Setez piesa selectata
            self.butoane[x][y].config(bg="yellow")  #Marchez piesa selectata cu galben
        else:
            x1, y1 = self.selectie  #Preiau coordonatele piesei selectate
            if self.mutare_valida(x1, y1, x, y):  #Verific daca mutarea este valida
                self.muta_piesa(x1, y1, x, y)  #Mut piesa

                # Alternam jucatorul dupa fiecare mutare valida
                self.jucator = "Negru" if self.jucator == "Alb" else "Alb"

            else:
                messagebox.showwarning("Mutare invalida", "Mutare invalida conform regulilor jocului.")  #mutare invalida
            self.selectie = None  #Resetam selectie
            self.afiseaza_tabla()  #Actualizam tabla


    def mutare_valida(self, x1, y1, x2, y2):
        #Verific daca mutarea piesei este valida
        piesa = self.tabla[x1][y1]
        tinta = self.tabla[x2][y2]

        #Verific daca piesa tinta e de aceeasi culoare
        if (piesa.isupper() and tinta.isupper()) or (piesa.islower() and tinta.islower()):
            return False  #Nu putem captura o piesa de aceeasi culoare

        dx, dy = abs(x2 - x1), abs(y2 - y1)

        if piesa in "♙♟":  #Pion
            directie = -1 if piesa == "♙" else 1  #directia de miscare pentru pioni
            if y1 == y2 and (x2 - x1) == directie and tinta == ".":
                return True  # Mutare standard pe verticala
            if y1 == y2 and (x2 - x1) == 2 * directie and self.tabla[x1 + directie][y1] == "." and tinta == ".":
                if (piesa == "♙" and x1 == 6) or (piesa == "♟" and x1 == 1):
                    return True  #Mutare initiala de doua casute
            if dx == 1 and dy == 1 and (x2 - x1) == directie and tinta != ".":
                return True  #Capturare pe diagonala

        elif piesa in "♖♜":  #Tura
            if x1 == x2 or y1 == y2:
                return self.cale_libera(x1, y1, x2, y2)  #Verific daca calea e libera

        elif piesa in "♘♞":  #Cal
            if (dx, dy) in [(2, 1), (1, 2)]:
                return True  # Calul poate muta in forma de L

        elif piesa in "♗♝":  #Nebun
            if dx == dy:
                return self.cale_libera(x1, y1, x2, y2)  # Verific daca calea e libera pe diagonala

        elif piesa in "♕♛":  #Dama
            if dx == dy or x1 == x2 or y1 == y2:
                return self.cale_libera(x1, y1, x2, y2)  # Dama poate muta pe orice directie

        elif piesa in "♔♚":  #Rege
            if max(dx, dy) == 1:
                return True  # Regele poate muta pe o casuta vecina

        return False

    def cale_libera(self, x1, y1, x2, y2):
        #Verific daca calea dintre doua casute este libera
        dx = (x2 - x1) // max(1, abs(x2 - x1)) if x1 != x2 else 0
        dy = (y2 - y1) // max(1, abs(y2 - y1)) if y1 != y2 else 0
        x, y = x1 + dx, y1 + dy
        while (x, y) != (x2, y2):  #parcurg toate casutele de pe drum
            if self.tabla[x][y] != ".":
                return False   #Daca gasim o piesa pe drum, calea nu e libera
            x, y = x + dx, y + dy
        return True

    def muta_piesa(self, x1, y1, x2, y2):
        """Mut piesa de la x1, y1 la x2, y2"""
        self.tabla[x2][y2] = self.tabla[x1][y1]  #Mut piesa pe tabla
        self.tabla[x1][y1] = "."  #Sterg piesa din pozitia initiala


if __name__ == "__main__":
    root = tk.Tk()
    app = JocSahTkinter(root)
    root.mainloop()