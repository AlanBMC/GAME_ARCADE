import pygame
import pytmx
import time
from carrega_sprites.desenha_na_tela import *
from variaveis_gravidade_pulo import *
from pygame.locals import *
from pytmx.util_pygame import load_pygame
from classes import *
from variaveis_global import *
from fase2 import *
pygame.init()
screen = pygame.display.set_mode((1200, 600))
mago = Mago(POSICAO_INICIAL_X, POSICAO_INICIAL_Y, [], 100)
mago.carrega_sprites()
mago.criar_retangulo()

lutador = Lutador(POSICAO_LUTADOR_X, POSICAO_LUTADOR_Y, [], 100)
lutador.carrega_sprites()
lutador.criar_retangulo()

inimigo = inimigo2(POS_INIMIGOX, POS_INIMIGOY, [], 100)
inimigo.carrega_sprites()
inimigo.retangulo()

interface = Interface()
interface.carrega_sprites()


def reseta_jogo():
    global POSICAO_INICIAL_X, POSICAO_INICIAL_Y, POSICAO_LUTADOR_X_INICIAL, POSICAO_LUTADOR_Y_INICIAL, ESTADO_JOGO, POS_INIMIGOX, INIMIGO_VIVO, VIVO_INIMIGO
    mago.vida = 100
    lutador.vida = 100
    inimigo.vida = 100
    mago.x = POSICAO_INICIAL_X
    mago.y = POSICAO_INICIAL_Y
    lutador.x = POSICAO_LUTADOR_X_INICIAL
    lutador.y = POSICAO_LUTADOR_Y_INICIAL
    inimigo.x = POS_INIMIGOX
    inimigo.y = POS_INIMIGOX
    INIMIGO_VIVO =True
    VIVO_INIMIGO = True
    ESTADO_JOGO = 'jogando'
    
def desenha_mapa(surface, tm, offset_x, scale=0.5):
    tw = int(tm.tilewidth * scale)
    th = int(tm.tileheight * scale)
    for layer in tm.visible_layers:
        if layer.name != "colisor_piso":  # Ignore the collision layer for regular tile drawing
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = tm.get_tile_image_by_gid(gid)
                    if tile:
                        tile = pygame.transform.scale(tile, (tw, th))
                        surface.blit(tile, ((x * tw) - offset_x, y * th))



def carrega_mapa(filename):
    tm = load_pygame(filename)

    tm.colisor_pisos_chao = []
    collision_layer = tm.get_layer_by_name("colisor_chao")
    for x, y, gid in collision_layer:
        if gid:
            rect = pygame.Rect(x * tm.tilewidth, y *
                               tm.tileheight, tm.tilewidth, tm.tileheight)
            tm.colisor_pisos_chao.append(rect)

    tm.colisor_pisos_elevados = []
    collision_layer_elevado = tm.get_layer_by_name("colisor_elevado")
    for x, y, gid in collision_layer_elevado:
        if gid:
            rect3 = pygame.Rect(x * tm.tilewidth, y *
                                tm.tileheight, tm.tilewidth, tm.tileheight)
            tm.colisor_pisos_elevados.append(rect3)

    tm.piso_final_elevado = []
    colisor_piso_elevado_final = tm.get_layer_by_name("colisor_fim_elevado")
    for x, y, gid in colisor_piso_elevado_final:
        if gid:
            rect4 = pygame.Rect(x * tm.tilewidth, y *
                                tm.tileheight, tm.tilewidth, tm.tileheight)
            tm.piso_final_elevado.append(rect4)

    tm.piso_inicio_elevado = []
    colisor_piso_inicio_elevado = tm.get_layer_by_name(
        "colisor_inicio_elevado")
    for x, y, gid in colisor_piso_inicio_elevado:
        if gid:
            rect5 = pygame.Rect(x * tm.tilewidth, y *
                                tm.tileheight, tm.tilewidth, tm.tileheight)
            tm.piso_inicio_elevado.append(rect5)

    tm.portal = []
    portal = tm.get_layer_by_name('portal')
    for x, y, gid in portal:
        if gid:
            rect6 = pygame.Rect(x * tm.tilewidth, y *
                                tm.tileheight, tm.tilewidth, tm.tileheight)
            tm.portal.append(rect6)

    return tm



def colide_portal(tm, offset_x, scale=0.5):
    global  ACELERACAO_Y,PULANDO, EM_CIMA_PISOS_ELEVADOS, BLOCO_CHAO, PASSOU
    for rect in tm.portal:
        scaled_rect = pygame.Rect(
            (rect.x * scale - offset_x), rect.y * scale, rect.width * scale, rect.height * scale)
        if mago.rec.colliderect(scaled_rect):
            PASSOU = True
            

