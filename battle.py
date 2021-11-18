import pygame
import random
import button

pygame.init()

clock = pygame.time.Clock()
fps = 60

#variables
current_fighter = 1
total_fighters = 3
action_cooldown = 0
action_wait_time = 90
attack = False
potion = False
potion_effect = 300
clicked = False
game_over = 0

#game window
bottom_panel = 150
screen_width = 800
screen_height = 400 + bottom_panel
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('𝔊𝔞𝔯𝔢𝔫 𝔳𝔰 𝔗𝔥𝔲𝔤𝔰')


#fonts and colors
font = pygame.font.SysFont('garamond', 22)
red = (140, 5, 5)
green = (31, 121, 5)
aqua = (0, 0, 50)
yellow = (255, 255, 0)

#images
restart_img = pygame.image.load('img/Icons/restart.png').convert_alpha()
background_img = pygame.image.load('img/Background/background.png').convert_alpha()
panel_img = pygame.image.load('img/Icons/panel.png').convert_alpha()
potion_img = pygame.image.load('img/Icons/potion.png').convert_alpha()
defeat_img = pygame.image.load('img/Icons/defeat.png').convert_alpha()
sword_img = pygame.image.load('img/Icons/sword.png').convert_alpha()
victory_img = pygame.image.load('img/Icons/victory.png').convert_alpha()


#draw text
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

#draw background onto screen
def draw_bg():
	screen.blit(background_img, (0, 0))

#draw panel onto screen
def draw_panel():
	screen.blit(panel_img, (0, screen_height - bottom_panel))
	draw_text(f'{knight.name} HP: {knight.hp}', font, aqua, 100, screen_height - bottom_panel + 10)
	
	for count, i in enumerate(bandit_list):
		#display health and name onto panel
		draw_text(f'{i.name} HP: {i.hp}', font, aqua, 550, (screen_height - bottom_panel + 10) + count * 60)

#fighter class
class Fighter():
	def __init__(self, x, y, name, max_hp, strength, potions):
		self.name = name
		self.max_hp = max_hp
		self.hp = max_hp
		self.strength = strength
		self.start_potions = potions
		self.potions = potions
		self.alive = True
		self.animation_list = []
		self.frame_index = 0
		self.action = 0#0:idle, 1:attack, 2:hurt, 3:dead
		self.update_time = pygame.time.get_ticks()
		
		#load idle images
		temp_list = []
		for i in range(8):
			img = pygame.image.load(f'img/{self.name}/Idle/{i}.png')
			img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
			temp_list.append(img)
		self.animation_list.append(temp_list)
		
		#load attack images
		temp_list = []
		for i in range(8):
			img = pygame.image.load(f'img/{self.name}/Attack/{i}.png')
			img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
			temp_list.append(img)
		self.animation_list.append(temp_list)
		
		#load hurt images
		temp_list = []
		for i in range(3):
			img = pygame.image.load(f'img/{self.name}/Hurt/{i}.png')
			img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
			temp_list.append(img)
		self.animation_list.append(temp_list)
		
		#load death images
		temp_list = []
		for i in range(10):
			img = pygame.image.load(f'img/{self.name}/Death/{i}.png')
			img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
			temp_list.append(img)

		self.animation_list.append(temp_list)
		self.image = self.animation_list[self.action][self.frame_index]
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)


	def update(self):
		animation_cooldown = 100
		#change motion based on the current action of character
		self.image = self.animation_list[self.action][self.frame_index]
		
		#check time since last update so timer resets
		if pygame.time.get_ticks() - self.update_time > animation_cooldown:
			self.update_time = pygame.time.get_ticks()
			self.frame_index += 1

		#reset timer if it has reached len - 1
		if self.frame_index >= len(self.animation_list[self.action]):
			if self.action == 3:
				self.frame_index = len(self.animation_list[self.action]) - 1
			else:
				self.idle()


	#function for idle motion
	def idle(self):
		self.action = 0
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	#function for attacking motion
	def attack(self, target):
		rand = random.randint(-100, 100)
		damage = self.strength + rand
		target.hp -= damage
		target.hurt()

		if target.hp < 1:
			target.hp = 0
			target.alive = False
			target.death()
		damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), red)
		damage_text_group.add(damage_text)


		self.action = 1
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	#function for hurt motion
	def hurt(self):
		self.action = 2
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	#function for death motion
	def death(self):
		self.action = 3
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	#function for once game is completed and want to play again
	def reset (self):
		self.alive = True
		self.potions = self.start_potions
		self.hp = self.max_hp
		self.frame_index = 0
		self.action = 0
		self.update_time = pygame.time.get_ticks()


	def draw(self):
		screen.blit(self.image, self.rect)



class HealthBar():
	def __init__(self, x, y, hp, max_hp):
		self.x = x
		self.y = y
		self.hp = hp
		self.max_hp = max_hp


	def draw(self, hp):
		#update with new health
		self.hp = hp
		#calculate health ratio
		ratio = self.hp / self.max_hp
		pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
		pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))



