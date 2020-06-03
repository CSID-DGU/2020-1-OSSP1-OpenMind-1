while running :
   if pause : 

   elif multiplay_start:
        # �޺� ī��Ʈ
        #pressed = lambda key: event.type == pygame.KEYDOWN and event.key == key
        #unpressed = lambda key: event.type == pygame.KEYUP and event.key == key

        for event in pygame.event.get():
            #event.key = pygame.key.get_pressed()
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                # Set speed
                if not game_over:
                    keys_pressed = pygame.key.get_pressed()
                    if keys_pressed[K_DOWN]:
                        pygame.time.set_timer(pygame.USEREVENT, framerate * 1)
                    else:
                        pygame.time.set_timer(pygame.USEREVENT, framerate * 20)

                # Draw a mino
                draw_mino(dx, dy, mino, rotation)
                # Draw player 2 mino

                draw_board(next_mino, hold_mino, score, level, goal)
                # Draw player 2 ����

                # Erase a mino
                if not game_over:
                    erase_mino(dx, dy, mino, rotation)

                # Move mino down
                if not is_bottom(dx, dy, mino, rotation):
                    dy += 1

                # Create new mino
                else:
                    if hard_drop or bottom_count == 6:
                        hard_drop = False
                        bottom_count = 0
                        score += 10 * level
                        draw_mino(dx, dy, mino, rotation)
                        draw_board(next_mino, hold_mino, score, level, goal)
                        if is_stackable(next_mino):
                            mino = next_mino
                            next_mino = randint(1, 7)
                            dx, dy = 3, 0
                            rotation = 0
                            hold = False
                        else: #���̻� ���� �� ������ ���ӿ���
                            ui_variables.GameOver_sound.play()
                            start = False
                            game_over = True
                            pygame.time.set_timer(pygame.USEREVENT, 1)
                    else:
                        bottom_count += 1

                # Erase line
                # �޺� ī��Ʈ 
                erase_count = 0
                combo_value = 0
                sent = 0

                for j in range(21):
                    is_full = True
                    for i in range(10):
                        if matrix[i][j] == 0:
                            is_full = False
                    if is_full:
                        erase_count += 1
                        k = j
                        combo_value += 1
                        while k > 0:
                            for i in range(10):
                                matrix[i][k] = matrix[i][k - 1]
                            k -= 1

                # ���� ������ ������ �޺� -1
                #if erase_count == 0 :
                    #combo_count -= 1
                    #if combo_count < 0:
                        #combo_count = 0

                if erase_count >= 1:
                    combo_count += 1
                    if erase_count == 1:
                        ui_variables.break_sound.play()
                        ui_variables.single_sound.play()
                        score += 50 * level * erase_count + combo_count
                        sent += 1
                    elif erase_count == 2:
                        ui_variables.break_sound.play()
                        ui_variables.double_sound.play()
                        ui_variables.double_sound.play()
                        score += 150 * level * erase_count + 2 * combo_count
                        sent += 2
                    elif erase_count == 3:
                        ui_variables.break_sound.play()
                        ui_variables.triple_sound.play()
                        ui_variables.triple_sound.play()
                        ui_variables.triple_sound.play()
                        score += 350 * level * erase_count + 3 * combo_count
                        sent += 3
                    elif erase_count == 4:
                        ui_variables.break_sound.play()
                        ui_variables.tetris_sound.play()
                        ui_variables.tetris_sound.play()
                        ui_variables.tetris_sound.play()
                        ui_variables.tetris_sound.play()
                        score += 1000 * level * erase_count + 4 * combo_count
                        screen.blit(ui_variables.combo_4ring, (250, 160))
                        sent += 4

                    for i in range(1, 11) :
                        if combo_count == i :  # 1 ~ 10 �޺� �̹���
                            screen.blit(ui_variables.large_combos[i-1], (124, 190))  # blits the combo number
                        elif combo_count > 10 : # 11 �̻� �޺� �̹���
                            screen.blit(tetris4, (100, 190))  # blits the combo number

                    for i in range(1, 10) :
                        if combo_count == i+2 : # 3 ~ 11 �޺� ����
                            ui_variables.combos_sound[i-1].play()


                sent = checkCombo(combo_count, sent)  # �޺� ����

                # Increase level
                goal -= erase_count
                if goal < 1 and level < 15:
                    level += 1
                    ui_variables.LevelUp_sound.play()
                    ui_variables.LevelUp_sound.play()
                    ui_variables.LevelUp_sound.play()
                    ui_variables.LevelUp_sound.play()
                    goal += level * 5
                    framerate = int(framerate * 0.8)

            elif event.type == KEYUP:                                 ##�߿�
                erase_mino(dx, dy, mino, rotation)
                if event.key == K_ESCAPE:
                    ui_variables.click_sound.play()
                    start = False
                    pause = True
                # Hard drop
                elif event.key == K_SPACE:
                    ui_variables.fall_sound.play()
                    ui_variables.drop_sound.play()
                    while not is_bottom(dx, dy, mino, rotation):
                        dy += 1
                    hard_drop = True
                    pygame.time.set_timer(pygame.USEREVENT, 1)
                    draw_mino(dx, dy, mino, rotation)
                    draw_board(next_mino, hold_mino, score, level, goal)
                # Hold
                elif event.key == K_LSHIFT or event.key == K_q:
                    if hold == False:
                        ui_variables.move_sound.play()
                        if hold_mino == -1:
                            hold_mino = mino
                            mino = next_mino
                            next_mino = randint(1, 7)
                        else:
                            hold_mino, mino = mino, hold_mino
                        dx, dy = 3, 0
                        rotation = 0
                        hold = True
                    draw_mino(dx, dy, mino, rotation)
                    draw_board(next_mino, hold_mino, score, level, goal)
                # Turn right
                elif event.key == K_UP or event.key == K_w:
                    if is_turnable_r(dx, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        rotation += 1
                    # Kick
                    elif is_turnable_r(dx, dy - 1, mino, rotation):
                        ui_variables.move_sound.play()
                        dy -= 1
                        rotation += 1
                    elif is_turnable_r(dx + 1, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx += 1
                        rotation += 1
                    elif is_turnable_r(dx - 1, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx -= 1
                        rotation += 1
                    elif is_turnable_r(dx, dy - 2, mino, rotation):
                        ui_variables.move_sound.play()
                        dy -= 2
                        rotation += 1
                    elif is_turnable_r(dx + 2, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx += 2
                        rotation += 1
                    elif is_turnable_r(dx - 2, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx -= 2
                        rotation += 1
                    if rotation == 4:
                        rotation = 0
                    draw_mino(dx, dy, mino, rotation)
                    draw_board(next_mino, hold_mino, score, level, goal)
                # Turn left
                elif event.key == K_z or event.key == K_LCTRL:
                    if is_turnable_l(dx, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        rotation -= 1
                    # Kick
                    elif is_turnable_l(dx, dy - 1, mino, rotation):
                        ui_variables.move_sound.play()
                        dy -= 1
                        rotation -= 1
                    elif is_turnable_l(dx + 1, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx += 1
                        rotation -= 1
                    elif is_turnable_l(dx - 1, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx -= 1
                        rotation -= 1
                    elif is_turnable_l(dx, dy - 2, mino, rotation):
                        ui_variables.move_sound.play()
                        dy -= 2
                        rotation += 1
                    elif is_turnable_l(dx + 2, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx += 2
                        rotation += 1
                    elif is_turnable_l(dx - 2, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx -= 2
                    if rotation == -1:
                        rotation = 3
                    draw_mino(dx, dy, mino, rotation)
                    draw_board(next_mino, hold_mino, score, level, goal)
                # Move left
                elif keys_pressed[K_LEFT] :                     # key = pygame.key.get_pressed()
                    if not is_leftedge(dx, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        keys_pressed = pygame.key.get_pressed()
                        pygame.time.set_timer(pygame.KEYUP, framerate * 3)
                        dx -= 1
                    draw_mino(dx, dy, mino, rotation)
                    draw_board(next_mino, hold_mino, score, level, goal)
                # Move right
                elif keys_pressed[K_RIGHT] :
                    if not is_rightedge(dx, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        keys_pressed = pygame.key.get_pressed()
                        pygame.time.set_timer(pygame.KEYUP, framerate * 3)
                        dx += 1
                    draw_mino(dx, dy, mino, rotation)
                    draw_board(next_mino, hold_mino, score, level, goal)

                #elif unpressed(pygame.K_LEFT) :
                #   movement_keys_timer = movement_keys_speed * 2
                #elif unpressed(pygame.K_RIGHT) :
                #    movement_keys_timer = movement_keys_speed * 2

        if any(movement_keys.values()):
            movement_keys_timer += clock.tick(50)
        #if movement_keys_timer > movement_keys_speed:
        #    pressed(pygame.K_LEFT)
        #    pressed(pygame.K_RIGHT)
        #    movement_keys_timer %= movement_keys_speed

        pygame.display.update()

    # Game over screen
def draw_2Pboard(next, hold, score, level, goal):
    screen.fill(ui_variables.grey_1)

    # Draw sidebar
    pygame.draw.rect(
        screen,
        ui_variables.white,
        Rect(948, 0, 180, 730)
    )   

    # Draw next mino
    grid_n = tetrimino.mino_map[next - 1][0]

    for i in range(4): # 16���� �׸��� ĭ���� true�� ���� �̾Ƽ� draw.rect
        for j in range(4):
            dx = 979 + block_size * j
            dy = 220 + block_size * i
            if grid_n[i][j] != 0:
                draw_block(dx,dy,ui_variables.t_color[grid_n[i][j]]) # ���� ������ ���� �������� ����.
                

    # Draw hold mino
    grid_h = tetrimino.mino_map[hold - 1][0]

    if hold_mino != -1:
        for i in range(4):
            for j in range(4):
                dx = 979 + block_size * j
                dy = 60 + block_size * i
                if grid_h[i][j] != 0:
                    draw_block(dx,dy,ui_variables.t_color[grid_h[i][j]])

    # Set max score
    if score > 999999:
        score = 999999

    # Draw texts
    text_hold = ui_variables.h5.render("HOLD", 1, ui_variables.black)
    text_next = ui_variables.h5.render("NEXT", 1, ui_variables.black)
    text_combo = ui_variables.h5.render("COMBO", 1, ui_variables.black) # �޺� 
    text_score = ui_variables.h5.render("SCORE", 1, ui_variables.black)
    combo_value = ui_variables.h4.render(str(combo_count), 1, ui_variables.black) # �޺� ��

    score_value = ui_variables.h4.render(str(score), 1, ui_variables.black)
    text_level = ui_variables.h5.render("LEVEL", 1, ui_variables.black)
    level_value = ui_variables.h4.render(str(level), 1, ui_variables.black)
    text_goal = ui_variables.h5.render("GOAL", 1, ui_variables.black)
    goal_value = ui_variables.h4.render(str(goal), 1, ui_variables.black)

    # Place texts
### <<<<<<< HEAD
    screen.blit(text_hold, (779, 14))
    screen.blit(text_next, (779, 104))
    screen.blit(text_score, (779, 194))
    screen.blit(score_value, (784, 210))
    screen.blit(text_level, (779, 254))
    screen.blit(level_value, (784, 270)) 
    screen.blit(text_goal, (779, 314))
    screen.blit(goal_value, (784, 330))
## =======
    screen.blit(text_hold, (979, 20))
    screen.blit(text_next, (979, 170))
    screen.blit(text_score, (979, 340))
    screen.blit(score_value, (984, 370))
    screen.blit(text_level, (979, 470))
    screen.blit(level_value, (984, 500))
    screen.blit(text_combo,(979,600))
    screen.blit(combo_value,(984,630))

    # Draw board
    for x in range(width):
        for y in range(height):
            dx = 17 + block_size * x
            dy = 17 + block_size * y
            draw_block(dx, dy, ui_variables.t_color[matrix[x][y + 1]])