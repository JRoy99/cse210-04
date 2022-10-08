import random
import os

DATA_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/data/highscore.txt"

class Director:
    """A person who directs the game. 
    
    The responsibility of a Director is to control the sequence of play.

    Attributes:
        _keyboard_service (KeyboardService): For getting directional input.
        _video_service (VideoService): For providing video output.
    """

    def __init__(self, keyboard_service, video_service):
        """Constructs a new Director using the specified keyboard and video services.
        
        Args:
            keyboard_service (KeyboardService): An instance of KeyboardService.
            video_service (VideoService): An instance of VideoService.
        """
        self._keyboard_service = keyboard_service
        self._video_service = video_service
        
    def start_game(self, cast):
        """Starts the game using the given cast. Runs the main game loop.

        Args:
            cast (Cast): The cast of actors.
        """
        self._video_service.open_window()
        while self._video_service.is_window_open():
            self._get_inputs(cast)
            self._do_updates(cast)
            self._do_outputs(cast)
        self._video_service.close_window()

    def _get_inputs(self, cast):
        """Gets directional input from the keyboard and applies it to the robot.
        
        Args:
            cast (Cast): The cast of actors.
        """
        robot = cast.get_first_actor("robots")
        velocity = self._keyboard_service.get_direction()
        if (velocity.get_y() == 0):
            robot.set_velocity(velocity)        

    def _do_updates(self, cast):
        """Updates the robot's position and resolves any collisions with artifacts.
        
        Args:
            cast (Cast): The cast of actors.
        """
        banner = cast.get_first_actor("banners")
        robot = cast.get_first_actor("robots")
        objects = cast.get_actors("objects")

        banner.set_text("")
        max_x = self._video_service.get_width()
        max_y = self._video_service.get_height()
        robot.move_next(max_x, max_y)

        with open(DATA_PATH,"r") as f:
            high_score = int(f.readline())
        if robot.get_score() > high_score:
            with open(DATA_PATH,"w") as f:
                f.write(str(robot.get_score()))
        #banner.set_text(f"MAX X: {max_x} MAX Y: {max_y}")    
        banner.set_text(f"SCORE: {robot.get_score()} HIGH SCORE: {high_score}")     
        #banner.set_text(f"X: {robot.get_position().get_x()} Y: {robot.get_position().get_y()}")     
        
        for object in objects:
            try:
                if (object.get_position().get_x() == robot.get_position().get_x() and 
                object.get_position().get_y() >= robot.get_position().get_y() - 5):
                    robot.set_score(robot.get_score() + object.get_score())
                    cast.remove_actor("objects", object)
            except:
                pass
            try:
                if object.get_position().get_y() == max_y:
                    cast.remove_actor("objects", object)
                else:
                    object.move_next(max_x, max_y+1)   
            except:
                pass             

        cast.add_actor("objects", object)
        
    def _do_outputs(self, cast):
        """Draws the actors on the screen.
        
        Args:
            cast (Cast): The cast of actors.
        """
        self._video_service.clear_buffer()
        actors = cast.get_all_actors()
        self._video_service.draw_actors(actors)
        self._video_service.flush_buffer()