class DamageText(pygame.sprite.Sprite):
	def __init__(self, x, y, damage, colour):
		pygame.sprite.Sprite.__init__(self)
		self.image = font.render(damage, True, colour)
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.counter = 0


	def update(self):
		#move damage text up
		self.rect.y -= 1
		#delete the text after a few seconds
		self.counter += 1
		if self.counter > 30:
			self.kill()



damage_text_group = pygame.sprite.Group()


knight = Fighter(200, 260, 'Garen', 1000, 350, 3)
bandit1 = Fighter(550, 270, 'Thug', 1000, 100, 1)
bandit2 = Fighter(700, 270, 'Thug', 1000, 110, 1)

bandit_list = []
bandit_list.append(bandit1)
bandit_list.append(bandit2)

knight_health_bar = HealthBar(100, screen_height - bottom_panel + 40, knight.hp, knight.max_hp)
bandit1_health_bar = HealthBar(550, screen_height - bottom_panel + 40, bandit1.hp, bandit1.max_hp)
bandit2_health_bar = HealthBar(550, screen_height - bottom_panel + 100, bandit2.hp, bandit2.max_hp)

#buttons
potion_button = button.Button(screen, 100, screen_height - bottom_panel + 70, potion_img, 64, 64)
restart_button = button.Button(screen, 330, 120, restart_img, 120, 30)

run = True
while run:

	clock.tick(fps)

	#draw background and panel
	draw_bg()
	draw_panel()

	#draw characters health bars
	knight_health_bar.draw(knight.hp)
	bandit1_health_bar.draw(bandit1.hp)
	bandit2_health_bar.draw(bandit2.hp)

	#draw characters
	knight.update()
	knight.draw()
	for bandit in bandit_list:
		bandit.update()
		bandit.draw()

	#draw damage on panel
	damage_text_group.update()
	damage_text_group.draw(screen)

	attack = False
	potion = False
	target = None
	pygame.mouse.set_visible(True)
	pos = pygame.mouse.get_pos()
	for count, bandit in enumerate(bandit_list):
		if bandit.rect.collidepoint(pos):
			pygame.mouse.set_visible(False)
			#show sword as the cursor for the user
			screen.blit(sword_img, pos)
			if clicked == True and bandit.alive == True:
				attack = True
				target = bandit_list[count]
	if potion_button.draw():
		potion = True
	#draw num of magical random pots remaining
	draw_text(str(knight.potions), font, red, 150, screen_height - bottom_panel + 70)


	if game_over == 0:
		if knight.alive == True:
			if current_fighter == 1:
				action_cooldown += 1
				if action_cooldown >= action_wait_time:
					if attack == True and target != None:
						knight.attack(target)
						current_fighter += 1
						action_cooldown = 0
					#If user clicks on potion
					if potion == True:
						if knight.potions > 0:
							rand = random.randint(1, 4)
							if rand == 4:
								dmg_boost = 1000
								knight.strength += dmg_boost
								damage_text = DamageText(knight.rect.centerx, knight.rect.y, str(dmg_boost), yellow)
								damage_text_group.add(damage_text)
								knight.potions -= 1
								current_fighter += 1
								action_cooldown = 0
							else:
								if knight.max_hp - knight.hp > potion_effect:
									heal_amount = potion_effect
								else:
									heal_amount = knight.max_hp - knight.hp
								knight.hp += heal_amount
								knight.potions -= 1
								damage_text = DamageText(knight.rect.centerx, knight.rect.y, str(heal_amount), green)
								damage_text_group.add(damage_text)
								current_fighter += 1
								action_cooldown = 0
		else:
			game_over = -1


		#enemy's turn
		for count, bandit in enumerate(bandit_list):
			if current_fighter == 2 + count:
				if bandit.alive == True:
					action_cooldown += 1
					if action_cooldown >= action_wait_time:
						#check to see if enemy is below half health to excersise potion
						if (bandit.hp / bandit.max_hp) < 0.5 and bandit.potions > 0:
							if bandit.max_hp - bandit.hp > potion_effect:
								heal_amount = potion_effect
							else:
								heal_amount = bandit.max_hp - bandit.hp
							bandit.hp += heal_amount
							bandit.potions -= 1
							damage_text = DamageText(bandit.rect.centerx, bandit.rect.y, str(heal_amount), green)
							damage_text_group.add(damage_text)
							current_fighter += 1
							action_cooldown = 0
						#if healing not an option then attack
						else:
							bandit.attack(knight)
							current_fighter += 1
							action_cooldown = 0
				else:
					current_fighter += 1

		#if all characters have had a turn then reset
		if current_fighter > total_fighters:
			current_fighter = 1


	dead_bandits = 0
	for bandit in bandit_list:
		if bandit.alive == False:
			dead_bandits += 1
	if dead_bandits == 2:
		game_over = 1


	#check if game is over, if so determine victory or defeat
	if game_over != 0:
		knight.strength = 350
		if game_over == 1:
			screen.blit(victory_img, (250, 50))
		if game_over == -1:
			screen.blit(defeat_img, (290, 50))
		if restart_button.draw():
			knight.reset()
			for bandit in bandit_list:
				bandit.reset()
			current_fighter = 1
			action_cooldown
			game_over = 0



	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			clicked = True
		else:
			clicked = False

	pygame.display.update()

pygame.quit()