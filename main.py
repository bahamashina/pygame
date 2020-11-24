import pygame

pygame.init()
screenwidth = 950
screenheight = 600
screen = pygame.display.set_mode((screenwidth,screenheight))
pygame.display.set_caption('Forest treasures')
pygame.display.set_icon(pygame.image.load('pictures/icon.png'))

#!!! pictures

bg = pygame.transform.scale(pygame.image.load('pictures/background.png'),(screenwidth,screenheight))
button_play=pygame.transform.scale(pygame.image.load('pictures/button_play.png'),(75,75))
button_play_2=pygame.transform.scale(pygame.image.load('pictures/button_play_2.png'),(75,75))
button_options=pygame.transform.scale(pygame.image.load('pictures/button_options.png'),(75,75))
button_options_2=pygame.transform.scale(pygame.image.load('pictures/button_options_2.png'),(75,75))
music_on=pygame.transform.scale(pygame.image.load('pictures/music_on.png'),(90,90))
music_on_2=pygame.transform.scale(pygame.image.load('pictures/music_on_2.png'),(90,90))
music_off=pygame.transform.scale(pygame.image.load('pictures/music_off.png'),(90,90))
music_off_2=pygame.transform.scale(pygame.image.load('pictures/music_off_2.png'),(90,90))
title=pygame.transform.scale(pygame.image.load('pictures/title.png'),(475,100))
game_bg=pygame.transform.scale(pygame.image.load('pictures/game_bg.png'),(screenwidth,screenheight))
menu_button=pygame.transform.scale(pygame.image.load('pictures/menu_button.png'),(75,75))
menu_button_2=pygame.transform.scale(pygame.image.load('pictures/menu_button_2.png'),(80,80))
options_titles=pygame.transform.scale(pygame.image.load('pictures/options_titles.png'),(300,300))
example_buttons=pygame.transform.scale(pygame.image.load('pictures/example_buttons.png'),(50,250))
# explosionSound=pygame.mixer.Sound('sounds/explosion.wav')



font2 =pygame.font.Font('ThaleahFat.ttf', 16)
font3 =pygame.font.Font('ThaleahFat.ttf', 32)
font4 =pygame.font.Font('ThaleahFat.ttf', 56)

click = False

def draw_text(text,font1,color,surface,x,y):
	textobj = font1.render(text,1,color)
	textrect = textobj.get_rect()
	textrect.topleft = (x,y)
	surface.blit(textobj,textrect)

def buttons_animation():
	global button_tick,button_anim
	if button_tick ==50:
		button_anim = False
	elif button_tick == 0:
		button_anim = True

	if button_anim:
		button_tick +=2
	else:
		button_tick -=2


