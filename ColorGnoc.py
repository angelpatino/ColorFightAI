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
game.connect(room = 'nopublic')

if game.register(username = 'AngelP123' + str(random.randint(1, 100)), \
        password = 'YeeHaw'):




    while True:
        cmd_list = []
        my_attack_list = []
        game.update_turn()
        if game.me == None:
            continue
        me = game.me
        if is_first_move:
            print(len(game.me.cells))
            for cell in game.me.cells.values():
                home = cell.position
                print("home: ", home.x, home.y)
                position = home

                is_first_move = False

        while continue_moving:
            
            if side == TOP:
                for i in range(ring - moved_this_side):
                    position.x = position.x-1
                    if (position.x >= 0 and position.x < game.game_map.width and position.y >= 0 and position.y < game.game_map.height):
                        c = game.game_map[position]
                        print("Checking cell ({}, {})".format(position.x, position.y))
                        if c.attack_cost < me.energy and c.owner != game.uid and me.energy > MIN_ENERGY:
                            cmd_list.append(game.attack(position, c.attack_cost))
                            print("We are attacking ({}, {}) with {} energy".format(position.x, position.y, c.attack_cost))
                            game.me.energy -= c.attack_cost
                            my_attack_list.append(c.position)
                        else:
                            # save everything
                            moved_this_side = i
                            is_stopping = True
                            break
                if is_stopping:
                    break           
                
                if ring_finished:
                    position.y = position.y + 1
                    ring_finished = False
                    ring += 1 
                    for i in range(ring):
                        position.x = position.x-1
                        if (position.x >= 0 and position.x < game.game_map.width and position.y >= 0 and position.y < game.game_map.height):
                            # print("left", position.x, position.y)
                            c = game.game_map[position]
                            print("Checking cell ({}, {})".format(position.x, position.y))
                            if c.attack_cost < me.energy and c.owner != game.uid and me.energy > MIN_ENERGY:
                                cmd_list.append(game.attack(position, c.attack_cost))
                                print("We are attacking ({}, {}) with {} energy".format(position.x, position.y, c.attack_cost))
                                game.me.energy -= c.attack_cost
                                my_attack_list.append(c.position)
                side = LEFT
            
            if side == LEFT:
                for i in range(2*ring):
                    position.y = position.y-1
                    if (position.x >= 0 and position.x < game.game_map.width and position.y >= 0 and position.y < game.game_map.height):
                        # print("down", position.x, position.y)
                        c = game.game_map[position]
                        if c.attack_cost < me.energy and c.owner != game.uid and me.energy > MIN_ENERGY:
                            cmd_list.append(game.attack(position, c.attack_cost))
                            print("We are attacking ({}, {}) with {} energy".format(position.x, position.y, c.attack_cost))
                            game.me.energy -= c.attack_cost
                            my_attack_list.append(c.position)
                side = BOTTOM

            if side == BOTTOM:
                for i in range(2*ring):
                    position.x = position.x+1
                    if (position.x >= 0 and position.x < game.game_map.width and position.y >= 0 and position.y < game.game_map.height):
                        c = game.game_map[position]
                        print("Checking cell ({}, {})".format(position.x, position.y))
                        if c.attack_cost < me.energy and c.owner != game.uid and me.energy > MIN_ENERGY:
                            cmd_list.append(game.attack(position, c.attack_cost))
                            print("We are attacking ({}, {}) with {} energy".format(position.x, position.y, c.attack_cost))
                            game.me.energy -= c.attack_cost
                            my_attack_list.append(c.position)
                side = RIGHT

            if side == RIGHT:
                for i in range(2*ring):
                    position.y = position.y+1
                    if (position.x >= 0 and position.x < game.game_map.width and position.y >= 0 and position.y < game.game_map.height):
                        c = game.game_map[position]
                        if c.attack_cost < me.energy and c.owner != game.uid and me.energy > MIN_ENERGY:
                            cmd_list.append(game.attack(position, c.attack_cost))
                            print("We are attacking ({}, {}) with {} energy".format(position.x, position.y, c.attack_cost))
                            game.me.energy -= c.attack_cost
                            my_attack_list.append(c.position)
                side = TOP
                ring_finished = True

        for cell in game.me.cells.values():
            # Check the surrounding position
            for pos in cell.position.get_surrounding_cardinals():
                c = game.game_map[pos] 
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




        # act from current position

 
    
        
            