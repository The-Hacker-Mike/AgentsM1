from mesa import Agent


class Rumba(Agent):

    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.direction = 4 	# start in the middle position, 0-8 tiles.
        self.pos = pos

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,  # set to False to exclude diagonals like the Bishop in chess.
            include_center=True)

        self.direction = (self.random.randint(0, len(possible_steps)-1))

        # clean dirty tiles
        for a in self.model.grid.get_cell_list_contents(self.pos):
            if (isinstance(a, tile) and a.condition == "Dirty"):
                a.condition = "Clean"

        self.model.grid.move_agent(self, possible_steps[self.direction])

    def step(self):
        self.move()


class tile(Agent):

    def __init__(self, pos, model):
        super().__init__(pos, model)
        self.pos = pos
        self.condition = "Clean"

    def step(self):
        pass
