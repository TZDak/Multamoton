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
import copy
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
global hix, lox, hiy, loy
global neighborhood_width
global neighborhood_height
global population
global next_generation
global target_process_window
global current_process_window
def max_if_any(arg):
    if len(arg) == 0:
        return 0
    else:
        return max(arg)
def min_if_any(arg):
    if len(arg) == 0:
        return 0
    else:
        return min(arg)
def max_if_any(arg):
    if len(arg) == 0:
        return 0
    else:
        return max(arg)
pas = lambda *args, **kwargs:None
def bitwise_and(arg):
    if len(arg) == 0:
        return 0
    return functools.reduce(operator.and_, arg)
def bitwise_inclusive_or(arg):
    if len(arg) == 0:
        return 0
    return functools.reduce(operator.or_, arg)
def bitwise_exclusive_or(arg):
    if len(arg) == 0:
        return 0
    return functools.reduce(operator.xor, arg)
def neighborhood_size():
    return SIDES_PER_NEIGHBORHOOD + NEIGHBORHOODS_INCLUDE_CORNERS * SIDES_PER_NEIGHBORHOOD
def sign(n):
    return int(mpmath.sign(int(n)))
def zsplit(splitter, to_be_split):
    tbs = to_be_split
    return 1 + (splitter > tbs) - (splitter < tbs)