class Player(pygame.sprite.Sprite):
	# Изначально игрок смотрит вправо, поэтому эта переменная True
	right = True

	# Методы
	def __init__(self):
		# Стандартный конструктор класса
		# Нужно ещё вызывать конструктор родительского класса
		super().__init__()

		# Создаем изображение для игрока

		self.images=[pygame.transform.scale(pygame.image.load('pictures/hero.png'),(75,75)),
            pygame.transform.scale(pygame.image.load('pictures/jump.png'),(75,75)),
                    pygame.transform.scale(pygame.image.load('pictures/fall.png'),(75,75))]
		self.image_anim=[]
		self.image = self.images[0]
		# Установите ссылку на изображение прямоугольника
		self.rect = self.image.get_rect()

		# Задаем вектор скорости игрока
		self.change_x = 0
		self.change_y = 0

	def update(self):
		# В этой функции мы передвигаем игрока
		# Сперва устанавливаем для него гравитацию
		self.calc_grav()

		# Передвигаем его на право/лево
		# change_x будет меняться позже при нажатии на стрелочки клавиатуры
		self.rect.x += self.change_x

		# Следим ударяем ли мы какой-то другой объект, платформы, например
		block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)


		# Перебираем все возможные объекты, с которыми могли бы столкнуться
		for block in block_hit_list:
			# Если мы идем направо,
			# устанавливает нашу правую сторону на левой стороне предмета, которого мы ударили
			if self.change_x > 0:
				self.rect.right = block.rect.left
			elif self.change_x < 0:
				# В противном случае, если мы движемся влево, то делаем наоборот
				self.rect.left = block.rect.right

		# Передвигаемся вверх/вниз
		self.rect.y += self.change_y

		# То же самое, вот только уже для вверх/вниз
		block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
		for block in block_hit_list:
			# Устанавливаем нашу позицию на основе верхней / нижней части объекта, на который мы попали
			if self.change_y > 0:
				self.rect.bottom = block.rect.top
				if(self.right): # Проверяем куда он смотрит и если что, то переворачиваем его
					self.image=self.images[0]
				else:
					self.image=self.images[0]
					self.flip()
			elif self.change_y < 0:
				self.rect.top = block.rect.bottom
				if(self.right): # Проверяем куда он смотрит и если что, то переворачиваем его
					self.image=self.images[0]
				else:
					self.image=self.images[0]
					self.flip()

			# Останавливаем вертикальное движение
			self.change_y = 0

	def calc_grav(self):
		global done
		# Здесь мы вычисляем как быстро объект будет
		# падать на землю под действием гравитации
		if self.change_y == 0:
			self.change_y = 1
		else:
			self.change_y += 0.95
			if self.change_y >0:
				if(self.right): # Проверяем куда он смотрит и если что, то переворачиваем его
					self.image=self.images[2]
				else:
					self.image=self.images[2]
					self.flip()
		# Если уже на земле, то ставим позицию Y как 0
		if self.rect.y >= screenheight - self.rect.height and self.change_y >= 0:
			done=True
			self.change_y = 0
			self.rect.y = screenheight - self.rect.height
			if(self.right): # Проверяем куда он смотрит и если что, то переворачиваем его
				self.image=self.images[0]
			else:
				self.image=self.images[0]
				self.flip()

	def jump(self):
		# Обработка прыжка
		# Нам нужно проверять здесь, контактируем ли мы с чем-либо
		# или другими словами, не находимся ли мы в полете.
		# Для этого опускаемся на 10 единиц, проверем соприкосновение и далее поднимаемся обратно
		self.rect.y += 10
		platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
		self.rect.y -= 10

		# Если все в порядке, прыгаем вверх
		if len(platform_hit_list) > 0 or self.rect.bottom >= screenheight:
			self.change_y = -16
			if(self.right): # Проверяем куда он смотрит и если что, то переворачиваем его
				self.image=self.images[1]
			else:
				self.image=self.images[1]
				self.flip()
		else:
			if(self.right): # Проверяем куда он смотрит и если что, то переворачиваем его
				self.image=self.images[2]
			else:
				self.image=self.images[2]
				self.flip()

	# Передвижение игрока
	def go_left(self):
		# Сами функции будут вызваны позже из основного цикла
		self.change_x = -9 # Двигаем игрока по Х
		if(self.right): # Проверяем куда он смотрит и если что, то переворачиваем его
			self.flip()
			self.right = False

	def go_right(self):
		# то же самое, но вправо
		self.change_x = 9
		if (not self.right):
			self.flip()
			self.right = True


	def stop(self):
		# вызываем этот метод, когда не нажимаем на клавиши
		self.change_x = 0

	def flip(self):
		# переворот игрока (зеркальное отражение)
		self.image = pygame.transform.flip(self.image, True, False)


