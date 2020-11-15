import tkinter as tk
from PIL import Image, ImageTk 
import sys,math

"""Interfaz gráfica"""
app = tk.Tk() #definimos la ventana de la aplicacion
app.title("SUDOKU SOLVER by @contreraspablo9") #titulo de la ventana
app.resizable(width=False, height=False) #tamaño de ventana fijo
app.geometry("432x432")
imagen = Image.open("/Users/contr/Desktop/SudokuSolver/Fondo.gif") #Importar imagen
fondo = ImageTk.PhotoImage(imagen) # declarar el fondo

#dibujar en la ventana
cuadricula = tk.Canvas(app, width = "432", height = "432") #crea el lienzo
cuadricula.pack(side='top', fill='both', expand = "yes")
cuadricula.create_image(0,0,image = fondo, anchor = "nw") #agregar el fondo

#crear la matriz para imprimir numeros
letra = [[cuadricula.create_text(24+x*48,24+y*48,text = " ", font=("arial", 35),fill = "darkred") for x in range(9)] for y in range(9)]
cuadricula.update()
#cuadricula.remove(letra) #borrar un objeto del canvas

"""Motor de la app"""
listo = 0 #bandera problema resuelto
anterio = 0
actual = 0
def actualizar_matrices():
    global sudoku
    global posibles
    global anterior,actual
    #escribimos en los espacios con solo un candidato posible
    for renglon in range(9):
        for columna in range(9):
            if sudoku[renglon][columna] == 0: #el espacio esta vacio?
                cont = 0 
                for posible in range(9):#contamos los candidatos posibles para una casilla
                    if posibles[renglon][columna][posible]!=0:
                           cont+=1 
                if cont == 1: #cuando solo queda un candidato para la casilla
                    for posible in range(9): #identificamos al candidato
                        if posibles[renglon][columna][posible]!=0: #ya lo encontramos
                            for x in range(9):
                                    posibles[renglon][columna][x]=0 #eliminamos todos los candidatos de esa casilla
                            for x in range(9):
                                posibles[renglon][x][posible]=0 #eliminamos el candidato en todo el renglon
                                posibles[x][columna][posible]=0 #y en toda la columna
                            #eliminamos al candidato de todo el cuadrante
                            inicio_x = -(columna % 3) #inicio del barrido en x
                            inicio_y = -(renglon % 3) #inicio del barrido en y
                            for y in range(inicio_y,inicio_y+3):
                                for x in range(inicio_x,inicio_x+3):
                                    posibles[renglon+y][columna+x][posible]=0 #eliminamos el candidato en todo el cuadrante
                            sudoku[renglon][columna] = posible + 1 #rescribimos el nuevo numero
                            #mostramos el nuevo numero
                            cuadricula.itemconfigure(letra[renglon][columna], text=sudoku[renglon][columna], fill= "black")
                            
            else: #si el espacio ya esta ocupado
                for x in range(9): #borramos todos sus candidatos
                    posibles[renglon][columna][x] = 0
                
                

def salir():
    global listo 
    cont = 0
    for renglon in range(9):
        for columna in range(9):
            if sudoku[renglon][columna]!=0:
                cont+=1
    if cont == 81:
        listo = 1
    
    
