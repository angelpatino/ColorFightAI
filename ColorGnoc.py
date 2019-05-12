from colorfight import Colorfight
import time
import random
from colorfight.constants import BLD_GOLD_MINE, BLD_ENERGY_WELL, BLD_FORTRESS

game = Colorfight()
TOP = 1
LEFT = 2
BOTTOM = 3
RIGHT = 4

MIN_ENERGY = 500
side = 1 
ring = 1
is_first_move = True
continue_moving = True
ring_finished = False
is_stopping = False
moved_this_side = 0
game.connect(room = 'public1')

if game.register(username = 'AngelP123', \
        password = 'YeeHaw'):
    while True:
        cmd_list = []
        my_attack_list = []
        game.update_turn()
        if game.me == None:
            continue
        me = game.me

        while True:

            if is_first_move:
                print(len(game.me.cells))
                for cell in game.me.cells.values():
                    home = cell.position
                    print("home: ", home.x, home.y)
                    position = home
            
                position.y = position.y+1
                c = game.game_map[position]
                print("Checking cell ({}, {})".format(position.x, position.y))
                if c.attack_cost < me.energy and c.owner != game.uid and me.energy > MIN_ENERGY:
                    cmd_list.append(game.attack(position, c.attack_cost))
                    print("We are attacking ({}, {}) with {} energy".format(position.x, position.y, c.attack_cost))
                    game.me.energy -= c.attack_cost
                    my_attack_list.append(c.position)
                is_first_move = False
            
            if side == TOP:
                for i in range(ring - moved_this_side):
                    position.x = position.x-1
                    if (position.x >= 0 and position.x < 30 and position.y >= 0 and position.y < 30):
                        c = game.game_map[position]
                        print("Checking cell ({}, {})".format(position.x, position.y))
                        if c.attack_cost < me.energy and c.owner != game.uid and me.energy > MIN_ENERGY:
                            cmd_list.append(game.attack(position, c.attack_cost))
                            print("We are attacking ({}, {}) with {} energy".format(position.x, position.y, c.attack_cost))
                            game.me.energy -= c.attack_cost
                            my_attack_list.append(c.position)
                        else:
                            moved_this_side = i + 1
                            is_stopping = True
                            break
                    if is_stopping:
                        moved_this_side = 0
                        break
                if is_stopping:
                    is_stopping = False
                    moved_this_side = 0
                    break           
                
            if ring_finished:
                position.y = position.y + 1
                ring_finished = False
                ring += 1 
                for i in range(ring):
                    position.x = position.x-1
                    if (position.x >= 0 and position.x < 30 and position.y >= 0 and position.y < 30):
                        # print("left", position.x, position.y)
                        c = game.game_map[position]
                        print("Checking cell ({}, {})".format(position.x, position.y))
                        if c.attack_cost < me.energy and c.owner != game.uid and me.energy > MIN_ENERGY:
                            cmd_list.append(game.attack(position, c.attack_cost))
                            print("We are attacking ({}, {}) with {} energy".format(position.x, position.y, c.attack_cost))
                            game.me.energy -= c.attack_cost
                            my_attack_list.append(c.position)
                        else:
                            moved_this_side = i + 1
                            is_stopping = True
                            break
                    if is_stopping:
                        moved_this_side = 0
                        break
                if is_stopping:
                    is_stopping = False
                    moved_this_side = 0
                    break       
                side = LEFT
            
            if side == LEFT:
                for i in range(2*ring):
                    position.y = position.y-1
                    if (position.x >= 0 and position.x < 30 and position.y >= 0 and position.y < 30):
                        # print("down", position.x, position.y)
                        c = game.game_map[position]
                        if c.attack_cost < me.energy and c.owner != game.uid and me.energy > MIN_ENERGY:
                            cmd_list.append(game.attack(position, c.attack_cost))
                            print("We are attacking ({}, {}) with {} energy".format(position.x, position.y, c.attack_cost))
                            game.me.energy -= c.attack_cost
                            my_attack_list.append(c.position)
                        else:
                            moved_this_side = i + 1
                            is_stopping = True
                            break
                    if is_stopping:
                        moved_this_side = 0
                        break
                if is_stopping:
                    is_stopping = False
                    moved_this_side = 0
                    break
                side = BOTTOM

            if side == BOTTOM:
                for i in range(2*ring):
                    position.x = position.x+1
                    if (position.x >= 0 and position.x < 30 and position.y >= 0 and position.y < 30):
                        c = game.game_map[position]
                        print("Checking cell ({}, {})".format(position.x, position.y))
                        if c.attack_cost < me.energy and c.owner != game.uid and me.energy > MIN_ENERGY:
                            cmd_list.append(game.attack(position, c.attack_cost))
                            print("We are attacking ({}, {}) with {} energy".format(position.x, position.y, c.attack_cost))
                            game.me.energy -= c.attack_cost
                            my_attack_list.append(c.position)
                        else:
                            moved_this_side = i + 1
                            is_stopping = True
                            break
                    if is_stopping:
                        moved_this_side = 0
                        break
                if is_stopping:
                    is_stopping = False
                    moved_this_side = 0
                    break
                side = RIGHT

            if side == RIGHT:
                for i in range(2*ring):
                    position.y = position.y+1
                    if (position.x >= 0 and position.x < 30 and position.y >= 0 and position.y < 30):
                        c = game.game_map[position]
                        if c.attack_cost < me.energy and c.owner != game.uid and me.energy > MIN_ENERGY:
                            cmd_list.append(game.attack(position, c.attack_cost))
                            print("We are attacking ({}, {}) with {} energy".format(position.x, position.y, c.attack_cost))
                            game.me.energy -= c.attack_cost
                            my_attack_list.append(c.position)
                        else:
                            moved_this_side = i + 1
                            is_stopping = True
                            break
                    if is_stopping:
                        moved_this_side = 0
                        break
                if is_stopping:
                    is_stopping = False
                    moved_this_side = 0
                    break 
                side = TOP
                ring_finished = True

            if cell.building.can_upgrade and \
                (cell.building.is_home or cell.building.level < me.tech_level) and \
                cell.building.upgrade_gold < me.gold and \
                cell.building.upgrade_energy < me.energy:
                cmd_list.append(game.upgrade(cell.position))
                print("We upgraded ({}, {})".format(cell.position.x, cell.position.y))
                me.gold   -= cell.building.upgrade_gold
                me.energy -= cell.building.upgrade_energy
            
            # Build a random building if we have enough gold
            if cell.owner == me.uid and cell.building.is_empty and me.gold >= 100:
                building = random.choice([BLD_FORTRESS, BLD_GOLD_MINE, BLD_ENERGY_WELL])
                cmd_list.append(game.build(cell.position, building))
                print("We build {} on ({}, {})".format(building, cell.position.x, cell.position.y))
                me.gold -= 100
            
        result = game.send_cmd(cmd_list)
        print(result)


 
    
        
            
