import pygame
from variaveis_global import *
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

    def carrega_sprites(self):
        self.colisor = pygame.transform.scale(pygame.image.load('sprite_colisor_mago/1.png').convert_alpha(),(100,100))
        self.sprite_parado_frente = [pygame.transform.scale(pygame.image.load(f'parado_f/parado ({i+1}).png').convert_alpha(), (100, 100)) for i in range(17)]
        self.sprite_parado_tras = [pygame.transform.scale(pygame.image.load(f'mago_parado_t/{i+1}.png').convert_alpha(), (100, 100)) for i in range(8)]
        self.sprite_andando_frente = [pygame.transform.scale(pygame.image.load(f'anda_mago_f/frente ({i+1}).png').convert_alpha(), (100, 100)) for i in range(8)]
        self.sprite_anda_tras = [pygame.transform.scale(pygame.image.load(f'anda_mago_t/frente ({i+1}).png').convert_alpha(), (100, 100)) for i in range(8)]
        
        self.ataque1 = [pygame.transform.scale(pygame.image.load(f'ataque1_mago/15 ({i+1}).png').convert_alpha(),(140,140)) for i in range(15)]

    def criar_retangulo(self):
        # Criamos o retângulo a partir do primeiro sprite
        self.rec = self.colisor.get_rect()
        self.ataque1_rec = self.ataque1[0].get_rect()
        

    def carregar_posicao(self,x,y):
        self.rec.x = 250
        self.rec.y = y
        self.ataque1_rec.x = self.posicao_ataquex
        self.ataque1_rec.y = self.posicao_ataquey
        


    def movimentacao(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:# anda pra frente
            self.x += VELOCIDADE
            self.andando_f = True
            self.andando_t = False
            self.ultima_direcao = 'frente'
        else:
            self.andando_f = False

        if keys[pygame.K_LEFT]:
            self.x -= VELOCIDADE #anda pra tras
            self.andando_t = True
            self.andando_f = False
            self.ultima_direcao = 'tras'
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


    def gravidade(self, bloco_chao):
        if self.pulando and EM_CIMA_DO_BLOCO:
            self.y += self.velocidade_pulo
            print(BLOCO2)
            self.velocidade_pulo += GRAVIDADE
            if self.y > (BLOCO2-100):
                print('entrou porra')
        if self.pulando:
            self.y += self.velocidade_pulo
            self.velocidade_pulo += GRAVIDADE
          
            if self.y > (bloco_chao-100):
                self.y = (bloco_chao-100)
                
                
                self.pulando = False
                self.velocidade_pulo =0
            
        
                
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
    def carrega_sprites(self):
        global SIZE_LUTADOR
        self.sprite_colisor_guerreiro = pygame.transform.scale(pygame.image.load(f'guerreiro_1/g_andando (1).png').convert_alpha(), (120,100)) 
        self.sprite_anda_f = [pygame.transform.scale(pygame.image.load(f'g_correndo_t/guerreiro ({i+1}).png').convert_alpha(), SIZE_LUTADOR) for i in range(9)]
        self.sprite_anda_t = [pygame.transform.scale(pygame.image.load(f'g_correndo_f/guerreiro ({i+1}).png').convert_alpha(), SIZE_LUTADOR) for i in range(9)]
        self.sprite_ataque_f = [pygame.transform.scale(pygame.image.load(f'ataque_g_f/1 ({i+1}).png').convert_alpha(), SIZE_LUTADOR) for i in range(12)]
        self.sprite_ataque_t = [pygame.transform.scale(pygame.image.load(f'ataque_g_t/1 ({i+1}).png').convert_alpha(), SIZE_LUTADOR) for i in range(12)]

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