safe_eval_dict = dict({k: eval('set.'+k) for k in dir(set)})
coldict = dict({k: eval('collections.'+k) for k in dir(collections)})
safe_eval_dict.update(coldict)
iterdict = dict({k: eval('itertools.'+k) for k in dir(itertools)})
safe_eval_dict.update(iterdict)
funcdict = dict({k: eval('functools.'+k) for k in dir(functools)})
safe_eval_dict.update(funcdict)
decdict = dict({k: eval('decimal.'+k) for k in dir(decimal)})
safe_eval_dict.update(decdict)
colordict = dict({k: eval('colorsys.'+k) for k in dir(colorsys)})
safe_eval_dict.update(colordict)
tmplist = ['abs', 'all', 'any', 'ascii', 'bin', 'bool', 'bytearray', 'bytes', 'chr', 'complex', 'dict', 'divmod', 'enumerate']
tmplist += ['filter', 'float', 'format', 'frozenset', 'getattr', 'hasattr', 'hash', 'hex', 'int', 'isinstance', 'issubclass']
tmplist += ['iter', 'len', 'list', 'map', 'oct', 'ord', 'pow', 'property', 'range', 'repr', 'reversed', 'round']
tmplist += ['set', 'slice', 'sorted', 'str', 'sum', 'tuple', 'type', 'vars', 'zip']
tmpdict = dict({k: eval(k) for k in tmplist})
safe_eval_dict.update(tmpdict)
mpdict = dict({k: eval('operator.'+k) for k in dir(operator)})
safe_eval_dict.update(mpdict)
mpdict = dict({k: eval('mpmath.'+k) for k in dir(mpmath)})
safe_eval_dict.update(mpdict)
finalizedict = {'intersection':set.intersection, 'union':set.union, 'max':max_if_any, 'min':min_if_any, 'zsplit':zsplit, 'sign':sign}
finalizedict.update({'bitwise_and':bitwise_and, 'bitwise_inclusive_or':bitwise_inclusive_or, 'bitwise_exclusive_or':bitwise_exclusive_or})
finalizedict.update({'neighborhood_size':neighborhood_size, 'print':print, 'input':pas, 'eval':pas, 'exit':pas, 'quit':pas})
safe_eval_dict.update(finalizedict)
list_of_consensus_options = []
list_of_consensus_options.append('-1')
list_of_consensus_options.append('BIRTH')
list_of_consensus_options.append('SURVIVAL')
list_of_consensus_options.append('min(census)')
list_of_consensus_options.append('max(census)')
list_of_consensus_options.append('sum(census)')
list_of_consensus_options.append('len(census)')
list_of_consensus_options.append('len(census)-1')
list_of_consensus_options.append('min(census)+1')
list_of_consensus_options.append('max(census)-1')
list_of_consensus_options.append('bitwise_and(census)')
list_of_consensus_options.append('sum(census)//len(census)')
list_of_consensus_options.append('bitwise_inclusive_or(census)')
list_of_consensus_options.append('bitwise_exclusive_or(census)')
list_of_consensus_options.append('sum(census)-NUMBER_OF_UNIVERSES')
list_of_consensus_options.append('sum(census)%NUMBER_OF_UNIVERSES')
list_of_consensus_options.append('neighborhood_size()-max(census)')
list_of_consensus_options.append('BIRTH if len(census)>3 else SURVIVAL')
list_of_consensus_options.append('BIRTH if len(census)>4 else SURVIVAL')
list_of_consensus_options.append('BIRTH if len(census)>5 else SURVIVAL')
list_of_consensus_options.append('SURVIVAL if len(census)==2 else DEATH')
list_of_consensus_options.append('min(census.intersection(BIRTH_RULE.union(SURVIVAL_RULE)))')
list_of_consensus_options.append('max(census.intersection(BIRTH_RULE.union(SURVIVAL_RULE)))')
list_of_consensus_options.append('(SURVIVAL,max(census),DEATH)[zsplit(len(census)-1,NUMBER_OF_UNIVERSES)]')
list_of_consensus_options.append('(SURVIVAL,max(census),DEATH)[zsplit(len(census)-2,NUMBER_OF_UNIVERSES)]')
list_of_consensus_options.append('BIRTH if len(census) == 2 else SURVIVAL if len(census) == 3 else DEATH')
list_of_consensus_options.append('SURVIVAL if len(census) in [2, 3] else BIRTH if len(census)==4 else DEATH')
list_of_consensus_options.append('BIRTH if len(census)>=min([neighborhood_size(),NUMBER_OF_UNIVERSES]) else SURVIVAL')
list_of_consensus_options.append('BIRTH if len(census) >= min([neighborhood_size(), NUMBER_OF_UNIVERSES]) else SURVIVAL')
list_of_birth_rule_options = []
list_of_birth_rule_options.append({3})
list_of_birth_rule_options.append({2, 3, 4})
list_of_birth_rule_options.append({3, 4})
list_of_birth_rule_options.append({3, 6})
list_of_birth_rule_options.append({3, 4, 5})
list_of_birth_rule_options.append({3, 6, 8})
list_of_birth_rule_options.append({3, 5, 7})
list_of_birth_rule_options.append({1, 3, 5, 7})
list_of_birth_rule_options.append({3, 7, 8})
list_of_birth_rule_options.append({3, 6, 7, 8})
list_of_birth_rule_options.append({3, 5, 6, 7, 8})
list_of_birth_rule_options.append({4, 5, 6, 7, 8})
list_of_birth_rule_options.append({1})
list_of_survival_rule_options = []
list_of_survival_rule_options.append({2, 3})
list_of_survival_rule_options.append({4})
list_of_survival_rule_options.append({3})
list_of_survival_rule_options.append({2})
list_of_survival_rule_options.append({})
list_of_survival_rule_options.append({3, 4})
list_of_survival_rule_options.append({5})
list_of_survival_rule_options.append({1, 2, 5})
list_of_survival_rule_options.append({1, 2, 3, 4})
list_of_survival_rule_options.append({4, 5, 6, 7, 8})
list_of_survival_rule_options.append({1, 2, 3, 4, 5})
list_of_survival_rule_options.append({2, 4, 5})
list_of_survival_rule_options.append({2, 3, 8})
list_of_survival_rule_options.append({1, 3, 5, 8})
list_of_survival_rule_options.append({4, 5, 6, 7})
list_of_survival_rule_options.append({1, 3, 5, 7})
list_of_survival_rule_options.append({2, 3, 5, 6, 7, 8})
list_of_survival_rule_options.append({3, 4, 6, 7, 8})
list_of_survival_rule_options.append({5, 6, 7, 8})
list_of_survival_rule_options.append({2, 3, 4, 5})
list_of_survival_rule_options.append({1, 2, 3, 4, 5, 6, 7, 8})
list_of_survival_rule_options.append({1})
list_of_predefined_bs_options = []
list_of_predefined_bs_options.append(({3},{2, 3}))
list_of_predefined_bs_options.append(({3},{4}))
list_of_predefined_bs_options.append(({3},{3}))
list_of_predefined_bs_options.append(({3},{2}))
list_of_predefined_bs_options.append(({2, 3, 4},{}))
list_of_predefined_bs_options.append(({3, 4},{3, 4}))
list_of_predefined_bs_options.append(({3, 6},{2, 3}))
list_of_predefined_bs_options.append(({3, 4, 5},{5}))
list_of_predefined_bs_options.append(({3, 6},{1, 2, 5}))
list_of_predefined_bs_options.append(({3},{1, 2, 3, 4}))
list_of_predefined_bs_options.append(({3},{4, 5, 6, 7, 8}))
list_of_predefined_bs_options.append(({3},{1, 2, 3, 4, 5}))
list_of_predefined_bs_options.append(({3, 6, 8},{2, 4, 5}))
list_of_predefined_bs_options.append(({3, 5, 7},{2, 3, 8}))
list_of_predefined_bs_options.append(({3, 5, 7},{1, 3, 5, 8}))
list_of_predefined_bs_options.append(({3, 4, 5},{4, 5, 6, 7}))
list_of_predefined_bs_options.append(({1, 3, 5, 7},{1, 3, 5, 7}))
list_of_predefined_bs_options.append(({3, 7, 8},{2, 3, 5, 6, 7, 8}))
list_of_predefined_bs_options.append(({3, 6, 7, 8},{3, 4, 6, 7, 8}))
list_of_predefined_bs_options.append(({3, 5, 6, 7, 8},{5, 6, 7, 8}))
list_of_predefined_bs_options.append(({4, 5, 6, 7, 8},{2, 3, 4, 5}))
list_of_predefined_bs_options.append(({3},{1, 2, 3, 4, 5, 6, 7, 8}))
list_of_predefined_bs_options.append(({3, 6, 7, 8},{2, 3, 5, 6, 7, 8}))
list_of_predefined_bs_options.append(({1},{1}))
BIRTH = any
SURVIVAL = ...
DEATH = None
AUTO_RESCALE = False
PROCESS_EVERY_UNIVERSE_FOR_EACH_CELL = True
CONSENSUS_OPTIONS = list_of_consensus_options
BIRTH_RULE_OPTIONS = list_of_birth_rule_options
SURVIVAL_RULE_OPTIONS = list_of_survival_rule_options
BG_COLOR = [0,0,0]
d_CHOSEN_MULTIVERSE = CHOSEN_MULTIVERSE = ''
d_CENSUS_RESOLUTION = CENSUS_RESOLUTION = CONSENSUS_OPTIONS[0]
d_BIRTH_RULE = BIRTH_RULE = BIRTH_RULE_OPTIONS[0]
d_SURVIVAL_RULE = SURVIVAL_RULE = SURVIVAL_RULE_OPTIONS[0]
d_SCALE = SCALE = 4 # Number of pixels per cell radius.
d_NUMBER_OF_UNIVERSES = NUMBER_OF_UNIVERSES = 3
d_NUMBER_OF_START_THINGS = NUMBER_OF_START_THINGS = 12
d_CELL_RADIUS_AUGMENTATION = CELL_RADIUS_AUGMENTATION = 1
d_SIDES_PER_NEIGHBORHOOD = SIDES_PER_NEIGHBORHOOD = 4
d_NEIGHBORHOODS_INCLUDE_CORNERS = NEIGHBORHOODS_INCLUDE_CORNERS = True
d_FRAME_RATE_TEST = FRAME_RATE_TEST = True
d_ROCKIT_SPEED = ROCKIT_SPEED = 13
d_PERCENTAGE_OF_TILT_TO_START_WITH = PERCENTAGE_OF_TILT_TO_START_WITH = 20
d_MAXIMUM_TILT = MAXIMUM_TILT = 10
d_PROCESS_RED_SEPARATELY = PROCESS_RED_SEPARATELY = False
d_PROCESS_GREEN_SEPARATELY = PROCESS_GREEN_SEPARATELY = False
d_PROCESS_BLUE_SEPARATELY = PROCESS_BLUE_SEPARATELY = False
d_HUE_OFFSET = HUE_OFFSET = -70
d_CPU_BIRTHS = CPU_BIRTHS = 15
d_RED_DIES_BLUE = RED_DIES_BLUE = False
d_RED_DIES_GREEN = RED_DIES_GREEN = False
d_GREEN_DIES_RED = GREEN_DIES_RED = False
d_GREEN_DIES_BLUE = GREEN_DIES_BLUE = False
d_BLUE_DIES_GREEN = BLUE_DIES_GREEN = False
d_BLUE_DIES_RED = BLUE_DIES_RED = False
d_COLOR_BY_UNIVERSE = COLOR_BY_UNIVERSE = 7
d_COLOR_BY_ITEM = COLOR_BY_ITEM = 5
d_COLOR_BY_CELL = COLOR_BY_CELL = 2
d_RANDOM_START_COLORS = RANDOM_START_COLORS = 3
d_COLOR_DESATURATION = COLOR_DESATURATION = 0
d_ALLOW_SURVIVAL_MUTATION = ALLOW_SURVIVAL_MUTATION = False
d_RANDOM_PLACEMENT = RANDOM_PLACEMENT = False
d_INITIAL_ITEM_ROTATION = INITIAL_ITEM_ROTATION = 90
d_U_BLINKER = U_BLINKER = False
d_U_RPENT = U_RPENT = True
d_U_GLIDER0 = U_GLIDER0 = False
d_U_GLIDER1 = U_GLIDER1 = True
d_U_ACORN = U_ACORN = False
d_U_TENCELL = U_TENCELL = False
d_U_TPENT = U_TPENT = False
d_U_QPENT = U_QPENT = False
d_U_OPENT = U_OPENT = False
d_U_XPENT = U_XPENT = False
constdict1 = {'CENSUS_RESOLUTION':CENSUS_RESOLUTION, 'BIRTH_RULE':BIRTH_RULE, 'SURVIVAL_RULE':SURVIVAL_RULE, 'NUMBER_OF_UNIVERSES':NUMBER_OF_UNIVERSES}
safe_eval_dict.update(constdict1)
constdict2 = {'BIRTH':BIRTH, 'SURVIVAL':SURVIVAL, 'DEATH':DEATH}
safe_eval_dict.update(constdict2)
SAFE_EVAL = safe_eval_dict
HORIZONTAL_BORDER_PERCENTAGE = 25
VERTICAL_BORDER_PERCENTAGE = 25
def lol(*args):
    reflatten = False
    la = len(args)
    if la == 1:
        arg = args[0]
        if isinstance(arg, str):
            return tuple(arg)
        elif not hasattr(arg,'__len__') or not hasattr(arg,'__iter__'):
            return tuple(arg)
    elif la == 0:
        return args
    rv = []
    for arg in args:
        if hasattr(arg,'__len__') or hasattr(arg,'__iter__'):
            if isinstance(arg, str):
                rv.append([arg])
            else:
                rv.append(list(arg))
                reflatten = True
        else:
            rv.append([arg])
    if reflatten:
        rv = lol(*itertools.chain(*rv))
    return rv
