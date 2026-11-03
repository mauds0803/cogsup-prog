from expyriment.misc import constants

EXPERIMENT_NAME = "Ternus self-test"

BACKGROUND = (0, 0, 0)
FOREGROUND = (255, 255, 255)

ITEM_Y = -50
CANVAS_SIZE = (600, 300)
DOT_RADIUS = 20
FRAME_A_X = (-120, -40, 40)
FRAME_B_X = (-40, 40, 120)
FRAME_C_SHAPES = [("circle", -120), ("triangle", -40), ("square", 40)]
FRAME_D_SHAPES = [("triangle", -40), ("square", 40), ("circle", 120), ]
FRAME_MS = 250

CROSS_SIZE = (20, 20)
CROSS_WIDTH = 4


INSTRUCTIONS_HEADING = "Ternus experiment"
INSTRUCTIONS_TEXT = (
    "Keep your eyes on the central cross.\n\n"
    "LEFT = element motion\nRIGHT = group motion\n\n"
    "Press SPACE to start."
)
RESPONSE_HEADING = "What did you see?"
RESPONSE_TEXT = "LEFT = element motion\nRIGHT = group motion"

CONDITIONS = ("DOTS", "SHAPES")

ISI_VALUES_MS = (0, 50, 500, 1000)
TRIALS_PER_ISI = 1
DEVELOP_MODE = False

FRAME_MS = 250
FIXATION_MS = 200
INTERTRIAL_MS = 500
REPETITIONS = 3


RESPONSE_CODING = {
    constants.K_LEFT: ("element", 0),
    constants.K_RIGHT: ("group", 1),
}
START_KEY = constants.K_SPACE
 