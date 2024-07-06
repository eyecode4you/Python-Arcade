from game import Game
from main_menu import MainMenu
from game_play import GamePlay
import settings

game = Game("PyInvaders", settings.screen_size[0], settings.screen_size[1])
main_menu = MainMenu(game.screen)
game_play = GamePlay(game.screen)
main_menu.gameplay_scene = game_play
game_play.main_menu = main_menu

game.run(main_menu)