def colisao_pisos_elevados( tm, offset_x, scale=0.5):
    global  ACELERACAO_Y,PULANDO, EM_CIMA_PISOS_ELEVADOS, BLOCO_CHAO
    for rect in tm.colisor_pisos_elevados:
        scaled_rect = pygame.Rect(
            (rect.x * scale - offset_x), rect.y * scale, rect.width * scale, rect.height * scale)
        personagem_bottom = mago.rec.bottom
        bloco_top = scaled_rect.top
        
      
        if mago.rec.colliderect(scaled_rect):
                if personagem_bottom > bloco_top:
                    mago.rec.bottom = scaled_rect.top
                    mago.y = mago.rec.y
                    ACELERACAO_Y = 5
                    PULANDO = False
                    EM_CIMA_PISOS_ELEVADOS = True
           
def colisao_pisos_baixos(surface,tm, offset_x, scale=0.5):
    global  ACELERACAO_Y,PULANDO, EM_CIMA_PISOS_ELEVADOS, BLOCO_CHAO
    
    for rect in tm.piso_inicio_elevado:
        scaled_rect = pygame.Rect(
            (rect.x * scale - offset_x), rect.y * scale, rect.width * scale, rect.height * scale)
   
        if mago.rec.colliderect(scaled_rect):
           
            mago.rec.bottom= BLOCO_CHAO
            mago.y = mago.rec.y
            ACELERACAO_Y = 5
            PULANDO = False
            EM_CIMA_PISOS_ELEVADOS = False

def colisao(tm, offset_x, scale=0.5):
    global ACELERACAO_Y,PULANDO, EM_CIMA_PISOS_ELEVADOS, BLOCO_CHAO, ACELERACAO_Y_INIMIGO, ACELERACAO_Y_LUTADOR
    for rect in tm.colisor_pisos_chao:
        scaled_rect = pygame.Rect(
            (rect.x * scale - offset_x), rect.y * scale, rect.width * scale, rect.height * scale)
       
        if mago.rec.colliderect(scaled_rect):
            mago.rec.bottom = scaled_rect.top
            BLOCO_CHAO = scaled_rect.top
            mago.y = mago.rec.y
            ACELERACAO_Y = 8
            PULANDO = False
            EM_CIMA_PISOS_ELEVADOS = False

        if lutador.rec.colliderect(scaled_rect):
            lutador.rec.bottom = scaled_rect.top
            lutador.y = lutador.rec.y
            ACELERACAO_Y_LUTADOR = 8
            
        if inimigo.rec.colliderect(scaled_rect):
            inimigo.rec.bottom = scaled_rect.top
            inimigo.y = inimigo.rec.y
            ACELERACAO_Y_INIMIGO = 8
            

def limita_posicao_personagem(x, y, tm, window_width, window_height):
    # Calcula a largura máxima do mapa ajustada pela escala
    max_x = tm.width * tm.tilewidth * 0.5 - 100
    # Calcula a altura máxima do mapa ajustada pela escala
    max_y = tm.height * tm.tileheight * 0.5 - 100
    x = max(0, min(x, max_x))
    y = max(0, min(y, max_y))
    return x, y