class Chest(pygame.sprite.Sprite):
	global screen
	def __init__(self):

		super().__init__()

		self.width=75
		self.height =75

		self.images = [ pygame.transform.scale(pygame.image.load('pictures/chest/1.png'),(self.width,self.height)),
                        pygame.transform.scale(pygame.image.load('pictures/chest/2.png'),(self.width,self.height)),
                        pygame.transform.scale(pygame.image.load('pictures/chest/3.png'),(self.width,self.height)),
                        pygame.transform.scale(pygame.image.load('pictures/chest/4.png'),(self.width,self.height)),
                        pygame.transform.scale(pygame.image.load('pictures/chest/5.png'),(self.width,self.height)),
                        pygame.transform.scale(pygame.image.load('pictures/chest/6.png'),(self.width,self.height)),
                        pygame.transform.scale(pygame.image.load('pictures/chest/7.png'),(self.width,self.height)),
                        pygame.transform.scale(pygame.image.load('pictures/chest/8.png'),(self.width,self.height)),
                        pygame.transform.scale(pygame.image.load('pictures/chest/9.png'),(self.width,self.height))]
		self.cnt=0
		self.open_chest=0


	def draw(self,player,x,y):
		global current_level_no
		self.rect = screen.blit(self.images[0],(x,y))

		if self.open_chest >=40:
			self.cnt=1

		col=self.rect.colliderect(player.rect)

		if col:
			if self.cnt == 0:
				screen.blit(self.images[self.open_chest//5],(x,y))
				self.open_chest +=1
			else:
				screen.blit(self.images[8],(x,y))
				current_level_no += 1
		else:
			screen.blit(self.images[0],(x,y))


class Platform(pygame.sprite.Sprite):
	def __init__(self, width, height):
		# Конструктор платформ
		super().__init__()
		# Также указываем фото платформы
		self.image = pygame.transform.scale(pygame.image.load('pictures/platform1.png'),(150,50))

		# Установите ссылку на изображение прямоугольника
		self.rect = self.image.get_rect()


class Enemy(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		# Также указываем фото платформы
		self.image = pygame.transform.scale(pygame.image.load('pictures/enemy.png'),(150,150))
		# Установите ссылку на изображение прямоугольника
		self.rect = self.image.get_rect()
		self.timer=0
		self.anim =True


	def draw(self,player,x,y):

		global current_level_no,done
		self.speed=2

		if self.timer == 200:
			self.anim=False
		elif self.timer == 0:
			self.anim = True

		if self.anim:
			self.timer +=self.speed
		else:
			self.timer -=self.speed
		self.rect = screen.blit(self.image,(x+self.timer,y))
		collision=self.rect.colliderect(player.rect)

		if collision:
			done=True
		else:
			screen.blit(self.image,(x+self.timer,y))


class Coin(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.images = [pygame.transform.scale(pygame.image.load('pictures/coin/1.png'),(25,25)),
		pygame.transform.scale(pygame.image.load('pictures/coin/2.png'),(25,25)),
		pygame.transform.scale(pygame.image.load('pictures/coin/3.png'),(25,25)),
		pygame.transform.scale(pygame.image.load('pictures/coin/4.png'),(25,25)),
		pygame.transform.scale(pygame.image.load('pictures/coin/5.png'),(25,25)),
		pygame.transform.scale(pygame.image.load('pictures/coin/6.png'),(25,25)),
		pygame.transform.scale(pygame.image.load('pictures/coin/7.png'),(25,25)),
		pygame.transform.scale(pygame.image.load('pictures/coin/8.png'),(25,25)),
		pygame.transform.scale(pygame.image.load('pictures/coin/9.png'),(25,25)),
		pygame.transform.scale(pygame.image.load('pictures/coin/10.png'),(25,25)),
		pygame.transform.scale(pygame.image.load('pictures/coin/11.png'),(25,25)),
		pygame.transform.scale(pygame.image.load('pictures/coin/12.png'),(25,25)),
		pygame.transform.scale(pygame.image.load('pictures/coin/13.png'),(25,25)),
		pygame.transform.scale(pygame.image.load('pictures/coin/14.png'),(25,25)),
		pygame.transform.scale(pygame.image.load('pictures/coin/15.png'),(25,25)),
		pygame.transform.scale(pygame.image.load('pictures/coin/16.png'),(25,25)),
		pygame.transform.scale(pygame.image.load('pictures/coin/17.png'),(25,25))]
		self.coin_anim=0
		self.coin_cnt=0

	def draw(self,player,x,y):
		global current_level_no,coin_count

		if self.coin_anim >=51:
			self.coin_anim =0


		if self.coin_cnt == 0:
			self.rect = screen.blit(self.images[0],(x,y))

			self.col=self.rect.colliderect(player.rect)

			if self.col==0:
				screen.blit(self.images[self.coin_anim//3],(x,y))
				self.coin_anim+=1
			else:
			 	coin_count +=1
			 	self.coin_cnt=1


# Класс для расстановки платформ на сцене
class Level(object):
	def __init__(self, player,level):
		# Создаем группу спрайтов (поместим платформы различные сюда)
		self.platform_list = pygame.sprite.Group()
		# Ссылка на основного игрока
		self.player = player
		self.chest=Chest()
		self.level=level
		self.chests=[[700,225],[770,180],[650,260]]
		self.coins=[]
		self.enemy=Enemy()


		self.enemies_pos=[[],[],[300,50]]

		self.coins_pos = [[[175,450],[330,350],[575,250]],
                      [[125,330],[475,300],[600,200]],
                      [[270,150],[330,350],[575,250]]]

		self.coin_cnt =-1

		for coin in range(len(self.coins_pos[self.level])):
			coin_block=Coin()
			self.coins.append(coin_block)

	# Чтобы все рисовалось, то нужно обновлять экран
	# При вызове этого метода обновление будет происходить
	def update(self):
		self.platform_list.update()


	# Метод для рисования объектов на сцене
	def draw(self, screen):
		# Рисуем задний фон
		screen.blit(game_bg, (0, 0))

		# Рисуем все платформы из группы спрайтов
		self.platform_list.draw(screen)
		self.chest.draw(self.player,self.chests[self.level][0],self.chests[self.level][1])

		try:
			for enem in self.enemies_pos:
					self.enemy.draw(self.player,self.enemies_pos[self.level][0],self.enemies_pos[self.level][1])
		except:
			pass

		for coin_id in range(len(self.coins)):
			self.coins[coin_id].draw(self.player,self.coins_pos[self.level][coin_id][0],self.coins_pos[self.level][coin_id][1])


# Класс, что описывает где будут находится все платформы
# на определенном уровне игры
class Level_01(Level):
	def __init__(self, player):
		# Вызываем родительский конструктор
		Level.__init__(self, player,0)

		# Массив с данными про платформы. Данные в таком формате:
		# ширина, высота, x и y позиция
		level = [
			[210, 32, 100, 500],
			[210, 32, 400, 400],
			[210, 32, 650, 300],
		]

		# Перебираем массив и добавляем каждую платформу в группу спрайтов - platform_list
		for platform in level:
			block = Platform(platform[0], platform[1])
			block.rect.x = platform[2]
			block.rect.y = platform[3]
			block.player = self.player
			self.platform_list.add(block)


class Level_02(Level):
	def __init__(self, player):
		# Вызываем родительский конструктор
		Level.__init__(self, player,1)

		# Массив с данными про платформы. Данные в таком формате:
		# ширина, высота, x и y позиция
		level = [
			[150, 32, 50, 230],
			[150, 32, 360, 380],
			[150, 32, 700, 250],
			[150, 32, 230, 500]
		]

		# Перебираем массив и добавляем каждую платформу в группу спрайтов - platform_list
		for platform in level:
			block = Platform(platform[0], platform[1])
			block.rect.x = platform[2]+tick
			block.rect.y = platform[3]
			block.player = self.player
			self.platform_list.add(block)


class Level_03(Level):
	def __init__(self, player):
		# Вызываем родительский конструктор
		Level.__init__(self, player,2)

		# Массив с данными про платформы. Данные в таком формате:
		# ширина, высота, x и y позиция
		level = [
			[150, 32, 75, 350],
			[150, 32, 350, 450],
			[150, 32, 575, 330],
			[150, 32, 270, 220]
		]

		# Перебираем массив и добавляем каждую платформу в группу спрайтов - platform_list
		for platform in level:
			block = Platform(platform[0], platform[1])
			block.rect.x = platform[2]+tick
			block.rect.y = platform[3]
			block.player = self.player
			self.platform_list.add(block)

def game_over(win):
	game_over=True
	while game_over:
		screen.blit(pygame.transform.scale(pygame.image.load('pictures/title2.png'),(500,300)),(200,150))
		if win :draw_text("               You Win",font3,(255,255,0),screen,250,225)
		else:draw_text("              You Lost",font3,(255,255,0),screen,250,225)
		draw_text("You Score is : {} out of 9".format(coin_count),font3,(255,255,0),screen,250,250)
		draw_text("Press ESC Button to return",font3,(255,255,0),screen,250,290)
		draw_text("Main Menu ",font3,(255,255,0),screen,250,310)
		draw_text("Press SPACE Button to ",font3,(255,255,0),screen,250,350)
		draw_text("Play again",font3,(255,255,0),screen,250,370)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				game_over=False
			if event.type==pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					game_over=False
					return True
				elif event.key == pygame.K_ESCAPE:
					game_over=False
					return False
		pygame.display.update()
		pygame.time.Clock().tick(30)

button_tick=0
button_anim=True
tick=0
anim=True
current_level_no = 0
coin_count=0
done = False

def game():
	global current_level_no,coin_count,done,tick,anim
	for play_again in range(1000):
		current_level_no = 0
		coin_count=0
		# Создаем игрока
		player = Player()
		win=False

		# Создаем все уровни

		# Устанавливаем текущий уровень
		hero_pos = [[100,screenheight - 200],[50,200],[150,300]]

		# Цикл будет до тех пор, пока пользователь не нажмет кнопку закрытия

		done = False
		# Используется для управления скоростью обновления экрана
		clock = pygame.time.Clock()
		level_list = [Level_01(player),Level_02(player),Level_03(player)]
		hero_cnt = 0
		# move=  [[[],[],[]],
		# 		[[],[],[],[]],
		# 		[[],[],[]]]
		tick=0
		anim=True

		# Основной цикл программы
		while not done:
			if hero_cnt == current_level_no :
				player.rect.x=hero_pos[current_level_no][0]
				player.rect.y=hero_pos[current_level_no][1]
				hero_cnt += 1
			current_level = level_list[current_level_no]

			active_sprite_list = pygame.sprite.Group()
			player.level = current_level
			active_sprite_list.add(player)
			# Отслеживание действий
			for event in pygame.event.get():
				if event.type == pygame.QUIT: # Если закрыл программу, то останавливаем цикл
					done = True

				# Если нажали на стрелки клавиатуры, то двигаем объект
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_LEFT:
						player.go_left()
					if event.key == pygame.K_RIGHT:
						player.go_right()
					if event.key == pygame.K_UP:
						player.jump()

				if event.type == pygame.KEYUP:
					if event.key == pygame.K_LEFT and player.change_x < 0:
						player.stop()
					if event.key == pygame.K_RIGHT and player.change_x > 0:
						player.stop()

			# Обновляем игрока
			active_sprite_list.update()

			# Обновляем объекты на сцене
			current_level.update()


			if current_level_no==1 or current_level_no==2:
				i=current_level.platform_list.sprites()
				i[1].rect.x +=tick
				if tick == 15:
					anim = False
				elif tick == -15:
					anim = True

				if anim:
					tick +=1
				else:
					tick -=1

			# Если игрок приблизится к правой стороне, то дальше его не двигаем
			if player.rect.right > screenwidth:
				player.rect.right = screenwidth

			# Если игрок приблизится к левой стороне, то дальше его не двигаем
			if player.rect.left < 0:
				player.rect.left = 0

			# Рисуем объекты на окне
			current_level.draw(screen)
			active_sprite_list.draw(screen)
			draw_text("Coins: {}".format(coin_count),font4,(255,255,0),screen,30,30)

			# Устанавливаем количество фреймов
			clock.tick(30)

			# Обновляем экран после рисования объектов
			pygame.display.flip()
			if current_level_no ==len(level_list):
				done=True
				win=True
		play_again=game_over(win)
		if not play_again:
			break

def options():
	global click
	option=True

	while option:
		menu_button_rect = screen.blit(menu_button,(100,350+button_tick))
		screen.blit(bg,(0,0))
		screen.blit(options_titles,(250,200))
		screen.blit(example_buttons,(600,220))

		draw_text("""                  Instructions""",font2,(255,255,255),screen,270,220)
		draw_text("""  Your main goal is to collect coins""",font2,(255,255,255),screen,270,290)
		draw_text("""  and reach the chest""",font2,(255,255,255),screen,270,310)
		draw_text("""  Don't fall to the ground """,font2,(255,255,255),screen,270,360)
		draw_text("""  Use controll buttons (as shown)""",font2,(255,255,255),screen,270,380)
		draw_text("""  to move your Hero""",font2,(255,255,255),screen,270,400)
		draw_text("""               The Game Made by """,font2,(255,255,255),screen,270,445)
		draw_text("""                     19BDTEAM""",font2,(255,255,255),screen,270,465)

		buttons_animation()
		mx,my = pygame.mouse.get_pos()

		if menu_button_rect.collidepoint(mx,my):
			screen.blit(menu_button_2,(98,348+button_tick))
			if click:
				pygame.mixer.music.load('music/click.mp3')
				pygame.mixer.music.load('music/menu_music.mp3')
				pygame.mixer.music.play(1)
				option =False
		else:screen.blit(menu_button,(100,350+button_tick))

		click=False

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					option=False
		pygame.display.update()
		pygame.time.Clock().tick(30)

music=True



def MainMenu():
    global click,bg,music
    pygame.mixer.init()
    pygame.mixer.music.load('music/menu_music.mp3')
    pygame.mixer.music.play(1)
    pygame.mixer.music.set_volume(0.5)


    button_play_rect = screen.blit(button_play,(570,450+button_tick))
    button_options_rect = screen.blit(button_options,(440,450+button_tick))
    music_on_rect=screen.blit(music_on,(290,440+button_tick))
    music_off_rect=screen.blit(music_off,(290,440+button_tick))

    while True:
        button_play_rect = screen.blit(button_play,(570,450+button_tick))
        button_options_rect = screen.blit(button_options,(440,450+button_tick))
        music_on_rect=screen.blit(music_on,(290,440+button_tick))
        buttons_animation()

        screen.blit(bg,(0,0))
        screen.blit(title,(247+button_tick,150))

        draw_text("Forest treasures",font4,(255,255,255),screen,275+button_tick,180)
        mx,my = pygame.mouse.get_pos()

        if button_play_rect.collidepoint(mx,my):
            screen.blit(button_play_2,(570,450+button_tick))
            if click:
                pygame.mixer.music.load('music/click.mp3')
                pygame.mixer.music.play(1)
                if music:
                    pygame.mixer.music.load('music/game_music.mp3')
                    pygame.mixer.music.play(1)
                game()
                if music:
                    pygame.mixer.music.load('music/menu_music.mp3')
                    pygame.mixer.music.play(1)
        else :
            screen.blit(button_play,(570,450+button_tick))
        if button_options_rect.collidepoint(mx,my):
            screen.blit(button_options_2,(440,450+button_tick))
            if click:
                pygame.mixer.music.load('music/click.mp3')
                pygame.mixer.music.play(1)
                options()
        else :
            screen.blit(button_options,(440,450+button_tick))
        if music:
            if music_on_rect.collidepoint(mx,my):
                screen.blit(music_on_2,(290,440+button_tick))
                if click:
                    pygame.mixer.music.set_volume(0)
                    music = False
            else :
                screen.blit(music_on,(290,440+button_tick))
        else:
            if music_off_rect.collidepoint(mx,my):
                screen.blit(music_off_2,(290,440+button_tick))
                if click:
                    pygame.mixer.music.set_volume(1)
                    music = True
            else:
                screen.blit(music_off,(290,440+button_tick))

        click=False


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.update()
        pygame.time.Clock().tick(30)

MainMenu()
