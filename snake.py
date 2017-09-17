# -*- coding: utf-8 -*-
from vector import Vector2
import pygame
from pygame.locals import *
from sys import exit
import random

class Snake(object):
	def __init__(self,image,mode):
		self.image=image
		self.lenth=0
		self.body=[Vector2(30,360)]
		self.direction=Vector2(1,0) #move to right
		self.eat=False
		self.dead=False
		self.lock=False
		self.game_mode=mode
	def move(self,food):
		self.check(food)
		if not self.dead:
			head=self.body[0]
			head+=self.direction*30
			self.body.insert(0,head)
			if not self.eat:
				self.body.pop()
			if self.game_mode:
				if self.body[0].x<0:
					self.body[0].x=1050
				if self.body[0].x>=1080:
					self.body[0].x=0
				if self.body[0].y<0:
					self.body[0].y=690
				if self.body[0].y>=720:
					self.body[0].y=0

	def check(self,food):
		if self.body[0]==food:
			self.eat=True
			self.lenth+=1
		else:
			self.eat=False
		if self.body[0] in self.body[1:]:
			self.dead=True
		if (self.body[0].x==0 and self.direction==(-1,0)) or \
			(self.body[0].x==1050 and self.direction==(1,0)) or\
			(self.body[0].y==0 and self.direction==(0,-1)) or \
			(self.body[0].y==690 and self.direction==(0,1)):
			if not self.game_mode:
				self.dead=True
	def change(self,key):
		new_d=self.direction

		if key==pygame.K_UP and self.direction!=(0,1):
			new_d=Vector2(0,-1)
		if key==pygame.K_DOWN and self.direction!=(0,-1):
			new_d=Vector2(0,1)
		if key==pygame.K_LEFT and self.direction!=(1,0):
			new_d=Vector2(-1,0)
		if key==pygame.K_RIGHT and self.direction!=(-1,0):
			new_d=Vector2(1,0)	
		if new_d!=self.direction and not self.lock:
			self.direction=new_d
			self.lock=True
	def display(self,surface,head):
		for section in self.body:
			surface.blit(self.image,section)
		surface.blit(head,self.body[0])	
class Food(object):
	def __init__(self,image,snake):
		self.location=Vector2(-30,-30)
		self.set_food(snake)
		self.image=image
	def display(self,surface):
		surface.blit(self.image,self.location)
	def check(self,snake):		
		if snake.eat:
			self.set_food(snake)
	def set_food(self,snake):
		self.rand()
		while(self.location in snake.body):
			self.rand()
	def rand(self):
		x=random.randint(0,35)
		y=random.randint(0,23)
		self.location=Vector2(x,y)*30


screen_size=Vector2(1080,720)
pygame.init()
screen=pygame.display.set_mode(screen_size,0,32)
pygame.display.set_caption('snake')



clock=pygame.time.Clock()


font=pygame.font.SysFont("楷体",80)
score_font=pygame.font.SysFont("楷体",40)
gameover=font.render("GAME OVER",True,(0,0,0))
retry_font=pygame.font.SysFont("楷体",40)
retry=retry_font.render("Press 'r' to play again",True,(0,0,0))

black=(0,0,0)
white=(255,255,255)
def new_game():
	global snake,food,game_mode
	load_setting()
	snake=Snake(snake_image,game_mode)
	food=Food(food_image,snake)
	
def menu(mouse,button,names):
	global settings
	num=len(names)	
	for i in range(num):
		if state_stack[-1]=='color':
			text=pygame.image.load(names[i]+'.png').convert()
		else:
			text=font.render(names[i],True,black)
		w,h=text.get_size()
		position=(540-w/2,330-h+(i-num/2+1)*100)
		block=Rect(position,(w,h))
		mouse_in_blocks=in_rect(block,mouse)
		if (state_stack[-1] in settings) and settings[state_stack[-1]]==names[i]:
			display(text,block,mouse_in_blocks,True)
		else:
			display(text,block,mouse_in_blocks)
		if button and mouse_in_blocks:
			click(names[i],(state_stack[-1] in settings))		
			
