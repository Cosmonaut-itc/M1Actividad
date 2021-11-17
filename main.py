import numpy as np
# Model design
import agentpy as ap
import time


class CleaningModel(ap.Model):

    def setup(self):
        n_roomba = self.p['Cleaners']
        n_tiles = int(self.p['Tile density'] * (self.p.size ** 2))
        self.movimientos = 0

        self.tiles = ap.AgentList(self, n_tiles)
        self.roomba = ap.AgentList(self, n_roomba)
        self.roomba.condition = 5
        self.tiles.condition = 0

        self.grid = self.roomba.grid = ap.Grid(self, [self.p.size] * 2, track_empty=True)

        self.grid.add_agents(self.tiles, random=True, empty=True)
        self.grid.add_agents(self.roomba, positions=[(0, 0) for i in range(self.p['Cleaners'])])

    def step(self):
        robots = self.roomba
        dirty_tiles = self.tiles.select(self.tiles.condition == 0)

        for robot in robots:
            flag = True
            dirty_tiles = self.tiles.select(self.tiles.condition == 0)
            while flag:
                pos = self.grid.positions[robot]
                rand_pos = np.random.randint(-1, 2, size=2)
                sum = tuple(map(lambda i, j: i + j, pos, rand_pos))
                if all(x >= y for x, y in zip(sum, tuple([0] * 2))) and all(x <= y for x, y in zip(sum, tuple([self.p.size-1] * 2))):
                    flag = False
                    pos = sum
                    var = self.grid.agents[pos[0], pos[1]].to_list()
                    n = var.select(var.condition == 0)
                    if len(n) != 0:
                        self.grid.move_by(robot, tuple(rand_pos))
                        n.condition = 1
                        self.movimientos += 1
                    else:
                        self.grid.move_by(robot, tuple(rand_pos))
                        self.movimientos += 1

        if len(dirty_tiles) == 0:
            self.stop()

    def end(self):
        burned_trees = len(self.tiles.select(self.tiles.condition == 1))
        self.report('Percentage of cleaned tiles',
                    burned_trees / len(self.tiles))
        self.report('time', time.time() - start)
        self.report('movimientos', self.movimientos)

parameters = {
    'Tile density': 0.8,  # Percentage of grid covered by trees
    'Cleaners': 1,
    'size': 10,  # Height and length of the grid
    'steps': 500,
}

start = time.time()
sample = ap.Sample(parameters, n=30)
# Perform experiment
exp = ap.Experiment(CleaningModel, sample, iterations=40)
results = exp.run()
results.save()
results = ap.DataDict.load('CleaningModel')
