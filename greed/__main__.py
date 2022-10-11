import os
import random

from game.casting.actor import Actor
from game.casting.object import Object
from game.casting.cast import Cast

from game.directing.director import Director

from game.services.keyboard_service import KeyboardService
from game.services.video_service import VideoService

from game.shared.color import Color
from game.shared.point import Point


FRAME_RATE = 30
MAX_X = 1200
MAX_Y = 600
CELL_SIZE = 40
FONT_SIZE = 40
COLS = 30
ROWS = 15
CAPTION = "Greed"

WHITE = Color(255, 255, 255)
MAX_OBJECTS = 50 # Maximum objects on screen

def spawn_objects(cast, current_objects, curr_score):
# create the objects


    for n in range(current_objects, MAX_OBJECTS):
        x = random.randint(1, COLS - 1)
        y = random.randint(1, int((ROWS - 1)/3))
        position = Point(x, y)
        position = position.scale(CELL_SIZE)

        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        color = Color(r, g, b)
        
        object = Object()

        #Weight object spawning using current score
        gem_chance = 100 - curr_score / 10
        rock_chance = curr_score
        if gem_chance < 10:
            gem_chance = 10
            rock_chance = 90
        elif rock_chance < 10:
            rock_chance = 10
            gem_chance = 90
        object.set_text(''.join(random.choices(["*", "o"], weights = (gem_chance, rock_chance), k=1)))

        #Set score values
        if object.get_text() == "*":            
            object.set_score(random.randint(1, 5))
        else:
            object.set_score(random.randint(-5, -1))

        object.set_font_size(FONT_SIZE)
        object.set_color(color)
        object.set_position(position)
        object.set_velocity(Point(0, abs(object.get_score())))


        cast.add_actor("objects", object)

def main():
    
    # create the cast
    cast = Cast()
    
    # create the banner
    banner = Actor()
    banner.set_text("")
    banner.set_font_size(FONT_SIZE)
    banner.set_color(WHITE)
    banner.set_position(Point(CELL_SIZE, 0))
    cast.add_actor("banners", banner)
    
    # create the robot
    x = int(MAX_X / 2)
    y = int(MAX_Y - CELL_SIZE)
    position = Point(x, y)

    robot = Actor()
    robot.set_text("#")
    robot.set_font_size(FONT_SIZE)
    robot.set_color(WHITE)
    robot.set_position(position)
    cast.add_actor("robots", robot)
    
    spawn_objects(cast, 0, 0)
    
    # start the game
    keyboard_service = KeyboardService(CELL_SIZE)
    video_service = VideoService(CAPTION, MAX_X, MAX_Y, CELL_SIZE, FRAME_RATE)
    director = Director(keyboard_service, video_service)
    director.start_game(cast)


if __name__ == "__main__":
    main()