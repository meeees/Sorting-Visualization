import os, sys, time
import pygame
import random
import traceback
import sorting_algos
import colorsys

class SortingVis :

	WIDTH = 640
	HEIGHT = 480
	global time_delay
	time_delay = 0.01
	global keys_to_funcs

	BLOCK_SIZE = 20 #20 seems to work well for the visualization steps I want to show

	def __init__(self, width = WIDTH, height = HEIGHT) :
		pygame.init()
		print '------------------------ Sorting Visualization -------------------------'
		print '| When the current sort is finished, press a key to start the next one |'
		print '|       B: Bubble, I: Insertion, S: Selection, Q: Quick, M: Merge      |'
		print '------------------------------------------------------------------------'
		print 'Starting Bubble Sort...'
		self.width = width
		self.height = height
		self.screen = pygame.display.set_mode((self.width, self.height))
		self.setup_keys()
		self.ele_list = []
		self.ele_sprite_list = pygame.sprite.Group()
		self.gen_random_elements(self.ele_list, self.ele_sprite_list)

	def main_loop(self) :
		self.background = pygame.Surface(self.screen.get_size())
		self.background = self.background.convert()
		self.background.fill((0,0,0))
		sorting = True
		start_delay = False
		start_time = time.time()
		try :
			sort_iter = iter(sorting_algos.bubble_sort(self.ele_list))

			while True :
				for event in pygame.event.get() :
					if event.type == pygame.QUIT :
						pygame.quit()
						sys.exit()
					if event.type == pygame.KEYDOWN :
						if not sorting :
							sort_iter = self.parse_keys(event.key)
							if sort_iter != None :
								sorting = True

				self.screen.blit(self.background, (0,0))
				self.ele_sprite_list.draw(self.screen)
				if(sorting) :
					i = sort_iter.next()
					if(i == -1) :
						#print 'Done Sorting' #, took', time.time() - start_time, 'seconds.'
						if(sorting_algos.check_sorted(self.ele_list)) :
							print 'Done sorting, sorted correctly'
						else :
							print 'Done sorting, sorted incorrectly - THIS IS A BUG'
						sorting = False
					for x in range(len(self.ele_list)) :
						self.ele_list[x].update(x)
				pygame.display.flip()
				time.sleep(time_delay)
				if(start_delay) :
					time.sleep(3)
					start_delay = False
					start_time = time.time()

		except Exception as e:
			print 'exited due to ', sys.exc_info()[0]
			print traceback.format_exc()
			pygame.quit()
			sys.exit()

	def parse_keys(self, key) :
		if key in keys_to_funcs.keys() :
			global time_delay
			time_delay = keys_to_funcs[key][2]
			print 'Starting', keys_to_funcs[key][1], 'Sort...'
			self.gen_random_elements(self.ele_list, self.ele_sprite_list)
			return iter(keys_to_funcs[key][0](self.ele_list))
		return None

	def gen_random_elements(self, ele_list, ele_sprite_list, count = (WIDTH/BLOCK_SIZE) * (HEIGHT/BLOCK_SIZE)) :
		del ele_list[:]
		ele_sprite_list.empty()
		for x in range(count) :
			rand = random.randint(0, 2)
			if(rand == 0) :
				c = pygame.Color(random.randint(0, 255), 0, 0, 255)
			elif (rand == 1) :
				c = pygame.Color(0, random.randint(0, 255), 0, 255)
			elif (rand == 2) :
				c = pygame.Color(0, 0, random.randint(0, 255), 255)
			else :
				r = random.randint(0, 255)
				c = pygame.Color(r, r, r, 255)
			e = Element(c, x)
			ele_list.append(e)
			ele_sprite_list.add(e)

	#setup keys to map to a sort and a decent time delay to watch the sort at
	def setup_keys(self) :
		global keys_to_funcs
		keys_to_funcs = {}
		keys_to_funcs[pygame.K_b] = (sorting_algos.bubble_sort, 'Bubble', 0.01)
		keys_to_funcs[pygame.K_s] = (sorting_algos.selection_sort, 'Selection', 0.01)
		keys_to_funcs[pygame.K_i] = (sorting_algos.insertion_sort, 'Insertion', 0.01)
		keys_to_funcs[pygame.K_q] = (sorting_algos.quick_sort, 'Quick', 0.00)
		keys_to_funcs[pygame.K_m] = (sorting_algos.merge_sort, 'Merge', 0.00)



class Element(pygame.sprite.Sprite) :

	def __init__(self, color, pos) :
		pygame.sprite.Sprite.__init__(self)
		self.global_pos = pos
		self.image = pygame.Surface([SortingVis.BLOCK_SIZE,SortingVis.BLOCK_SIZE])
		self.image.fill(color)
		self.color = color
		self.rgb = (color.r << 16) | (color.g << 8) | color.b
		#self.rgb = colorsys.rgb_to_hls(color.r, color.g, color.b)[1] #this has issues with two 0-values it seems
		self.rect = self.image.get_rect()
		self.calc_pos(pos)

	def calc_pos(self, pos) :
		x = pos % (SortingVis.WIDTH / SortingVis.BLOCK_SIZE)
		y = pos / (SortingVis.WIDTH / SortingVis.BLOCK_SIZE)
		self.rect.x = x * SortingVis.BLOCK_SIZE
		self.rect.y = y * SortingVis.BLOCK_SIZE

	def update(self, pos) :
		self.calc_pos(pos)

	#I'm really lazy so all of my comparisons have had to be >
	def __gt__(self, other) :
		return self.rgb > other.rgb

if __name__ == '__main__' :
	SimWindow = SortingVis()
	SimWindow.main_loop()