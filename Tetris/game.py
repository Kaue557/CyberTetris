from random import choice

import pygame

from settings import *
from timer import Timer

class Game:
    def __init__(self, get_next_shape, upadate_score):

        #geral
        self.surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.display_surface = pygame.display.get_surface()
        self.rect = self.surface.get_rect(topleft = (PADDING, PADDING))
        self.sprites = pygame.sprite.Group()
        self.update_score = upadate_score

        #conexao do jogo
        self.get_next_shape = get_next_shape

        # linhas
        self.line_surface = self.surface.copy()
        self.line_surface.fill((0, 255, 0))
        self.line_surface.set_colorkey((0, 255, 0))
        self.line_surface.set_alpha(100)

        #tetromino
        self.field_data = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
        self.tetromino = Tetromino(
            choice(list(TETROMINOS.keys())),
            self.sprites,
            self.create_new_tetromino,
            self.field_data)

        #timer
        self.down_speed = UPDATE_START_SPEED
        self.down_speed_faster = self.down_speed * 0.3
        self.down_pressed = False
        self.timers = {
            'vertical move': Timer(UPDATE_START_SPEED, True, self.move_down),
            'horizontal move': Timer(MOVE_WAIT_TIME),
            'rotate': Timer(ROTATE_WAIT_TIME)
        }
        self.timers['vertical move'].activate()

        #score
        self.current_level = 1
        self.current_score = 0
        self.current_lines = 0

    def calculate_score(self, num_lines):
        self.current_lines += num_lines
        self.current_score += SCORE_DATA[num_lines] * self.current_lines

        #a cada 10 linhas limpas, sobe de nivel
        if self.current_lines / 10 > self.current_level:
            self.current_level += 1
        self.update_score(self.current_lines, self.current_score, self.current_level)

    def create_new_tetromino(self):
        # antes de criar uma forma nova checa se precisa limpar alguma linha
        self.check_finished_rows()
        self.tetromino = Tetromino(
            self.get_next_shape(),
            self.sprites,
            self.create_new_tetromino,
            self.field_data)

    def move_down(self):
        self.tetromino.move_down()

    def draw_grid(self):
        for col in range(1, COLUMNS):
            x = col * CELL_SIZE
            pygame.draw.line(self.line_surface, LINE_COLORII, (x, 0), (x, self.surface.get_height()), 1)
        for row in range(1, ROWS):
            y = row * CELL_SIZE
            pygame.draw.line(self.line_surface, LINE_COLORII, (0, y), (self.surface.get_width(), y), 1)

        self.surface.blit(self.line_surface, (0, 0))

    def input(self):
        keys = pygame.key.get_pressed()

        #checando movimento horizontal
        if not self.timers['horizontal move'].active:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.tetromino.move_horizontal(-1)
                self.timers['horizontal move'].activate()
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.tetromino.move_horizontal(1)
                self.timers['horizontal move'].activate()

        # checando rotacao
        if not self.timers['rotate'].active:
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.tetromino.rotate()
                self.timers['rotate'].activate()

        # acelerar decida
        if not self.down_pressed and (keys[pygame.K_DOWN] or keys[pygame.K_s]): #'se nao estiver sendo pressionada e aí pressionar'
            self.down_pressed = True
            self.timers['vertical move'].duration = self.down_speed_faster

        if self.down_pressed and not (keys[pygame.K_DOWN] or keys[pygame.K_s]): #'se estamos deixando de pressionar'
            self.down_pressed = False
            self.timers['vertical move'].duration = self.down_speed

    def timer_update(self):
        for timer in self.timers.values():
            timer.update()

    def check_finished_rows(self):
        #guardar os indices das linhas cheias
        delete_rows = []
        for i, row in enumerate(self.field_data):
            if all(row): #se linha estiver cheia
                delete_rows.append(i)

        if delete_rows: #se tem linhas para limpar
            for delete_row in delete_rows:

                # limpar linha
                for block in self.field_data[delete_row]:
                    block.kill() #exclui o sprite e o mesmo nao eh mais atualizado

                #mover os blocos para baixo
                for row in self.field_data:
                    for block in row:
                        #"se for bloco e estiver acima da linha que serah limpada"
                        if block and block.pos.y < delete_row:
                            block.pos.y += 1


            #reconstruir field_data para manter precisao com a parte visivel
            self.field_data = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
            for block in self.sprites:
                self.field_data[int(block.pos.y)][int(block.pos.x)] = block
            #atualizando o numero de linhas limpas
            self.calculate_score(len(delete_rows))

    def run(self):
        #update
        self.input()
        self.timer_update()
        self.sprites.update()

        #desenho
        self.surface.fill(GRAY)

        # limpa a área do jogo
        # self.surface.fill("black")

        self.sprites.draw(self.surface)
        self.draw_grid()
        self.display_surface.blit(self.surface, (PADDING, PADDING))
        pygame.draw.rect(self.display_surface, LINE_COLORII, self.rect, 2, 1)

