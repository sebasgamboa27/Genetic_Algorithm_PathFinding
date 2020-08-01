from Game import *
# create the game object
g = Game(1,15) #Dificultad y cantidad de robots por generación
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()

