import pygame as pg
import random

class SoundManager():
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def __init__(self):
        pg.mixer.music.load("sounds/bgm.wav")
        self._over = pg.mixer.Sound("sounds/over.wav")
        self._clear = pg.mixer.Sound("sounds/clear.wav")
        self._clap1 = pg.mixer.Sound("sounds/clap1.wav")
        self._clap2 = pg.mixer.Sound("sounds/clap2.wav")
        self._clap3 = pg.mixer.Sound("sounds/clap3.wav")
        self._blast = pg.mixer.Sound("sounds/blast.wav")
        self._bomb = pg.mixer.Sound("sounds/bomb.wav")

    def bgmstart(self):
        pg.mixer.music.play(-1)

    def bgmstop(self):
        pg.mixer.music.stop()

    def playover(self):
        self._over.play()

    def playclear(self):
        self._clear.play()

    def playattack(self):
        r = random.randint(0, 3)
        if r == 0:
            self._clap1.play()
        if r == 1:
            self._clap2.play()
        else:
            self._clap3.play()
    
    def playblast(self):
        self._blast.play()
    
    def playbomb(self):
        self._bomb.play()


