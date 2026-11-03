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



if variables.DEVELOP_MODE:
    xpy.control.set_develop_mode()
xpy.control.initialize(e)

#xpy.control.initialize(e)

#Design of the experiement

# DOTS stimuli

frame_a = xpy.stimuli.Canvas(size=variables.CANVAS_SIZE, colour=variables.BACKGROUND)
for x in variables.FRAME_A_X:
    xpy.stimuli.Circle(
        radius=variables.DOT_RADIUS,
        position=(x, variables.ITEM_Y),
        colour=variables.FOREGROUND,
    ).plot(frame_a)

frame_b = xpy.stimuli.Canvas(size=variables.CANVAS_SIZE, colour=variables.BACKGROUND)
for x in variables.FRAME_B_X:
    xpy.stimuli.Circle(
        radius=variables.DOT_RADIUS,
        position=(x, variables.ITEM_Y),
        colour=variables.FOREGROUND,
    ).plot(frame_b)


# SHAPES stimuli
#Creating a loop that will create the differents shape, so they are more easily called and created later.

def make_shape(kind, x):
    if kind == "circle":
        return xpy.stimuli.Circle(
            radius=variables.DOT_RADIUS,
            position=(x, variables.ITEM_Y),
            colour=variables.FOREGROUND,
        )
    if kind == "triangle":
        return xpy.stimuli.Shape(
            vertex_list=xpy.misc.geometry.vertices_regular_polygon(3, 54),
            position=(x, variables.ITEM_Y),
            colour=variables.FOREGROUND,
        )
    if kind == "square":
        return xpy.stimuli.Rectangle(
            size=(35, 35),
            position=(x, variables.ITEM_Y),
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
for stimulus in (frame_a, frame_b, frame_c, frame_d, fixation_screen,
                 blank_screen, instructions_screen, response_screen):
    stimulus.preload()


condition_frames = {
    "DOTS": (frame_a, frame_b),
    "SHAPES": (frame_c, frame_d),
}

#Function that allows to create a block with a number of trial that can be easily changed and in a randomized way
def make_block(condition):
    
    block = xpy.design.Block(name=condition)
    block.set_factor("condition", condition)
    for isi_ms in variables.ISI_VALUES_MS:
        trial = xpy.design.Trial()
        trial.set_factor("isi_ms", isi_ms)
        block.add_trial(trial, copies=variables.TRIALS_PER_ISI)
    block.shuffle_trials()
    return block



 #Creation of a function that shows one Ternus sequence; return (response, group_response, key, rt).
def run_trial(condition, isi_ms):
    first_frame, second_frame = condition_frames[condition]
 
    fixation_screen.present()
    e.clock.wait(variables.FIXATION_MS)
 
    for _ in range(variables.REPETITIONS):
        for frame in (first_frame, second_frame):
            frame.present()
            e.clock.wait(variables.FRAME_MS)
            if isi_ms > 0:  # ISI 0: the next image replaces this one directly
                fixation_screen.present()
                e.clock.wait(isi_ms)
 
    response_screen.present()
    key, rt = e.keyboard.wait(keys=list(variables.RESPONSE_CODING))
    response, group_response = variables.RESPONSE_CODING[key]
 
    blank_screen.present()
    e.clock.wait(variables.INTERTRIAL_MS)
    return response, group_response, key, rt
 


for condition in variables.CONDITIONS:
    e.add_block(make_block(condition))
 
xpy.control.start(skip_ready_screen=True)
 
# Counterbalancing: odd participant -> DOTS first, even -> SHAPES first
e.permute_blocks(xpy.design.permute.P_BALANCED_LATIN_SQUARE)
#check_design(e.blocks)
 
instructions_screen.present()
e.keyboard.wait(keys=[variables.START_KEY])
 
for block in e.blocks:
    condition = block.get_factor("condition")
    for trial in block.trials:
        isi_ms = trial.get_factor("isi_ms")
        response, group_response, key, rt = run_trial(condition, isi_ms)
        e.data.add([condition, trial.id, isi_ms, variables.FRAME_MS,
                             response, group_response, key, rt])
        e.data.save()

 
# Experiment end
xpy.control.end()
