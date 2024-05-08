import pygame
import pytmx
from variaveis_global import *
from pytmx.util_pygame import load_pygame

def carrega_mapa_fase2(filename):
    tm = load_pygame(filename)
    tm.colisor_pisos_chao = []
    collision_layer = tm.get_layer_by_name("colisor_chao")
    for x, y, gid in collision_layer:
        if gid:
            rect = pygame.Rect(x * tm.tilewidth, y *
                               tm.tileheight, tm.tilewidth, tm.tileheight)
            tm.colisor_pisos_chao.append(rect)
    return tm

def desenha_mapa_fase2(surface, tm, offset_x, scale=0.5):
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




def colisao_fase2(tm, offset_x, mago,scale = 0.5):
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