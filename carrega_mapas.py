
from variaveis_global import *
from variaveis_gravidade_pulo import *
import pygame
from pytmx.util_pygame import load_pygame
import pytmx



    


def desenha_mapa(surface, tm, offset_x, scale=0.5):
    tw = int(tm.tilewidth * scale)
    th = int(tm.tileheight * scale)
    start_x = int(offset_x / tw)
    end_x = start_x + int(surface.get_width() / tw) + 1  # +1 para cobrir casos de borda

    for layer in tm.visible_layers:
        if layer.name != "colisor_piso":
            if isinstance(layer, pytmx.TiledTileLayer):
                for x in range(start_x, min(end_x, layer.width)):
                    for y in range(layer.height):  # Assumindo que queremos desenhar toda a altura
                        gid = layer.data[y][x]
                        tile = tm.get_tile_image_by_gid(gid)
                        if tile:
                            tile = pygame.transform.scale(tile, (tw, th))
                            surface.blit(tile, ((x * tw) - offset_x, y * th))


def carrega_mapa_fase2(filename):
    tm = load_pygame(filename)
    tm.colisor_pisos_chao = []
    collision_layer = tm.get_layer_by_name("colisor_chao")
    for x, y, gid in collision_layer:
        if gid:
            rect = pygame.Rect(x * tm.tilewidth, y *
                               tm.tileheight, tm.tilewidth, tm.tileheight)
            tm.colisor_pisos_chao.append(rect)

    tm.colisor_lados = []
    blocos_lados = tm.get_layer_by_name('colisor_lados')
    for x, y, gid in blocos_lados:
        if gid:
            rect2 = pygame.Rect(x * tm.tilewidth, y *
                               tm.tileheight, tm.tilewidth, tm.tileheight)
            tm.colisor_lados.append(rect2)
    return tm


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
