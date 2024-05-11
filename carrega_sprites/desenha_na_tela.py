

def anima_sprite_ataque(sprite, FRAME):
    
    index = (FRAME//2) % len(sprite)
    return index
def anima_sprite_inimigo(sprite,FRAME):
 
    index = (FRAME // 6) % len(sprite)
    return index

def anima_mago(sprite, frame):
    index = (frame // 5) % len(sprite)
    return index

def anima_ataque_mago(sprite, frame):
    index = (frame // 5) % len(sprite)
    return index

def anima_sprite_ataque2(sprite, frame):
    index = (frame //3) % len(sprite)
    return index
def carrega_imagens_inimigo(screen, mago, inimigo, FRAME):
    
    if inimigo.esta_vivo:
        if (inimigo.x-(mago.x-100)) > 200 and not inimigo.atacar:
            inimigo.direcao = 'tras'
            index = anima_sprite_inimigo(inimigo.sprite_anda_f, FRAME)
            screen.blit(inimigo.sprite_anda_f[index], (inimigo.x-(mago.x-100),inimigo.y))
        elif (inimigo.x-(mago.x-100)) < 250 and not inimigo.atacar:
            inimigo.direcao = 'frente'
            index = anima_sprite_inimigo(inimigo.sprite_anda_t, FRAME)
            screen.blit(inimigo.sprite_anda_t[index], (inimigo.x-(mago.x-100),inimigo.y))

        if inimigo.atacar:
            index = anima_sprite_ataque2(inimigo.sprite_ataque_f, FRAME)
            if inimigo.direcao == 'frente':
                screen.blit(inimigo.sprite_ataque_f[index], (inimigo.x-(mago.x-100), inimigo.y-50))
            elif inimigo.direcao == 'tras':
                screen.blit(inimigo.sprite_ataque_t[index], (inimigo.x-(mago.x-100), inimigo.y-50))
            inimigo.atacar = False

def carrega_imagens_lutador(screen, mago, lutador, FRAME, LUTADOR_SOFREU_DANO):
    if lutador.esta_vivo:
            if (lutador.x-(mago.x)) > 250 and not lutador.atacar:
                lutador.direcao = 'tras'
                index_lutador = anima_sprite_inimigo(lutador.sprite_anda_f, FRAME)
                screen.blit(lutador.sprite_anda_f[index_lutador], (lutador.x-(mago.x-50), lutador.y-13)) #mago ta atras
            elif (lutador.x-(mago.x)) < 250 and not lutador.atacar:
                lutador.direcao = 'frente'
                index_lutador = anima_sprite_inimigo(lutador.sprite_anda_f, FRAME)
                screen.blit(lutador.sprite_anda_t[index_lutador], (lutador.x-(mago.x-100), lutador.y-13))#mago ta na frente
            if lutador.atacar:
                index_lutador = anima_sprite_ataque(lutador.sprite_ataque_f, FRAME)
                if lutador.direcao == 'frente':
                    screen.blit(lutador.sprite_ataque_f[index_lutador], (lutador.x-(mago.x-100), lutador.y-13))
                elif lutador.direcao == 'tras':
                    screen.blit(lutador.sprite_ataque_t[index_lutador], (lutador.x-(mago.x-100), lutador.y-13))
                lutador.atacar = False
                
            if LUTADOR_SOFREU_DANO:
                LUTADOR_SOFREU_DANO = False
                if lutador.direcao == 'tras':
                    screen.blit(lutador.sofre_dano_sprite[1], (lutador.x-(mago.x-100), lutador.y+10))
                elif lutador.direcao == 'frente':
                    screen.blit(lutador.sofre_dano_sprite[0], (lutador.x-(mago.x-100), lutador.y+10))



def carrega_imagens_mago(screen, mago, POSICAO_X_PERSONAGEM, frame):
        if mago.update_ataque():
                index_ataque1 = anima_ataque_mago(mago.ataque1, frame)
                screen.blit(mago.ataque1[index_ataque1], (mago.posicao_ataquex, mago.posicao_ataquey ))

        if mago.andando_f:
            mago.ultima_direcao = 'frente'
            
            INDEX_MAGO = anima_mago(mago.sprite_andando_frente, frame)
            screen.blit(mago.sprite_andando_frente[INDEX_MAGO], (POSICAO_X_PERSONAGEM, mago.y-10))
    
        if mago.andando_t:
            mago.ultima_direcao = 'tras'
            INDEX_MAGO = anima_mago(mago.sprite_anda_tras, frame)
            screen.blit(mago.sprite_anda_tras[INDEX_MAGO], (POSICAO_X_PERSONAGEM, mago.y-10))

        if not mago.andando_t and not mago.andando_f:
            if mago.ultima_direcao == 'frente':
                INDEX_MAGO = anima_mago(mago.sprite_parado_frente, frame)
                screen.blit(mago.sprite_parado_frente[INDEX_MAGO], (POSICAO_X_PERSONAGEM, mago.y-10))
            elif mago.ultima_direcao == 'tras':
                INDEX_MAGO = anima_mago(mago.sprite_parado_tras, frame)
                screen.blit(mago.sprite_parado_tras[INDEX_MAGO], (POSICAO_X_PERSONAGEM, mago.y-10))



