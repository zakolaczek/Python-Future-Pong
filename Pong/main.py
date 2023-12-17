import pygame
import os
import random
pygame.font.init()

WHITE = (255,255,255)
BLACK = (0,0,0)
WIDTH, HEIGHT = 1920, 1080
PALLET_WIDTH, PALLET_HEIGHT = 50, 200
BALL_CORDS = 50
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
PALLET_VEL = 15
BALL_VEL = 15
pygame.display.set_caption("Future Pong")

BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("Files", "background.png")), (WIDTH, HEIGHT))

LEFT_PALLET = pygame.transform.scale(
	pygame.image.load(os.path.join("Files", "pallet1.png")), (PALLET_WIDTH, PALLET_HEIGHT))

RIGHT_PALLET= pygame.transform.rotate(
	pygame.transform.scale(pygame.image.load(os.path.join("Files", "pallet2.png")), (PALLET_WIDTH, PALLET_HEIGHT)), 180)

BALL = pygame.transform.scale(pygame.image.load(os.path.join("Files", "ball.png")), (BALL_CORDS, BALL_CORDS))

FPS = 60

IS_TOUCHING_LEFT = pygame.USEREVENT + 1
IS_TOUCHING_RIGHT = pygame.USEREVENT + 2
IS_TOUCHING_LEFT_BORDER = pygame.USEREVENT + 3
IS_TOUCHING_RIGHT_BORDER = pygame.USEREVENT + 4
IS_TOUCHING_UP_LEFT = pygame.USEREVENT + 5
IS_TOUCHING_UP_RIGHT = pygame.USEREVENT + 6
IS_TOUCHING_DOWN_LEFT = pygame.USEREVENT + 7
IS_TOUCHING_DOWN_RIGHT = pygame.USEREVENT + 8

SCORE_FONT = pygame.font.SysFont("caladea", 100)
WINNER_FONT = pygame.font.SysFont("caladea", 100)

def show_winner(text, color):
	final_text = WINNER_FONT.render(text, 1, color)
	WINDOW.blit(final_text, (WIDTH / 2 - final_text.get_width() / 2, HEIGHT / 2 - final_text.get_height() / 2 + 100))
	pygame.display.update()
	pygame.time.delay(5000);

def pallets_movement(left, right, keys_pressed):
	if keys_pressed[pygame.K_w] and left.y - PALLET_VEL > 0: #LEFT UP
		left.y -= PALLET_VEL
	if keys_pressed[pygame.K_s] and left.y + PALLET_VEL < HEIGHT - left.height: #LEFT DOWN
		left.y += PALLET_VEL
	if keys_pressed[pygame.K_UP] and right.y - PALLET_VEL > 0: #RIGHT UP
		right.y -= PALLET_VEL
	if keys_pressed[pygame.K_DOWN] and right.y + PALLET_VEL < HEIGHT - right.height: #RIGHT DOWN
		right.y += PALLET_VEL

