import csv
class DataCollector:
    def __init__(self):
        self.filename = "agentsData.cvs"
    def writeLine(self,pacman_pos_x,pacman_pos_y,ghost1_pos_x,ghost1_pos_y,distance_ghost_1,ghost2_pos_x,ghost2_pos_y,distance_ghost_2,
    distance_ghost_scared,distance_ghost_scared_2,closest_food1_x,closest_food1_y,capsule1_pos_x,capsule1_pos_y,
    distance_capsule_1,capsule2_pos_x,capsule2_pos_y,distance_capsule_2,score,direction):
        with open(self.filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([pacman_pos_x,pacman_pos_y,ghost1_pos_x,ghost1_pos_y,distance_ghost_1,ghost2_pos_x,ghost2_pos_y,distance_ghost_2,distance_ghost_scared,distance_ghost_scared_2,closest_food1_x,closest_food1_y,capsule1_pos_x,capsule1_pos_y,distance_capsule_1,capsule2_pos_x,capsule2_pos_y,distance_capsule_2,score,direction])

#test=DataCollector()
#test.writeLine(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