def flatten(*args):
    rv = lol(*args)
    return tuple(r[0] for r in rv)
def flatset(*args):
    return set(flatten(args))
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
row = []
row.append(sg.Text(f"Algorithm for resolving multiverse neighbor count disagreement:"))
row.append(sg.Combo(values = CONSENSUS_OPTIONS, default_value = f'{CENSUS_RESOLUTION}', size = (80,19), enable_events = True, key = 'CENSUS_RESOLUTION'))
layout.append(row)
row = []
row.append(sg.Text(f"Birth rule: (Possible number of neighbors with which a cell can be born.)"))
row.append(sg.Combo(values = BIRTH_RULE_OPTIONS, default_value = f'{BIRTH_RULE}', size = (69,19), enable_events = True, key = 'BIRTH_RULE'))
layout.append(row)
row = []
row.append(sg.Text(f"Survival rule: (Possible number of neighbors with which a cell can survive.)"))
row.append(sg.Combo(values = SURVIVAL_RULE_OPTIONS, default_value = f'{SURVIVAL_RULE}', size = (69,19), enable_events = True, key = 'SURVIVAL_RULE'))
layout.append(row)
row = []
row.append(sg.Text(f"Display at what scale?"))
row.append(sg.Input(f'{SCALE}',key = 'SCALE'))
layout.append(row)
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
row.append(sg.Slider(range = (-100, 100), size = (70,10), default_value = PERCENTAGE_OF_TILT_TO_START_WITH, resolution = 1, orientation = 'h', key = 'PERCENTAGE_OF_TILT_TO_START_WITH'))
layout.append(row)
row = []
row.append(sg.Text(f"How many degrees maximum tilt?"))
row.append(sg.Slider(range = (-360, 360), size = (80,10), default_value = MAXIMUM_TILT, resolution = 1, orientation = 'h', key = 'MAXIMUM_TILT'))
layout.append(row)
row = []
row.append(sg.Text(f"Color separation settings: ", tooltip = 'Turning any of these on causes the red, green or blue color channels of each cell to be treated as in their own world of only that color.'))
row.append(sg.Checkbox(text = f"Process red separately.", tooltip = f"Turn this on to treat the red component of each cell like a separate cell in a parallen universe.", default = PROCESS_RED_SEPARATELY, key = 'PROCESS_RED_SEPARATELY'))
row.append(sg.Checkbox(text = f"Process green separately.", tooltip = f"Turn this on to treat the green component of each cell like a separate cell in a parallen universe.", default = PROCESS_GREEN_SEPARATELY, key = 'PROCESS_GREEN_SEPARATELY'))
row.append(sg.Checkbox(text = f"Process blue separately.", tooltip = f"Turn this on to treat the blue component of each cell like a separate cell in a parallen universe.", default = PROCESS_BLUE_SEPARATELY, key = 'PROCESS_BLUE_SEPARATELY'))
layout.append(row)
row = []
row.append(sg.Text(f"Offset color hue by what percentage?"))
row.append(sg.Slider(range = (-100, 100), size = (70,10), default_value = HUE_OFFSET, resolution = 1, orientation = 'h', key = 'HUE_OFFSET'))
layout.append(row)
row = []
tooltip = f"When a cell's parents are all from the same universe, by what percentage should its birth color be set based on which universe?"
row.append(sg.Text(f"Percentage of birth color to base on universe of origin?", tooltip = tooltip))
row.append(sg.Slider(range = (0, 100), size = (50,10), default_value = CPU_BIRTHS, tooltip = tooltip, resolution = 1, orientation = 'h', key = 'CPU_BIRTHS'))
layout.append(row)
              
