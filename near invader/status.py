import pygame as pg

class Observer:
    def update(sellf, ntype):
        pass

class Status(Observer):
    def __init__(self):
        self.reset()
        #何この関数
        self._board = pg.Surface((800, 36), pg.SRCALPHA)
    
    @property
    def score(self):
        return self._score
    
    def reset(self):
        self._font = pg.font.Font(None, 32)
        self._distance = 0
        self._score = 0

    def reset_h(self):
        self._font = pg.font.Font(None, 32)
        self._distance = 0
        self._score = 0

    def update(self, ntype):
        if ntype == "distance":
            self._distance += 2
        if ntype == "score":
            self._score += 1
        if ntype == "Noscore":
            self._score += 0

    def draw(self, screen):
        pg.draw.rect(self._board, (0, 0, 0, 128), pg.Rect(0, 0, 800, 36))
        screen.blit(self._board, (0, 0))
        #info1は進んだ距離、info2はスコアの表示
        info1 = self._font.render(f"DISTANCE : {self._distance}", True, pg.Color("White"))
        info2 = self._font.render(f"SCORE : {self._score}", True, pg.Color("White"))
        screen.blit(info1, (20, 10))
        screen.blit(info2, (450, 10))