import pygame as pg
import sys
from time import sleep
from source.model.ball import Ball
from source.model.paddle import Paddle
from source.model.pause_text import PauseText
from source.model.scoreboard import Scoreboard
from source.utils.palette import BG_COLOR
from source.utils.settings import FPS, RESOLUTION
from source.view.screen import Screen


class Game:
    def __init__(self):
        pg.init()
        # Window
        self.window = pg.display.set_mode(RESOLUTION)
        pg.display.set_caption("Pong Ultimate")
        icon_path = "assets/images/game-icon.png"
        icon = pg.image.load(icon_path)
        pg.display.set_icon(icon)
        # Clock
        self.clock = pg.time.Clock()
        # Groups
        self.entities = pg.sprite.Group()
        self.info = pg.sprite.Group()
        # Entities
        self.p1 = Paddle(self.entities, "left")
        self.p2 = Paddle(self.entities, "right")
        self.ball = Ball(self.entities, [self.p1, self.p2])
        # Info
        self.scoreboard_p1 = Scoreboard(self.info, self.p1)
        self.scoreboard_p2 = Scoreboard(self.info, self.p2)
        self.pause_txt = PauseText(self.info, self.ball)
        self.screen = Screen(self.info, self.entities)
        # Threads
        self.run_threads = True
        # BGM
        music_path = "assets/music/Beep_beat_by-feels_B._loop.wav"
        bg_music = pg.mixer.Sound(music_path)
        bg_music.play(-1)
        bg_music.set_volume(0.2)

    def run(self):
        while True:
            self.clock.tick(FPS)
            self._events()
            self._update()
            self._draw()

    def _events(self):
        for event in pg.event.get():
            keys = pg.key.get_pressed()
            if event.type == pg.QUIT or keys[pg.K_ESCAPE]:
                self.run_threads = False
                print("GAME OVER!\n")
                sys.exit()

    def _update(self):
        self.screen.update()

    def _draw(self):
        self.window.fill(BG_COLOR)
        self.screen.draw()
        pg.display.flip()

    def increase_ball_speed(self):
        count = 1
        while self.run_threads:
            if self.ball.is_moving():
                if count == 5:
                    self.ball.increase_speed()
                    count = 1
                sleep(1)
                count += 1
