import random
import expyriment as xpy
import variables

# Experiment initialization
e = xpy.design.Experiment(
    name=variables.EXPERIMENT_NAME , 
    background_colour=variables.BACKGROUND, 
    foreground_colour=variables.FOREGROUND
    )

e.data_variable_names = [
    "condition", 
    "trial", 
    "isi_ms", 
    "frame_ms", 
    "response", 
    "group_response", 
    "key", 
    "rt_ms"]


xpy.control.initialize(e)

# DOTS stimuli

frame_a = xpy.stimuli.Canvas(size=variables.CANVAS_SIZE, colour=variables.BACKGROUND)
for x in variables.FRAME_A_X:
    xpy.stimuli.Circle(
        radius=variables.DOT_RADIUS,
        position=(x, 0),
        colour=variables.FOREGROUND,
    ).plot(frame_a)

frame_b = xpy.stimuli.Canvas(size=variables.CANVAS_SIZE, colour=variables.BACKGROUND)
for x in variables.FRAME_B_X:
    xpy.stimuli.Circle(
        radius=variables.DOT_RADIUS,
        position=(x, 0),
        colour=variables.FOREGROUND,
    ).plot(frame_b)


# SHAPES stimuli
#Creating a loop that will create the differents shape, so they are more easily called and created later.

def make_shape(kind, x):
    if kind == "circle":
        return xpy.stimuli.Circle(
            radius=variables.DOT_RADIUS,
            position=(x, 0),
            colour=variables.FOREGROUND,
        )
    if kind == "triangle":
        return xpy.stimuli.Shape(
            vertex_list=xpy.misc.geometry.vertices_regular_polygon(3, 54),
            position=(x, 0),
            colour=variables.FOREGROUND,
        )
    if kind == "square":
        return xpy.stimuli.Rectangle(
            size=(35, 35),
            position=(x, 0),
            colour=variables.FOREGROUND,
        )
    raise ValueError(f"Unknown shape kind: {kind}")

frame_c = xpy.stimuli.Canvas(size=variables.CANVAS_SIZE, colour=variables.BACKGROUND)
for kind, x in variables.FRAME_C_SHAPES:
    make_shape(kind, x).plot(frame_c)

frame_d = xpy.stimuli.Canvas(size=variables.CANVAS_SIZE, colour=variables.BACKGROUND)
for kind, x in variables.FRAME_D_SHAPES:
    make_shape(kind, x).plot(frame_d)




# Fixation cross
def make_fixation():
    return xpy.stimuli.FixCross(size=variables.CROSS_SIZE,
                                line_width=variables.CROSS_WIDTH,
                                colour=variables.FOREGROUND)


# Fixation cross alone (gap between images) and blank screen (inter-trial)
fixation_screen = xpy.stimuli.BlankScreen(colour=variables.BACKGROUND)
make_fixation().plot(fixation_screen)
blank_screen = xpy.stimuli.BlankScreen(colour=variables.BACKGROUND)


# Fixation on stimulus screen
make_fixation().plot(frame_a)
make_fixation().plot(frame_b)
make_fixation().plot(frame_c)
make_fixation().plot(frame_d)

#Instruction and response screens 
instructions_screen = xpy.stimuli.TextScreen(
    heading=variables.INSTRUCTIONS_HEADING, text=variables.INSTRUCTIONS_TEXT)
response_screen = xpy.stimuli.TextScreen(
    heading=variables.RESPONSE_HEADING, text=variables.RESPONSE_TEXT)


# Preloading
screen1.preload()
screen2.preload()
screen3.preload()
screen4.preload()
screen5.preload()
text1.preload()
text2.preload()
screen6.preload()

# DOTS block and trial construction
b1 = xpy.design.Block(name="DOTS")
b1.set_factor("condition", "DOTS")
for v in [0, 0, 0, 0, 0, 50, 50, 50, 50, 50, 500, 500, 500, 500, 500, 1000, 1000, 1000, 1000, 1000]:
    t = xpy.design.Trial()
    t.set_factor("isi_ms", v)
    b1.add_trial(t)

# Randomization of DOTS trials
for i in range(len(b1.trials) - 1, 0, -1):
    j = random.randint(0, i)
    b1.trials[i], b1.trials[j] = b1.trials[j], b1.trials[i]

# SHAPES block and trial construction
b2 = xpy.design.Block(name="SHAPES")
b2.set_factor("condition", "SHAPES")
for v in [0, 0, 0, 0, 0, 50, 50, 50, 50, 50, 500, 500, 500, 500, 500, 1000, 1000, 1000, 1000, 1000]:
    t = xpy.design.Trial()
    t.set_factor("isi_ms", v)
    b2.add_trial(t)

# Randomization of SHAPES trials
for i in range(len(b2.trials) - 1, 0, -1):
    j = random.randint(0, i)
    b2.trials[i], b2.trials[j] = b2.trials[j], b2.trials[i]

# Stimuli for DOTS trials
for t in b1.trials:
    t.add_stimulus(screen1)
    t.add_stimulus(screen2)
    t.add_stimulus(screen5)
    t.add_stimulus(text2)
    t.add_stimulus(screen5)
    t.add_stimulus(screen6)

# Stimuli for SHAPES trials
for t in b2.trials:
    t.add_stimulus(screen3)
    t.add_stimulus(screen4)
    t.add_stimulus(screen5)
    t.add_stimulus(text2)
    t.add_stimulus(screen5)
    t.add_stimulus(screen6)

# Experiment start
e.add_block(b1)
e.add_block(b2)
xpy.control.start(skip_ready_screen=True)

# Counterbalancing
if e.subject % 2 == 0:
    e.blocks.reverse()

# Instructions
text1.present()
e.keyboard.wait(keys=[xpy.misc.constants.K_SPACE])

# Trial presentation
for b in e.blocks:
    for t in b.trials:
        v = t.get_factor("isi_ms")
        t.stimuli[2].present()
        e.clock.wait(200)

        for i in range(3):
            t.stimuli[0].present()
            e.clock.wait(250)
            if v > 0:
                t.stimuli[4].present()
                e.clock.wait(v)

            t.stimuli[1].present()
            e.clock.wait(250)
            if v > 0:
                t.stimuli[4].present()
                e.clock.wait(v)

        # Response collection
        t.stimuli[3].present()
        k, r = e.keyboard.wait(keys=[xpy.misc.constants.K_LEFT, xpy.misc.constants.K_RIGHT])

        if k == xpy.misc.constants.K_LEFT:
            a = "element"
            g = 0
        else:
            a = "group"
            g = 1

        # Intertrial interval
        t.stimuli[5].present()
        e.clock.wait(500)
        # Data saving
        e.data.add([b.get_factor("condition"), t.id, v, 250, a, g, k, r])
        e.data.save()

# Experiment end
xpy.control.end()
