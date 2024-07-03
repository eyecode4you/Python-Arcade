from game import Game
from main_menu import MainMenu
from second_menu import SecondMenu

game = Game("PyInvaders", 800, 800)
main_menu = MainMenu()
second_menu = SecondMenu()

main_menu.second_menu = second_menu
second_menu.main_menu = main_menu

game.run(main_menu)