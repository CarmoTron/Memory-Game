from tkinter import messagebox
from tkinter import *                                # noqa: F403, E999
import tkinter as tk
import random
import pygame
import time 

#definir as configuraçoes do jogo
#CONSTANTES
N_LIN= 4
N_COL= 4
CARTAO_SIZE_W=10
CARTAO_SIZE_H=5
CARTAO_COR= ['red','blue','green','yellow','orange','purple','cyan','white']
COR_FUNDO = '#343A40'
COR_LETRA = '#feffff'
FONT_STYLE={'Consolas',12,'bolder'}
MAX_TENTATIVAS = 20
TEMPO=90
tries = 0
tempo_inicial = 0
tempo_restante = TEMPO

pygame.init()

#funcoes
def play():
    pygame.mixer.init()
    pygame.mixer.music.load("mp3/good-night-160166.mp3")
    pygame.mixer.music.play(-1)

# menu inicial



def menu_inicial():
    global menu_janela
    menu_janela = tk.Toplevel(janela)
    menu_janela.title('Menu Inicial')
    menu_janela.geometry('300x200')

    botao_inicio = tk.Button(menu_janela,text='Iniciar Jogo',command=start_game)
    botao_como_jogar = tk.Button(menu_janela,text='Como Jogar',command=mostrar_instrucoes)
    botao_sair = tk.Button(menu_janela,text='SAIR', command=janela.destroy)

    botao_inicio.pack(pady=12)
    botao_como_jogar.pack(pady=12)
    botao_sair.pack(pady=12)

#funcoes suplementares -> tempo

def iniciar_tempo():
    global tempo_inicial
    tempo_inicial = time.time()

def atualizar_tempo():
    global tempo_restante
    tempo_passado = int(time.time() - tempo_inicial)
    tempo_restante = TEMPO- tempo_passado

    if tempo_restante <= 0:
        tempo_restante = 0
        game_over()

    janela.after(2000, atualizar_tempo) 

#criar grelha aleatoria para img/cores para o cartoes

def criar_grade():
    cores=CARTAO_COR*2
    random.shuffle(cores)
    grelha=[]

    for _ in range(N_LIN):
        linha = []
        for _ in range(N_COL):
            cor = cores.pop() #remove se existir cor igual 
            linha.append(cor) 
        grelha.append(linha)
    return grelha

#messageboxes
######
def game_over():
    messagebox.showinfo('Game Over', ' Você perdeu o jogo. Better luck next time!')
    menu_inicial()
    janela.withdraw()
    
def mostrar_instrucoes():
    messagebox.showinfo("Como Jogar", "Objetivo do jogo:\nEncontrar os pares das cartas no\nmenor tempo possível e com menos tentativas possíveis!\nBOA SORTE!")

def sobre():
    messagebox.showinfo('Sobre', 'Olá, sou o Bruno Carmo, este jogo foi desenvolvido por mim em python com a GUI Tkinter\nversion 1.0 - Outubro 2023')
######

####
#criar funçao para o clique
def click_na_carta(linha,coluna):
    carta = cartoes[linha][coluna]
    cor = carta['bg']
    if cor == 'black':
        carta['bg'] = grelha[linha][coluna]
        cartas_reveladas.append(carta)

        if len(cartas_reveladas) == 2:
            janela.update()
            jogada() 
     
# criar funcao para verificar jogada, check win e atualizar score
def jogada():
    carta1,carta2=cartas_reveladas
    if carta1['bg'] == carta2['bg']:
        cartas_iguais.extend([carta1,carta2])

        verifica_win()
    else:
        # Somente redefina a imagem para cartas não correspondentes
        carta1.after(350,lambda : carta1.config(bg='black'))
        carta2.after(350,lambda : carta2.config(bg='black'))

    cartas_reveladas.clear()
    atualizar_pontos()
####

def verifica_win():
    if len(cartas_iguais) == N_LIN * N_COL:
        messagebox.showinfo('PARABÉNS','VOCÊ GANHOU O JOGO!')
        menu_inicial()
        janela.withdraw()
####