class Tetromino:
    def __init__(self, shape, group, create_new_tetromino, field_data):

        #setup
        self.shape = shape
        self.block_positions = TETROMINOS[shape]['shape']
        self.color = TETROMINOS[shape]['color']
        self.create_new_tetromino = create_new_tetromino
        self.field_data = field_data

        #criar blocos
        self.blocks = [Block(group, pos, self.color) for pos in self.block_positions]

    #colisoes
    def next_move_horizontal_collide(self, blocks, amount):
        collision_list = [block.horizontal_collide(int(block.pos.x + amount), self.field_data) for block in blocks]
        return True if any(collision_list) else False

    def next_move_vertical_collide(self, blocks, amount):
        collision_list = [block.vertical_collide(int(block.pos.y + amount), self.field_data) for block in blocks]
        return True if any(collision_list) else False

    #movimentos
    def move_horizontal(self, amount):
        if not self.next_move_horizontal_collide(self.blocks, amount): #"se o prox. movimento horizontal nao cria colisao"
            for block in self.blocks:
                block.pos.x += amount

    def move_down(self):
        if not self.next_move_vertical_collide(self.blocks, 1): #"se nao ha colisao vertical"
            for block in self.blocks:
                block.pos.y += 1
        else: #"se chegar no chao"
            for block in self.blocks:
                # por padrao, o vetor tem numeros de ponto flutuante,
                # mas para indices precisamos de int
                self.field_data[int(block.pos.y)][int(block.pos.x)] = block

            self.create_new_tetromino()

    def rotate(self):
        if self.shape != 'O': #o quadrado nao roda [economiza processamento (ou nao :))]

            #1. ponto pivo (center mass, that part they aim for)
            pivot_pos = self.blocks[0].pos # de settings.py, o pivo serah sempre o (0, 0), primeira coordenada

            #2. novas posicoes do bloco
            new_block_positions = [block.rotate(pivot_pos) for block in self.blocks]

            #3. checar colisao (da pra fazer em um if so, mas ficaria horroroso)
            for pos in new_block_positions:
                # checar horizontal
                if pos.x < 0 or pos.x >= COLUMNS:
                    return

                # esta checagem deve estar antes do proximo if para prevenir que
                # a funcao tente acessar field_data[20], que nao existe, evitando erro/crash
                # checar vertical
                if pos.y >= ROWS:
                    return

                # checar campo (colisao com outras pecas)
                if self.field_data[int(pos.y)][int(pos.x)]: #"se ja tem um bloco nessa posicao"
                    return #impede a rotacao

            #4. implementar nova posicao
            for i, block in enumerate(self.blocks):
                block.pos = new_block_positions[i]

class Block(pygame.sprite.Sprite):
    def __init__(self, group, pos, color):

        #geral
        super().__init__(group)
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.image.fill(color)

        # posiçao
        self.pos = pygame.Vector2(pos) + BLOCK_OFFSET
        self.rect = self.image.get_rect(topleft= self.pos * CELL_SIZE)

    def rotate(self, pivot_pos):
        # distance = self.pos - pivot_pos
        # rotated = distance.rotate(90)
        # new_pos = pivot_pos + rotated
        # return new_pos
        return pivot_pos + (self.pos - pivot_pos).rotate(90) # mais complexo porem mais elegante

    def horizontal_collide(self, x, field_data):
        if not 0 <= x < COLUMNS: #"se a posicao estiver fora dos limites"
            return True
        if field_data[int(self.pos.y)][x]:
            return True

    def vertical_collide(self, y, field_data):
        if y >= ROWS:
            return True
        if y >= 0 and field_data[y][int(self.pos.x)]:
            return True

    def update(self):
        self.rect.topleft = self.pos * CELL_SIZE