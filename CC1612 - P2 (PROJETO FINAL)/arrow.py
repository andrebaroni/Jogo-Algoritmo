# --------- CRIADO POR: --------  #

# ALEXANDRE CARDOSO FEITOSA RA: 22.217.002-9
# ANDRÉ LUIZ BARONI RA: 22.217.036-7
# LETICIA AUGUSTO RA: 22.217.039-1

# CENTRO UNIVERSITÁRIO FEI - CIÊNCIA DA COMPUTAÇÃO - 1°CICLO - 2°SEM/2017


# --------------------------- MÓDULOS --------------------------- #

import pygame
import sys
import random
from pygame.locals import *

pygame.init()

# --------------------------- CONSTANTES --------------------------- #
# ---- TAMANHOS PARA A JANELA DE JOGO ---- #
LARGURA = 1000
ALTURA = 500

# -- ABERTURA DA JANELA --- #
pygame.display.set_icon(pygame.image.load("imagens/logoArrow.png"))
pygame.display.set_caption("Ajude o Flash 2.0!")
tela = pygame.display.set_mode((LARGURA, ALTURA))

# --------- CORES --------  #
COR_BRANCA = (255, 255, 255)
COR_VERDE = (0, 155, 0)
COR_AZUL = (108, 194, 236)
COR_VERMELHA = (255, 0, 0)
GRAVIDADE = 1.29

# --------- SONS ---------- #
musica_menu = pygame.mixer.Sound("sons/musicamenu.ogg")
musica_fundo = pygame.mixer.Sound("sons/musicafundo.ogg")
musica_won = pygame.mixer.Sound("sons/musicawon.ogg")
somFlecha = pygame.mixer.Sound("sons/somFlecha.ogg")
musica_over = pygame.mixer.Sound("sons/musicalose.ogg")

# --------- FONTES -------- #
smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 80)

# --------------------------- FUNÇÕES --------------------------- #

# -- Definição de Estilos para textos -- #
def text_objects(text, varColor, size):
    if size == "small":
        textSurface = smallfont.render(text, True, varColor)
    elif size == "medium":
        textSurface = medfont.render(text, True, varColor)
    elif size == "large":
        textSurface = largefont.render(text, True, varColor)
    return textSurface, textSurface.get_rect()

# --- Renderização de Textos  ---------- #
def message_to_screen(msg, varColor, y_displace=0, size="small"):
    textSurf, textRect = text_objects(msg, varColor, size)
    textRect.center = (LARGURA /2), (ALTURA / 2) + y_displace
    tela.blit(textSurf, textRect)


# -------- Menu Inicial do Jogo --------- #
def game_intro():
    intro = True
    player=Arrow()
    player.rect.x=0
    player.rect.y=100
    active_sprite_list = pygame.sprite.Group()
    active_sprite_list.add(player)


    while intro:
        musica_menu.play(loops=-1)
        clock = pygame.time.Clock()
        tela.blit(ImagemFundoBlur, (0, 0))
        message_to_screen("Bem Vindo a Star City!", COR_VERDE, -100, "large")
        message_to_screen("Seu objetivo é salvar o Flash!", COR_VERDE, 30, "medium")
        message_to_screen("Tente chegar ao outro lado para salvá-lo", COR_VERDE, 80, "small")
        message_to_screen("Aperte espaço para jogar ou q para sair", COR_BRANCA, 180)
        clock.tick(200)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro = False
                    musica_menu.stop()
                    arrowplay()
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        pygame.display.flip()
        active_sprite_list.update()

        pygame.display.update()


# --------- Tela de Game-Over ----------- #
def game_over(pontuacao):
    gameover = True
    pts = str(pontuacao)
    flash = Flash(500, 360)
    musica_fundo.stop()
    musica_over.play()
    while gameover:
        clock = pygame.time.Clock()
        tela.blit(ImagemFundoBlur, (0, 0))
        message_to_screen("Você falhou com esta cidade!", COR_VERDE, -100, "medium")
        message_to_screen("Aperte espaço para jogar ou q para sair", COR_BRANCA, 180)
        message_to_screen("Sua pontuação final foi: %s" %pts, COR_AZUL, 30, "small")
        clock.tick(200)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    arrowplay()
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        flash.colocar(tela)
        pygame.display.flip()
        pygame.display.update()