def sudoku_solve():
    global anterior,actual
    global listo
    global posibles
    global sudoku
    while listo == 0:
        #encontramos los posibles numeros para cada casilla
        #verificamos primero lo que ya esta escrito en pantalla:
        for renglon in range(9): 
            for columna in range(9):
                if sudoku[renglon][columna] == 0: #solo buscamos para casillas vacias
                    for posible in range(1,10): #proponemos un candidato
                        bandera = 1 #suponemos que si es un candidato
                        for x in range(9):
                            if posible == sudoku[renglon][x]:#si ya existe en el renglon
                                bandera = 0 #descartamos el candidato
                            if posible == sudoku[x][columna]:#si ya existe en la columna
                                bandera = 0 #descartamos el candidato
                        #verificamos dentro del cuadrante 
                        inicio_x = -(columna % 3) #inicio del barrido en x
                        inicio_y = -(renglon % 3) #inicio del barrido en y
                        for y in range(inicio_y,inicio_y+3):
                            for x in range(inicio_x,inicio_x+3):    
                                if posible==sudoku[renglon+y][columna+x]: #si ya existe
                                    bandera = 0 #descartar candidato
                        if bandera == 1: #si no fue descartado
                            posibles[renglon][columna][posible-1]=posible #guardamos al candidato
                    
        actualizar_matrices()
        
        #Ahora verificamos a nivel de las posibles respuestas para cada casilla
        for renglon in range(9):
            for columna in range(9):
                if sudoku[renglon][columna]==0: #solo buscamos en las casillas vacías
                    for posible in range(9): #proponemos un candidato
                        if posibles[renglon][columna][posible]!=0: #solo si es un candidato valido
                            bandera = 1
                            for x in range(9): #buscamos si el candidato es posible en otra parte del renglon 
                                if posibles[renglon][columna][posible]==posibles[renglon][x][posible] and columna!=x and sudoku[renglon][x]==0:
                                    bandera = 0 #nuestro candidato no es definitivo
                            if bandera == 0: #si aun no lo encontramos
                                bandera = 1
                                for y in range(9): #buscamos si el candidato es posible en otra parte de la columna
                                    if posibles[renglon][columna][posible]==posibles[y][columna][posible] and renglon!=y and sudoku[y][columna]==0:
                                        bandera = 0 #nuestro candidato no es definitivo 
                            if bandera == 0:
                                #ahora vamos a buscar dentro del cuadrante
                                bandera = 1
                                inicio_x = -(columna % 3) #inicio del barrido en x
                                inicio_y = -(renglon % 3) #inicio del barrido en y
                                for y in range(inicio_y,inicio_y+3):
                                    for x in range(inicio_x,inicio_x+3):
                                        if columna!=columna+x or renglon!=renglon+y and posibles[renglon][columna][posible]==posibles[renglon+y][columna+x][posible] and sudoku[renglon+y][columna+x]==0: #si puede estar en otra casilla del cuadrante
                                            bandera = 0 #nuestro candidato no es definitivo
                            #se pueden agregar mas filtros              
                                            
                            if bandera == 1: #si el candidato es definitivo
                                for x in range(9):
                                    posibles[renglon][columna][x]=0 #eliminamos todos los candidatos de esa casilla
                                for x in range(9):
                                    posibles[renglon][x][posible]=0 #eliminamos el candidato en todo el renglon
                                    posibles[x][columna][posible]=0 #y en toda la columna
                                inicio_x = -(columna % 3) #inicio del barrido en x
                                inicio_y = -(renglon % 3) #inicio del barrido en y
                                for y in range(inicio_y,inicio_y+3):
                                    for x in range(inicio_x,inicio_x+3):
                                        posibles[renglon+y][columna+x][posible]=0 #eliminamos el candidato en todo el cuadrante
                                sudoku[renglon][columna] = posible + 1 #rescribimos el nuevo numero
                                #mostramos el nuevo numero
                                cuadricula.itemconfigure(letra[renglon][columna], text=sudoku[renglon][columna], fill= "black")
                                cuadricula.update()
                            
        actualizar_matrices()
        salir()
                        

def click(event): #Registra los clics en la ventana
    global posx
    global posy
    posx = event.x
    posx = math.floor(posx*9/432) #truncar numeros a enteros
    posy = event.y
    posy = math.floor(posy*9/432) #truncar numeros a enteros
    if posx > 8: #limitar posiciones x y 
        posx = 8
    if posx < 0:
        posx = 0
    if posy > 8: 
        posy = 8
    if posy < 0:
        posy = 0
    
def tecla(event): #Ingresar datos
    global sudoku
    num = ord(event.char) #convertir a ascii
    if num > 48 and num < 58: #Filtrar teclas no numericas
        num = num - 48  #convertir a entero
        cuadricula.itemconfigure(letra[posy][posx], text = num)
        sudoku[posy][posx] = num
    elif num == 8: #backspace
        cuadricula.itemconfigure(letra[posy][posx], text = " ")
        sudoku[posy][posx] = 0
        cuadricula.update()
    elif num == 13:
        sudoku_solve()

        

#ventana_emergente = Toplevel() #Sirve para definir ventanas emergentes
#ventana_emergente.wait_window() #Atender eventos dentro hasta que la ventana se cierre

posx = 0 #inicializar variables de posicion
posy = 0
sudoku = [[0 for x in range(9)] for y in range(9)] #crea matriz x por y
#Posibilidades para cada casilla:
posibles = [[[0 for _ in range(9)] for _ in range(9)] for _ in range(9)]
app.bind("<Key>", tecla)
app.bind("<Button-1>", click)

app.mainloop() #aplicacion principal
