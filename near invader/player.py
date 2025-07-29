import pygame as pg

class PlayerState():
    def __init__(self, player):
        self._player = player
        self._image = None

    def update(self):
        pass

    @property
    def image(self):
        return self._image

class IdleState(PlayerState):
    def __init__(self, player):
        super().__init__(player)
        self._image = pg.image.load("images/kaeru1.png")

    def update(self):
        key = pg.key.get_pressed()
        #モーションの管理
        if key[pg.K_a] or key[pg.K_d]:
            return MovingState(self._player)
        else:
            return self

#アニメーション及び動き処理
class MovingState(PlayerState):
    def __init__(self, player):
        super().__init__(player)
        #変数の初期化宣言
        self._images = [
            pg.image.load("images/kaeru1.png"),
            pg.image.load("images/kaeru2.png"),
            pg.image.load("images/kaeru3.png"),
            pg.image.load("images/kaeru4.png")
        ]
        self._cnt = 0
        self._image = self._images[0]

    def update(self):
        self._cnt += 1
        self._image = self._images[self._cnt // 5 % 4]
        key = pg.key.get_pressed()
        #モーションリセット
        if not (key[pg.K_a] or key[pg.K_d]):
            return IdleState(self._player)
        else:
            return self
        
#ダメージ処理
class DamageState(PlayerState):
    def __init__(self, player):
        super().__init__(player)
        self._images = [
            pg.image.load("images/kaeru5.png"),
            pg.image.load("images/kaeru6.png")
        ]
        self._cnt = 0
        self._image = self._images[0]
        self._timeout = 20

    def update(self):
        self._cnt += 1
        self._image = self._images[self._cnt // 5 % 2]
        self._timeout -= 1
        if self._timeout < 0:
            return IdleState(self._player)
        else:
            return self

class Player():
    #読み込み
    def __init__(self):
        self.reset()
    
    @property
    def rect(self):
        return self._rect
    @rect.setter
    def rect(self, value):
        self._rect = value

    def reset_h(self):
        self._state = IdleState(self)
        self._rect = pg.Rect(250, 550, 50, 50)
        self._speed = 10
        self._maxhp = 100
        self._hp = 100

    def reset(self):
        self._state = IdleState(self)
        self._rect = pg.Rect(250, 550, 50, 50)
        self._speed = 10
        self._maxhp = 150
        self._hp = 150

    @property
    def maxhp(self):
        return self._maxhp
    @property
    def hp(self):
        return self._hp
    @hp.setter
    def hp(self, value):
        self._hp = value
    
    def update(self):
        self._state = self._state.update()
        key = pg.key.get_pressed()
        vx = 0
        if key[pg.K_d]:
            vx = self._speed
        if key[pg.K_a]:
            vx = -self._speed
        if self._rect.x + vx < 0 or self._rect.x + vx > 550:
            vx = 0
        self._rect.x += vx
        

    #画面への表示処理
    def draw(self, screen):
        screen.blit(self._state.image, self._rect)
        rect1 = pg.Rect(self._rect.x, self._rect.y - 20, 4, 20)
        h = (self.hp / self._maxhp) * 20
        rect2 = pg.Rect(self._rect.x, self._rect.y - h, 4, h)
        pg.draw.rect(screen, pg.Color("Red"), rect1)
        pg.draw.rect(screen, pg.Color("Green"), rect2)

    def damage(self):
        self._state = DamageState(self)


