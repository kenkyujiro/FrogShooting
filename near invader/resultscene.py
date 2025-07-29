import pygame as pg

class ResultScene():
    def __init__(self, game):
        font = pg.font.Font(None, 50)
        self._game = game
        self._msg = font.render("Press K to replay.", True, pg.Color('white'))
        self._msg2 = font.render("If Y is play HardMode.", True, pg.Color('white'))
        self._gameover = pg.image.load("images/gameover.png")
        self._gameclear = pg.image.load("images/gameclear.png")

    def update(self):
        key = pg.key.get_pressed()
        if key[pg.K_k]:
            self._game.reset()
        elif key[pg.K_y]:
            self._game.reset_h()

    def draw(self, screen):
        screen.blit(self._msg, (120, 380))
        #ゲームが終わったときにクリア条件が達成されているかどうか
        if self._game.is_playing == False:
            if self._game.is_cleared == True:
                #ゲームクリア
                screen.blit(self._msg2, (120, 420))
                screen.blit(self._gameclear, (50, 200))
            else:
                #ゲームオーバー
                screen.blit(self._gameover, (50, 200))