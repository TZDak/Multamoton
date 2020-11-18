# 🄯 DAK
import random
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 0)
import pygame
import time
import itertools
import functools
import operator
import collections
import mpmath
import colorsys
import decimal
import PySimpleGUI as sg
AUTO_RESTART_TIMER = False
RESTART_ON_STAGNATION = True
global life_checksum
global birth_count
global death_count
global survival_count
global restart
restart = False
global process_buffer
global future_buffer
global sine_wave_angle
global neighborhood_shapes
global all_neighborhood_locations
global halo
d_CHOSEN_MULTIVERSE = CHOSEN_MULTIVERSE = ''
d_SCALE = SCALE = 4 # Number of pixels per cell edge.
d_NUMBER_OF_UNIVERSES = NUMBER_OF_UNIVERSES = 5
d_NUMBER_OF_START_THINGS = NUMBER_OF_START_THINGS = 20
d_CELL_RADIUS_AUGMENTATION = CELL_RADIUS_AUGMENTATION = 0
d_SIDES_PER_NEIGHBORHOOD = SIDES_PER_NEIGHBORHOOD = 4
d_NEIGHBORHOODS_INCLUDE_CORNERS = NEIGHBORHOODS_INCLUDE_CORNERS = True
d_FRAME_RATE_TEST = FRAME_RATE_TEST = True
d_ROCKIT_SPEED = ROCKIT_SPEED = 13
d_PERCENTAGE_OF_TILT_TO_START_WITH = PERCENTAGE_OF_TILT_TO_START_WITH = 20
d_MAXIMUM_TILT = MAXIMUM_TILT = 10
d_COLOR_BY_UNIVERSE = COLOR_BY_UNIVERSE = 7
d_COLOR_BY_ITEM = COLOR_BY_ITEM = 5
d_COLOR_BY_CELL = COLOR_BY_CELL = 2
d_RANDOM_START_COLORS = RANDOM_START_COLORS = 3
d_COLOR_DESATURATION = COLOR_DESATURATION = 0
d_ALLOW_SURVIVAL_MUTATION = ALLOW_SURVIVAL_MUTATION = False
d_RANDOM_PLACEMENT = RANDOM_PLACEMENT = False
d_U_BLINKER = U_BLINKER = False
d_U_RPENT = U_RPENT = False
d_U_GLIDER0 = U_GLIDER0 = True
d_U_GLIDER1 = U_GLIDER1 = True
d_U_ACORN = U_ACORN = False
d_U_TENCELL = U_TENCELL = False
d_U_TPENT = U_TPENT = False
d_U_QPENT = U_QPENT = False
d_U_OPENT = U_OPENT = False
d_U_XPENT = U_XPENT = False
HORIZONTAL_BORDER_PERCENTAGE = 25
VERTICAL_BORDER_PERCENTAGE = 25
def iof(intorfloat):
    intorfloat = decimal.Decimal(intorfloat)
    ioiof = int(intorfloat)
    return ioiof if ioiof == intorfloat else float(intorfloat)
def siof(stringintorfloat):
    try:
        stringintorfloat = decimal.Decimal(stringintorfloat)
        ioiof = int(stringintorfloat)
        return ioiof if ioiof == stringintorfloat else float(stringintorfloat)
    except:
        return str(stringintorfloat)
neighborhood_maps = []
def seed_from_string(s):
    global CHOSEN_MULTIVERSE
    seed =0
    if s in ['', 'default', None]:
        if CHOSEN_MULTIVERSE == '' and s != 'default':
            random.seed(time.time())
            seed = int(time.time())&15
            CHOSEN_MULTIVERSE = None
            print(f'Multiverse seed number {seed} activated.')
        else:
            CHOSEN_MULTIVERSE = 'default'
            print(f'Default multiverse selected.')
    elif s == 'random':
        random.seed(time.time())
        seed = random.randint(-1000,1000000)
        CHOSEN_MULTIVERSE = 'random'
        print(f'Multiverse seed number {seed} chosen at random "{s}".')
    else:
        seed = siof(s)
        if s != seed:
            print(f'Multiverse seed number {seed} extracted from string "{s}".')
        CHOSEN_MULTIVERSE = seed
    random.seed(seed)
    print(f'CHOSEN_MULTIVERSE == {CHOSEN_MULTIVERSE}')
    return seed
