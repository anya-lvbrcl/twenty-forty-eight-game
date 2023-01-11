import numpy
import random
import pygame
from pygame.locals import *
from Data import results, saving

from ColorsInTheGame import colors

Z = 4
USERNAME = None
GAMERS_DB = results()


class GameLoop:

    def __init__(self):

        self.grid = numpy.zeros((Z, Z), dtype=int)
        self.score = 0
        self.sScore = 0

        self.W = 400
        self.H = self.W
        self.margin = 5

        pygame.init()
        pygame.display.set_caption("2048")
        self.screen = pygame.display.set_mode((self.W, self.H + 130))

        pygame.font.init()
        self.font = pygame.font.Font('retro-land-mayhem.ttf', 35)

    def __str__(self):
        return str(self.grid)

    def new_number(self, k=1):
        free_poss = list(zip(*numpy.where(self.grid == 0)))
        for pos in random.sample(free_poss, k=k):
            if random.random() < .1:
                self.grid[pos] = 4
            else:
                self.grid[pos] = 2

    @staticmethod
    def get_num(this):
        this1 = this[this != 0]
        sum = []
        skip = False
        for j in range(len(this1)):
            if skip:
                skip = False
                continue
            if j != len(this1) - 1 and this1[j] == this1[j + 1]:
                new_n = this1[j] * 2
                skip = True
            else:
                new_n = this1[j]

            sum.append(new_n)

        return numpy.array(sum)

    def make_swipe(self, swipe):
        for i in range(Z):

            if swipe in 'lr':
                this = self.grid[i, :]
                pygame.mixer.music.load('swipe-sound.mp3')
                pygame.mixer.music.play(1)
            else:
                this = self.grid[:, i]
                pygame.mixer.music.load('swipe-sound.mp3')
                pygame.mixer.music.play(1)

            flipped = False
            if swipe in 'rd':
                flipped = True
                this = this[::-1]
            this_n = self.get_num(this)

            this2 = numpy.zeros_like(this)
            this2[:len(this_n)] = this_n

            if flipped:
                this2 = this2[::-1]
            if swipe in 'lr':
                self.grid[i, :] = this2
                pygame.mixer.music.load('swipe-sound.mp3')
                pygame.mixer.music.play(1)
            else:
                self.grid[:, i] = this2
                pygame.mixer.music.load('swipe-sound.mp3')
                pygame.mixer.music.play(1)

    def draw_top(self):
        font_best = pygame.font.Font('retro-land-mayhem.ttf', 25)
        font_best_2 = pygame.font.Font('retro-land-mayhem.ttf', 15)
        text_best = font_best.render("Best try: ", True, colors['text'])
        self.screen.blit(text_best, (200, 430))
        for index, gamer in enumerate(GAMERS_DB):
            name, score = gamer
            s = f'{name}-{score}'
            text_gamer = font_best_2.render(s, True, colors['text'])
            self.screen.blit(text_gamer, (200, 460 + 20 * index))
            print(index, name, score)

    def draw_game(self):
        self.screen.fill(colors['back'])

        for i in range(Z):
            for j in range(Z):
                n = self.grid[i][j]

                rect_x = j * self.W // Z + self.margin
                rect_y = i * self.H // Z + self.margin
                rect_w = self.W // Z - 2 * self.margin
                rect_h = self.H // Z - 2 * self.margin
                border_width = 5

                pygame.draw.rect(self.screen,
                                 colors[n],
                                 pygame.Rect(rect_x, rect_y, rect_w, rect_h),
                                 border_radius=4, width=border_width)
                if n == 0:
                    continue
                text_surface = self.font.render(f'{n}', True, colors['text'])
                text_rect = text_surface.get_rect(center=(rect_x + rect_w / 2,
                                                          rect_y + rect_h / 2))
                self.screen.blit(text_surface, text_rect)

                self.score = 0
                self.score -= self.sScore
                for x in range(Z):
                    for y in range(Z):
                        self.score += self.grid[x][y]

                counter_font = pygame.font.Font('retro-land-mayhem.ttf', 25)
                score_counter = counter_font.render(str(self.score), True, colors['text'])
                self.screen.blit(score_counter, (120, 430))

                font_score = pygame.font.Font('retro-land-mayhem.ttf', 25)
                text_score = font_score.render("Score: ", True, colors['text'])
                self.screen.blit(text_score, (15, 430))

                self.draw_top()

    @staticmethod
    def wait_for_key():
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return 'q'
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        return 'u'
                    elif event.key == K_RIGHT:
                        return 'r'
                    elif event.key == K_LEFT:
                        return 'l'
                    elif event.key == K_DOWN:
                        return 'd'
                    elif event.key == K_q or event.key == K_ESCAPE:
                        return 'q'

    def game_over(self):
        grid_bu = self.grid.copy()
        for swipe in 'lrud':
            self.make_swipe(swipe)
            if not all((self.grid == grid_bu).flatten()):
                self.grid = grid_bu
                return False
        return True

    def play(self):
        self.new_number(k=2)
        for x in range(Z):
            for y in range(Z):
                self.sScore += self.grid[x][y]

        while True:
            self.draw_game()
            pygame.display.flip()
            cmd = self.wait_for_key()
            if cmd == 'q':
                break

            old_grid = self.grid.copy()
            self.make_swipe(cmd)
            print(game.grid)
            if self.game_over():
                print('GAME OVER!', self.score)
                self.draw_outro()
                break

            if not all((self.grid == old_grid).flatten()):
                self.new_number()

    def draw_intro(self):

        intro_img = pygame.image.load('pixel-frame-0.png')
        intro_img_2 = pygame.image.load('pixel-frame-1.png')
        intro_img_3 = pygame.image.load('pixel-frame-2.png')

        welcome_font = pygame.font.Font('retro-land-mayhem.ttf', 50)
        rules_font = pygame.font.Font('retro-land-mayhem.ttf', 30)

        welcome_text = welcome_font.render("Hello!", True, colors['text'])
        rules_text = rules_font.render("Use to play:", True, colors['text'])
        rules_text_1 = rules_font.render("Press", True, colors['text'])

        player_name = 'Enter name'
        find_name = False

        while not find_name:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return 0
                elif event.type == KEYDOWN:
                    if event.unicode.isalpha():
                        if player_name == 'Enter name':
                            player_name = event.unicode
                        else:
                            player_name += event.unicode
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    elif event.key == pygame.K_RETURN:
                        if len(player_name) > 2:
                            global USERNAME
                            USERNAME = player_name
                            find_name = True
                            self.play()
                            break

            self.screen.fill(colors['back'])
            player_font = pygame.font.Font('retro-land-mayhem.ttf', 30)
            name_text = player_font.render(player_name, True, colors['text'])
            rect_name = name_text.get_rect()
            rect_name.center = self.screen.get_rect().center
            self.screen.blit(pygame.transform.scale(intro_img, [150, 150]), [10, 10])
            self.screen.blit(pygame.transform.scale(intro_img_2, [150, 200]), [120, 280])
            self.screen.blit(pygame.transform.scale(intro_img_3, [70, 50]), [228, 435])
            self.screen.blit(welcome_text, (200, 50))
            self.screen.blit(rules_text, (96, 290))
            self.screen.blit(rules_text_1, (120, 440))
            self.screen.blit(name_text, rect_name)
            pygame.display.update()

    def draw_outro(self):
        score_font = pygame.font.Font('retro-land-mayhem.ttf', 30)
        outro_font = pygame.font.Font('retro-land-mayhem.ttf', 40)

        outro_text = outro_font.render("Game over!", True, colors['text'])
        typed_text = score_font.render("You typed:", True, colors['text'])
        outro_count = score_font.render(str(self.score), True, colors['text'])

        largest_count = GAMERS_DB[0][1]
        if int(self.score) > largest_count:
            text = "New score!"
        else:
            text = f"Best try: {largest_count}"
        score_text = score_font.render(text, True, colors['text'])
        saving(USERNAME, int(self.score))
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return 0
            self.screen.fill(colors['back'])
            self.screen.blit(outro_text, (65, 30))
            self.screen.blit(typed_text, (70, 80))
            self.screen.blit(outro_count, (280, 80))
            self.screen.blit(score_text, (75, 110))
            pygame.display.update()


if __name__ == '__main__':
    game = GameLoop()
    game.draw_intro()