def atualizar_pontos():
    global tries #ask teacher uma maneira mais correta..
    tries +=1
    label_tempo_restante.config(text=f'Tempo Restante: {tempo_restante} s')
    label_tentativas.config(text='Tentativas: {}/{}'.format(tries,MAX_TENTATIVAS),fg=COR_LETRA, bg=COR_FUNDO,font=FONT_STYLE)
    if tries>= MAX_TENTATIVAS or tempo_restante <= 0:
        game_over()
    else:
        label_tempo_restante.config(text=f'Tempo Restante: {tempo_restante} s')
        label_tentativas.config(text='Tentativas: {}/{}'.format(tries,MAX_TENTATIVAS),fg=COR_LETRA, bg=COR_FUNDO,font=FONT_STYLE)
        
####
#start new game e nova janela
def start_game():
    janela.deiconify()
    menu_janela.destroy()
    reset_game()

def reset_game():
    global tries, tempo_restante, cartoes, cartas_reveladas, cartas_iguais
    tries = 0
    tempo_restante = TEMPO
    label_tempo_restante.config(text=f'Tempo Restante: {tempo_restante} s')

    cartas_reveladas = []
    cartas_iguais = []
    grelha = criar_grade()

    for linha in range(N_LIN):
        for col in range(N_COL):
            cor = grelha[linha][col]
            cartoes[linha][col]['bg'] = 'black'

    label_tentativas.config(text=f'Tentativas: {tries}/{MAX_TENTATIVAS}')

    iniciar_tempo()
    atualizar_tempo()
    play()

######

###FIM DAS FUNCOES ###
#
#
### MAIN ###

#criar a interface 
janela = tk.Tk() #ask teacher
janela.title('Jogo de Memória')
janela.configure(bg=COR_FUNDO)


menu_inicial()

#criar grelha para os cartoes

grelha = criar_grade()
cartoes =[]
cartas_reveladas = []
cartas_iguais = []

for linha in range(N_LIN):
    linha_cartoes = []
    for col in range(N_COL):
        #botao
        global carta
        carta = tk.Button(janela, width=CARTAO_SIZE_W, height=CARTAO_SIZE_H, relief=tk.RAISED, bd=3,command=lambda li=linha, c=col: click_na_carta(li,c))
        #grid é grelha, funcao ja existente 
        carta.grid(row=linha, column=col, padx=5, pady=5)
        linha_cartoes.append(carta)
    cartoes.append(linha_cartoes)

#personalizar o botao
button_style = {'activebackground':'#f8f9fa','font':FONT_STYLE, 'fg':COR_LETRA}
janela.option_add("Button",button_style)


#label para as tentativas
label_tentativas = tk.Label(janela,text='Tentativas: {}/{}'.format(tries,MAX_TENTATIVAS),fg=COR_LETRA, bg=COR_FUNDO,font=FONT_STYLE)
label_tentativas.grid(row=N_LIN,columnspan=N_COL,padx=10,pady=10)
label_tempo_restante = tk.Label(janela, text=f'Tempo Restante: {tempo_restante} s', fg=COR_LETRA, bg=COR_FUNDO, font=FONT_STYLE)
label_tempo_restante.grid(row=N_LIN + 1, columnspan=N_COL, padx=10, pady=10)

## codigo para aparecer menu em cima
menubar = Menu(janela)
janela.config(menu=menubar)

file_menu = Menu(menubar, tearoff=False)
file_menu.add_command(label='Menu',command=menu_inicial)
file_menu.add_command(label='Novo',command=reset_game)
file_menu.add_separator()

file_menu.add_command(label='Sair',command=janela.destroy)
menubar.add_cascade(label='Ficheiro',menu=file_menu,underline=0)

about_menu = Menu(menubar,tearoff=0)
about_menu.add_command(label='Sobre',command=sobre)
about_menu.add_command(label='Como jogar',command=mostrar_instrucoes)

menubar.add_cascade(label='Ajuda', menu=about_menu)

#codigo para a janela aparecer no meio do ecrã
########

janela.update()

width_janela = janela.winfo_width()
height_janela = janela.winfo_height()
width_ecra = janela.winfo_screenwidth()
height_ecra = janela.winfo_screenheight()

x = int((width_ecra / 2) - (width_janela / 2))
y = int((height_ecra / 2) - (height_janela / 2))

janela.geometry(f'{width_janela}x{height_janela}+{x}+{y}')
#para a geometria da janela nao afetar nenhuma modificaçao colocamos
#resizable false false
janela.resizable(width=False, height=False)
#######

janela.withdraw()
janela.mainloop()

## FIM DA MAIN