other_universes = []
other_universes.append(1+random.randint(0,1)/10)
other_universes.append(2+random.randint(0,3)/10)
other_universes.append(3+random.randint(1,3)/10)
other_universes.append(4+random.randint(2,9)/10)
other_universes.append(random.randint(5,9)+random.randint(0,9)/10)
other_universes.append(10)
other_universes.append(random.randint(2,4)*10)
other_universes.append(random.randint(50,99))
other_universes.append(100)
other_universes.append(random.randint(1,3) * 100 + random.randint(1,9))
other_universes.append(random.randint(310,999))
other_universes.append('1e'+str(random.randint(3,5)))
other_universes.append('1.'+str(random.randint(1,9))+'e'+str(random.randint(5,7)))
other_universes.append('1.'+str(random.randint(1,99))+'e'+str(random.randint(7,9)))
other_universes.append(str(random.randint(2,9))+'.'+str(random.randint(1,999))+'e'+str(random.randint(7,9)))
other_universes.append(str(random.randint(1,9))+'.'+str(random.randint(1,9999))+'e'+str(random.randint(10,20)))
layout = []
layout.append([sg.Text(f"Select a multiverse. (Changing this setting changes other settings.)")])
row = []
row.append(sg.Combo(values = ['default', 0, *other_universes , 'random'], default_value = f'{CHOSEN_MULTIVERSE}', size = (49,19), enable_events = True, key = 'CHOSEN_MULTIVERSE'))
row.append(sg.Button('Apply change of multiverse!'))
layout.append(row)
layout.append([sg.Text(f"Display at what scale?"), sg.Input(f'{SCALE}',key = 'SCALE')])
layout.append([sg.Text(f"Number of universes?"), sg.Input(f'{NUMBER_OF_UNIVERSES}', key = 'NUMBER_OF_UNIVERSES')])
layout.append([sg.Text(f"Number of things to start with?"), sg.Input(f'{NUMBER_OF_START_THINGS}', key = 'NUMBER_OF_START_THINGS')])

layout.append([sg.Text(f"How much cell radius augmentation?"), sg.Input(f'{CELL_RADIUS_AUGMENTATION}', key = 'CELL_RADIUS_AUGMENTATION')])
layout.append([sg.Text(f"How many sides per neighborhood?"), sg.Input(f'{SIDES_PER_NEIGHBORHOOD}', key = 'SIDES_PER_NEIGHBORHOOD')])


row = []
row.append(sg.Checkbox(text = f'Are the cell neighborhoods to include "corners"?', tooltip = f"(Corners are neighbor cell locations two adjacent neighbor vectors away. Include them in the neighborhood?)", default = NEIGHBORHOODS_INCLUDE_CORNERS, key = 'NEIGHBORHOODS_INCLUDE_CORNERS'))
row.append(sg.Checkbox(text = f"Periodically report program speed in standard output?", default = FRAME_RATE_TEST, key = 'FRAME_RATE_TEST'))
layout.append(row)


layout.append([sg.Text(f"Change tilt at what speed?"), sg.Input(f'{ROCKIT_SPEED}', key = 'ROCKIT_SPEED')])
row = []
row.append(sg.Text(f"Start with what percentage of maximum tilt?"))
row.append(sg.Slider(range = (-100, 100), size = (50,10), default_value = PERCENTAGE_OF_TILT_TO_START_WITH, resolution = 1, orientation = 'h', key = 'PERCENTAGE_OF_TILT_TO_START_WITH'))
layout.append(row)

layout.append([sg.Text(f"How many degrees maximum tilt?")])
layout.append([sg.Slider(range = (-360, 360), size = (90,10), default_value = MAXIMUM_TILT, resolution = 1, orientation = 'h', key = 'MAXIMUM_TILT')])
              
row = []
row.append(sg.Text(f"Color settings: "))
row.append(sg.Spin(list(range(10)), initial_value = COLOR_BY_UNIVERSE, tooltip = f"What portion of initial coloration should be per universe?", key = 'COLOR_BY_UNIVERSE'))
row.append(sg.Spin(list(range(10)), initial_value = COLOR_BY_ITEM, tooltip = f"What portion of initial coloration should be per item?", key = 'COLOR_BY_ITEM'))
row.append(sg.Spin(list(range(10)), initial_value = COLOR_BY_CELL, tooltip = f"What portion of initial coloration should be per cell?", key = 'COLOR_BY_CELL'))
row.append(sg.Spin(list(range(10)), initial_value = RANDOM_START_COLORS, tooltip = f"What portion should initial coloration be randomized?", key = 'RANDOM_START_COLORS'))
row.append(sg.Spin(list(range(10)), initial_value = COLOR_DESATURATION, tooltip = f"What portion should starting colors be desaturated?", key = 'COLOR_DESATURATION'))
row.append(sg.Checkbox(text = f"Allow survival color mutation?", tooltip = f"(Allow non-random algorythmic color mutation on survival?)", default = ALLOW_SURVIVAL_MUTATION, key = 'ALLOW_SURVIVAL_MUTATION'))
layout.append(row)

layout.append([sg.Text(f"Randomize item placement by what percentage?"), sg.Slider(range = (0, 100), default_value = RANDOM_PLACEMENT, resolution = 0.5, orientation = 'h', key = 'RANDOM_PLACEMENT')])
row = []
row.append(sg.Checkbox(text = f"blinker", tooltip = f"Allow placement of blinker?", default = U_BLINKER, key = 'U_BLINKER'))
row.append(sg.Checkbox(text = f"glider [A]", tooltip = f"Allow placement of glider [A]?", default = U_GLIDER0, key = 'U_GLIDER0'))
row.append(sg.Checkbox(text = f"glider [B]", tooltip = f"Allow placement of glider [B]?", default = U_GLIDER1, key = 'U_GLIDER1'))
row.append(sg.Checkbox(text = f"acorn", tooltip = f"Allow placement of acorn?", default = U_ACORN, key = 'U_ACORN'))
row.append(sg.Checkbox(text = f"ten-cell", tooltip = f"Allow placement of ten-cell?", default = U_TENCELL, key = 'U_TENCELL'))
layout.append(row)

