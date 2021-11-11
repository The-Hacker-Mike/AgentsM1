from mesa import Model
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation
from mesa.space import MultiGrid  # used to be Grid, was modified.
from agent import Rumba, tile


class RandomFloorModel(Model):

    def __init__(self, height=100, width=100, density=0.65, n_rumbas=1, counter=0, max=100):

        self.num_rumbas = n_rumbas
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(height, width, torus=False)
        self.counter = 0
        self.max = max

        self.datacollector = DataCollector(
            {
                "Dirty": lambda m: self.count_type(m, "Dirty"),
                "Clean": lambda m: self.count_type(m, "Clean"),
            }
        )

        for i in range(self.num_rumbas):
            agent = Rumba(i, (1, 1), self)
            self.schedule.add(agent)
            self.grid.place_agent(agent, (1, 1))

        for (contents, x, y) in self.grid.coord_iter():
            new_tile = tile((x, y), self)

            if self.random.random() < density:
                new_tile.condition = "Dirty"

            self.schedule.add(new_tile)
            self.grid.place_agent(new_tile, (x, y))

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

        if self.count_type(self, "Dirty") == 0:
            self.running = False

        if self.counter == self.max:
            print(f"The max was reached: {self.counter}")
            self.running = False
        else:
            self.counter += 1

    @staticmethod
    def count_type(model, cond):
        count = 0
        for ft in model.schedule.agents:
            if(isinstance(ft, tile)):
                if ft.condition == cond:
                    count += 1
        return count
