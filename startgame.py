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

lutador = Lutador(POSICAO_LUTADOR_X, POSICAO_LUTADOR_Y, [], 100)
lutador.carrega_sprites()
lutador.criar_retangulo()


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


# ----------------------------------- FUNÇÕES DE COLISÃO COM O MAPA ------------------------------------- #



def checa_colisao_personagem_piso_elevado(surface, tm, offset_x, scale=0.5):
    global bloco_chao, EM_CIMA_DO_BLOCO
    for rect in tm.colisor_pisos_elevados:
        scaled_rect = pygame.Rect(
            (rect.x * scale - offset_x), rect.y * scale, rect.width * scale, rect.height * scale)
        
        personagem_bottom = mago.rec.bottom
        bloco_top = scaled_rect.top
        bloco_bottom = scaled_rect.bottom
        personagem_top = mago.rec.top

        if mago.rec.colliderect(scaled_rect):
            if mago.pulando and mago.velocidade_pulo < 0 and personagem_top < bloco_bottom and not EM_CIMA_DO_BLOCO: # bate no blocos abaixo
     
                mago.velocidade_pulo = 0
                mago.pulando = False
                mago.rec.bottom = bloco_chao
                mago.y = mago.rec.y
                EM_CIMA_DO_BLOCO = False
                return True
                # NESTA FUNCAO ADICIONAR NO TILEMAP UM BLOCO PARA COLISAO ABAIXO DO BLOCO

            elif not mago.pulando or mago.velocidade_pulo > 0 and personagem_bottom > bloco_top: #sobe em cima
          
                mago.rec.bottom = bloco_top + 1
                BLOCO2 = bloco_top
                EM_CIMA_DO_BLOCO = True
                mago.y = mago.rec.y
                mago.pulando = False
                mago.velocidade_pulo = 0
                return True
            
                
    return False



def colisao_piso_elevado_inicio(surface, tm, offset_x, scale=0.5):
    global bloco_chao
    for rect in tm.piso_inicio_elevado:
            bloco_e_inicio = pygame.Rect((rect.x * scale - offset_x), rect.y * scale, rect.width * scale, rect.height * scale)
            
            if mago.ataque1_rec.colliderect(bloco_e_inicio):
                mago.reseta_ataque()
            elif mago.rec.colliderect(bloco_e_inicio):
                if bloco_e_inicio.left > 210:
                    
                    mago.rec.bottom = bloco_chao
                    mago.y = mago.rec.y


def colisao_piso_elevado_fim(surface, tm, offset_x, scale=0.5):
    global bloco_chao
    colidiu = False
    for rect in tm.piso_final_elevado:
        scaled_rect = pygame.Rect(
            (rect.x * scale - offset_x), rect.y * scale, rect.width * scale, rect.height * scale)
     
        if mago.ataque1_rec.colliderect(scaled_rect):
                mago.reseta_ataque()
        if mago.rec.colliderect(scaled_rect):
            if scaled_rect.x < 245:
                
                mago.rec.bottom = bloco_chao+50
                mago.y = mago.rec.y
                colidiu = True
    return colidiu    

def checa_colisao_personagens_piso(surface, tm, offset_x, scale=0.5):
    global bloco_chao
    colidiu = False
    for rect in tm.colisor_pisos_chao:
        scaled_rect = pygame.Rect(
            (rect.x * scale - offset_x), rect.y * scale, rect.width * scale, rect.height * scale)
        if lutador.rec.colliderect(scaled_rect):
            lutador.rec.bottom = scaled_rect.top
            lutador.y = lutador.rec.y
            colidiu = True
        if mago.rec.colliderect(scaled_rect):
           
            mago.rec.bottom = scaled_rect.top
            bloco_chao = scaled_rect.top
            mago.y = mago.rec.y
            
            colidiu = True

    return colidiu

# ----------------------------------- fim FUNÇÕES DE COLISÃO COM O MAPA ------------------------------------- #


# ----------------------------------- FUNCOES LUTADOR ------------------------------------- #

