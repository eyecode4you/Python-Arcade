from game import Game
from main_menu import MainMenu

game = Game("PyInvaders", 800, 800)
main_menu = MainMenu()

game.run(main_menu)
