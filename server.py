from agent import Rumba, tile
from model import RandomFloorModel
from mesa.visualization.modules import CanvasGrid, ChartModule, PieChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter


colors = {"Dirty": "#808080", "Clean": "#299438"}


def floor_portrayal(agent):
    if agent is None:
        return

    portrayal = {"Shape": "rect",
                 "w": 1,
                 "h": 1,
                 "Filled": "true",
                 "Layer": 0}

    if (isinstance(agent, tile)):

        (x, y) = agent.pos
        portrayal["x"] = x
        portrayal["y"] = y
        portrayal["Color"] = colors[agent.condition]

    elif (isinstance(agent, Rumba)):

        portrayal["Color"] = "red"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.7
        portrayal["Shape"] = "circle"

    return portrayal


canvas_element = CanvasGrid(floor_portrayal, 10, 10, 500, 500)

tree_chart = ChartModule(
    [{"Label": label, "Color": color} for (label, color) in colors.items()])

pie_chart = PieChartModule(
    [{"Label": label, "Color": color} for (label, color) in colors.items()])

model_params = {"height": UserSettableParameter("slider", "Height", 10, 100, 500, 1),
                "width": UserSettableParameter("slider", "Width", 10, 100, 500, 1),
                "density": UserSettableParameter("slider", "Dirt density", 0.65, 0.01, 1.0, 0.01),
                "n_rumbas": UserSettableParameter("slider", "Rubma noº", 1, 1, 10, 1),
                "max": UserSettableParameter("slider", "max", 120, 100, 500, 10)
                }

server = ModularServer(RandomFloorModel, [canvas_element, tree_chart,
                       pie_chart], "Rumba cleaning", model_params)

server.launch()
