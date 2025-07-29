import pygame as pg
import random, player, enemy, bullet, status, sound
from enemy import HealEnemy

#playerとenemyの一括管理ファイル

class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def notify(self, ntype):
        for observer in self._observers:
            observer.update(ntype)

class GameManager(Subject):
    def __init__(self):
        super().__init__()
        self._is_paused = False  # ポーズ状態を管理するフラグ
        self._HardMode = False#ハードモードを管理するフラグ
        self._player = player.Player()
        self._enemies = []
        self._effects = []
        self._bullets = []
        self._factory = enemy.EnemyFactory()
        self._status = status.Status()
        self.attach(self._status)
        self.reset()

    @property
    def is_playing(self):
        return self._is_playing
    @property
    def is_cleared(self):
        return self._is_cleared
    
    @property
    def is_paused(self):
        return self._is_paused

    def toggle_pause(self):
        self._is_paused = not self._is_paused  # ポーズ状態を切り替える
        
    def reset_h(self):
        self._is_playing = True
        self._is_cleared = False
        self._HardMode = True
        self._player.reset_h()
        self._enemies.clear()
        self._spawn_count = 0
        self._bullets.clear()
        self._bullet_count = 0
        self._status.reset_h()
        sound.SoundManager.get_instance().bgmstart()
        for i in range(2):
            self._enemies.append(enemy.FlameEnemy())
        for i in range(2):
            self._enemies.append(enemy.IceEnemy())
        for i in range(2):
            self._enemies.append(enemy.NonameEnemy())
        for i in range(1):
            self._enemies.append(enemy.HealEnemy())

    def reset(self):
        self._is_playing = True
        self._is_cleared = False
        self._HardMode = False
        self._player.reset()
        self._enemies.clear()
        #次の敵までの出現カウント
        self._spawn_count = 0
        self._bullets.clear()
        self._bullet_count = 0
        self._status.reset()
        sound.SoundManager.get_instance().bgmstart()
        for i in range(2):
            self._enemies.append(enemy.Enemy())
        for i in range(1):
            self._enemies.append(enemy.FlameEnemy())
        for i in range(1):
            self._enemies.append(enemy.IceEnemy())
        for i in range(1):
            self._enemies.append(enemy.NonameEnemy())
        for i in range(1):
            self._enemies.append(enemy.HealEnemy())

    def update(self):
        self.notify("distance")
        self._bullet_count += 1
        if self._bullet_count > 10:
            key = pg.key.get_pressed()
            #SPACEボタンで発射
            if key[pg.K_SPACE]:
                self._bullets.append(bullet.Bullet(self._player.rect))
                self._bullet_count = 0
        
        for e in self._effects:
            e.update()
        for b in self._bullets:
            b.update()
        self._player.update()
        self._spawn_count += 1
        if self._HardMode == True:
            if self._spawn_count > 7:
                self._spawn_count = 0
                self._enemies.append(self._factory.random_create_h())
        else:
            if self._spawn_count > 15:
                self._spawn_count = 0
                self._enemies.append(self._factory.random_create())
        for e in self._enemies:
            #弾丸に当たった敵の処理
            for b in self._bullets:
                if e.rect.colliderect(b.rect):
                    sound.SoundManager.get_instance().playattack()
                    self._bullets.remove(b)
                    e.hp -= 50
                    if e.hp <= 0:
                        #回復する敵のみスコアが加算しない
                        if isinstance(e, HealEnemy):
                            self.notify("Noscore")
                        else:
                            self.notify("score")
                        b = enemy.BombEffect(e.rect, self._effects)
                        sound.SoundManager.get_instance().playblast()
                        self._effects.append(b)
                        self._enemies.remove(e)
                        if self._status.score == 30:
                            self._is_playing = False
                            self._is_cleared = True
                            sound.SoundManager.get_instance().bgmstop()
                            sound.SoundManager.get_instance().playclear()
            if e._is_alive == False:
                self._enemies.remove(e)
                break
            e.update()
            
            #一番下に行くと敵が消える
            if e.rect.y >= 650:
                self._enemies.remove(e)
            if e in self._enemies:
            #ぶつかったときの判定
                if e.rect.colliderect(self._player.rect):
                    sound.SoundManager.get_instance().playbomb()
                    if isinstance(e, HealEnemy):  # HealEnemy かどうか判定
                        e.heal_player(self._player)
                        self._enemies.remove(e)
                    else:
                        self._enemies.remove(e)
                        self._player.damage()
                        #自機がぶつかったらダメージ
                        self._player.hp -= 50
                        if self._player.hp <= 0:
                            self._is_playing = False
                            sound.SoundManager.get_instance().bgmstop()
                            sound.SoundManager.get_instance().playover()
                    e.rect.y = self._player.rect.y - 70
                    e.vy = -abs(e.vy)
                    #一回の反射でHPを50減らす
                    e.hp -= 50
                    #if e.hp <= 0:
                    #    b = enemy.BombEffect(e.rect, self._effects)
                    #    self._effects.append(b)
                    #    self._enemies.remove(e)
                    #    #全ての敵がいなくなったらクリア
                    #    if len(self._enemies) == 0:
                    #        self._is_playing = False
                    #        self._is_cleared = True
                    #    return
    
    def draw(self, screen):
        #弾の表示
        for b in self._bullets:
            b.draw(screen)
        #エフェクトの表示
        for e in self._effects:
            e.draw(screen)
        #プレイヤーの表示
        self._player.draw(screen)
        #敵の表示
        for e in self._enemies:
            e.draw(screen)
        #UIの表示
        for e in self._observers:
            e.draw(screen)

