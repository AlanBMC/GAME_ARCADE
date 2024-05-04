import pygame
from variaveis_global import *
class Mago:
    def __init__(self, x, y, sprites, vida):
        self.x = 150
        self.y = y
        self.posicao_ataquex = 180
        self.posicao_ataquey = 420
        self.sprites = sprites
        self.andando_frente = None
        self.velocidade_pulo = ALTURA_DO_PULO
        self.pulando = False
        self.vida = vida
        self.ataque1 = None
        self.atacando = False
        self.andando_f = False
        self.andando_t = False
        self.rec = None  # Inicializamos o retângulo como None

    def carrega_sprites(self):
        self.sprites = [pygame.transform.scale(pygame.image.load(f'parado1/parado ({i+1}).png').convert_alpha(), (100, 100)) for i in range(17)]
        self.ataque1 = [pygame.transform.scale(pygame.image.load(f'ataque1_mago/15 ({i+1}).png').convert_alpha(),(140,140)) for i in range(15)]
        self.andando_frente = [pygame.transform.scale(pygame.image.load(f'anda_f/frente ({i+1}).png').convert_alpha(), (120, 120)) for i in range(8)]

    def criar_retangulo(self):
        # Criamos o retângulo a partir do primeiro sprite
        self.rec = self.sprites[0].get_rect()
        self.ataque1_rec = self.ataque1[0].get_rect()
        self.andando_f_rec = self.andando_frente[0].get_rect()

    def carregar_posicao(self,x,y):
        self.rec.x = 150
        self.rec.y = y
        self.ataque1_rec.x = self.posicao_ataquex
        self.ataque1_rec.y = self.posicao_ataquey
        self.andando_f_rec.x = 150
        self.andando_f_rec.y = y


    def movimentacao(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:# anda pra frente
            self.x += VELOCIDADE
            self.andando_f = True
            self.andando_t = False
        else:
            self.andando_f = False

        if keys[pygame.K_LEFT]:
            self.x -= VELOCIDADE #anda pra tras
            self.andando_t = True
            self.andando_f = False
        else:
            self.andando_t= False

        if keys[pygame.K_UP] and not self.pulando: #pulo
            self.pulando = True
            self.velocidade_pulo = - ALTURA_DO_PULO
            
            
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

    def continuar_ataque(self):
        self.posicao_ataquex += VELOCIDADE_ATAQUE
        self.ataque1_rec.x = self.posicao_ataquex
        if self.posicao_ataquex > 1000:
            self.reseta_ataque()
            self.atacando = False
       
    def reseta_ataque(self):
        self.atacando = False
        self.posicao_ataquex = 180
        self.posicao_ataquey = 420
        self.ataque1_rec.x = 180
        self.ataque1_rec.y = 420


    def gravidade(self, bloco_chao):
     
        if self.pulando:
            self.y += self.velocidade_pulo
            
            self.velocidade_pulo += GRAVIDADE  
            if self.y > (bloco_chao-100):
                self.y = (bloco_chao-100)
                
                
                self.pulando = False
                self.velocidade_pulo =0
            
        
                
class lutador:
    def __init__(self, x, y, sprites, velocidade, vida):
        self.x = x
        self.y = y
        self.sprites = sprites
        self.velocidade = velocidade
        self.vida = vida
        self.rec = None  # Inicializamos o retângulo como None

    def carrega_sprites(self):
        self.sprites = [pygame.transform.scale(pygame.image.load(f'g_correndo_t/g_andando ({i+1}).png').convert_alpha(), (150,150)) for i in range(6)]

    def criar_retangulo(self):
        # Criamos o retângulo a partir do primeiro sprite
        self.rec = self.sprites[0].get_rect()

    def carregar_posicao(self, x, y):
        self.rec.x = x
        self.rec.y = y