def draw_screen(left, right, balls, left_score, right_score):
	WINDOW.blit(BACKGROUND, (0,0))
	WINDOW.blit(LEFT_PALLET, (left.x, left.y))
	WINDOW.blit(RIGHT_PALLET, (right.x, right.y))

	left_text = SCORE_FONT.render(str(left_score), 1, BLACK)
	right_text = SCORE_FONT.render(str(right_score), 1, BLACK)

	WINDOW.blit(left_text, (WIDTH // 2 - left_text.get_width(), 10))
	WINDOW.blit(right_text, (WIDTH // 2 + right_text.get_width(), 10))
	WINDOW.blit(BALL, (balls.x, balls.y))
	pygame.display.update()

def generate_site():
	return random.randint(1,2)

def generate_add_minus():
	return random.randint(1,2)

def generate_ball_vel():
	return random.randint(10,15)

def ball_movement(balls, site, left, right, add_minus, rand_ball_vel):
	if site == 0:
		balls.x = WIDTH // 2 - BALL_CORDS // 2
		balls.y = HEIGHT // 2 - BALL_CORDS // 2
	if site == 1 and not right.colliderect(balls) and not balls.x > WIDTH - BALL_CORDS: #COMING RIGHT
		balls.x += BALL_VEL
		if add_minus == 1: #COMING DOWN
			balls.y += rand_ball_vel
			if balls.y > HEIGHT - BALL_CORDS:
				pygame.event.post(pygame.event.Event(IS_TOUCHING_DOWN_RIGHT))
		elif add_minus == 2: #COMING UP
			balls.y -= rand_ball_vel
			if balls.y < 0 + BALL_CORDS:
				pygame.event.post(pygame.event.Event(IS_TOUCHING_UP_RIGHT))		
		if right.colliderect(balls):
			pygame.event.post(pygame.event.Event(IS_TOUCHING_RIGHT))
		elif balls.x > WIDTH - BALL_CORDS:
			pygame.event.post(pygame.event.Event(IS_TOUCHING_RIGHT_BORDER))
	if site == 2 and not left.colliderect(balls) and not balls.x < 0: #COMING LEFT
		balls.x -= BALL_VEL
		if add_minus == 1: #COMING DOWN
			balls.y += rand_ball_vel
			if balls.y > HEIGHT - BALL_CORDS:
				pygame.event.post(pygame.event.Event(IS_TOUCHING_DOWN_LEFT))
		elif add_minus == 2: #COMING UP
			balls.y -= rand_ball_vel
			if balls.y < 0 + BALL_CORDS // 2:
				pygame.event.post(pygame.event.Event(IS_TOUCHING_UP_LEFT))	
		if left.colliderect(balls):
			pygame.event.post(pygame.event.Event(IS_TOUCHING_LEFT))
		elif balls.x < 0:
			pygame.event.post(pygame.event.Event(IS_TOUCHING_LEFT_BORDER))

def main():
	site = generate_site()
	add_minus = generate_add_minus()
	rand_ball_vel = generate_ball_vel()
	clock = pygame.time.Clock()
	winner_text = ""

	left_score = 0
	right_score = 0 

	left = pygame.Rect(10, HEIGHT // 2 - PALLET_HEIGHT // 2, PALLET_WIDTH, PALLET_HEIGHT)
	right = pygame.Rect(WIDTH - PALLET_WIDTH - 10, HEIGHT // 2 - PALLET_HEIGHT // 2, PALLET_WIDTH, PALLET_HEIGHT)
	balls = pygame.Rect(WIDTH // 2 - BALL_CORDS // 2, HEIGHT // 2 - BALL_CORDS // 2, BALL_CORDS, BALL_CORDS)
	run = True
	while run:
		clock.tick(FPS)

		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					run = False
					pygame.quit()

			if event.type == IS_TOUCHING_RIGHT:
				site = 2
				rand_ball_vel = generate_ball_vel()
				add_minus = generate_add_minus()
			if event.type == IS_TOUCHING_LEFT:
				site = 1
				rand_ball_vel = generate_ball_vel()
				add_minus = generate_add_minus()
			if event.type == IS_TOUCHING_LEFT_BORDER:
				right_score += 1
				balls.x = WIDTH // 2 - BALL_CORDS // 2
				balls.y = HEIGHT // 2 - BALL_CORDS // 2
				rand_ball_vel = generate_ball_vel()
				add_minus = generate_add_minus()
				draw_screen(left, right, balls, left_score, right_score)
				pygame.time.delay(1000)
				site = generate_site()

			if event.type == IS_TOUCHING_RIGHT_BORDER:
				left_score += 1
				balls.x = WIDTH // 2 - BALL_CORDS // 2
				balls.y = HEIGHT // 2 - BALL_CORDS // 2
				rand_ball_vel = generate_ball_vel()
				add_minus = generate_add_minus()
				draw_screen(left, right, balls, left_score, right_score)
				pygame.time.delay(1000)
				site = generate_site()
			if event.type == IS_TOUCHING_UP_LEFT or event.type == IS_TOUCHING_UP_RIGHT:
				rand_ball_vel = generate_ball_vel()
				add_minus = 1
			if event.type == IS_TOUCHING_DOWN_LEFT or event.type == IS_TOUCHING_DOWN_RIGHT:
				rand_ball_vel = generate_ball_vel()
				add_minus = 2

		if left_score >= 10:
			winner_text = "Player on a left won!"
		if right_score >= 10:
			winner_text = "Player on a right won!"
		if winner_text != "":
			show_winner(winner_text, WHITE)
			break

		keys_pressed = pygame.key.get_pressed()
		ball_movement(balls, site, left, right, add_minus, rand_ball_vel)
		pallets_movement(left, right, keys_pressed)
		draw_screen(left, right, balls, left_score, right_score)

if __name__ == '__main__':
	main()