# ---------- Tela Jogo Ganho ------------#
def game_won(pontuacao):
    gamewon = True
    flashcorrendo = Flashcorrendo(500, 310)
    speed = SpeedForce(830, 280)
    pts = str(pontuacao)
    musica_fundo.stop()
    musica_won.play()
    while gamewon:
        clock = pygame.time.Clock()
        tela.blit(ImagemFundoBlur, (0, 0))
        message_to_screen("Você salvou o Flash!", COR_VERDE, -100, "large")
        message_to_screen("Aperte espaço para jogar ou q para sair", COR_BRANCA, 180)
        message_to_screen("Sua pontuação final foi: %s" %pts, COR_AZUL, 30, "small")
        clock.tick(200)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    arrowplay()
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        flashcorrendo.colocar(tela)
        speed.colocar(tela)
        pygame.display.flip()
        pygame.display.update()

# --------------------------- OBJETOS ESTÁTICOS --------------------------- #
# --------- Plano de Fundo ----------- #
ImagemFundo = pygame.image.load("imagens/planoDeFundo.png").convert()
ImagemFundoBlur = pygame.image.load("imagens/planoDeFundoBlur.png").convert()
# --------- Calçada ----------- #
calcada = pygame.image.load("imagens/calcada.jpg")


# --------------------------- OBJETOS DINÂMICOS --------------------------- #

# --------- SpriteSheets ----------- #
class Sprite:
    # Carrega a imagem, usamos o convert() por ser uma imagem png
    def __init__(self, filename):
        self.sprite=pygame.image.load(filename).convert()
    # Pega o spritesheet e transforma em pequenas imagens
    def get_image(self,x,y,width,height):
        imagem= pygame.Surface([width,height]).convert()
        imagem.blit(self.sprite, (0,0),(x,y,width,height))
        # Cancela a cor Branca do fundo da sprite
        imagem.set_colorkey(COR_BRANCA)
        return imagem


# --------- Personagem Principal ----------- #
class Arrow(pygame.sprite.Sprite):
    posX=0
    posY=0
    andar_direita=[]
    andar_esquerda=[]
    # Direção que o player começa encarando, direita ou esquerda.
    direction='D'


    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        sprite=Sprite("imagens/arrow.png")
    # Carrega a sprite em lista, passando com parametro a imagem e suas coordenadas.
        image = sprite.get_image(0, 0, 97, 148)
        self.andar_direita.append(image)
        image = sprite.get_image(97, 0, 83, 148)
        self.andar_direita.append(image)
        image = sprite.get_image(180, 0, 92, 148)
        self.andar_direita.append(image)
        image = sprite.get_image(272, 0, 102, 148)

        # Muda a animação para a esquerda, ou seja, vira a imagem.
        image = sprite.get_image(0, 0, 97, 148)
        # Método flip, vira a imagem, mudando apenas o X (True) da imagem  e mantendo o Y (False) para nao ficar de ponta cabeça.
        image = pygame.transform.flip(image, True, False)
        self.andar_esquerda.append(image)
        image = sprite.get_image(97, 0, 83, 148)
        image = pygame.transform.flip(image, True, False)
        self.andar_esquerda.append(image)
        image = sprite.get_image(180, 0, 92, 148)
        image = pygame.transform.flip(image, True, False)
        self.andar_esquerda.append(image)
        image = sprite.get_image(272, 0, 102, 148)
        image = pygame.transform.flip(image, True, False)
        self.andar_esquerda.append(image)

        # Começando com a primeira iamgem da lista [0]
        self.image= self.andar_direita[0]
        self.rect=self.image.get_rect()
        self.rect.centerx = 50
        self.rect.centery = ALTURA - 95


        self.listaDisparo = []
        self.listaDisparoContrario=[]
        self.vida = True
        self.velocidade = 50

    def movimentoDireita(self):
        self.posX = 6
        self.direction = "D"
        # Limitando a movimentação para que o personagem não saia da tela
        if self.rect.x < 900:
            self.rect.x += self.velocidade
        self.__movimento()
        pos = self.rect.x + self.velocidade
        if self.direction == "D":
            frame = pos % len(self.andar_direita)
            self.image = self.andar_direita[frame]
        else:
            frame = pos % len(self.andar_esquerda)
            self.image = self.andar_esquerda[frame]


    def movimentoEsquerda(self):
        self.posX = -6
        self.direction = "E"
        # Limitando a movimentação para que o personagem não saia da tela
        if self.rect.x > 10:
            self.rect.x -= self.velocidade
        self.__movimento()
        pos = self.rect.x + self.velocidade
        if self.direction == "E":
            frame = pos % len(self.andar_esquerda)
            self.image = self.andar_esquerda[frame]
        else:
            frame = pos % len(self.andar_direita)
            self.image = self.andar_direita[frame]

    def __movimento(self):
        # Limitação, para não passar da parede.
        if self.vida == True:
            if self.rect.top + 101 >= 500:
                self.rect.top = 350
            elif self.rect.top <= 0:
                self.rect.top = 0

    def disparar(self, x, y):
        minhaFlecha = Flecha(x, y)
        self.listaDisparo.append(minhaFlecha)
        somFlecha.play()

    def dispararContraria(self, x, y):
        minhaFlecha = FlechaInversa(x, y)
        self.listaDisparoContrario .append(minhaFlecha)
        somFlecha.play()


    def colocar(self, superficie):
        superficie.blit(self.image, self.rect)