row = []
row.append(sg.Text(f"Colorful death settings: "))
row.append(sg.Checkbox(text = f"Red dies blue.", tooltip = f"Dissipate the red color channel to the blue color channel upon cell death.", default = RED_DIES_BLUE, key = 'RED_DIES_BLUE'))
row.append(sg.Checkbox(text = f"Red dies green.", tooltip = f"Dissipate the red color channel to the green color channel upon cell death.", default = RED_DIES_GREEN, key = 'RED_DIES_GREEN'))
row.append(sg.Checkbox(text = f"Green dies red.", tooltip = f"Dissipate the green color channel to the red color channel upon cell death.", default = GREEN_DIES_RED, key = 'GREEN_DIES_RED'))
row.append(sg.Checkbox(text = f"Green dies blue.", tooltip = f"Dissipate the green color channel to the blue color channel upon cell death.", default = GREEN_DIES_BLUE, key = 'GREEN_DIES_BLUE'))
row.append(sg.Checkbox(text = f"Blue dies green.", tooltip = f"Dissipate the blue color channel to the green color channel upon cell death.", default = BLUE_DIES_GREEN, key = 'BLUE_DIES_GREEN'))
row.append(sg.Checkbox(text = f"Blue dies red.", tooltip = f"Dissipate the blue color channel to the red color channel upon cell death.", default = BLUE_DIES_RED, key = 'BLUE_DIES_RED'))
layout.append(row)
row = []
row.append(sg.Text(f"Initial placement color settings: "))
row.append(sg.Spin(list(range(10)), initial_value = COLOR_BY_UNIVERSE, tooltip = f"What portion of initial coloration should be per universe?", key = 'COLOR_BY_UNIVERSE'))
row.append(sg.Spin(list(range(10)), initial_value = COLOR_BY_ITEM, tooltip = f"What portion of initial coloration should be per item?", key = 'COLOR_BY_ITEM'))
row.append(sg.Spin(list(range(10)), initial_value = COLOR_BY_CELL, tooltip = f"What portion of initial coloration should be per cell?", key = 'COLOR_BY_CELL'))
row.append(sg.Spin(list(range(10)), initial_value = RANDOM_START_COLORS, tooltip = f"What portion should initial coloration be randomized?", key = 'RANDOM_START_COLORS'))
row.append(sg.Spin(list(range(10)), initial_value = COLOR_DESATURATION, tooltip = f"What portion should starting colors be desaturated?", key = 'COLOR_DESATURATION'))
row.append(sg.Checkbox(text = f"Allow survival color mutation?", tooltip = f"(Allow non-random algorythmic color mutation on survival?)", default = ALLOW_SURVIVAL_MUTATION, key = 'ALLOW_SURVIVAL_MUTATION'))
layout.append(row)
layout.append([sg.Text(f"Randomize item placement by what percentage?"), sg.Slider(range = (0, 100), size = (50,10), default_value = RANDOM_PLACEMENT, resolution = 1, orientation = 'h', key = 'RANDOM_PLACEMENT')])
row = []
row.append(sg.Text(f"During initialization, rotate items to be placed by how many degrees?"))
row.append(sg.Slider(range = (-360, 360), size = (80,10), default_value = INITIAL_ITEM_ROTATION, resolution = 1, orientation = 'h', key = 'INITIAL_ITEM_ROTATION'))
layout.append(row)
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
        seed = seed_from_string(vcm)
        if CHOSEN_MULTIVERSE == 'default':
            CHOSEN_MULTIVERSE = d_CHOSEN_MULTIVERSE
            CENSUS_RESOLUTION = d_CENSUS_RESOLUTION
            BIRTH_RULE = d_BIRTH_RULE
            SURVIVAL_RULE = d_SURVIVAL_RULE
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
            PROCESS_RED_SEPARATELY = d_PROCESS_RED_SEPARATELY
            PROCESS_GREEN_SEPARATELY = d_PROCESS_GREEN_SEPARATELY
            PROCESS_BLUE_SEPARATELY = d_PROCESS_BLUE_SEPARATELY
            HUE_OFFSET = d_HUE_OFFSET
            CPU_BIRTHS = d_CPU_BIRTHS
            RED_DIES_BLUE = d_RED_DIES_BLUE
            RED_DIES_GREEN = d_RED_DIES_GREEN
            GREEN_DIES_RED = d_GREEN_DIES_RED
            GREEN_DIES_BLUE = d_GREEN_DIES_BLUE
            BLUE_DIES_GREEN = d_BLUE_DIES_GREEN
            BLUE_DIES_RED = d_BLUE_DIES_RED
            COLOR_BY_UNIVERSE = d_COLOR_BY_UNIVERSE
            COLOR_BY_ITEM = d_COLOR_BY_ITEM
            COLOR_BY_CELL = d_COLOR_BY_CELL
            RANDOM_START_COLORS = d_RANDOM_START_COLORS
            COLOR_DESATURATION = d_COLOR_DESATURATION
            ALLOW_SURVIVAL_MUTATION = d_ALLOW_SURVIVAL_MUTATION
            RANDOM_PLACEMENT = d_RANDOM_PLACEMENT
            INITIAL_ITEM_ROTATION = d_INITIAL_ITEM_ROTATION
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
            CENSUS_RESOLUTION = random.choice((random.choice(CONSENSUS_OPTIONS), CONSENSUS_OPTIONS[0]))
            BIRTH_RULE = random.choice((random.choice(BIRTH_RULE_OPTIONS), BIRTH_RULE_OPTIONS[0]))
            SURVIVAL_RULE = random.choice((random.choice(SURVIVAL_RULE_OPTIONS), SURVIVAL_RULE_OPTIONS[0]))
            NUMBER_OF_START_THINGS = random.randint(1, random.randint(1, 30 // SCALE))
            CELL_RADIUS_AUGMENTATION = random.choice((True, False))
            SIDES_PER_NEIGHBORHOOD = 4 + random.choice([0] * 4 + [1, -1, -2, -3]) + random.choice([0] * 4 + list(range(5))) + random.choice([0] * 7 + list(range(4)))
            NEIGHBORHOODS_INCLUDE_CORNERS = random.choice((True, False)) * (SIDES_PER_NEIGHBORHOOD < random.randint(0,10))
            FRAME_RATE_TEST = random.choice((True,False))
            ROCKIT_SPEED = random.randint(1, int(d_ROCKIT_SPEED * 2.5))
            PERCENTAGE_OF_TILT_TO_START_WITH = random.choice((True, False)) * random.randint(-99, 99)
            MAXIMUM_TILT = min(-360,max(360,random.choice((True, False)) * random.randint(int(-d_MAXIMUM_TILT * 2.5), int(d_MAXIMUM_TILT * 2.5))))
            PROCESS_RED_SEPARATELY = random.choice([True] + 7 * [False])
            PROCESS_GREEN_SEPARATELY = random.choice([True] + 7 * [False])
            PROCESS_BLUE_SEPARATELY = random.choice([True] + 7 * [False])
            HUE_OFFSET = random.choice((-1, 0, 1)) * random.choice((random.randint(-99, 99), d_HUE_OFFSET))
            CPU_BIRTHS = random.choice((True, False)) * 50 + random.randint(-50,50)
            RED_DIES_BLUE = random.choice([True] * (PROCESS_BLUE_SEPARATELY * 2 + 1) + 15 * [False])
            RED_DIES_GREEN = random.choice([True] * (PROCESS_GREEN_SEPARATELY * 2 + 1) + 15 * [False])
            GREEN_DIES_RED = random.choice([True] * (PROCESS_RED_SEPARATELY * 2 + 1) + 15 * [False])
            GREEN_DIES_BLUE = random.choice([True] * (PROCESS_BLUE_SEPARATELY * 2 + 1) + 15 * [False])
            BLUE_DIES_GREEN = random.choice([True] * (PROCESS_GREEN_SEPARATELY * 2 + 1) + 15 * [False])
            BLUE_DIES_RED = random.choice([True] * (PROCESS_RED_SEPARATELY * 2 + 1) + 15 * [False])
            COLOR_BY_UNIVERSE = random.choice((True, False)) * random.randint(0,9)
            COLOR_BY_ITEM = random.choice((True, False)) * random.randint(0,9)
            COLOR_BY_CELL = random.choice((True, False)) * random.randint(0,9)
            RANDOM_START_COLORS = random.choice((True, False)) * random.randint(0,9)
            COLOR_DESATURATION = random.choice((True, False)) * random.randint(0,9)
            if COLOR_BY_UNIVERSE+COLOR_BY_ITEM+COLOR_BY_CELL+RANDOM_START_COLORS+COLOR_DESATURATION == 0:
                COLOR_DESATURATION = 1
            ALLOW_SURVIVAL_MUTATION = random.choice((True, False))
            RANDOM_PLACEMENT = (random.choice((True, False)) + random.choice((True, False))) * random.randint(1,50)
            INITIAL_ITEM_ROTATION = random.choice((-1, -.5, 0, .5, 1)) * random.choice((random.randint(0, 360), d_INITIAL_ITEM_ROTATION))
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
            try:
                tmpv = eval(str(key))
                window[key].update(tmpv)
            except:
                pass
    elif event == 'Begin':
        CHOSEN_MULTIVERSE = PREVIOUSLY_CHOSEN_MULTIVERSE
        window['CHOSEN_MULTIVERSE'].update(value = CHOSEN_MULTIVERSE)
    else:
        values = None
window.close()
if values == None:
    CHOSEN_MULTIVERSE = d_CHOSEN_MULTIVERSE
    CENSUS_RESOLUTION = d_CENSUS_RESOLUTION
    BIRTH_RULE = d_BIRTH_RULE
    SURVIVAL_RULE = d_SURVIVAL_RULE
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
    PROCESS_RED_SEPARATELY = d_PROCESS_RED_SEPARATELY
    PROCESS_GREEN_SEPARATELY = d_PROCESS_GREEN_SEPARATELY
    PROCESS_BLUE_SEPARATELY = d_PROCESS_BLUE_SEPARATELY
    HUE_OFFSET = d_HUE_OFFSET
    CPU_BIRTHS = d_CPU_BIRTHS
    RED_DIES_BLUE = d_RED_DIES_BLUE
    RED_DIES_GREEN = d_RED_DIES_GREEN
    GREEN_DIES_RED = d_GREEN_DIES_RED
    GREEN_DIES_BLUE = d_GREEN_DIES_BLUE
    BLUE_DIES_GREEN = d_BLUE_DIES_GREEN
    BLUE_DIES_RED = d_BLUE_DIES_RED
    COLOR_BY_UNIVERSE = d_COLOR_BY_UNIVERSE
    COLOR_BY_ITEM = d_COLOR_BY_ITEM
    COLOR_BY_CELL = d_COLOR_BY_CELL
    RANDOM_START_COLORS = d_RANDOM_START_COLORS
    COLOR_DESATURATION = d_COLOR_DESATURATION
    ALLOW_SURVIVAL_MUTATION = d_ALLOW_SURVIVAL_MUTATION
    RANDOM_PLACEMENT = d_RANDOM_PLACEMENT
    INITIAL_ITEM_ROTATION = d_INITIAL_ITEM_ROTATION
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
    CENSUS_RESOLUTION = values['CENSUS_RESOLUTION']
    try:
        btmp = set(item for item in list(eval(values['BIRTH_RULE'],{'__builtins__':pas},SAFE_EVAL)))
        tmp = []
        for bt in btmp:
            try:
                bt = round(abs(bt))
                tmp.append(bt)
            except:
                pass
        BIRTH_RULE = set(tmp)
        BIRTH_RULE.discard(0)
    except:
        pass
    try:
        btmp = set(item for item in list(eval(values['SURVIVAL_RULE'],{'__builtins__':pas},SAFE_EVAL)))
        tmp = []
        for bt in btmp:
            try:
                bt = round(abs(bt))
                tmp.append(bt)
            except:
                pass
        SURVIVAL_RULE = set(tmp)
        SURVIVAL_RULE.discard(0)
    except:
        pass
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
    PROCESS_RED_SEPARATELY = bool(values['PROCESS_RED_SEPARATELY'])
    PROCESS_GREEN_SEPARATELY = bool(values['PROCESS_GREEN_SEPARATELY'])
    PROCESS_BLUE_SEPARATELY = bool(values['PROCESS_BLUE_SEPARATELY'])
    HUE_OFFSET = round(float(values['HUE_OFFSET']))
    CPU_BIRTHS = round(float(values['CPU_BIRTHS']))
    RED_DIES_BLUE = bool(values['RED_DIES_BLUE'])
    RED_DIES_GREEN = bool(values['RED_DIES_GREEN'])
    GREEN_DIES_RED = bool(values['GREEN_DIES_RED'])
    GREEN_DIES_BLUE =bool(values['GREEN_DIES_BLUE'])
    BLUE_DIES_GREEN = bool(values['BLUE_DIES_GREEN'])
    BLUE_DIES_RED = bool(values['BLUE_DIES_RED'])
    COLOR_BY_UNIVERSE = iof(values['COLOR_BY_UNIVERSE'])
    COLOR_BY_ITEM = iof(values['COLOR_BY_ITEM'])
    COLOR_BY_CELL = iof(values['COLOR_BY_CELL'])
    RANDOM_START_COLORS = iof(values['RANDOM_START_COLORS'])
    COLOR_DESATURATION = bool(values['COLOR_DESATURATION'])
    if COLOR_BY_UNIVERSE+COLOR_BY_ITEM+COLOR_BY_CELL+RANDOM_START_COLORS+COLOR_DESATURATION == 0:
        COLOR_DESATURATION = 1
    ALLOW_SURVIVAL_MUTATION = bool(values['ALLOW_SURVIVAL_MUTATION'])
    RANDOM_PLACEMENT = iof(values['RANDOM_PLACEMENT'])
    INITIAL_ITEM_ROTATION = iof(values['INITIAL_ITEM_ROTATION'])
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
UPPER_LEFT = (0,0)
MAXIMUM_WS = WS = (int((FWS[0] + mfws) / SCALE / 2) | 1, int((FWS[1] + mfws) / SCALE / 2) | 1) # Actual process window size, including borders. WINDOW_SIZE
current_process_window = target_process_window = ((0,0), WS)
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
    return [round(i * 255) for i in colorsys.hsv_to_rgb(h % 1, 1, .75)]
def universal_color(universe_number):
    return hrgb(((universe_number + HUE_OFFSET * NUMBER_OF_UNIVERSES / 100) % NUMBER_OF_UNIVERSES) / NUMBER_OF_UNIVERSES)
def unique_list(m):
    return list(map(list,set(map(tuple,m))))
class AnyDict(dict):
    def __init__(self,any=None,*args,**kwargs):
        dict.__init__(self,*args,**kwargs)
        self.any = any
    def __missing__(self,key):
        if self.any == any:
            self.any = AnyDict()
        r = copy.deepcopy(self.any)
        return r
    def __repr__(self):
        return f'AnyDict({str(dict(self))})#{repr(self.any)}'
class Cells(AnyDict):
    bg_color = BG_COLOR.copy()
    def __init__(self,any=AnyDict(),*args,**kwargs):
        AnyDict.__init__(self,*args,**kwargs)
        self.any = any
        self.any['neighborhoods'] = [{'number_of_sides':0, 'relative locations':[]}]
        self.any['color'] = BG_COLOR
        self.any['alive'] = False
    def __repr__(self):
        return f'Cell({str(dict(self))})#{repr(self.any)}'
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
        global current_process_window
        if not hasattr(index,'__len__'):
            index = [index]
        if len(index) == 1:
            index = (index[0] % self.__width__ ,index[0] // self.__width__)
        else:
            index = list(index)
            if AUTO_RESCALE:
                index[0] -= current_process_window[0][0]
                index[1] -= current_process_window[0][1]
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
        global current_process_window
        if not hasattr(index,'__len__'):
            index = [index]
        if len(index) == 1:
            index = (index[0] % self.__width__ ,index[0] // self.__width__)
        else:
            index = list(index)
            if AUTO_RESCALE:
                index[0] -= current_process_window[0][0]
                index[1] -= current_process_window[0][1]
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
        except Exception as e:
            raise Exception(f'error refnum 783...    index == {index}    value == {value}.   Exception == {e}')
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
    for this_side in range(1, sides_count + 1):
        cntr0 = (int(mcos(n+q+this_side*hp)*radius), int(msin(n+q+this_side*hp)*radius))
        neighborhood.append(cntr0)
    if has_corners:
        for this_side in range(0, sides_count):
            cntr0 = neighborhood[this_side]
            cntr1 = neighborhood[(this_side + 1) % sides_count]
            corner = cntr0[0]+cntr1[0], cntr0[1]+cntr1[1]
            corners.append(corner)
        neighborhood += corners
    return neighborhood
def calculate_neighborhoods(orientation_count = 3, sides_count = 4, radius_augment = 1, has_corners = True, neighborhoods_so_far = []):
    accepted_radius = False
    radius = 1
    while not radius == accepted_radius:
        locations = []
        neighborhoods=[]
        for n in range(orientation_count):
            neighborhood = calculate_neighborhood(n / orientation_count, sides_count, radius, has_corners)
            locations += neighborhood
            neighborhoods.append(neighborhood)
        if len(set(locations)) == len(locations):
            if CELL_RADIUS_AUGMENTATION and not accepted_radius:
                accepted_radius = radius
                radius += CELL_RADIUS_AUGMENTATION
            else:
                accepted_radius = radius
        else:
            if accepted_radius:
                accepted_radius += 1
            radius += 1
    locations = []
    neighborhoods = neighborhoods_so_far
    for n in range(orientation_count):
        neighborhood = calculate_neighborhood(n / orientation_count, sides_count, radius, has_corners)
        locations += neighborhood
        neighborhoods.append({'number of sides':sides_count, 'relative locations':neighborhood})
    print(f'Neighborhood radius set to {radius}.')
    return locations, neighborhoods
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
    global WS
    global MWS1
    global MWS2
    global MWS3
    global BS0
    global BS1
    global OBS0
    global OBS1
    global OWS
    global MW
    global MH
    global MWS
    global OBS0
    global OBS1
    global OWS
    global IMBORDER
    global CC_DS
    global TC_DS
    global TR_DS
    global CR_DS
    global BR_DS
    global BC_DS
    global BL_DS
    global CL_DS
    global TL_DS
    global neighborhood_shapes
    global all_neighborhood_locations
    global halo
    global hix, lox, hiy, loy
    global neighborhood_width
    global neighborhood_height
    global process_buffer
    global next_generation
    global population
    population = Cells()
    all_neighborhood_locations, neighborhood_shapes = calculate_neighborhoods(radius_augment = CELL_RADIUS_AUGMENTATION, orientation_count = NUMBER_OF_UNIVERSES, sides_count = SIDES_PER_NEIGHBORHOOD, has_corners = NEIGHBORHOODS_INCLUDE_CORNERS)
    population.any['neighborhoods'] = copy.deepcopy(neighborhood_shapes)
    hix = hiy = 0
    lox = WS[0]
    loy = WS[1]
    for nsh in neighborhood_shapes:
        for x,y in nsh['relative locations']:
            lox = min(x,lox)
            loy = min(y,loy)
            hix = max(x,hix)
            hiy = max(y,hiy)
    neighborhood_width = hix - lox + 1
    neighborhood_height = hiy - loy + 1
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
    n_shape_number = random.randint(0, NUMBER_OF_UNIVERSES - 1)
    cell_number = 0
    if min(number_of_clusters, NUMBER_OF_UNIVERSES) <= 0:
        cellhuedivisor = max(number_of_clusters, NUMBER_OF_UNIVERSES)
    else:
        cellhuedivisor = max(number_of_clusters, NUMBER_OF_UNIVERSES) / min(number_of_clusters, NUMBER_OF_UNIVERSES)
    for cluster_number in range(number_of_clusters):
        cluster = random.choice(clusters)
        item_rotation_offset = INITIAL_ITEM_ROTATION * number_of_clusters / -360
        direction_to_point = int(((cluster_number + item_rotation_offset) * NUMBER_OF_UNIVERSES * SIDES_PER_NEIGHBORHOOD / number_of_clusters) % ( NUMBER_OF_UNIVERSES * SIDES_PER_NEIGHBORHOOD))
        crude_direction = (SIDES_PER_NEIGHBORHOOD - direction_to_point // NUMBER_OF_UNIVERSES -1)
        universe_number = NUMBER_OF_UNIVERSES - direction_to_point % NUMBER_OF_UNIVERSES - 1
        n_shape_number = int(universe_number)
        if universe_number < 0:
            print("Error #1082, universe number less than zero")
            exit()
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
        rns = neighborhood_shapes[n_shape_number]['relative locations']
        neighborhood_color = universal_color(universe_number)
        dsx = random.randint(WS[0]*2//7,WS[0]*5//7)
        dsy = random.randint(WS[1]*2//7,WS[1]*5//7)
        nsn = mpmath.pi * 2 * cluster_number / number_of_clusters
        if cluster_number % 3 == 2:
            movx = int(mpmath.sin(nsn) * WS[0] / (2.2 + (6 - number_of_clusters) * (number_of_clusters < 6)))
            movy = int(mpmath.cos(nsn) * WS[1] / (2.9 + (6 - number_of_clusters) * (number_of_clusters < 6)))
        elif cluster_number % 3 == 1:
            movx = int(mpmath.sin(nsn) * WS[0] / (2.7 + (6 - number_of_clusters) * (number_of_clusters < 6)))
            movy = int(mpmath.cos(nsn) * WS[1] / (3.35 + (6 - number_of_clusters) * (number_of_clusters < 6)))
        else:
            movx = int(mpmath.sin(nsn) * WS[0] / (3.50 + (6 - number_of_clusters) * (number_of_clusters < 6)))
            movy = int(mpmath.cos(nsn) * WS[1] / (4.05 + (6 - number_of_clusters) * (number_of_clusters < 6)))
        destx = WS[0]//2 + movx
        desty = WS[1]//2 + movy
        destx = round((destx * (100 - RANDOM_PLACEMENT) + dsx * RANDOM_PLACEMENT) / 100)
        desty = round((desty * (100 - RANDOM_PLACEMENT) + dsy * RANDOM_PLACEMENT) / 100)
        rns0 = rns[crude_direction % neighborhood_shapes[n_shape_number]['number of sides']]
        rns1 = rns[(crude_direction + 1) % neighborhood_shapes[n_shape_number]['number of sides']]
        if number_of_clusters == 1:
            destx = round((WS[0]//2 * (100 - RANDOM_PLACEMENT) + dsx * RANDOM_PLACEMENT) / 100)
            desty = round((WS[1]//2 * (100 - RANDOM_PLACEMENT) + dsy * RANDOM_PLACEMENT) / 100)
        color_offset = HUE_OFFSET / 100
        for xy in cluster:
            cell_number += 1
            rndc = random.choice(color_choices)
            cellhue = (cell_number / cellhuedivisor)
            cellhue = cellhue - int(cellhue)
            cellcolor =hrgb((color_offset + cellhue) % 1)
            itemcolor =hrgb((color_offset + cluster_number / number_of_clusters) % 1)
            total_color_weight = COLOR_BY_UNIVERSE + COLOR_BY_ITEM + COLOR_BY_CELL + RANDOM_START_COLORS + COLOR_DESATURATION
            colch = [(neighborhood_color[i] * COLOR_BY_UNIVERSE + itemcolor[i] * COLOR_BY_ITEM + cellcolor[i] * COLOR_BY_CELL + rndc[i] * RANDOM_START_COLORS + 128 * COLOR_DESATURATION) // total_color_weight for i in [0,1,2]]
            set_location = (xy[0]*rns0[0]+xy[1]*rns1[0]+destx, xy[1]*rns1[1]+xy[0]*rns0[1]+desty)
            process_buffer.Surface.set_at(set_location,colch)
            cell_to_set = copy.deepcopy(population[set_location])
            cell_to_set['color'] = colch
            cell_to_set['neighborhoods'] = [neighborhood_shapes[universe_number]]
            cell_to_set['alive'] = True
            population[set_location] = cell_to_set
    hix = hiy = 0
    lox = WS[0]
    loy = WS[1]
    for key, member in population.items():
        if member['alive']:
            x, y = key
            lox = min(x,lox)
            loy = min(y,loy)
            hix = max(x,hix)
            hiy = max(y,hiy)
    display_process_buffer()
    pygame.display.update()
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
    potential_mates = [m for m in list(itertools.chain(*potential_mates)) if m != BG_COLOR]
    if BG_COLOR in potential_mates:
        potential_mates.remove(BG_COLOR)
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
    
def stork(cell_location):
    global population
    cell = population[cell_location]
    zygote = copy.deepcopy(cell)
    if PROCESS_EVERY_UNIVERSE_FOR_EACH_CELL:
        neighboring_cell_locations = []
    this_cell = population[cell_location]
    potential_mates = Cells()
    live_neighbor_color = list()
    potential_mates.any = copy.deepcopy(population.any)
    for neighborhood in this_cell['neighborhoods']:
        for r_loc in neighborhood['relative locations']:
            neighbor_location = (cell_location[0] + r_loc[0], cell_location[1] + r_loc[1])
            neighbor = population[neighbor_location]
            if neighbor['alive'] or neighbor['color'] != BG_COLOR:
                potential_mates[neighbor_location] = copy.copy(population[neighbor_location])
    if len(potential_mates) == 0:
        zygote['debug'] = 1434
        return zygote
    potential_mate_colors = [m['color'] for m in potential_mates.values() if m['color'] != BG_COLOR]
    if BG_COLOR in potential_mate_colors:
        potential_mate_colors.remove(BG_COLOR)
    if len(potential_mate_colors) == 0:
        zygote['debug'] = 1441
        return cell_color
    potential_mate_colors = [n['color'] for n in potential_mates.values()]
    rare_potential_mate_colors = []
    siz = 0
    while rare_potential_mate_colors == []:
        siz += 1
        rare_potential_mate_colors = unique_list(m for m in potential_mate_colors if potential_mate_colors.count(m) == siz)
    if len(rare_potential_mate_colors) == 1:
        mate_color = rare_potential_mate_colors[0]
    else:
        r = functools.reduce(operator.xor,(p[0] for p in rare_potential_mate_colors))
        g = functools.reduce(operator.xor,(p[1] for p in rare_potential_mate_colors))
        b = functools.reduce(operator.xor,(p[2] for p in rare_potential_mate_colors))
        if (r, g, b) == (0, 0, 0):
            r = max(p[0] for p in rare_potential_mate_colors)
            g = max(p[1] for p in rare_potential_mate_colors)
            b = max(p[2] for p in rare_potential_mate_colors)
        mate_color = [r,g,b]
        if sum(mate_color) < 48: # TODO.. REPLACE THIS!
            mate = [mt+32 for mt in mate_color]
    zygote['color'] = mate_color
    potential_home_universes = [n['neighborhood'] for n in potential_mates.values()]
    rare_potential_mate_colors = []
    siz = 0
    while rare_potential_mate_colors == []:
        siz += 1
        rare_potential_mate_colors = unique_list(m for m in potential_mate_colors if potential_mate_colors.count(m) == siz)
    if len(rare_potential_mate_colors) == 1:
        mate_color = rare_potential_mate_colors[0]
    else:
        r = functools.reduce(operator.xor,(p[0] for p in rare_potential_mate_colors))
        g = functools.reduce(operator.xor,(p[1] for p in rare_potential_mate_colors))
        b = functools.reduce(operator.xor,(p[2] for p in rare_potential_mate_colors))
        if (r, g, b) == (0, 0, 0):
            r = max(p[0] for p in rare_potential_mate_colors)
            g = max(p[1] for p in rare_potential_mate_colors)
            b = max(p[2] for p in rare_potential_mate_colors)
        mate_color = [r,g,b]
        if sum(mate_color) < 48: # TODO.. REPLACE THIS!
            mate = [mt+32 for mt in mate_color]
    zygote['color'] = mate_color
    zygote['debug'] = 1493
    return zygote
def locations_to_check():
    global population
    set_of_locations = set()
    for k,v in population.items():
        if v['alive']:
            set_of_locations.add(k)
            for n in v['neighborhoods']:
                for loc in n['relative locations']:
                    set_of_locations.add((k[0]+loc[0], k[1]+loc[1]))
    for location in set_of_locations:
        yield location
    
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
    global hix, lox, hiy, loy
    global population
    global next_generation
    global target_process_window
    global current_process_window
    next_generation = Cells()
    next_generation.any = copy.deepcopy(population.any)
    population.any['neighborhoods'] = copy.deepcopy(neighborhood_shapes)
    next_generation.any['neighborhoods'] = copy.deepcopy(neighborhood_shapes)
    assert population.any == next_generation.any
    lox = hix = WS[0] // 2
    loy = hiy = WS[1] // 2
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
    palette[0] = BG_COLOR.copy()
    for r in [not PROCESS_RED_SEPARATELY, 1]:
        for g in [not PROCESS_GREEN_SEPARATELY, 1]:
            for b in [not PROCESS_BLUE_SEPARATELY, 1]:
                palette[r + 2 * g + 4 * b] = [r,g,b]
                palette[8 * r + 16 * g + 32 * b] = [not r, not g, not b]
    coms.set_palette(palette)
    coms.blit(cmms,(0,0))
    surface_per_universe = [pygame.Surface(MWS) for _ in range(NUMBER_OF_UNIVERSES)]
    for universe_number in range(NUMBER_OF_UNIVERSES):
        nshape = neighborhood_shapes[universe_number]['relative locations']
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
    
    for cell_location in locations_to_check():
        got_birth_color = False
        cell_color = process_buffer[cell_location]
        x,y = cell_location
        full_new_cell_color = BG_COLOR.copy()
        channel_groups = [slice(0,3)]
        separate = PROCESS_RED_SEPARATELY + PROCESS_GREEN_SEPARATELY + PROCESS_BLUE_SEPARATELY
        if separate > 1:
            channel_groups = [slice(0,1),slice(1,2),slice(2,3)]
        elif separate == 1:
            if PROCESS_RED_SEPARATELY:
                channel_groups = [slice(0,1),slice(1,3)]
            elif PROCESS_GREEN_SEPARATELY:
                channel_groups = [slice(1,2),slice(0,3,2)]
            elif PROCESS_BLUE_SEPARATELY:
                channel_groups = [slice(2,3),slice(0,2)]
        cell_color = process_buffer[cell_location]
        colored_corpses = BG_COLOR.copy()
        backup_of_cell_color = cell_color.copy()
        neigh_shapes = tuple(tuple(tuple((x+dst[0], y+dst[1])) for dst in nbh['relative locations']) for nbh in neighborhood_shapes)
        sh_neighborhoods =[[process_buffer[address] for address in neigh_shapes[i]] for i in range(len(neigh_shapes))]
        born = False
        survived = False
        for channels_to_process in channel_groups:
            totalistics = [sum([population[(cell_location[0]+nl[0], cell_location[1]+nl[1])]['alive'] for nl in n['relative locations']]) for n in population[cell_location]['neighborhoods']]
            totalset = set(totalistics)
            totalset.discard(0)
            census = totalset
            gdic = {'__builtins__':None}
            if len(census) == 0:
                census = 0
            elif len(census) == 1:
                census = census.pop()
            else:
                tmpdict = {'census':census, 'CENSUS_RESOLUTION':CENSUS_RESOLUTION}
                SAFE_EVAL.update(tmpdict)
                census = eval(CENSUS_RESOLUTION,gdic,SAFE_EVAL)
            ltot = len(totalset)
            life_checksum *= 1.0001
            life_checksum += ltot
            if life_checksum > POTENTIAL_CELL_COUNT:
                life_checksum -= (POTENTIAL_CELL_COUNT - 1)
            cell_color = backup_of_cell_color[channels_to_process]
            new_cell_color = full_new_cell_color.copy()[channels_to_process]
            if cell_color == BG_COLOR[channels_to_process]:
                if census in BIRTH_RULE or census == BIRTH:
                    born = True
                    birth_count += 1
                    neigh_shapes = tuple(tuple(tuple((x+dst[0], y+dst[1])) for dst in nbh['relative locations']) for nbh in neighborhood_shapes)
                    sh_neighborhoods =[[process_buffer[address] for address in neigh_shapes[i]] for i in range(len(neigh_shapes))]
                    if not got_birth_color:
                        old_birth_color = baby_maker(backup_of_cell_color, sh_neighborhoods)
                        baby = stork(cell_location)
                        birth_color = baby['color']
                        got_birth_color = True
                    temp_new_cell_color = old_birth_color.copy()
                    if temp_new_cell_color[channels_to_process] == BG_COLOR[channels_to_process]:
                        temp_new_cell_color = [temp_new_cell_color[1], temp_new_cell_color[2], temp_new_cell_color[0]]
                        if temp_new_cell_color[channels_to_process] == BG_COLOR[channels_to_process]:
                            temp_new_cell_color = [temp_new_cell_color[1], temp_new_cell_color[2], temp_new_cell_color[0]]
                            if temp_new_cell_color[channels_to_process] == BG_COLOR[channels_to_process]:
                                temp_new_cell_color = [255,255,255]
                    new_cell_color = temp_new_cell_color[channels_to_process]
                    if CPU_BIRTHS:
                        if totalistics.count(0) == NUMBER_OF_UNIVERSES - 1:
                            unum = totalistics.index(census)
                            tmpcolor = universal_color(unum)
                            new_cell_color = [(new_cell_color[i] * (100-CPU_BIRTHS) + tmpcolor[channels_to_process][i] * CPU_BIRTHS) // 100 for i in range(len(BG_COLOR[channels_to_process]))]
                    if born and new_cell_color == BG_COLOR[channels_to_process]:
                        new_cell_color = [255, 255, 255]
                else: # stay unalive
                    new_cell_color = BG_COLOR.copy()[channels_to_process]
            else:
                life_checksum += 1
                if census in SURVIVAL_RULE or census == SURVIVAL:
                    survival_count += 1
                    survived = True
                    if ALLOW_SURVIVAL_MUTATION:
                        temp_new_cell_color = mutateColor(backup_of_cell_color)
                        if temp_new_cell_color[channels_to_process] == BG_COLOR[channels_to_process]:
                            new_cell_color = backup_of_cell_color[channels_to_process]
                        else:
                            new_cell_color = temp_new_cell_color[channels_to_process]
                    else:
                        new_cell_color = backup_of_cell_color[channels_to_process]
                    if survived and new_cell_color == BG_COLOR[channels_to_process]:
                        new_cell_color = [255, 255, 255]
                else: # death
                    if RED_DIES_BLUE or RED_DIES_GREEN or GREEN_DIES_RED or GREEN_DIES_BLUE or BLUE_DIES_GREEN or BLUE_DIES_RED:
                        nccr = (backup_of_cell_color[1] * GREEN_DIES_RED >> 1) + (backup_of_cell_color[2] * BLUE_DIES_RED >> 1)
                        nccg = (backup_of_cell_color[2] * BLUE_DIES_GREEN >> 1) + (backup_of_cell_color[0] * RED_DIES_GREEN >> 1)
                        nccb = (backup_of_cell_color[0] * RED_DIES_BLUE >> 1) + (backup_of_cell_color[1] * GREEN_DIES_BLUE >> 1)
                        new_cell_color = BG_COLOR.copy()[channels_to_process]
                        colored_corpses = [colored_corpses[0]|nccr, colored_corpses[1]|nccg, colored_corpses[2]|nccb]
                    else:
                        new_cell_color = BG_COLOR.copy()[channels_to_process]
                    death_count += 1
            full_new_cell_color[channels_to_process] = new_cell_color
            if colored_corpses != BG_COLOR:
                full_new_cell_color = [full_new_cell_color[i] | colored_corpses[i] for i in [0,1,2]]
        population.any['neighborhoods'] = copy.deepcopy(neighborhood_shapes)
        next_generation.any['neighborhoods'] = copy.deepcopy(neighborhood_shapes)
        if survived:
            aged_cell = copy.deepcopy(population[cell_location])
            next_generation[cell_location] = aged_cell
            next_generation[cell_location]['color'] = full_new_cell_color
            next_generation[cell_location]['alive'] = True
        elif born:
            next_generation[cell_location] = copy.deepcopy(baby)
            next_generation[cell_location]['color'] = full_new_cell_color
            next_generation[cell_location]['alive'] = True
        future_buffer[cell_location] = full_new_cell_color
        if born or survived:
            if x < lox or x > hix or y < loy or y > hiy:
                lox = min(x,lox)
                loy = min(y,loy)
                hix = max(x,hix)
                hiy = max(y,hiy)
                target_process_window = ((lox - neighborhood_width, loy - neighborhood_height), (hix-lox+1 + neighborhood_width * 2, hiy-loy+1 + neighborhood_height * 2))
    process_buffer.Surface.blit(future_buffer.Surface, (0,0))
    display_process_buffer()
    target_process_window = ((lox - neighborhood_width, loy - neighborhood_height), (hix-lox+1 + neighborhood_width * 2, hiy-loy+1 + neighborhood_height * 2))
    old_population = population
    population = next_generation
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
            if AUTO_RESCALE and generationNumber > 1:
                raw = target_process_window[0][0] - current_process_window[0][0]
                chng00 = max(-1-neighborhood_width,min(1+neighborhood_width, raw))
                raw = target_process_window[1][0] - current_process_window[1][0]
                chng10 = max(-1-neighborhood_width,min(1+neighborhood_width, raw))
                raw = target_process_window[0][1] - current_process_window[0][1]
                chng01 = max(-1-neighborhood_height,min(1+neighborhood_height, raw))
                raw = target_process_window[1][1] - current_process_window[1][1]
                chng11 = max(-1-neighborhood_height,min(1+neighborhood_height, raw))
                cpw = current_process_window
                current_process_window = ((cpw[0][0]+chng00,cpw[0][1]+chng01),(cpw[1][0]+chng10,cpw[1][1]+chng11))
                UPPER_LEFT = (-current_process_window[0][0], -current_process_window[0][1])
                WS = current_process_window[1]
                process_buffer = ColorGrid()
                future_buffer = ColorGrid()
                mws = max(WS[0],WS[1])
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