row = []
row.append(sg.Checkbox(text = f"o-pentamino", tooltip = f"Allow placement of o-pentamino?", default = U_OPENT, key = 'U_OPENT'))
row.append(sg.Checkbox(text = f"q-pentamino", tooltip = f"Allow placement of q-pentamino?", default = U_QPENT, key = 'U_QPENT'))
row.append(sg.Checkbox(text = f"r-pentamino", tooltip = f"Allow placement of r-pentamino?", default = U_RPENT, key = 'U_RPENT'))
row.append(sg.Checkbox(text = f"t-pentamino", tooltip = f"Allow placement of t-pentamino?", default = U_TPENT, key = 'U_TPENT'))
row.append(sg.Checkbox(text = f"x-pentamino", tooltip = f"Allow placement of x-pentamino?", default = U_XPENT, key = 'U_XPENT'))
layout.append(row)

layout.append([sg.Button('Begin'), sg.Button('Quit')])
window = sg.Window('Welcome to the CA Multiverse!', layout)
event = True
values = None
while event not in [sg.WINDOW_CLOSED, 'Quit', 'Begin']:
    PREVIOUSLY_CHOSEN_MULTIVERSE = CHOSEN_MULTIVERSE
    event,values = window.Read()
    print(f'event,values == {event,values}')

    try:
        SCALE = iof(values['SCALE'])
    except:
        pass
    try:
        NUMBER_OF_UNIVERSES = round(float(values['NUMBER_OF_UNIVERSES']))
    except:
        pass
    try:
        NUMBER_OF_START_THINGS = round(float(values['NUMBER_OF_START_THINGS']))
    except:
        pass
    if event in ['CHOSEN_MULTIVERSE', 'Apply change of multiverse!']:
        vcm = values['CHOSEN_MULTIVERSE']
        print(f'GOT HERE! {vcm}')
        seed = seed_from_string(vcm)
        if CHOSEN_MULTIVERSE == 'default':
            CHOSEN_MULTIVERSE = d_CHOSEN_MULTIVERSE
            SCALE = d_SCALE
            NUMBER_OF_UNIVERSES = d_NUMBER_OF_UNIVERSES
            NUMBER_OF_START_THINGS = d_NUMBER_OF_START_THINGS
            CELL_RADIUS_AUGMENTATION = d_CELL_RADIUS_AUGMENTATION
            SIDES_PER_NEIGHBORHOOD = d_SIDES_PER_NEIGHBORHOOD
            NEIGHBORHOODS_INCLUDE_CORNERS = d_NEIGHBORHOODS_INCLUDE_CORNERS
            FRAME_RATE_TEST = d_FRAME_RATE_TEST
            ROCKIT_SPEED = d_ROCKIT_SPEED
            PERCENTAGE_OF_TILT_TO_START_WITH = d_PERCENTAGE_OF_TILT_TO_START_WITH
            MAXIMUM_TILT = d_MAXIMUM_TILT
            COLOR_BY_UNIVERSE = d_COLOR_BY_UNIVERSE
            COLOR_BY_ITEM = d_COLOR_BY_ITEM
            COLOR_BY_CELL = d_COLOR_BY_CELL
            RANDOM_START_COLORS = d_RANDOM_START_COLORS
            COLOR_DESATURATION = d_COLOR_DESATURATION
            ALLOW_SURVIVAL_MUTATION = d_ALLOW_SURVIVAL_MUTATION
            RANDOM_PLACEMENT = d_RANDOM_PLACEMENT
            U_BLINKER = d_U_BLINKER
            U_RPENT = d_U_RPENT
            U_GLIDER0 = d_U_GLIDER0
            U_GLIDER1 = d_U_GLIDER1
            U_ACORN = d_U_ACORN
            U_TENCELL = d_U_TENCELL
            U_TPENT = d_U_TPENT
            U_QPENT = d_U_QPENT
            U_OPENT = d_U_OPENT
            U_XPENT = d_U_XPENT
            seed = time.time()
        else:
            SCALE = random.randint(1,4)
            NUMBER_OF_UNIVERSES = random.randint(1, random.randint(1, 30 // SCALE))
            NUMBER_OF_START_THINGS = random.randint(1, random.randint(1, 30 // SCALE))
            CELL_RADIUS_AUGMENTATION = random.choice((True, False))
            SIDES_PER_NEIGHBORHOOD = 4 + random.choice([0] * 4 + [1, -1, -2, -3]) + random.choice([0] * 4 + list(range(5))) + random.choice([0] * 7 + list(range(4)))
            NEIGHBORHOODS_INCLUDE_CORNERS = random.choice((True, False)) * (SIDES_PER_NEIGHBORHOOD < random.randint(0,10))

            FRAME_RATE_TEST = random.choice((True,False))
            ROCKIT_SPEED = random.randint(1, int(d_ROCKIT_SPEED * 2.5))
            PERCENTAGE_OF_TILT_TO_START_WITH = random.choice((True, False)) * random.randint(-99, 99)
            MAXIMUM_TILT = min(-360,max(360,random.choice((True, False)) * random.randint(int(-d_MAXIMUM_TILT * 2.5), int(d_MAXIMUM_TILT * 2.5))))
            COLOR_BY_UNIVERSE = random.choice((True, False)) * random.randint(0,9)
            COLOR_BY_ITEM = random.choice((True, False)) * random.randint(0,9)
            COLOR_BY_CELL = random.choice((True, False)) * random.randint(0,9)
            RANDOM_START_COLORS = random.choice((True, False)) * random.randint(0,9)
            COLOR_DESATURATION = random.choice((True, False)) * random.randint(0,9)
            if COLOR_BY_UNIVERSE+COLOR_BY_ITEM+COLOR_BY_CELL+RANDOM_START_COLORS+COLOR_DESATURATION == 0:
                COLOR_DESATURATION = 1
            ALLOW_SURVIVAL_MUTATION = random.choice((True, False))
            RANDOM_PLACEMENT = (random.choice((True, False)) + random.choice((True, False))) * random.randint(1,50)
            U_BLINKER = random.choice((True, False))
            U_RPENT = random.choice((True, False))
            U_GLIDER0 = random.choice((True, False))
            U_GLIDER1 = random.choice((True, False))
            U_ACORN = random.choice((True, False))
            U_TENCELL = random.choice((True, False))
            U_TPENT = random.choice((True, False))
            U_QPENT = random.choice((True, False))
            U_OPENT = random.choice((True, False))
            U_XPENT = random.choice((True, False))
        PREVIOUSLY_CHOSEN_MULTIVERSE = CHOSEN_MULTIVERSE
        for key, val in values.items():
            tmpv = eval(str(key))
            window[key].update(tmpv)
    elif event == 'Begin':
        CHOSEN_MULTIVERSE = PREVIOUSLY_CHOSEN_MULTIVERSE
        window['CHOSEN_MULTIVERSE'].update(value = CHOSEN_MULTIVERSE)
    else:
        values = None
window.close()

print(type(values))
if values == None:
    CHOSEN_MULTIVERSE = d_CHOSEN_MULTIVERSE
    SCALE = d_SCALE
    NUMBER_OF_UNIVERSES = d_NUMBER_OF_UNIVERSES
    NUMBER_OF_START_THINGS = d_NUMBER_OF_START_THINGS
    CELL_RADIUS_AUGMENTATION = d_CELL_RADIUS_AUGMENTATION
    SIDES_PER_NEIGHBORHOOD = d_SIDES_PER_NEIGHBORHOOD
    NEIGHBORHOODS_INCLUDE_CORNERS = d_NEIGHBORHOODS_INCLUDE_CORNERS
    FRAME_RATE_TEST = d_FRAME_RATE_TEST
    ROCKIT_SPEED = d_ROCKIT_SPEED
    PERCENTAGE_OF_TILT_TO_START_WITH = d_PERCENTAGE_OF_TILT_TO_START_WITH
    MAXIMUM_TILT = d_MAXIMUM_TILT
    COLOR_BY_UNIVERSE = d_COLOR_BY_UNIVERSE
    COLOR_BY_ITEM = d_COLOR_BY_ITEM
    COLOR_BY_CELL = d_COLOR_BY_CELL
    RANDOM_START_COLORS = d_RANDOM_START_COLORS
    COLOR_DESATURATION = d_COLOR_DESATURATION
    ALLOW_SURVIVAL_MUTATION = d_ALLOW_SURVIVAL_MUTATION
    RANDOM_PLACEMENT = d_RANDOM_PLACEMENT
    U_BLINKER = d_U_BLINKER
    U_RPENT = d_U_RPENT
    U_GLIDER0 = d_U_GLIDER0
    U_GLIDER1 = d_U_GLIDER1
    U_ACORN = d_U_ACORN
    U_TENCELL = d_U_TENCELL
    U_TPENT = d_U_TPENT
    U_QPENT = d_U_QPENT
    U_OPENT = d_U_OPENT
    U_XPENT = d_U_XPENT
else:
    SCALE = iof(values['SCALE'])
    NUMBER_OF_UNIVERSES = round(float(values['NUMBER_OF_UNIVERSES']))
    NUMBER_OF_START_THINGS = round(float(values['NUMBER_OF_START_THINGS']))
    CELL_RADIUS_AUGMENTATION = round(float(values['CELL_RADIUS_AUGMENTATION']))
    SIDES_PER_NEIGHBORHOOD = round(float(values['SIDES_PER_NEIGHBORHOOD']))
    NEIGHBORHOODS_INCLUDE_CORNERS = bool(values['NEIGHBORHOODS_INCLUDE_CORNERS'])
    FRAME_RATE_TEST = bool(values['FRAME_RATE_TEST'])
    ROCKIT_SPEED = iof(values['ROCKIT_SPEED'])
    PERCENTAGE_OF_TILT_TO_START_WITH = iof(values['PERCENTAGE_OF_TILT_TO_START_WITH'])
    MAXIMUM_TILT = iof(values['MAXIMUM_TILT'])
    COLOR_BY_UNIVERSE = iof(values['COLOR_BY_UNIVERSE'])
    COLOR_BY_ITEM = iof(values['COLOR_BY_ITEM'])
    COLOR_BY_CELL = iof(values['COLOR_BY_CELL'])
    RANDOM_START_COLORS = iof(values['RANDOM_START_COLORS'])
    COLOR_DESATURATION = bool(values['COLOR_DESATURATION'])
    if COLOR_BY_UNIVERSE+COLOR_BY_ITEM+COLOR_BY_CELL+RANDOM_START_COLORS+COLOR_DESATURATION == 0:
        COLOR_DESATURATION = 1
    U_BLINKER = bool(values['U_BLINKER'])
    U_RPENT = bool(values['U_RPENT'])
    U_GLIDER0 = bool(values['U_GLIDER0'])
    U_GLIDER1 = bool(values['U_GLIDER1'])
    U_ACORN = bool(values['U_ACORN'])
    U_TENCELL = bool(values['U_TENCELL'])
    U_TPENT = bool(values['U_TPENT'])
    U_QPENT = bool(values['U_QPENT'])
    U_OPENT = bool(values['U_OPENT'])
    U_XPENT = bool(values['U_XPENT'])
if event == 'Quit':
    exit()
sine_wave_angle = mpmath.asin(PERCENTAGE_OF_TILT_TO_START_WITH / 100)
pygame.init()
display_surface = pygame.display.set_mode()
FWS = (display_surface.get_width(), display_surface.get_height()) # Actual graphic display size FULL_WINDOW_SIZE
mfws = max(FWS[0],FWS[1])
WS = (int((FWS[0] + mfws) / SCALE / 2) | 1, int((FWS[1] + mfws) / SCALE / 2) | 1) # Actual process window size, including borders. WINDOW_SIZE
mws = max(WS[0],WS[1])
print(f"Process area center is at {WS[0] /2}, {WS[1] / 2}")
POTENTIAL_CELL_COUNT = WS[0] * WS[1]
MWS1 = ((WS[0]+FWS[0])//3,(WS[1]+FWS[1])//3)
MWS2 = ((WS[0]+FWS[0])//2,(WS[1]+FWS[1])//2)
MWS3 = ((WS[0]+FWS[0])*2//3,(WS[1]+FWS[1])*2//3)
BS0 = WS[0] * HORIZONTAL_BORDER_PERCENTAGE // 100
BS1 = WS[1] * VERTICAL_BORDER_PERCENTAGE // 100
OBS0 = int(BS0 * (FWS[0] / WS[0]))
OBS1 = int(BS1 * (FWS[1] / WS[1]))
OWS = (FWS[0] + OBS0 + OBS0, FWS[1] + OBS1 + OBS1)
MW = BS0 + WS[0] + BS0
MH = BS1 + WS[1] + BS1
MWS = (MW, MH)
fr = mfws/mws
OBS0 = int(BS0 * fr)
OBS1 = int(BS1 * fr)
OWS = (int(WS[0] * fr + OBS0 + OBS0), int(WS[1] * fr + OBS1 + OBS1))
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
def hrgb(h):
    return [round(i * 255) for i in colorsys.hsv_to_rgb(h,1,.75)]
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


def msin(n):
    return mpmath.sin(n*mpmath.pi*2)

def mcos(n):
    return mpmath.cos(n*mpmath.pi*2)


def calculate_neighborhood(orientation_fraction = 0, sides_count = 4, radius = any, has_corners = True, allow_zero_angle = False):
    if radius == any:
        radius = round(sides_count / 4) + 1
    hp = 1 / sides_count
    if allow_zero_angle:
        q = 0
    else:
        q = 2 / sides_count
    n = orientation_fraction / sides_count
    neighborhood=[]
    corners = []
    cntr1 = None
    for this_side in range(0, sides_count + 1):
        cntr0 = cntr1
        cntr1 = (int(mcos(n+q+this_side*hp)*radius*mpmath.sqrt(2)), int(msin(n+q+this_side*hp)*radius*mpmath.sqrt(2)))
        if this_side <= 0:
            continue
        corner = cntr0[0]+cntr1[0], cntr0[1]+cntr1[1]
        neighborhood.append(cntr0)
        corners.append(corner)
        last_side = this_side
    if has_corners:
        neighborhood += corners
    return neighborhood
def calculate_neighborhoods(orientation_count = 3, sides_count = 4, radius_augment = 1, has_corners = True):
    accepted_radius = False
    radius = 1
    while not accepted_radius:
        locations = []
        neighborhoods=[]
        for n in range(orientation_count):
            neighborhood = calculate_neighborhood(n / orientation_count, sides_count, radius, has_corners)
            locations += neighborhood
            neighborhoods.append(neighborhood)
        if len(set(locations)) == len(locations):
            accepted_radius = radius
            print(f'Neighborhood radius automatically set to {radius}.')
        else:
            radius += 1

    if radius_augment == any:
        radius_augment = 1

    radius += radius_augment
    locations = []
    neighborhoods=[]
    for n in range(orientation_count):
        neighborhood = calculate_neighborhood(n / orientation_count, sides_count, radius, has_corners)
        locations += neighborhood
        neighborhoods.append(neighborhood)
    print(f'Neighborhood radius set to {radius}.')
    return neighborhoods
def unique(them):
    if len(them) == 0:
        return them
    t = type(them[0])
    tt = type(them)
    them=map(tuple,them)
    them=set(them)
    them=map(set,them)
    them=map(t,them)
    them=tt(them)
    return them
def display_process_buffer():
    global sine_wave_angle
    global process_buffer
    global mirrored_surface
    mirrored_surface = pygame.Surface(MWS)
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
    coms = mirrored_surface.copy()
    dark_surface = coms.copy()
    mul_surface = pygame.Surface(MWS)
    mul_surface.fill((95,95,95))
    dark_surface.blit(mul_surface,(0,0), special_flags=pygame.BLEND_RGBA_MULT)
    for location in halo:
        coms.blit(dark_surface, (-location[0], -location[1]), special_flags=pygame.BLEND_RGBA_ADD)
    coms.blit(mirrored_surface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
    mirrored_surface = coms
    intermediate_surface = pygame.transform.smoothscale(mirrored_surface, (MWS1))
    intermediate_surface = pygame.transform.smoothscale(intermediate_surface, (MWS2))
    oversized_surface.blit(pygame.transform.scale(intermediate_surface, (OWS)), (0, 0))
    oversized_surface.blit(pygame.transform.smoothscale(intermediate_surface, (OWS)), (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
    screen_angle = MAXIMUM_TILT * mpmath.sin(sine_wave_angle)
    sine_wave_angle -= (mpmath.pi * ROCKIT_SPEED / 10000)
    mp2 = mpmath.pi * 2
    if sine_wave_angle < 0:
        sine_wave_angle -= mp2
    if sine_wave_angle > mp2:
        sine_wave_angle += mp2
    rotated_image = pygame.transform.rotate(oversized_surface, screen_angle)
    rrect = rotated_image.get_rect(center = oversized_surface.get_rect(topleft = (-OBS0,-OBS1)).center)
    surf = rotated_image.copy()
    surf.blit(rotated_image, (2,-2), special_flags=pygame.BLEND_RGBA_ADD)
    surf.blit(rotated_image, (2,2), special_flags=pygame.BLEND_RGBA_ADD)
    surf.blit(rotated_image, (-2,2), special_flags=pygame.BLEND_RGBA_ADD)
    surf.blit(rotated_image, (-2,-2), special_flags=pygame.BLEND_RGBA_ADD)
    rotated_image.blit(surf, (0,0), special_flags=pygame.BLEND_RGBA_ADD)
    display_surface.blit(rotated_image, ((FWS[0]-rotated_image.get_width())//2, (FWS[1]-rotated_image.get_height())//2))

    pygame.display.update()
    return

def initWorld(): #Initialize and draw some stuff to start with.
    global neighborhood_shapes
    global all_neighborhood_locations
    global halo
    neighborhood_shapes = calculate_neighborhoods(radius_augment = CELL_RADIUS_AUGMENTATION, orientation_count = NUMBER_OF_UNIVERSES, sides_count = SIDES_PER_NEIGHBORHOOD, has_corners = NEIGHBORHOODS_INCLUDE_CORNERS)
    all_neighborhood_locations = list(itertools.chain(*neighborhood_shapes))

    halo = set([(round(l[0]*.35),round(l[1]*.35)) for l in all_neighborhood_locations])
    clusters = []
    if U_BLINKER:
        clusters.append(((0,1),(0,0),(0,-1))) # blinker
    if U_RPENT:
        clusters.append(((0,1),(1,1),(-1,0),(0,0),(0,-1))) # r-pent
    if U_GLIDER0:
        clusters.append(((-1,-1),(0,-1),(1,-1),(1,0),(0,1))) # glider0
    if U_GLIDER1:
        clusters.append(((-1,-1),(0,-1),(0,0),(1,0),(-1,1))) # glider1
    if U_ACORN:
        clusters.append(((-3,1),(-2,1),(-2,-1),(0,0),(1,1),(2,1),(3,1))) # acorn
    if U_TENCELL:
        clusters.append(((-3,2),(-2,3),(-2,2),(-2,1),(0,2),(0,1),(0,0),(2,-1),(2,-2),(4,-2))) # ten cell
    if U_TPENT:
        clusters.append(((-1,0),(0,0),(1,0),(0,1),(0,2))) # t-pent
    if U_QPENT:
        clusters.append(((-2,0),(-1,0),(0,0),(1,0),(1,-1))) # q-pent
    if U_OPENT:
        clusters.append(((-2,0),(-1,0),(0,0),(1,0),(2,0))) # o-pent
    if U_XPENT:
        clusters.append(((-1,0),(0,-1),(0,0),(1,0),(0,1))) # x-pent
    if clusters == []:
        clusters.append(((0,0),))
    number_of_clusters = random.randint(7,11)
    number_of_clusters = NUMBER_OF_START_THINGS
    n_shape_number = random.randint(0, len(neighborhood_shapes) - 1)
    cell_number = 0
    if min(number_of_clusters, NUMBER_OF_UNIVERSES) <= 0:
        cellhuedivisor = max(number_of_clusters, NUMBER_OF_UNIVERSES)
    else:
        cellhuedivisor = max(number_of_clusters, NUMBER_OF_UNIVERSES) / min(number_of_clusters, NUMBER_OF_UNIVERSES)
    for cluster_number in range(number_of_clusters):
        cluster = random.choice(clusters)

        direction_to_point = cluster_number
        crude_direction = 3 - direction_to_point // len(neighborhood_shapes)
        fine_direction = len(neighborhood_shapes) - direction_to_point % len(neighborhood_shapes) - 1
        n_shape_number = fine_direction


        cluster = clusters[cluster_number % len(clusters)]
        ALLOW_RANDOM_MIRRORING = False
        if ALLOW_RANDOM_MIRRORING:
            if random.choice((True,False)):
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
                rc[random.choice((0,2))] = rc[random.choice((0,2))] | 128
            color_choices.append(rc)
        rns = neighborhood_shapes[n_shape_number]
        neighborhood_color = hrgb(n_shape_number / len(neighborhood_shapes))
        n_shape_number += 1
        n_shape_number %= len(neighborhood_shapes)

        dsx = random.randint(WS[0]*2//7,WS[0]*5//7)
        dsy = random.randint(WS[1]*2//7,WS[1]*5//7)
        nsn = mpmath.pi * 2 * cluster_number / number_of_clusters


        if cluster_number % 3 == 2:
            movx = int(mpmath.sin(nsn) * WS[0] / 2.2)
            movy = int(mpmath.cos(nsn) * WS[1] / 2.9)
        elif cluster_number % 3 == 1:
            movx = int(mpmath.sin(nsn) * WS[0] / 2.7)
            movy = int(mpmath.cos(nsn) * WS[1] / 3.35)
        else:
            movx = int(mpmath.sin(nsn) * WS[0] / 3.50)
            movy = int(mpmath.cos(nsn) * WS[1] / 4.05)
        destx = WS[0]//2 + movx
        desty = WS[1]//2 + movy
        destx = round((destx * (100 - RANDOM_PLACEMENT) + dsx * RANDOM_PLACEMENT) / 100)
        desty = round((desty * (100 - RANDOM_PLACEMENT) + dsy * RANDOM_PLACEMENT) / 100)
        if crude_direction == 0:
            rns0 = rns[0]
            rns1 = rns[3]
        elif crude_direction == 1:
            rns0 = rns[2]
            rns1 = rns[3]
        elif crude_direction == 2:
            rns0 = rns[2]
            rns1 = rns[1]
        elif crude_direction == 3:
            rns0 = rns[0]
            rns1 = rns[1]

        for xy in cluster:
            cell_number += 1
            rndc = random.choice(color_choices)
            cellhue = (cell_number / cellhuedivisor)
            cellhue = cellhue - int(cellhue)
            cellcolor =hrgb(cellhue)
            itemcolor =hrgb(cluster_number / number_of_clusters)
            total_color_weight = COLOR_BY_UNIVERSE + COLOR_BY_ITEM + COLOR_BY_CELL + RANDOM_START_COLORS + COLOR_DESATURATION
            colch = [(neighborhood_color[i] * COLOR_BY_UNIVERSE + itemcolor[i] * COLOR_BY_ITEM + cellcolor[i] * COLOR_BY_CELL + rndc[i] * RANDOM_START_COLORS + 128 * COLOR_DESATURATION) // total_color_weight for i in [0,1,2]]
            process_buffer.Surface.set_at((xy[0]*rns0[0]+xy[1]*rns1[0]+destx, xy[1]*rns1[1]+xy[0]*rns0[1]+desty),colch)
    display_process_buffer()
def mutateColor(c):
    if not ALLOW_SURVIVAL_MUTATION:
        return c
    c=list(c)
    if 0==c[0]==c[1]==c[2]:
        return c
    if c[0]==c[1]==c[2]:
        if sum(c) < 48:
            c = [rcc + 32 for rcc in c]
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
    rc= [min(max(c[0],0),255) & ~1 | (c[0]&1), min(max(c[1],0),255) & ~1 | (c[1]&1), min(max(c[2],0),255) & ~1 | (c[2]&1)]
    if sum(rc) < 48:
        rc = [rcc + 32 for rcc in rc]
    return rc


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
        if sum(mate) < 48:
            mate = [mt+32 for mt in mate]
    return mate
    
    
def playGame():
    global life_checksum
    global birth_count
    global death_count
    global survival_count
    global generationNumber
    global neighborhood_shapes
    global all_neighborhood_locations
    global mirrored_surface
    global halo
    mirrored_surface = pygame.Surface(MWS)
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



    cmms = mirrored_surface.copy()
    cmms.blit(cmms, (0,0), special_flags=pygame.BLEND_RGBA_ADD)
    cmms.blit(cmms, (0,0), special_flags=pygame.BLEND_RGBA_ADD)
    cmms.blit(cmms, (0,0), special_flags=pygame.BLEND_RGBA_ADD)
    cmms.blit(cmms, (0,0), special_flags=pygame.BLEND_RGBA_ADD)
    cmms.blit(cmms, (0,0), special_flags=pygame.BLEND_RGBA_ADD)
    cmms.blit(cmms, (0,0), special_flags=pygame.BLEND_RGBA_ADD)
    coms = pygame.Surface(MWS).convert(8)

    palette = [[1,1,1] for _ in range(256)]
    palette[0] = [0,0,0]
    coms.set_palette(palette)
    coms.blit(cmms,(0,0))
    surface_per_universe = [pygame.Surface(MWS) for _ in range(len(neighborhood_shapes))]
    for universe_number in range(len(neighborhood_shapes)):
        nshape = neighborhood_shapes[universe_number]
        unisurface = surface_per_universe[universe_number]
        for location in nshape:
            unisurface.blit(coms, (-location[0], -location[1]), special_flags=pygame.BLEND_RGBA_ADD)
    surfa = surface_per_universe.copy()
    surface_per_universe = [pygame.Surface(WS) for _ in range(len(surface_per_universe))]
    for n in range(len(surface_per_universe)):
        surface_per_universe[n].blit(surfa[n],(-BS0,-BS1))
    
    coms = pygame.Surface(WS)
    for uniserf in surface_per_universe:
        coms.blit(uniserf, (0,0), special_flags=pygame.BLEND_RGBA_ADD)
    life_checksum = mpmath.pi
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
        totalistics = [unisurface.get_at(cell_location)[0] for unisurface in surface_per_universe]
        totalset = set(totalistics)
        totalset.discard(0)
        ltot = len(totalset)
        life_checksum *= 1.0001 + ltot
        if life_checksum > POTENTIAL_CELL_COUNT:
            life_checksum -= (POTENTIAL_CELL_COUNT - 1)
        if ltot != 1:
            future_buffer[cell_location] = [0,0,0]
            continue
        effective_neighbor_count = totalset.pop()


        cell_color = process_buffer[cell_location]
        x,y = cell_location
        if cell_color == [0,0,0]:
            if effective_neighbor_count == 2:
                new_cell_color = [0,0,0]
            elif effective_neighbor_count == 3:
                neigh_shapes = tuple(tuple(tuple((x+dst[0], y+dst[1])) for dst in nbh) for nbh in neighborhood_shapes)
                sh_neighborhoods =[[process_buffer[address] for address in neigh_shapes[i]] for i in range(len(neigh_shapes))]
                new_cell_color = baby_maker(cell_color, sh_neighborhoods)
                if new_cell_color != [0,0,0]:
                    birth_count += 1
            else: # stay unalive
                new_cell_color = [0,0,0]
        else:
            life_checksum += 1
            if effective_neighbor_count == 2:
                survival_count += 1
                new_cell_color = mutateColor(cell_color)
            elif effective_neighbor_count == 3:
                survival_count += 1
                new_cell_color = mutateColor(cell_color)
            else: # death
                new_cell_color = [0,0,0]
                death_count += 1
        future_buffer[cell_location] = new_cell_color
    process_buffer.Surface.blit(future_buffer.Surface, (0,0))
    display_process_buffer()
running = True
life_checksum_deque = collections.deque([],WS[0]+WS[1])
stagnation_tolerance = 6
if AUTO_RESTART_TIMER >= 30:
    time_between_auto_restarts = AUTO_RESTART_TIMER
else:
    time_between_auto_restarts = 900
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
            if AUTO_RESTART_TIMER:
                if starttime + time_between_auto_restarts <= time.time():
                    restart_countdown -= 1
                if restart_countdown <= 0:
                    restart = True
                    starttime = time.time()
            if RESTART_ON_STAGNATION:
                fullcheck_str = f'{life_checksum} {birth_count} {death_count} {survival_count}'
                if fullcheck_str in life_checksum_deque:
                    stagnation_count += 1
                    print(f"Possible stagnation detected. {fullcheck_str}")
                    if stagnation_count > stagnation_tolerance:
                        restart = True
                else:
                    life_checksum_deque.append(fullcheck_str)
                    stagnation_count = 0

        pygame.event.get()
        restart = False
        restart_countdown = 4
        starttime = time.time()
                
'' # 🄯 DAK