# ------- Flash ------ #
class Flash(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
        pygame.sprite.Sprite.__init__(self)
        self.imagemFlash = pygame.image.load("imagens/flash1.png") #flash caido

        self.listaImagens = [self.imagemFlash]
        self.posImagem = 0
        self.imagemFlash = self.listaImagens[self.posImagem]
        self.rect = self.imagemFlash.get_rect()

        self.rect.right = posx
        self.rect.left = posx - 60
        self.rect.top = posy



    def colocar(self, superficie):
        self.imagemFlash = self.listaImagens[self.posImagem]
        superficie.blit(self.imagemFlash, self.rect)

class Flashcorrendo(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
        pygame.sprite.Sprite.__init__(self)
        self.imagemFlashcorrendo = pygame.image.load("imagens/flashcorrendo.png")  # flash correndo

        self.listaImagens = [self.imagemFlashcorrendo]
        self.posImagem = 0
        self.imagemFlashcorrendo = self.listaImagens[self.posImagem]
        self.rect = self.imagemFlashcorrendo.get_rect()

        self.rect.right = posx
        self.rect.left = posx - 60
        self.rect.top = posy

    def colocar(self, superficie):
        self.imagemFlashcorrendo = self.listaImagens[self.posImagem]
        superficie.blit(self.imagemFlashcorrendo, self.rect)

class SpeedForce(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
        pygame.sprite.Sprite.__init__(self)
        self.imagemSpeedforce = pygame.image.load("imagens/speedforce.png")  # flash correndo

        self.listaImagens = [self.imagemSpeedforce]
        self.posImagem = 0
        self.imagemSpeedforce = self.listaImagens[self.posImagem]
        self.rect = self.imagemSpeedforce.get_rect()

        self.rect.right = posx
        self.rect.left = posx - 60
        self.rect.top = posy

    def colocar(self, superficie):
        self.imagemSpeedforce = self.listaImagens[self.posImagem]
        superficie.blit(self.imagemSpeedforce, self.rect)


# --------- Inimigos ----------- #
class Inimigo(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
        pygame.sprite.Sprite.__init__(self)
        self.ImagemInimigo1 = pygame.image.load("imagens/pistoleiro.png")

        self.listaImagens = [self.ImagemInimigo1]
        self.posImagem = 0
        self.ImagemInimigo = self.listaImagens[self.posImagem]

        self.rect = self.ImagemInimigo.get_rect()

        self.listaDisparo = []
        self.velocidade = 20
        self.rect.right = posx
        self.rect.left = posx - 96
        self.rect.top = posy


    def colocar(self, superficie):
        self.ImagemInimigo = self.listaImagens[self.posImagem]
        superficie.blit(self.ImagemInimigo, self.rect)

    def atingido(self):
        self.rect.right = -1000
        self.rect.left = -1000
        self.rect.top = -1000


# --------- Flechas ----------- #
class Flecha(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
        pygame.sprite.Sprite.__init__(self)
        self.ImagemFlecha = pygame.image.load("imagens/flecha1.png")

        self.rect = self.ImagemFlecha.get_rect()
        self.velocidadeFlecha = 4
        self.rect.right = posx
        self.rect.top = posy



    def trajetoria(self):
        self.rect.right = self.rect.right + self.velocidadeFlecha
        self.rect.top = self.rect.top

    def colocar(self, superficie):
        superficie.blit(self.ImagemFlecha, self.rect)


# --------- Flechas Invertidas ----------- #
class FlechaInversa(pygame.sprite.Sprite):
    def __init__(self, posx: object, posy: object) -> object:
        pygame.sprite.Sprite.__init__(self)
        self.ImagemFlecha = pygame.image.load("imagens/flecha_invertida.png")
        self.rect = self.ImagemFlecha.get_rect()
        self.velocidadeFlecha = 4
        self.rect.left = posx
        self.rect.top = posy



    def trajetoriaInversa(self):
        self.rect.left = self.rect.left - self.velocidadeFlecha
        self.rect.top = self.rect.top


    def colocar(self, superficie):
        superficie.blit(self.ImagemFlecha, self.rect)


# ---------------------- FUNÇÃO PRINCIPAL DO JOGO ------------------------ #
def arrowplay():
    pontuacao = 0
    musica_over.stop()
    musica_won.stop()
    musica_fundo.play(loops=-1)
    jogador = Arrow()
    inimigo = Inimigo(900, 340)
    flash = Flash(910, 400)
    flecha = Flecha(100, 370)
    flechaInversa = FlechaInversa(100,370)

    # --------- Laço Principal ----------- #
    while True:
        flecha.trajetoria()
        flechaInversa.trajetoriaInversa()
        # Controlamos o funcionamento do nosso jogo através dos eventos
        for event in pygame.event.get():
            # Evento de clique no botão fechar
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Evento de pressionamento de uma tecla
            if event.type == pygame.KEYDOWN:
                # Eventos que são responsáveis pela movimentação do personagem
                if event.key == pygame.K_RIGHT:
                    jogador.movimentoDireita()
                    #inimigo = Inimigo(random.randint(500, 970), 340)  # Randomizar
                elif event.key == pygame.K_LEFT:
                    jogador.movimentoEsquerda()
                    #inimigo = Inimigo(random.randint(500, 980), 340)  # Randomizar

                # Evento que controla a saída das flechas
                elif event.key == K_SPACE:
                    if jogador.direction == "D":
                        # Limitando a duas flechas por frame
                        if len(jogador.listaDisparo) < 2:
                            x, y = jogador.rect.center
                            jogador.disparar(x+100, y-50)

                    elif jogador.direction == "E":
                        # Limitando a duas flechas por frame
                        if len(jogador.listaDisparo) < 2:
                            x, y = jogador.rect.center
                            jogador.dispararContraria(x-100, y-50)

        # Colocando os Objetos na Tela (X e Y iniciais)
        tela.blit(ImagemFundo, (0, 0))
        tela.blit(calcada, [0, 450])
        jogador.colocar(tela)
        inimigo.colocar(tela)
        flash.colocar(tela)

        # Detectando colisões envolvendo as flechas
        if len(jogador.listaDisparo) > 0:
            for x in jogador.listaDisparo:
                x.colocar(tela)
                x.trajetoria()
                # Removendo a flecha após sair da tela
                if x.rect.x > 1000:
                    jogador.listaDisparo.remove(x)
                    inimigo = Inimigo(random.randint(500, 900), 340)  # Randomizar
                # Colisão da Flecha com os inimigos
                if x.rect.x + 70 >= inimigo.rect.left and x.rect.y >= inimigo.rect.top and x.rect.x - 89 < inimigo.rect.right:
                    pontuacao += 1
                    inimigo.atingido()
        elif len(jogador.listaDisparoContrario) > 0:
            for x in jogador.listaDisparoContrario:
                x.colocar(tela)
                x.trajetoriaInversa()
                # Removendo a flecha após sair da tela
                if x.rect.x < -100:
                    jogador.listaDisparoContrario.remove(x)
                    inimigo = Inimigo(random.randint(500, 900), 340)  # Randomizar
                # Colisão da Flecha com os inimigos
                if x.rect.x + 70 >= inimigo.rect.left and x.rect.y >= inimigo.rect.top and x.rect.x - 89 < inimigo.rect.right:
                    pontuacao += 1
                    inimigo.atingido()


        # Colisão do Personagem Principal com o Inimigo
        if jogador.rect.x + 100 >= inimigo.rect.left and jogador.rect.x + 18 <= inimigo.rect.right:
            # Caso haja colisão, chamaremos a função game over.
            game_over(pontuacao)
        if jogador.rect.x + 10>= flash.rect.left:
            game_won(pontuacao)

        # Placar
        message_to_screen(str(pontuacao), COR_VERDE, -200)

        # Faz com que a janela seja constantemente atualizada
        pygame.display.update()


game_intro()
