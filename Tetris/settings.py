'''
Constantes e configurações, como:
- tamanho do grid,
- cores usadas,
- formato das peças e
- pontuação
'''

import pygame

# GAME SIZE
COLUMNS = 10
ROWS = 20
CELL_SIZE = 40 # em pixels
GAME_WIDTH = COLUMNS * CELL_SIZE
GAME_HEIGHT = ROWS * CELL_SIZE

# SIDE BAR SIZE
SIDEBAR_WIDTH = 200
PREVIEW_HEIGHT_FRACTION = 0.7
SCORE_HEIGHT_FRACTION = 1 - PREVIEW_HEIGHT_FRACTION

# WINDOW
PADDING = 20
WINDOW_WIDTH = GAME_WIDTH + SIDEBAR_WIDTH + PADDING * 3
WINDOW_HEIGHT = GAME_HEIGHT + PADDING * 2

# GAME BEHAVIOR
UPDATE_START_SPEED = 300
MOVE_WAIT_TIME = 150
ROTATE_WAIT_TIME = 200
BLOCK_OFFSET = pygame.Vector2(COLUMNS // 2, -1)

# COLORS - CYBERPUNK PALLETE :) TROCAR!
RED = '#c5003c'
BLUE = '#005678'
YELLOW = '#f3e600'
GREEN = '#00ff9f'
PURPLE = '#bd00ff'
CYAN = '#05d9e8'
ORANGE = '#f28444'
GRAY = '#1C1C1C'
LINE_COLOR = '#FFFFFF'
LINE_COLORII = '#B3B3B3'

# SHAPES
TETROMINOS = {
    'T': {'shape': [(0,0), (-1,0), (1,0), (0,-1)], 'color': PURPLE},
    'O': {'shape': [(0,0), (0,-1), (1,0), (1,-1)], 'color': YELLOW},
    'J': {'shape': [(0,0), (0,-1), (0,1), (-1,1)], 'color': BLUE},
    'L': {'shape': [(0,0), (0,-1), (0,1), (1,1)], 'color': ORANGE},
    'I': {'shape': [(0,0), (0,-1), (0,-2), (0,1)], 'color': CYAN},
    'S': {'shape': [(0,0), (-1,0), (0,-1), (1,-1)], 'color': GREEN},
    'Z': {'shape': [(0,0), (1,0), (0,-1), (-1,-1)], 'color': RED},
}

SCORE_DATA = {1: 40, 2: 100, 3: 300, 4: 1200}