def anima_mago(sprites_mago):
    
    index_m = (FRAME//6) % len(sprites_mago)
  
    return index_m

def gravidade(clock):
    global F,T,G,ACELERACAO_Y, ACELERACAO_Y_INIMIGO, ACELERACAO_Y_LUTADOR
    T = clock.get_time()/ 1000.0
    F = G*T
    if not PULANDO:
        ACELERACAO_Y += F
    else:
        ACELERACAO_Y = max(ACELERACAO_Y, -15)
    mago.y += ACELERACAO_Y
    ACELERACAO_Y_INIMIGO += F
    ACELERACAO_Y_LUTADOR += F
    lutador.y += ACELERACAO_Y_LUTADOR
    inimigo.y += ACELERACAO_Y_INIMIGO

def barra_vida_mago(screen):
            global ESTADO_JOGO
            screen.blit(mago.borda_geral,(10,10))
            if mago.vida == 100:
                screen.blit(mago.bloco_vida,(15,30))
                screen.blit(mago.bloco_vida,(33,30))
                screen.blit(mago.bloco_vida,(51,30))
                screen.blit(mago.bloco_vida,(69,30))
                screen.blit(mago.bloco_vida,(87,30))
                screen.blit(mago.bloco_vida,(105,30))
                screen.blit(mago.bloco_vida,(123,30))
                screen.blit(mago.bloco_vida,(141,30))
                screen.blit(mago.bloco_vida,(159,30))
                screen.blit(mago.bloco_vida,(177,30))
                screen.blit(mago.bloco_vida,(195,30))
                screen.blit(mago.bloco_vida,(213,30))
                screen.blit(mago.bloco_vida,(231,30))
            elif mago.vida ==90:
                screen.blit(mago.bloco_vida,(15,30))
                screen.blit(mago.bloco_vida,(33,30))
                screen.blit(mago.bloco_vida,(51,30))
                screen.blit(mago.bloco_vida,(69,30))
                screen.blit(mago.bloco_vida,(87,30))
                screen.blit(mago.bloco_vida,(105,30))
                screen.blit(mago.bloco_vida,(123,30))
                screen.blit(mago.bloco_vida,(141,30))
                screen.blit(mago.bloco_vida,(159,30))
                screen.blit(mago.bloco_vida,(177,30))
                screen.blit(mago.bloco_vida,(195,30))
                screen.blit(mago.bloco_vida,(213,30))
            elif mago.vida == 80:
                screen.blit(mago.bloco_vida,(15,30))
                screen.blit(mago.bloco_vida,(33,30))
                screen.blit(mago.bloco_vida,(51,30))
                screen.blit(mago.bloco_vida,(69,30))
                screen.blit(mago.bloco_vida,(87,30))
                screen.blit(mago.bloco_vida,(105,30))
                screen.blit(mago.bloco_vida,(123,30))
                screen.blit(mago.bloco_vida,(141,30))
                screen.blit(mago.bloco_vida,(159,30))
                screen.blit(mago.bloco_vida,(177,30))
                screen.blit(mago.bloco_vida,(195,30))
            elif mago.vida == 70:
                screen.blit(mago.bloco_vida,(15,30))
                screen.blit(mago.bloco_vida,(33,30))
                screen.blit(mago.bloco_vida,(51,30))
                screen.blit(mago.bloco_vida,(69,30))
                screen.blit(mago.bloco_vida,(87,30))
                screen.blit(mago.bloco_vida,(105,30))
                screen.blit(mago.bloco_vida,(123,30))
                screen.blit(mago.bloco_vida,(141,30))
                screen.blit(mago.bloco_vida,(159,30))
                screen.blit(mago.bloco_vida,(177,30))
            elif mago.vida == 60:
                screen.blit(mago.bloco_vida,(15,30))
                screen.blit(mago.bloco_vida,(33,30))
                screen.blit(mago.bloco_vida,(51,30))
                screen.blit(mago.bloco_vida,(69,30))
                screen.blit(mago.bloco_vida,(87,30))
                screen.blit(mago.bloco_vida,(105,30))
                screen.blit(mago.bloco_vida,(123,30))
                screen.blit(mago.bloco_vida,(141,30))
                screen.blit(mago.bloco_vida,(159,30))
            elif mago.vida == 50:
                screen.blit(mago.bloco_vida,(15,30))
                screen.blit(mago.bloco_vida,(33,30))
                screen.blit(mago.bloco_vida,(51,30))
                screen.blit(mago.bloco_vida,(69,30))
                screen.blit(mago.bloco_vida,(87,30))
                screen.blit(mago.bloco_vida,(105,30))
                screen.blit(mago.bloco_vida,(123,30))
                screen.blit(mago.bloco_vida,(141,30))
            elif mago.vida == 40:
                screen.blit(mago.bloco_vida,(15,30))
                screen.blit(mago.bloco_vida,(33,30))
                screen.blit(mago.bloco_vida,(51,30))
                screen.blit(mago.bloco_vida,(69,30))
                screen.blit(mago.bloco_vida,(87,30))
                screen.blit(mago.bloco_vida,(105,30))
                screen.blit(mago.bloco_vida,(123,30))
            elif mago.vida == 30:
                screen.blit(mago.bloco_vida,(15,30))
                screen.blit(mago.bloco_vida,(33,30))
                screen.blit(mago.bloco_vida,(51,30))
                screen.blit(mago.bloco_vida,(69,30))
                screen.blit(mago.bloco_vida,(87,30))
                screen.blit(mago.bloco_vida,(105,30))
            elif mago.vida == 20:
                screen.blit(mago.bloco_vida,(15,30))
                screen.blit(mago.bloco_vida,(33,30))
                screen.blit(mago.bloco_vida,(51,30))
                screen.blit(mago.bloco_vida,(69,30))
                screen.blit(mago.bloco_vida,(87,30))
            elif mago.vida == 10:
                screen.blit(mago.bloco_vida,(15,30))
                screen.blit(mago.bloco_vida,(33,30))
            elif mago.vida < 0:
                ESTADO_JOGO = 'GAMEOVER'

def barra_vida_lutador(screen):
    global VIVO_INIMIGO, TIPO_INIMIGO
    if VIVO_INIMIGO:
        
        screen.blit(lutador.borda_vida,(lutador.x-(mago.x-100), lutador.y+10))
        if lutador.vida == 100:
            screen.blit(lutador.bloco_vida,(lutador.x-(mago.x-90), lutador.y+11))
            screen.blit(lutador.bloco_vida,(lutador.x-(mago.x-107), lutador.y+11))
            screen.blit(lutador.bloco_vida,(lutador.x-(mago.x-124), lutador.y+11))
            screen.blit(lutador.bloco_vida,(lutador.x-(mago.x-141), lutador.y+11))
        elif lutador.vida == 70:
            screen.blit(lutador.bloco_vida,(lutador.x-(mago.x-90), lutador.y+11))
            screen.blit(lutador.bloco_vida,(lutador.x-(mago.x-107), lutador.y+11))
            screen.blit(lutador.bloco_vida,(lutador.x-(mago.x-124), lutador.y+11))
        elif lutador.vida == 40:
            screen.blit(lutador.bloco_vida,(lutador.x-(mago.x-90), lutador.y+11))
            screen.blit(lutador.bloco_vida,(lutador.x-(mago.x-107), lutador.y+11))
        elif lutador.vida == 10:
            screen.blit(lutador.bloco_vida,(lutador.x-(mago.x-90), lutador.y+11))
        elif lutador.vida < 0:
            VIVO_INIMIGO = False

def barra_de_vida_inimigo(screen):
    global INIMIGO_VIVO
    if INIMIGO_VIVO:
        
        screen.blit(inimigo.borda_vida,(inimigo.x-(mago.x-100), inimigo.y-15))
        if inimigo.vida == 100:
            screen.blit(inimigo.bloco_vida,(inimigo.x-(mago.x-90), inimigo.y-16))
            screen.blit(inimigo.bloco_vida,(inimigo.x-(mago.x-107), inimigo.y-16))
            screen.blit(inimigo.bloco_vida,(inimigo.x-(mago.x-124), inimigo.y-16))
            screen.blit(inimigo.bloco_vida,(inimigo.x-(mago.x-141), inimigo.y-16))
        elif inimigo.vida == 70:
            screen.blit(inimigo.bloco_vida,(inimigo.x-(mago.x-90), inimigo.y-16))
            screen.blit(inimigo.bloco_vida,(inimigo.x-(mago.x-107), inimigo.y-16))
            screen.blit(inimigo.bloco_vida,(inimigo.x-(mago.x-124), inimigo.y-16))
        elif inimigo.vida == 40:
            screen.blit(inimigo.bloco_vida,(inimigo.x-(mago.x-90), inimigo.y-16))
            screen.blit(inimigo.bloco_vida,(inimigo.x-(mago.x-107), inimigo.y-16))
        elif inimigo.vida == 10:
            screen.blit(inimigo.bloco_vida,(inimigo.x-(mago.x-90), inimigo.y-11))
        elif inimigo.vida < 0:
            INIMIGO_VIVO = False

def anima_lutador(sprite):
    index = (FRAME//10) % len(sprite)
    return index


def anima_lutador_ataque(sprite):
    index = (FRAME//3) % len(sprite)
    return index

def anima_ataque_mago(sprite_ataque):
    index = (FRAME//5) % len(sprite_ataque)
    return index

def combate(surface):
    global DANO, DANO_MAGICO_1, LUTADOR_SOFREU_DANO, VIVO_INIMIGO,INIMIGO_VIVO, SOFREU_DANO_INIMIGO,BLOCO_CHAO, PULANDO
    tempo_atual = time.time()
    pygame.draw.rect(surface, (255,0,0), lutador.rec, 2)
    pygame.draw.rect(surface, (255,0,0), inimigo.rec, 2)
    if mago.y >= BLOCO_CHAO:
        PULANDO =False
    if inimigo.rec.colliderect(mago.rec):
        inimigo.atacar = True
    if mago.ataque1_rec.colliderect(inimigo.rec):
        if INIMIGO_VIVO and mago.atacando:
            inimigo.vida -= DANO_MAGICO_1
            print(inimigo.vida)
            SOFREU_DANO_INIMIGO =  True
        mago.reseta_ataque()

    if lutador.rec.colliderect(mago.rec):
        lutador.atacar = True
    if mago.ataque1_rec.colliderect(lutador.rec):
        if VIVO_INIMIGO and mago.atacando:
            lutador.vida -= DANO_MAGICO_1
            LUTADOR_SOFREU_DANO =  True
        mago.reseta_ataque()
    if lutador.rec_ataque_t.colliderect(mago.rec) and lutador.atacar and (tempo_atual - mago.ultimo_dano) > mago.cooldown:
        if VIVO_INIMIGO:
            mago.vida -= DANO
            mago.ultimo_dano = tempo_atual
    if inimigo.rec_ataque_t.colliderect(mago.rec) and inimigo.atacar and (tempo_atual - mago.ultimo_dano) > mago.cooldown:
        if INIMIGO_VIVO:
            mago.vida -= DANO
            mago.ultimo_dano = tempo_atual

def main():
    global PASSOU,POS_INIMIGOY, POS_INIMIGOX, clock, G, F,T, ACELERACAO_Y, VELOCIDADE,PULANDO, ALTURA_MAX_PULO, FRAME, VIVO_INIMIGO, LUTADOR_SOFREU_DANO,POS_INIMIGOY, ESTADO_JOGO
    
    
    tm = carrega_mapa('teste3.tmx')
    
    tm2 = carrega_mapa_fase2('mapa_fase2.tmx')
    clock = pygame.time.Clock()
  
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        if ESTADO_JOGO == 'jogando':
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and not PULANDO:  
                ACELERACAO_Y = -15
                PULANDO = True

            if PULANDO and mago.y <= ALTURA_MAX_PULO and not EM_CIMA_PISOS_ELEVADOS:
                ACELERACAO_Y = 8
            if EM_CIMA_PISOS_ELEVADOS and mago.y <= 100:
                ACELERACAO_Y = 8
            
            mago.movimentacao()

            screen.fill((0, 0, 0))
           
            if PASSOU:
                desenha_mapa_fase2(screen, tm2, mago.x)
                colisao_fase2(tm2, mago.x, mago)
            
            else:
                desenha_mapa(screen, tm, mago.x )
                colide_portal(tm, mago.x)
            
            x = inimigo.movimento()
            inimigo.x = x
            inimigo.y = POS_INIMIGOY
            POSICAO_LUTADOR_X = lutador.movimento()
            lutador.y = POSICAO_LUTADOR_Y
            lutador.x = POSICAO_LUTADOR_X
            gravidade(clock)
            POSICAO_X, POSICAO_Y = limita_posicao_personagem(mago.x, mago.y, tm, screen.get_width(), screen.get_height())
            mago.x = POSICAO_X
            mago.y = POSICAO_Y
            mago.carregar_posicao( mago.x, mago.y)
            lutador.carregar_posicao(lutador.x-(mago.x-100), lutador.y+10)
            inimigo.carrega_posicao(inimigo.x-(mago.x-100), lutador.y)
            if not PASSOU:
                colisao(tm, mago.x)
                colisao_pisos_elevados(tm, mago.x)
                colisao_pisos_baixos(screen,tm, mago.x)
                combate(screen)
            
            carrega_imagens_mago(screen, mago, POSICAO_X_PERSONAGEM, FRAME)
            carrega_imagens_lutador(screen, mago, lutador, FRAME,VIVO_INIMIGO, LUTADOR_SOFREU_DANO)
            LUTADOR_SOFREU_DANO = False
            carrega_imagens_inimigo(screen, mago, inimigo, FRAME, INIMIGO_VIVO)

            barra_vida_lutador(screen)
            barra_vida_mago(screen)
            barra_de_vida_inimigo(screen)
            FRAME += 1
            

        elif ESTADO_JOGO == 'GAMEOVER':
            screen.blit(interface.gameover, (0,0))
            screen.blit(interface.recomecar, (POS_RECOMECAR[0],POS_RECOMECAR[1]))
            interface.retangulo()
            interface.lugar()
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if interface.recomecar_rec.collidepoint(pos):
                    reseta_jogo()

        elif ESTADO_JOGO == 'INICIAR':

            screen.blit(interface.comecar, (POS_COMECAR[0],POS_COMECAR[1]))
            screen.blit(interface.sair, (POS_SAIR[0], POS_SAIR[1]))
            interface.retangulo()
            interface.lugar()
            pygame.draw.rect(screen, (255, 0,0), interface.sair_rec, 2)
            pygame.draw.rect(screen, (255, 0,0), interface.comecar_rec, 2)
            
            
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if interface.comecar_rec.collidepoint(pos):
                    reseta_jogo()
                    
                if interface.sair_rec.collidepoint(event.pos):
                    pygame.quit()
                    return
        pygame.display.update()
        clock.tick(60)
if __name__ == "__main__":
    main()