def display(text,block,mouse_in_block,mark=False):
	pos=(block[0],block[1])
	if mark:
		sub=(block[0]-3,block[1]-3,block[2]+5,block[3]+5)
		pygame.draw.rect(screen,(80,80,80),sub,4)
	if mouse_in_block:
		pygame.draw.rect(screen,black,block,3)
	screen.blit(text,pos)
	
def click(name,set):
	if name=='start':
		new_game()
		state_stack.append('game')	
	if name=='option':
		state_stack.append('option')
	if name=='mode':
		state_stack.append('mode')
	if name=='speed':
		state_stack.append('speed')
	if name=='color':
		state_stack.append('color')

	if set:
		settings[state_stack[-1]]=name
		
def in_game():
	snake.lock=False
	if not game_mode:
		pygame.draw.rect(screen,(0,0,0),(0,0,1080,720),10)
	if not snake.dead:
		snake.move(food.location)
		food.check(snake)
	snake.display(screen,head_image)
	food.display(screen)
	if snake.dead:
		screen.blit(gameover,(400,300))		
		screen.blit(retry,(430,350))
	score=score_font.render("score:"+str(snake.lenth),True,(0,0,0))
	screen.blit(score,(0,0))
		
def in_rect(rect,point):
	if (point[0]<rect[0]+rect[2] and point[0]>rect[0]) and \
		(point[1]<rect[1]+rect[3] and point[1]>rect[1]):
		return True
	else:
		return False

state_stack=[]
state_stack.append('start')
settings={}
settings['mode']='no wall'
settings['speed']='10'
settings['color']='snake'
speed=60
def load_setting():
	global speed,game_mode,snake_image,head_image,food_image
	speed=int(settings['speed'])
	if settings['mode']=='wall':
		game_mode=False
	else:
		game_mode=True
	snake_image=pygame.image.load(settings['color']+'.png').convert()
	head_image=pygame.image.load(settings['color']+'_head.png').convert()
	food_image=pygame.image.load('food.png').convert()
	
def back(mouse,button):
	color=black
	width=2
	if in_rect((960,600,80,50),mouse):
		color=white
		width=0
		if button:
			state_stack.pop()	
	pygame.draw.rect(screen,(0,0,0),(960,600,80,50),width)
	back=score_font.render('back',True,color)
	screen.blit(back,(970,610))
	
def main(mouse,button):
	global state_stack
	state_id=state_stack[-1]
	go_back=False
	if state_id=='start':
		go_back=False
		menu(mouse,button,['start','option'])		
	if state_id=='option':
		go_back=True
		menu(mouse,button,['mode','speed','color'])
	if state_id=='game':
		in_game()
	if state_id=='mode':
		go_back=True
		menu(mouse,button,['wall','no wall'])
	if state_id=='speed':
		go_back=True
		menu(mouse,button,['5','10','15','20','25'])
	if state_id=='color':
		go_back=True
		menu(mouse,button,['red','snake','blue1','grey','yellow'])		
	if go_back:
		back(mouse,button)
		
while True:
	buttons=pygame.mouse.get_pressed()
	left=False
	for event in pygame.event.get():
		if event.type==QUIT:
			exit()			
		if event.type==KEYDOWN:
			if event.key==K_ESCAPE:
				exit()
			if event.key in (K_UP,K_DOWN,K_LEFT,K_RIGHT):
				snake.change(event.key)
			if event.key==K_r:
				if len(state_stack)>1:
					state_stack.pop()
					speed=60
		if event.type==pygame.MOUSEBUTTONUP and buttons[0]:
			left=True
	mouse_position=pygame.mouse.get_pos()
	time=clock.tick(speed)

	screen.fill((255,255,255))
	main(mouse_position,left)
	pygame.display.update()



