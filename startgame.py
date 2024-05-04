import pygame
from variaveis_global import *
from classes import *
import pytmx

from pytmx.util_pygame import load_pygame
bloco_chao = 0
pygame.init()
screen = pygame.display.set_mode((LARGURA, ALTURA))

mago = Mago(100, 544, [], 100)
mago.carrega_sprites()
mago.criar_retangulo()


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

# ----------------------- FUNÇÕES DE COLISÃO COM O MAPA ------------------------- #


def checa_colisao_personagem_piso_elevado(surface, tm, offset_x, scale=0.5):
    global bloco_chao
    for rect in tm.colisor_pisos_elevados:
        scaled_rect = pygame.Rect(
            (rect.x * scale - offset_x), rect.y * scale, rect.width * scale, rect.height * scale)
        
        personagem_bottom = mago.rec.bottom
        bloco_top = scaled_rect.top
        bloco_bottom = scaled_rect.bottom
        personagem_top = mago.rec.top

        if mago.rec.colliderect(scaled_rect):
            if mago.pulando and mago.velocidade_pulo < 0 and personagem_top < bloco_bottom: # bate no blocos abaixo
               
                mago.rec.bottom = bloco_chao
                mago.y = mago.rec.y
                mago.pulando = False
                mago.velocidade_pulo = 0
                return True
                # NESTA FUNCAO ADICIONAR NO TILEMAP UM BLOCO PARA COLISAO ABAIXO DO BLOCO

            elif not mago.pulando or mago.velocidade_pulo > 0 and personagem_bottom > bloco_top: #sobe em cima
                mago.rec.bottom = bloco_top 
                mago.y = mago.rec.y
                mago.pulando = False
                mago.velocidade_pulo = 0
                return True
            
                
    return False



def colisao_piso_elevado_inicio(surface, tm, offset_x, scale=0.5):
    global bloco_chao
    for rect in tm.piso_inicio_elevado:
            bloco_e_inicio = pygame.Rect((rect.x * scale - offset_x), rect.y * scale, rect.width * scale, rect.height * scale)
            pygame.draw.rect(surface, (255, 0, 0), bloco_e_inicio, 4)
            if mago.ataque1_rec.colliderect(bloco_e_inicio):
                mago.reseta_ataque()
            if mago.rec.colliderect(bloco_e_inicio):
                if bloco_e_inicio.left > 210:
                    print(bloco_e_inicio.left)
                    mago.rec.bottom = bloco_chao
                    mago.y = mago.rec.y

def colisao_piso_elevado_fim(surface, tm, offset_x, scale=0.5):
    global bloco_chao
    for rect in tm.piso_final_elevado:
        scaled_rect = pygame.Rect(
            (rect.x * scale - offset_x), rect.y * scale, rect.width * scale, rect.height * scale)
        pygame.draw.rect(surface, (255,0,0), mago.ataque1_rec, 3)
        if mago.ataque1_rec.colliderect(scaled_rect):
           mago.reseta_ataque()
        if mago.rec.colliderect(scaled_rect):
            if scaled_rect.x < 145:
                
                mago.rec.bottom = bloco_chao+50 # ajusta um bloco para jogar o personagem mais para baixo
                mago.y = mago.rec.y



def checa_colisao_personagens_piso(surface, tm, offset_x, scale=0.5):
    global bloco_chao
    colidiu = False
    for rect in tm.colisor_pisos_chao:
        scaled_rect = pygame.Rect(
            (rect.x * scale - offset_x), rect.y * scale, rect.width * scale, rect.height * scale)
        
        if mago.rec.colliderect(scaled_rect):
            mago.rec.bottom = scaled_rect.top
            bloco_chao = scaled_rect.top
            mago.y = mago.rec.y
            
            colidiu = True

    return colidiu

  # -------------------------------------------- FUNÇÕES DO MAGO ----------------------------------------- #


def anima_mago(sprites_mago):
    index_m = (FRAME//6) % len(sprites_mago)
    return index_m

def anima_ataque_mago(sprite_ataque):
    index = (FRAME//5) % len(sprite_ataque)
    return index

def limita_posicao_personagem(x, y, tm, window_width, window_height):
    # Calcula a largura máxima do mapa ajustada pela escala
    max_x = tm.width * tm.tilewidth * 0.5 - 100
    # Calcula a altura máxima do mapa ajustada pela escala
    max_y = tm.height * tm.tileheight * 0.5 - 100
    x = max(0, min(x, max_x))
    y = max(0, min(y, max_y))
    return x, y

  # -------------------------------------------- fim: FUNÇÕES DO MAGO ----------------------------------------- #


def main():
    tm = carrega_mapa('teste3.tmx')
    clock = pygame.time.Clock()

    global FRAME, bloco_chao
    while RODANDO:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        mago.movimentacao()
        screen.fill((0, 0, 0))
        desenha_mapa(screen, tm, mago.x - 100)
        # --------------------- FUNÇÕES DO MAGO ------------------------- #
        if checa_colisao_personagens_piso(screen, tm, mago.x - 100):
            pass
        if checa_colisao_personagem_piso_elevado(screen, tm, mago.x - 100):
            pass
        if colisao_piso_elevado_inicio(screen, tm, mago.x - 100):
            pass
        if colisao_piso_elevado_fim(screen, tm, mago.x - 100):
            pass
  
        mago.gravidade(bloco_chao)
        
        


        POSICAO_X, POSICAO_Y = limita_posicao_personagem(mago.x, mago.y, tm, screen.get_width(), screen.get_height())
        mago.x = POSICAO_X
        mago.y = POSICAO_Y
        
        
        mago.carregar_posicao(mago.x, mago.y)
        if mago.update_ataque():
            index_ataque1 = anima_ataque_mago(mago.ataque1)
            screen.blit(mago.ataque1[index_ataque1], (mago.posicao_ataquex, mago.posicao_ataquey ))
        if mago.andando_f:
            INDEX_MAGO = anima_mago(mago.andando_frente)
            screen.blit(mago.andando_frente[INDEX_MAGO], (150, mago.y))
        elif mago.andando_t:
            INDEX_MAGO = anima_mago(mago.andando_frente)
            screen.blit(mago.sprites[INDEX_MAGO], (150, mago.y))
        else:
            INDEX_MAGO = anima_mago(mago.andando_frente)
            screen.blit(mago.sprites[INDEX_MAGO], (150, mago.y))

        pygame.draw.rect(screen, (255, 0, 0), mago.rec, 2)
        # --------------------- FIM: FUNÇÕES DO MAGO ------------------------- #

        FRAME += 1
        pygame.display.flip()  # Atualizar a tela depois de todos os desenhos
        clock.tick(60)


if __name__ == "__main__":
    main()

# TASK'S
# trocar sprites para andar para tras
# fazer o ataque colider com parede
# trocar spretes para pular
# fazer funcao para os inimigos
#