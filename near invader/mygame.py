import pygame as pg, sys
import gamecontrol, resultscene

#全ての基本ファイル
pg.init()
screen = pg.display.set_mode((600, 650))
pg.display.set_caption("MYGAME")
game = gamecontrol.GameManager()
result = resultscene.ResultScene(game)

while True:
    screen.fill(pg.Color("Navy"))
    
    #床の表示
    #pg.draw.rect(screen, pg.Color("SeaGreen"), (0, 620, 600, 30))
    #花の表現
    #pg.draw.rect(screen, pg.Color("White"), (0, 620, 40, 10))
    #pg.draw.rect(screen, pg.Color("White"), (60, 620, 40, 10))
    #pg.draw.rect(screen, pg.Color("White"), (120, 620, 40, 10))
    #pg.draw.rect(screen, pg.Color("White"), (180, 620, 40, 10))
    #pg.draw.rect(screen, pg.Color("White"), (260, 620, 40, 10))
    #pg.draw.rect(screen, pg.Color("White"), (320, 620, 40, 10))
    #pg.draw.rect(screen, pg.Color("White"), (380, 620, 40, 10))
    #pg.draw.rect(screen, pg.Color("White"), (440, 620, 40, 10))
    #pg.draw.rect(screen, pg.Color("White"), (520, 620, 40, 10))
    #pg.draw.rect(screen, pg.Color("White"), (580, 620, 40, 10))

    
    #クローズ＆ポーズ処理
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_p:  # Pキーでポーズ切り替え
                game.toggle_pause()

    #ゲームクリア処理
    if not game.is_paused:
        if game.is_playing:
            game.update()
        else:
            result.update()

    #描画処理
    game.draw(screen)
    if not game.is_playing:
        result.draw(screen)

    #ポーズ中での表示
    if game.is_paused:
        font = pg.font.Font(None, 74)
        pause_text = font.render("PAUSED", True, pg.Color("White"))
        screen.blit(pause_text, (200, 300))

    #更新処理
    pg.display.update()
    pg.time.Clock().tick(60)

    #if game.is_playing == True:
        #game.update()
    #else:
        #result.update()
    #game.draw(screen)
    #if game.is_playing == False:
        #result.draw(screen)

    #pg.display.update()
    #pg.time.Clock().tick(60)
    #for event in pg.event.get():
        #if event.type == pg.QUIT:
            #pg.quit()
            #sys.exit()