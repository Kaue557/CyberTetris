from settings import *
from sys import exit

# componentes
from game import Game
from score import Score
from preview import Preview

from random import choice

class Main:
    def __init__(self):

        #geral
        pygame.init()
        self.dysplay_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Cyber Tetris')

        #formas
        self.next_shapes = [choice(list(TETROMINOS.keys())) for shape in range(3)]

        #componentes
        self.game = Game(self.get_next_shape, self.update_score)
        self.score = Score()
        self.preview = Preview()

    def update_score(self, lines, score, level):
        self.score.lines = lines
        self.score.score = score
        self.score.level = level

    def get_next_shape(self):
        next_shape = self.next_shapes.pop(0) #tira a proxima peça da lista e armazena
        self.next_shapes.append(choice(list(TETROMINOS.keys()))) #adiciona uma nova peça na lista
        return next_shape

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    #sair de tudo para evitar erro
                    exit()

            #display
            self.dysplay_surface.fill(GRAY)

            #componentes
            self.game.run()
            self.score.run()
            self.preview.run(self.next_shapes)

            #atualizando o jogo
            pygame.display.update()
            self.clock.tick(60)
            # se nao tiver argumento o jogo vai tentar rodar com o maior numero de frames possivel

if __name__ == '__main__': # garante que rodemos apenas o arquivo Main
    main = Main()
    main.run()