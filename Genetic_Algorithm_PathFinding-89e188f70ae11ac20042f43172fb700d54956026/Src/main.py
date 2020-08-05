from Game import *
g = Game(1,20) #Dificultad y cantidad de robots por generación
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()