def colisao_com_personagem(surface):
    pygame.draw.rect(surface, (255,0,0), lutador.rec_ataque_f, 2)
    pygame.draw.rect(surface, (255,0,0), mago.rec, 2)
    if lutador.rec.colliderect(mago.rec):
        lutador.atacar = True
    if mago.ataque1_rec.colliderect(lutador.rec):
        mago.reseta_ataque()

    if lutador.rec_ataque_t.colliderect(mago.rec):
        pass

    if lutador.rec_ataque_f.colliderect(mago.rec):
        pass
    #resetar ataque, tirar mana do mago, tirar vida do guerreiro, (funcao para ele defender?)

def anima_lutador(sprite):
    index = (FRAME//10) % len(sprite)
    return index
def anima_lutador_ataque(sprite):
    index = (FRAME//3) % len(sprite)
    return index
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

    global FRAME, bloco_chao, POSICAO_LUTADOR_X, POSICAO_LUTADOR_Y
    while RODANDO:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        mago.movimentacao()
        screen.fill((0, 0, 0))
        desenha_mapa(screen, tm, mago.x - 100)
        mago.gravidade(bloco_chao)
        # --------------------- CHAMA FUNCOES DE COLISAO ------------------------- #
        if checa_colisao_personagens_piso(screen, tm, mago.x - 100):
            pass
        if checa_colisao_personagem_piso_elevado(screen, tm, mago.x - 100):
            pass

        colisao_piso_elevado_inicio(screen, tm, mago.x - 100)
        if colisao_piso_elevado_fim(screen, tm, mago.x - 100):
            pass

        colisao_com_personagem(screen)

        # --------------------- FIM CHAMA FUNCOES DE COLISAO ------------------------- #

        # --------------------- FIM CHAMA FUNCOES DE COLISAO ------------------------- #

        
        
        


        POSICAO_X, POSICAO_Y = limita_posicao_personagem(mago.x, mago.y, tm, screen.get_width(), screen.get_height())
        mago.x = POSICAO_X
        mago.y = POSICAO_Y
        mago.carregar_posicao(mago.x, mago.y)

        POSICAO_LUTADOR_X = lutador.movimento()
        lutador.y = POSICAO_LUTADOR_Y
        lutador.x = POSICAO_LUTADOR_X
        lutador.carregar_posicao(lutador.x-(mago.x-100), lutador.y)
        # ------------------------------- CARREGANGO SPRITES MAGO ------------------------------- #
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
       
        

        

        # --------------------- FIM: FUNÇÕES DO MAGO ------------------------- #


        # ----------------- CARREGA IMAGENS LUTADOR ------------ #
     
        
        if (lutador.x-(mago.x-100)) > 250 and not lutador.atacar:
            lutador.direcao = 'tras'
            index_lutador = anima_lutador(lutador.sprite_anda_f)
            screen.blit(lutador.sprite_anda_f[index_lutador], (lutador.x-(mago.x-70), lutador.y))
        elif (lutador.x-(mago.x-100)) < 250 and not lutador.atacar:
            lutador.direcao = 'frente'
            index_lutador = anima_lutador(lutador.sprite_anda_f)
            screen.blit(lutador.sprite_anda_t[index_lutador], (lutador.x-(mago.x-70), lutador.y))
        if lutador.atacar:
            index_lutador = anima_lutador_ataque(lutador.sprite_ataque_f)
            if lutador.direcao == 'frente':
                screen.blit(lutador.sprite_ataque_f[index_lutador], (lutador.x-(mago.x-115), lutador.y-5))
            elif lutador.direcao == 'tras':
                screen.blit(lutador.sprite_ataque_t[index_lutador], (lutador.x-(mago.x-55), lutador.y-5))
            lutador.atacar = False
            
        
            
        
        
       
        
        # ---------------------- FIM LUTADOR ---------------------------#
        FRAME += 1
        pygame.display.flip()  # Atualizar a tela depois de todos os desenhos
        clock.tick(60)


if __name__ == "__main__":
    main()

# TASK'S
# trocar sprites para andar para tras

# fazer funcao para os inimigos
#