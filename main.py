#!/bin/python3
from pyanvil import World, BlockState
from pyanvil.coordinate import AbsoluteCoordinate
import logging

logging.basicConfig(level=logging.DEBUG, format='[%(relativeCreated)dms] [%(levelname)s] %(module)s.%(funcName)s.%(lineno)d: %(message)s')

with World(world_folder='/home/dallen/.minecraft/saves') as wrld:
    myBlock = wrld.get_block(AbsoluteCoordinate(15, 10, 25))
    myBlock.set_state(BlockState('minecraft:iron_block'))
