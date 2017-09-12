# -*- coding: utf-8 -*-
from vector import Vector2
import pygame
from pygame.locals import *
from sys import exit
import random


class Snake(object):
	def __init__(self,image):
		self.image=image
		self.lenth=0
		self.body=[Vector2(30,360)]
		self.direction=Vector2(1,0) #move to right
		self.eat=False
		self.dead=False
		self.lock=False
	def move(self,food):
		self.check(food)
		head=self.body[0]
		head+=self.direction*30
		self.body.insert(0,head)
		if not self.eat:
			self.body.pop()
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
snake_image=pygame.image.load('snake.png').convert()
food_image=pygame.image.load('food.png').convert()
head_image=pygame.image.load('head.png').convert()
clock=pygame.time.Clock()


font=pygame.font.SysFont("楷体",80)
score_font=pygame.font.SysFont("楷体",40)
gameover=font.render("GAME OVER",True,(0,0,0))
retry_font=pygame.font.SysFont("楷体",40)
retry=retry_font.render("Press 'r' to play again",True,(0,0,0))
def main():
	global snake,food
	snake=Snake(snake_image)
	food=Food(food_image,snake)
main()
while True:
	snake.lock=False
	for event in pygame.event.get():
		if event.type==QUIT:
			exit()			
		if event.type==KEYDOWN:
			if event.key==K_ESCAPE:
				exit()
			if event.key in (K_UP,K_DOWN,K_LEFT,K_RIGHT):
				snake.change(event.key)
			if event.key==K_r:
				main()

	time=clock.tick(20)
	screen.fill((255,255,255))

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

	pygame.display.update()



