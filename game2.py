import pygame
import pytmx
import time
from variaveis_gravidade_pulo import *
from pygame.locals import *
from pytmx.util_pygame import load_pygame
from classes import *
from variaveis_global import *

pygame.init()
screen = pygame.display.set_mode((1200, 600))
mago = Mago(POSICAO_INICIAL_X, POSICAO_INICIAL_Y, [], 100)
mago.carrega_sprites()
mago.criar_retangulo()

lutador = Lutador(POSICAO_LUTADOR_X, POSICAO_LUTADOR_Y, [], 100)
lutador.carrega_sprites()
lutador.criar_retangulo()

interface = Interface()
interface.carrega_sprites()
bloco_chao = 444

def reseta_jogo():
    global POSICAO_INICIAL_X, POSICAO_INICIAL_Y, POSICAO_LUTADOR_X_INICIAL, POSICAO_LUTADOR_Y_INICIAL, ESTADO_JOGO
    mago.vida = 100
    lutador.vida = 100
    mago.x = POSICAO_INICIAL_X
    mago.y = POSICAO_INICIAL_Y
    lutador.x = POSICAO_LUTADOR_X_INICIAL
    lutador.y = POSICAO_LUTADOR_Y_INICIAL
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

    
    return tm

def colisao_pisos_elevados( tm, offset_x, scale=0.5):
    global  ACELERACAO_Y,PULANDO, EM_CIMA_PISOS_ELEVADOS, BLOCO_CHAO
    for rect in tm.colisor_pisos_elevados:
        scaled_rect = pygame.Rect(
            (rect.x * scale - offset_x), rect.y * scale, rect.width * scale, rect.height * scale)
        personagem_bottom = mago.rec.bottom
        bloco_top = scaled_rect.top
        bloco_bottom = scaled_rect.bottom
        personagem_top = mago.rec.top
      
        if mago.rec.colliderect(scaled_rect):
                if personagem_bottom > bloco_top:
                    mago.rec.bottom = scaled_rect.top
                    mago.y = mago.rec.y
                    ACELERACAO_Y = 5
                    PULANDO = False
                    EM_CIMA_PISOS_ELEVADOS = False
           
def colisao_pisos_baixos(surface,tm, offset_x, scale=0.5):
    global  ACELERACAO_Y,PULANDO, EM_CIMA_PISOS_ELEVADOS, BLOCO_CHAO
    for rect in tm.piso_inicio_elevado:
        scaled_rect = pygame.Rect(
            (rect.x * scale - offset_x), rect.y * scale, rect.width * scale, rect.height * scale)
        pygame.draw.rect(surface, (255,0,0), scaled_rect, 2)
        pygame.draw.rect(surface, (255,0,0), mago.rec, 2)
        if mago.rec.colliderect(scaled_rect):
           
            mago.rec.bottom= BLOCO_CHAO
            mago.y = mago.rec.y
            ACELERACAO_Y = 5
            PULANDO = False
            
def colisao(tm, offset_x, scale=0.5):
    global ACELERACAO_Y,PULANDO, EM_CIMA_PISOS_ELEVADOS, BLOCO_CHAO
    for rect in tm.colisor_pisos_chao:
        scaled_rect = pygame.Rect(
            (rect.x * scale - offset_x), rect.y * scale, rect.width * scale, rect.height * scale)
       
        if mago.rec.colliderect(scaled_rect):
            mago.rec.bottom = scaled_rect.top
            BLOCO_CHAO = scaled_rect.top
            mago.y = mago.rec.y
            ACELERACAO_Y = 5
            PULANDO = False
            EM_CIMA_PISOS_ELEVADOS = True
        if lutador.rec.colliderect(scaled_rect):
            lutador.rec.bottom = scaled_rect.top
            lutador.y = lutador.rec.y
            ACELERACAO_Y = 5



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
    global F,T,G,ACELERACAO_Y
    T = clock.get_time()/ 1000
    F = G*T
    ACELERACAO_Y += F 
    mago.y += ACELERACAO_Y 
    lutador.y += ACELERACAO_Y

def barra_vida_mago(screen):
            
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
    global DANO, DANO_MAGICO_1, LUTADOR_SOFREU_DANO, VIVO_INIMIGO
    tempo_atual = time.time()
    pygame.draw.rect(surface, (255,0,0), lutador.rec, 2)
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
   

