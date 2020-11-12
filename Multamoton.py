# 🄯 DAK
import random
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 0)
import pygame
import time
import math
import itertools
import functools
import operator
AUTO_RESTART = False
global birth_count
global death_count
global survival_count
global restart
restart = False
global process_buffer
global future_buffer
global sine_wave_angle
global neighborhood_shapes
neighborhood_maps = []
SCALE = 2 # Number of pixels per cell edge.
FRAME_RATE_TEST = True
ROCKIT_SPEED = 13
PERCENTAGE_OF_TILT_TO_START_WITH = 30
MAXIMUM_TILT = 60
sine_wave_angle = math.asin(PERCENTAGE_OF_TILT_TO_START_WITH / 100)
pygame.init()
display_surface = pygame.display.set_mode()
FWS = (display_surface.get_width(), display_surface.get_height()) # Actual graphic display size FULL_WINDOW_SIZE
WS = (int(FWS[0] // SCALE) | 1, int(FWS[1] // SCALE) | 1) # Actual process window size, including borders. WINDOW_SIZE
print(f"Process area center is at {WS[0] /2}, {WS[1] / 2}")
MWS1 = ((WS[0]+FWS[0])//3,(WS[1]+FWS[1])//3)
MWS2 = ((WS[0]+FWS[0])//2,(WS[1]+FWS[1])//2)
MWS3 = ((WS[0]+FWS[0])*2//3,(WS[1]+FWS[1])*2//3)
HORIZONTAL_BORDER_PERCENTAGE = 10
VERTICAL_BORDER_PERCENTAGE = 55
BS0 = WS[0] * HORIZONTAL_BORDER_PERCENTAGE // 100
BS1 = WS[1] * VERTICAL_BORDER_PERCENTAGE // 100
OBS0 = int(BS0 * (FWS[0] / WS[0]))
OBS1 = int(BS1 * (FWS[1] / WS[1]))
OWS = (FWS[0] + OBS0 + OBS0, FWS[1] + OBS1 + OBS1)
MW = BS0 + WS[0] + BS0
MH = BS1 + WS[1] + BS1
MWS = (MW, MH)
IMBORDER = ((FWS[0]-MWS3[0])//2,(FWS[1]-MWS3[1])//2)
CC_DS = ((BS0, BS1),pygame.Rect(BS0, BS1, WS[0], WS[1]))
TC_DS = ((BS0, 0), pygame.Rect(BS0, MH - BS1 - BS1, WS[0], BS1))
TR_DS = ((MW - BS0, 0), pygame.Rect(BS0, MH - BS1 - BS1, BS0, BS1))
CR_DS = ((MW - BS0, BS1), pygame.Rect(BS0, BS1, BS0, MH - BS1))
BR_DS = ((MW - BS0, MH - BS1), pygame.Rect(BS0, BS1, BS0, BS1))
BC_DS = ((BS0, MH - BS1), pygame.Rect(BS0, BS1, WS[0], BS1))
BL_DS = ((0, MH - BS1), pygame.Rect(MW - BS0 - BS0, BS1, BS0, BS1))
CL_DS = ((0, BS1), pygame.Rect(MW - BS0 - BS0, BS1, BS0, MH - BS1))
TL_DS = ((0, 0), pygame.Rect(MW - BS0 - BS0, MH - BS1 - BS1, BS0, BS1))
print(f"Working internal simulation grid size, WS == {WS}. To exit, press and hold the Escape key while viewing the graphics screen.")
def unique_list(m):
    return list(map(list,set(map(tuple,m))))
class ColorGrid(object):
    def __init__(self):
        self.fill = pygame.Surface.fill
        data = pygame.transform.scale(display_surface, (WS))
        self.Surface = data
        self.__width__ = self.Surface.get_width()
        self.__height__ = self.Surface.get_height()
        self.mirror_width_on_wrap_height = True
        self.mirror_height_on_wrap_width = True
        self.wrapped = [False, False]
        self.wrapped_location = [None,None]
    def __repr__(self):
        return(f'States({self.Surface})')
    def __str__(self):
        return(f'States({self.Surface})')
    def __len__(self):
        return len(self.__width__ * self.__height__)
    def __getitem__(self, index):
        if not hasattr(index,'__len__'):
            index = [index]
        if len(index) == 1:
            index = (index[0] % self.__width__ ,index[0] // self.__width__)
        else:
            index = list(index)
            inboundsx = 0 <= index[0] < self.__width__
            inboundsy = 0 <= index[1] < self.__height__
            if not (inboundsx or inboundsy):
                self.wrapped[0] = index[1] // self.__height__
                self.wrapped[1] = index[0] // self.__width__
                index[0] %= self.__width__
                index[1] %= self.__height__
                if self.wrapped[0]:
                    index[0] = self.__width__ - 1 - index[0]
                if self.wrapped[1]:
                    index[1] = self.__height__ - 1 - index[1]
            elif not inboundsx:
                self.wrapped[1] = index[0] // self.__width__
                index[0] %= self.__width__
                if self.wrapped[1]:
                    index[1] = self.__height__ - 1 - index[1]
            elif not inboundsy:
                self.wrapped[0] = index[1] // self.__height__
                index[1] %= self.__height__
                if self.wrapped[0]:
                    index[0] = self.__width__ - 1 - index[0]
        self.wrapped_location = index
        c = self.Surface.get_at(index)
        return [c[0], c[1], c[2]]
    def __setitem__(self, index, value):
        if not hasattr(index,'__len__'):
            index = [index]
        if len(index) == 1:
            index = (index[0] % self.__width__ ,index[0] // self.__width__)
        else:
            index = list(index)
            inboundsx = 0 <= index[0] < self.__width__
            inboundsy = 0 <= index[1] < self.__height__
            if not (inboundsx or inboundsy):
                self.wrapped[0] = index[1] // self.__height__
                self.wrapped[1] = index[0] // self.__width__
                index[0] %= self.__width__
                index[1] %= self.__height__
                if self.wrapped[0]:
                    index[0] = self.__width__ - 1 - index[0]
                if self.wrapped[1]:
                    index[1] = self.__height__ - 1 - index[1]
            elif not inboundsx:
                self.wrapped[1] = index[0] // self.__width__
                index[0] %= self.__width__
                if self.wrapped[1]:
                    index[1] = self.__height__ - 1 - index[1]
            elif not inboundsy:
                self.wrapped[0] = index[1] // self.__height__
                index[1] %= self.__height__
                if self.wrapped[0]:
                    index[0] = self.__width__ - 1 - index[0]
        self.wrapped_location = index
        try:
            self.Surface.set_at(index, value)
        except:
            raise Exception(f'error refnum 201...    index == {index}    value == {value}')
process_buffer = ColorGrid()
future_buffer = ColorGrid()
def calculate_neighborhood(orientation_fraction = 0, sides_count = 4, radius = any, has_corners = True, allow_zero_angle = False):
    if radius == any:
        radius = int(sides_count / 4) + 1
    hp = math.pi * 2 / sides_count
    if allow_zero_angle:
        q = 0
    else:
        q = math.pi / sides_count
    n = math.pi * 2 * orientation_fraction / sides_count
    neighborhood=[]
    corners = []
    last_side = sides_count - 1
    for this_side in range(sides_count):
        cntr0 = (int(round(math.cos(n+q+last_side*hp)*radius*math.sqrt(2),0)), int(round(math.sin(n+q+last_side*hp)*radius*math.sqrt(2),0)))
        cntr1 = (int(round(math.cos(n+q+this_side*hp)*radius*math.sqrt(2),0)), int(round(math.sin(n+q+this_side*hp)*radius*math.sqrt(2),0)))
        corner = cntr0[0]+cntr1[0], cntr0[1]+cntr1[1]
        neighborhood.append(cntr0)
        corners.append(corner)
        last_side = this_side
    if has_corners:
        neighborhood += corners
    return neighborhood
def calculate_neighborhoods(orientation_count = 3, sides_count = 4, radius = any, has_corners = True):
    hp = math.pi * 2 / sides_count
    q = math.pi / sides_count
    a = math.pi * 2 / (orientation_count * sides_count)
    accepted_radius = False
    passed_in_radius = radius
    if radius == any:
        radius = 1
    while not accepted_radius:
        if radius == passed_in_radius:
            accepted_radius == True
        locations = []
        neighborhoods=[]
        for n in range(orientation_count):
            neighborhood = calculate_neighborhood(n / orientation_count, sides_count, radius, has_corners)
            locations += neighborhood
            neighborhoods.append(neighborhood)
        print(f'in calculate_neighborhoods, (neighborhoods, radius, orientation_count) = {(neighborhoods, radius, orientation_count)}')
        if len(set(locations)) == len(locations):
            accepted_radius = radius
        else:
            radius += 1
    print(f'len(neighborhoods) == ',len(neighborhoods))
    return neighborhoods
def unique(them):
    if len(them) == 0:
        return them
    t = type(them[0])
    tt = type(them)
    them=map(tuple,them)
    print(them)
    them=set(them)
    them=map(set,them)
    them=map(t,them)
    them=tt(them)
    return them
def display_process_buffer():
    global sine_wave_angle
    global process_buffer
    global mirrored_surface
    intermediate_surface1 = pygame.transform.scale(process_buffer.Surface, (MWS1))
    intermediate_surface2 = pygame.transform.scale(process_buffer.Surface, (MWS2))
    mirrored_surface = pygame.transform.scale(process_buffer.Surface, (MWS))
    oversized_surface = pygame.transform.scale(process_buffer.Surface, (OWS))
    mirrored_surface.blit(pygame.transform.scale(process_buffer.Surface, (WS)), (BS0, BS1))
    mirrored_surface.blit(pygame.transform.flip(mirrored_surface, True, True), TL_DS[0], TL_DS[1])
    mirrored_surface.blit(pygame.transform.flip(mirrored_surface, True, False), TC_DS[0], TC_DS[1])
    mirrored_surface.blit(pygame.transform.flip(mirrored_surface, True, True), TR_DS[0], TR_DS[1])
    mirrored_surface.blit(pygame.transform.flip(mirrored_surface, False, True), CR_DS[0], CR_DS[1])
    mirrored_surface.blit(pygame.transform.flip(mirrored_surface, True, True), BR_DS[0], BR_DS[1])
    mirrored_surface.blit(pygame.transform.flip(mirrored_surface, True, False), BC_DS[0], BC_DS[1])
    mirrored_surface.blit(pygame.transform.flip(mirrored_surface, True, True), BL_DS[0], BL_DS[1])
    mirrored_surface.blit(pygame.transform.flip(mirrored_surface, False, True), CL_DS[0], CL_DS[1])
    cms = pygame.transform.smoothscale(mirrored_surface, (MWS))
    cms3 = pygame.transform.smoothscale(mirrored_surface, (MWS[0]*3,MWS[1]*3))
    cms5 = pygame.transform.smoothscale(mirrored_surface, (MWS[0]*5,MWS[1]*5))
    cms3.set_alpha(127)
    cms5.set_alpha(191)
    cms3.blit(pygame.transform.smoothscale(mirrored_surface, (MWS[0]*3,MWS[1]*3)), (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
    mirrored_surface.blit(pygame.transform.smoothscale(cms3, (MWS)), (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
    cms5.blit(pygame.transform.smoothscale(mirrored_surface, (MWS[0]*5,MWS[1]*5)), (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
    mirrored_surface.blit(pygame.transform.smoothscale(cms5, (MWS)), (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
    mirrored_surface.blit(pygame.transform.smoothscale(cms5, (MWS)), (0, 0))
    cms5.blit(pygame.transform.smoothscale(cms3, (MWS[0]*5,MWS[1]*5)), (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
    cms5.blit(pygame.transform.smoothscale(mirrored_surface, (MWS[0]*5,MWS[1]*5)), (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
    mirrored_surface.blit(pygame.transform.smoothscale(cms3, (MWS)), (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
    cms3.blit(pygame.transform.smoothscale(mirrored_surface, (MWS[0]*3,MWS[1]*3)), (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
    mirrored_surface.blit(pygame.transform.smoothscale(cms3, (MWS)), (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
    mirrored_surface.blit(pygame.transform.smoothscale(cms3, (MWS)), (0, 0))
    cms3.blit(pygame.transform.smoothscale(mirrored_surface, (MWS[0]*3,MWS[1]*3)), (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
    mirrored_surface.blit(pygame.transform.smoothscale(cms3, (MWS)), (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
    mirrored_surface.blit(pygame.transform.smoothscale(cms3, (MWS)), (0, 0))
    mirrored_surface.blit(pygame.transform.smoothscale(cms, (MWS)), (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
    mirrored_surface.blit(pygame.transform.smoothscale(cms, (MWS)), (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
    mirrored_surface.blit(pygame.transform.smoothscale(cms, (MWS)), (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
    mirrored_surface.blit(pygame.transform.smoothscale(cms, (MWS)), (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
    cms.set_alpha(32)
    mirrored_surface.blit(pygame.transform.smoothscale(cms, (MWS)), (0, 0))
    cms.set_alpha(255)
    mirrored_surface.blit(pygame.transform.smoothscale(cms, (MWS)), (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
   
    intermediate_surface1.blit(pygame.transform.smoothscale(mirrored_surface, (MWS1)), (0, 0))
    intermediate_surface2.blit(pygame.transform.smoothscale(intermediate_surface1, (MWS2)), (0, 0))
    oversized_surface.blit(pygame.transform.smoothscale(intermediate_surface2, (OWS)), (0, 0))
    oversized_surface.blit(pygame.transform.smoothscale(intermediate_surface1, (OWS)), (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
    screen_angle = MAXIMUM_TILT * math.sin(sine_wave_angle)
    sine_wave_angle -= (math.pi * ROCKIT_SPEED / 10000)
    mp2 = math.pi * 2
    if sine_wave_angle < 0:
        sine_wave_angle -= mp2
    if sine_wave_angle > mp2:
        sine_wave_angle += mp2
    rotated_image = pygame.transform.rotate(oversized_surface, screen_angle)
    rrect = rotated_image.get_rect(center = oversized_surface.get_rect(topleft = (-OBS0,-OBS1)).center)
    display_surface.blit(rotated_image, rrect.topleft)
    pygame.display.update()
    return
def initWorld(): #Initialize and draw some stuff to start with.
    global neighborhood_shapes
    neighborhood_shapes = calculate_neighborhoods(radius = 4, orientation_count = 5, sides_count = 4)
    clusters = []
    clusters.append(((0,1),(0,0),(0,-1))) # blinker
    clusters.append(((0,1),(1,1),(-1,0),(0,0),(0,-1))) # r-pent
    clusters.append(((-3,1),(-2,1),(-2,-1),(0,0),(1,1),(2,1),(3,1))) # acorn
    clusters.append(((-3,2),(-2,3),(-2,2),(-2,1),(0,2),(0,1),(0,0),(2,-1),(2,-2),(4,-2))) # ten cell
    clusters.append(((-1,0),(0,0),(1,0),(0,1),(0,2))) # t-pent
    clusters.append(((-2,0),(-1,0),(0,0),(1,0),(1,-1))) # q-pent
    clusters.append(((-2,0),(-1,0),(0,0),(1,0),(2,0))) # o-pent
    clusters.append(((-1,0),(0,-1),(0,0),(1,0),(0,1))) # x-pent
    number_of_clusters = random.randint(7,11)
    n_shape_number = random.randint(0, len(neighborhood_shapes) - 1)
    for _ in range(number_of_clusters):
        cluster = random.choice(clusters)
        if True:
            cluster = tuple(((xy[1], xy[0]) for xy in cluster))
        if random.choice((True,False)):
            cluster = tuple(((-xy[0], xy[1]) for xy in cluster))
        if random.choice((True,False)):
            cluster = tuple(((xy[0], -xy[1]) for xy in cluster))
        red_threshold = random.randint(64,192)
        green_threshold = random.randint(64,192)
        blue_threshold = random.randint(64,192)
        color_bias = random.choice(range(7))
        color_choices = []
        while len(color_choices) < random.randint(1,3):
            if color_bias == 5:
                rc = [random.randint(red_threshold,255), random.randint(0,green_threshold), random.randint(blue_threshold,255)]
            elif color_bias == 4:
                rc = [random.randint(0,255), random.randint(0,255), random.randint(blue_threshold,255)]
            elif color_bias == 3:
                rc = [random.randint(0,red_threshold), random.randint(green_threshold,255), random.randint(blue_threshold,255)]
            elif color_bias == 2:
                rc = [random.randint(0,255), random.randint(green_threshold,255), random.randint(0,255)]
            elif color_bias == 1:
                rc = [random.randint(red_threshold,255), random.randint(green_threshold,255), random.randint(0,blue_threshold)]
            elif color_bias == 0:
                rc = [random.randint(red_threshold,255), random.randint(0,255), random.randint(0,255)]
            else:
                rc = [random.randint(0,255), random.randint(0,255), random.randint(0,255)]
            color_choices.append(rc)
        print(cluster)
        rns = neighborhood_shapes[n_shape_number]
        print(f'neighborhood shape number {n_shape_number} == {rns}')
        n_shape_number += 1
        n_shape_number %= len(neighborhood_shapes)
        destx = random.randint(WS[0]//3,WS[0]*2//3)
        desty = random.randint(WS[1]//3,WS[1]*2//3)
        for xy in cluster:
            print(xy)
            process_buffer.Surface.set_at((xy[0]*rns[0][0]+xy[1]*rns[1][0]+destx, xy[1]*rns[1][1]+xy[0]*rns[0][1]+desty),random.choice(color_choices))
    display_process_buffer()
def mutateColor(c):
    c=list(c)
    if c[0]==c[1]==c[2]:
        return c
    if type(c) != list:
        c = list(c)
    sm = sum(c)
    ad1 = 4
    ad2 = 6
    sb1 = 4
    sb2 = 6
    if sm > 640:
        ad1=0
        ad2=0
    elif sm < 128:
        sb1=0
        sb2=0
    if c[0] > c[1] and c[0] > c[2]:
        c[1] -= ad2 * (1-(c[0]&1)*2)
        c[2] += ad1 * (1-(c[0]&1)*2)
    elif c[1] > c[0] and c[1] > c[2]:
        c[2] -= ad2 * (1-(c[1]&1)*2)
        c[0] += ad1 * (1-(c[1]&1)*2)
    elif c[2] > c[1] and c[2] > c[0]:
        c[0] -= ad2 * (1-(c[2]&1)*2)
        c[1] += ad1 * (1-(c[2]&1)*2)
    elif c[0] < c[1] and c[0] < c[2]:
        c[1] += ad2 * (1-(c[0]&1)*2)
        c[2] -= ad1 * (1-(c[0]&1)*2)
    elif c[1] < c[0] and c[1] < c[2]:
        c[2] += ad2 * (1-(c[1]&1)*2)
        c[0] -= ad1 * (1-(c[1]&1)*2)
    elif c[2] < c[1] and c[2] < c[0]:
        c[0] += ad2 * (1-(c[1]&1)*2)
        c[1] -= ad1 * (1-(c[1]&1)*2)
    return [min(max(c[0],0),255) & ~1 | (c[0]&1), min(max(c[1],0),255) & ~1 | (c[1]&1), min(max(c[2],0),255) & ~1 | (c[2]&1)]
def baby_maker(cell_color, potential_mates):
    if len(potential_mates) == 0:
        return cell_color
    potential_mates = [m for m in list(itertools.chain(*potential_mates)) if m != [0,0,0]]
    if [0,0,0] in potential_mates:
        potential_mates.remove([0,0,0])
    if len(potential_mates) == 0:
        return cell_color
    rare_potential_mates = []
    siz = 0
    while rare_potential_mates == []:
        siz += 1
        rare_potential_mates = unique_list(m for m in potential_mates if potential_mates.count(m) == siz)
    if len(rare_potential_mates) == 1:
        mate = rare_potential_mates[0]
    else:
        r = functools.reduce(operator.xor,(p[0] for p in rare_potential_mates))
        g = functools.reduce(operator.xor,(p[1] for p in rare_potential_mates))
        b = functools.reduce(operator.xor,(p[2] for p in rare_potential_mates))
        if (r, g, b) == (0, 0, 0):
            r = max(p[0] for p in rare_potential_mates)
            g = max(p[1] for p in rare_potential_mates)
            b = max(p[2] for p in rare_potential_mates)
        mate = [r,g,b]
    return mate
    
    
def playGame():
    global birth_count
    global death_count
    global survival_count
    global generationNumber
    global neighborhood_shapes
    global __playGame_initialized__
    if generationNumber > 0:
        if FRAME_RATE_TEST and generationNumber & 5 == 5:
            frtr = f'{round(generationNumber/(time.time()-FRAME_RATE_TEST) * 60, 3)} generations per minute.'
        else:
            frtr = f'This cycle, {birth_count} were born, {death_count} died, and {survival_count} survived.'
        print(f"Generation number {generationNumber}.    {frtr}")
    else:
        print('Initializing...')
    generationNumber += 1
    birth_count = 0
    death_count = 0
    survival_count = 0
    for cell_location in [(x, y) for x in range(0, WS[0]) for y in range(0, WS[1])]:
        x,y = cell_location
        neigh_shapes = tuple(tuple(tuple((x+dst[0], y+dst[1])) for dst in nbh) for nbh in neighborhood_shapes)
        cell_color = process_buffer[cell_location]
        x, y = cell_location
        sh_neighborhoods =[[process_buffer[address] for address in neigh_shapes[i]] for i in range(len(neigh_shapes))] 
        neighcounts = [len(sh_neighborhoods[i]) - sh_neighborhoods[i].count([0,0,0]) for i in range(len(sh_neighborhoods))]
        if neighcounts.count(0) < len(neighcounts) - 2:
            effective_neighbor_count == 0
        else:
            effective_neighbor_count = max(neighcounts)
        if effective_neighbor_count == 2:
            if cell_color == [0,0,0]:
                new_cell_color = [0,0,0]
            else:
                survival_count += 1
                new_cell_color = mutateColor(cell_color)
        elif effective_neighbor_count == 3:
            if cell_color == [0,0,0]:
                birth_count += 1
                new_cell_color = baby_maker(cell_color, sh_neighborhoods)
            else:
                survival_count += 1
                new_cell_color = mutateColor(cell_color)
        else: # death
            new_cell_color = [0,0,0]
            if cell_color != [0,0,0]:
                death_count += 1
        future_buffer[cell_location] = new_cell_color
    process_buffer.Surface.blit(future_buffer.Surface, (0,0))
    display_process_buffer()
running = True
while running:
    if FRAME_RATE_TEST:
        FRAME_RATE_TEST = time.time()
    starttime = time.time()
    generationNumber = 0
    restart_countdown = 4
    if not (pygame.event.peek(pygame.MOUSEBUTTONDOWN)):
        kp = pygame.key.get_pressed()
        if kp[pygame.K_ESCAPE]:
            exit()
        pygame.event.get()
        initWorld()
        while not pygame.event.peek(pygame.MOUSEBUTTONDOWN) and not restart:
            playGame()
            if AUTO_RESTART:
                if AUTO_RESTART >= 60:
                    time_between_restarts = AUTO_RESTART
                if starttime + 900 <= time.time():
                    restart_countdown -= 1
                if restart_countdown <= 0:
                    restart = True
                    starttime = time.time()
        pygame.event.get()
        restart = False
        restart_countdown = 4
        starttime = time.time()
                
'' # 🄯 DAK
