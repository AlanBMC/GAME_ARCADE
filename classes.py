import time
import pygame
from variaveis_global import *
from variaveis_gravidade_pulo import *

class Mago:
    def __init__(self, x, y, sprite_parado_frente, vida):
        self.x = 250
        self.y = y
        self.posicao_ataquex = 180
        self.posicao_ataquey = 420
        self.sprite_parado_frente = sprite_parado_frente
        self.sprite_andando_frente = None
        self.sprite_anda_tras = None
        self.sprite_parado_tras = None
        self.velocidade_pulo = ALTURA_DO_PULO
        self.pulando = False
        self.vida = vida
        self.ataque1 = None
        self.atacando = False
        self.andando_f = False
        self.andando_t = False
        self.direcao_ataque = 'frente'
        self.ultima_direcao = 'frente'
        self.rec = None
        self.bloco_vida = None
        self.borda_geral = None
        self.borda_maior = None
        self.ultimo_dano = time.time()
        self.cooldown = 1.0
        
    def carrega_sprites(self):
        self.colisor = pygame.transform.scale(pygame.image.load(
            'sprite_colisor_mago/1.png').convert_alpha(), (100, 100))
        self.sprite_parado_frente = [pygame.transform.scale(pygame.image.load(
            f'parado_f/parado ({i+1}).png').convert_alpha(), (100, 100)) for i in range(17)]
        self.sprite_parado_tras = [pygame.transform.scale(pygame.image.load(
            f'mago_parado_t/{i+1}.png').convert_alpha(), (100, 100)) for i in range(8)]
        self.sprite_andando_frente = [pygame.transform.scale(pygame.image.load(
            f'anda_mago_f/frente ({i+1}).png').convert_alpha(), (100, 100)) for i in range(8)]
        self.sprite_anda_tras = [pygame.transform.scale(pygame.image.load(
            f'anda_mago_t/frente ({i+1}).png').convert_alpha(), (100, 100)) for i in range(8)]

        self.bloco_vida = pygame.transform.scale(pygame.image.load(
            f'barra_vida/bloco vida (16).png').convert_alpha(), (17, 18))
        self.borda_geral = pygame.transform.scale(pygame.image.load(
            f'barra_vida/borda_barra.png').convert_alpha(), (250, 50))
        self.borda_maior = pygame.transform.scale(pygame.image.load(
            f'barra_vida/borda_gui.png').convert_alpha(), (120, 100))

        self.ataque1 = [pygame.transform.scale(pygame.image.load(
            f'ataque1_mago/15 ({i+1}).png').convert_alpha(), (140, 140)) for i in range(15)]

    def criar_retangulo(self):
        # Criamos o retângulo a partir do primeiro sprite
        self.rec = self.colisor.get_rect()
        self.ataque1_rec = self.ataque1[0].get_rect()

    def carregar_posicao(self, x, y):
        self.rec.x = 250
        self.rec.y = y
        self.ataque1_rec.x = self.posicao_ataquex
        self.ataque1_rec.y = self.posicao_ataquey

    def movimentacao2(self):
        global EM_CIMA_DO_BLOCO, VELOCIDADE, ACELERACAO_Y, PULANDO, ALTURA_MAX_PULO, EM_CIMA_PISOS_ELEVADOS
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= VELOCIDADE
            self.andando_f = False
            self.andando_t = True
            self.ultima_direcao = 'tras'
        else:
            self.andando_t = False
        if keys[pygame.K_RIGHT]:
            self.x += VELOCIDADE
            self.andando_f = True
            self.andando_t = False
            self.ultima_direcao = 'frente'
        else:
            self.andando_f = False

        if keys[pygame.K_SPACE] and not self.atacando:
            self.ataque()


    def movimentacao(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:  # anda pra frente
            self.x += VELOCIDADE
            self.andando_f = True
            self.andando_t = False
            self.ultima_direcao = 'frente'
        else:
            self.andando_f = False

        if keys[pygame.K_LEFT]:
            self.x -= VELOCIDADE  # anda pra tras
            self.andando_t = True
            self.andando_f = False
            self.ultima_direcao = 'tras'
        else:
            self.andando_t = False

        if keys[pygame.K_UP] and not self.pulando:  # pulo
            global ACELERACAO
            #self.pulando = True
           # self.velocidade_pulo = - ALTURA_DO_PULO
            ACELERACAO -=30
        if keys[pygame.K_DOWN]:
            self.y += VELOCIDADE

        if keys[pygame.K_SPACE] and not self.atacando:
            self.ataque()

    def update_ataque(self):
        if self.atacando:
            self.continuar_ataque()
            return True
        elif not self.atacando:
            self.posicao_ataquey = self.y
            self.ataque1_rec.y = self.posicao_ataquey
            return False

    def ataque(self):
        self.atacando = True
        self.direcao_ataque = self.ultima_direcao

    def continuar_ataque(self):
        if self.direcao_ataque == 'frente':
            self.posicao_ataquex += VELOCIDADE_ATAQUE
            self.ataque1_rec.x = self.posicao_ataquex
            if self.posicao_ataquex > 1000:
                self.reseta_ataque()
                self.atacando = False
        elif self.direcao_ataque == 'tras':
            self.posicao_ataquex -= VELOCIDADE_ATAQUE
            self.ataque1_rec.x = self.posicao_ataquex
            if self.posicao_ataquex < -500:

                self.reseta_ataque()
                self.atacando = False

    def reseta_ataque(self):
        self.atacando = False
        self.posicao_ataquex = 180
        self.posicao_ataquey = 420
        self.ataque1_rec.x = 180
        self.ataque1_rec.y = 420
  



class Lutador:
    def __init__(self, x, y, sprite_colisor_guerreiro, vida):
        self.x = x
        self.y = y
        self.sprite_colisor_guerreiro = sprite_colisor_guerreiro
        self.velocidade = None
        self.vida = vida
        self.sprite_anda_f = None
        self.sprite_anda_t = None
        self.sprite_ataque_f = None
        self.sprite_ataque_t = None
        self.atacar = None
        self.direcao = 'tras'
        self.rec = None  # Inicializamos o retângulo como None
        self.rec_ataque_f = None
        self.rec_ataque_t = None
        self.bloco_vida = None
        self.borda_vida = None
        self.sofre_dano_sprite = None

    def carrega_sprites(self):
        global SIZE_LUTADOR
        self.sprite_colisor_guerreiro = pygame.transform.scale(pygame.image.load(
            f'guerreiro_1/g_andando (1).png').convert_alpha(), (120, 100))
        self.sprite_anda_f = [pygame.transform.scale(pygame.image.load(
            f'g_correndo_t/guerreiro ({i+1}).png').convert_alpha(), SIZE_LUTADOR) for i in range(9)]
        self.sprite_anda_t = [pygame.transform.scale(pygame.image.load(
            f'g_correndo_f/guerreiro ({i+1}).png').convert_alpha(), SIZE_LUTADOR) for i in range(9)]
        self.sprite_ataque_f = [pygame.transform.scale(pygame.image.load(
            f'ataque_g_f/1 ({i+1}).png').convert_alpha(), SIZE_LUTADOR) for i in range(12)]
        self.sprite_ataque_t = [pygame.transform.scale(pygame.image.load(
            f'ataque_g_t/1 ({i+1}).png').convert_alpha(), SIZE_LUTADOR) for i in range(12)]
        self.borda_vida = pygame.transform.scale(pygame.image.load(
            f'barra de vida inimigo/barra_de_vida_inimigo.jpg').convert_alpha(), (60, 20))
        self.bloco_vida = pygame.transform.scale(pygame.image.load(
            f'barra de vida inimigo/bloco vida (1).png').convert_alpha(), (17, 18))
        self.sofre_dano_sprite = [pygame.transform.scale(pygame.image.load(
            f'lutador sofre dano/sofredano{i+1}.png').convert_alpha(), SIZE_LUTADOR)for i in range(2)]

    def criar_retangulo(self):
        self.rec = self.sprite_colisor_guerreiro.get_rect()
        self.rec_ataque_f = self.sprite_ataque_f[9].get_rect()
        self.rec_ataque_t = self.sprite_ataque_t[9].get_rect()

    def carregar_posicao(self, x, y):
        self.rec.x = x
        self.rec.y = y

        self.rec_ataque_f.x = x
        self.rec_ataque_f.y = y

        self.rec_ataque_t.x = x
        self.rec_ataque_t.y = y

    def movimento(self):

        global VELOCIDADE_LUTADOR
        if self.direcao == 'tras' and not self.atacar:
            self.x -= VELOCIDADE_LUTADOR
        elif self.direcao == 'frente' and not self.atacar:
            self.x += VELOCIDADE_LUTADOR
        elif self.atacar:
            pass
        return self.x


class Interface:
    def __init__(self):
        self.gameover = None
        self.fundo = None
        self.comecar = None
        self.sair = None
        self.voltarjogo = None
        self.comecar_rec = None
        self.recomecar = None

        self.recomecar_rec = None

        self.sair_rec = None

    def carrega_sprites(self):
        global LARGURA, ALTURA, FONTE
        self.gameover = pygame.transform.scale(pygame.image.load(
            f'tela GUI/tela de game over.png').convert_alpha(), (LARGURA, ALTURA))
        self.comecar = pygame.transform.scale(pygame.image.load(
            f'tela GUI/comecar.png').convert_alpha(), FONTE)
        self.recomecar = pygame.transform.scale(pygame.image.load(
            f'tela GUI/recomecar.png').convert_alpha(), FONTE)
        self.sair = pygame.transform.scale(pygame.image.load(
            f'tela GUI/SAIR.png').convert_alpha(), FONTE)

    def retangulo(self):
        self.comecar_rec = self.comecar.get_rect()
        self.recomecar_rec = self.recomecar.get_rect()
        self.sair_rec = self.sair.get_rect()

    def lugar(self):
        global POS_SAIR, POS_COMECAR, POS_RECOMECAR
        self.comecar_rec.x = POS_COMECAR[0]
        self.comecar_rec.y = POS_COMECAR[1]
        self.recomecar_rec.x = POS_RECOMECAR[0]
        self.recomecar_rec.y = POS_RECOMECAR[1]
        self.sair_rec.x = POS_SAIR[0]
        self.sair_rec.y = POS_SAIR[1]


class inimigo2:
    def __init__(self, x, y, sprite_colisor, vida):
        self.x = x
        self.y = y
        self.sprite_colisor = sprite_colisor
        self.velocidade = None
        self.vida = vida
        self.sprite_anda_f = None
        self.sprite_anda_t = None
        self.sprite_ataque_f = None
        self.sprite_ataque_t = None
        self.atacar = None
        self.direcao = 'tras'
        self.rec = None  # Inicializamos o retângulo como None
        self.rec_ataque_f = None
        self.rec_ataque_t = None

        self.sofre_dano_sprite = None

    def carrega_sprites(self):
        self.sprite_colisor = pygame.transform.scale(pygame.image.load(
            f'guerreiro_1/g_andando (1).png').convert_alpha(), (120, 100))
        self.sprite_anda_t = [pygame.transform.scale(pygame.image.load(
            f'correndo inimigo 2/corre ({i+1}).png').convert_alpha(), (100, 100)) for i in range(4)]
        self.sprite_anda_f = [pygame.transform.scale(pygame.image.load(
            f'correndo inimigo 2 f/corre ({i+1}).png').convert_alpha(), (100, 100)) for i in range(4)]
        self.sprite_ataque_t = [pygame.transform.scale(pygame.image.load(
            f'ataque inimigo 2 f/ataque ({i+1}).png').convert_alpha(), (100, 100)) for i in range(8)]
        self.sprite_ataque_f = [pygame.transform.scale(pygame.image.load(
            f'ataque inimigo 2/ataque ({i+1}).png').convert_alpha(), (100, 100)) for i in range(8)]

    def retangulo(self):
        self.rec = self.sprite_colisor.get_rect()
        self.rec_ataque_f = self.sprite_ataque_f
        self.rec_ataque_t = self.sprite_anda_t

    def carrega_posicao(self, x, y):
        self.rec.x = x
        self.rec.y = y
        self.rec_ataque_f.x = x
        self.rec_ataque_f.y = y

        self.rec_ataque_t.x = x
        self.rec_ataque_t.y = y

    def movimento(self):

        global VELOCIDADE_LUTADOR, POSICAO_INICIAL_X_INIMIGO2, ATACAR_MAGO
        if self.direcao == 'tras' and not self.atacar:
            self.x -= VELOCIDADE_LUTADOR
        elif self.direcao == 'frente' and not self.atacar:
            self.x += VELOCIDADE_LUTADOR
        elif self.atacar:
            pass
        return self.x