def main():
    global clock, G, F,T, ACELERACAO_Y, VELOCIDADE,PULANDO, ALTURA_MAX_PULO, TARGET_FPS, FRAME, VIVO_INIMIGO, LUTADOR_SOFREU_DANO
    tm = carrega_mapa('teste3.tmx')
    clock = pygame.time.Clock()
  
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and not PULANDO:  
            ACELERACAO_Y = -15
            PULANDO = True
        if PULANDO and mago.y <= ALTURA_MAX_PULO and not EM_CIMA_PISOS_ELEVADOS:
            ACELERACAO_Y = 3
        if EM_CIMA_PISOS_ELEVADOS and mago.y <= 200:
            ACELERACAO_Y = 3

        mago.movimentacao2()

        screen.fill((0, 0, 0))
        desenha_mapa(screen, tm, mago.x )
       
        gravidade(clock)
        POSICAO_X, POSICAO_Y = limita_posicao_personagem(mago.x, mago.y, tm, screen.get_width(), screen.get_height())
        mago.x = POSICAO_X
        mago.y = POSICAO_Y
        POSICAO_LUTADOR_X = lutador.movimento()
        lutador.y = POSICAO_LUTADOR_Y
        lutador.x = POSICAO_LUTADOR_X

        lutador.carregar_posicao(lutador.x-(mago.x-100), lutador.y)

        mago.carregar_posicao( mago.x, mago.y)
        colisao(tm, mago.x)
        colisao_pisos_elevados(tm, mago.x)
        colisao_pisos_baixos(screen,tm, mago.x)
        combate(screen)
        if mago.update_ataque():
                index_ataque1 = anima_ataque_mago(mago.ataque1)
                screen.blit(mago.ataque1[index_ataque1], (mago.posicao_ataquex, mago.posicao_ataquey ))

        if mago.andando_f:
            mago.ultima_direcao = 'frente'
            
            INDEX_MAGO = anima_mago(mago.sprite_andando_frente)
            screen.blit(mago.sprite_andando_frente[INDEX_MAGO], (POSICAO_X_PERSONAGEM, mago.y))
    
        if mago.andando_t:
            mago.ultima_direcao = 'tras'
            INDEX_MAGO = anima_mago(mago.sprite_anda_tras)
            screen.blit(mago.sprite_anda_tras[INDEX_MAGO], (POSICAO_X_PERSONAGEM, mago.y))

        if not mago.andando_t and not mago.andando_f:
            if mago.ultima_direcao == 'frente':
                INDEX_MAGO = anima_mago(mago.sprite_parado_frente)
                screen.blit(mago.sprite_parado_frente[INDEX_MAGO], (POSICAO_X_PERSONAGEM, mago.y))
            elif mago.ultima_direcao == 'tras':
                INDEX_MAGO = anima_mago(mago.sprite_parado_tras)
                screen.blit(mago.sprite_parado_tras[INDEX_MAGO], (POSICAO_X_PERSONAGEM, mago.y))

        if VIVO_INIMIGO:
            if (lutador.x-(mago.x)) > 250 and not lutador.atacar:
                lutador.direcao = 'tras'
                index_lutador = anima_lutador(lutador.sprite_anda_f)
                screen.blit(lutador.sprite_anda_f[index_lutador], (lutador.x-(mago.x-50), lutador.y))
            elif (lutador.x-(mago.x)) < 250 and not lutador.atacar:
                lutador.direcao = 'frente'
                index_lutador = anima_lutador(lutador.sprite_anda_f)
                screen.blit(lutador.sprite_anda_t[index_lutador], (lutador.x-(mago.x-50), lutador.y))
            if lutador.atacar:
                index_lutador = anima_lutador_ataque(lutador.sprite_ataque_f)
                if lutador.direcao == 'frente':
                    screen.blit(lutador.sprite_ataque_f[index_lutador], (lutador.x-(mago.x-100), lutador.y-5))
                elif lutador.direcao == 'tras':
                    screen.blit(lutador.sprite_ataque_t[index_lutador], (lutador.x-(mago.x-100), lutador.y-5))
                lutador.atacar = False
                
            if LUTADOR_SOFREU_DANO:
                LUTADOR_SOFREU_DANO = False
                if lutador.direcao == 'tras':
                    screen.blit(lutador.sofre_dano_sprite[1], (lutador.x-(mago.x-150), lutador.y+10))
                elif lutador.direcao == 'frente':
                    screen.blit(lutador.sofre_dano_sprite[0], (lutador.x-(mago.x-100), lutador.y+10))

        barra_vida_lutador(screen)
        barra_vida_mago(screen)
        FRAME += 1
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()

