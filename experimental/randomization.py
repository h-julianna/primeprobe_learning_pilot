import random
import json
import pandas as pd

# global variables to be manipulated
stimulus_set = []
relay = 0

# defining stimulus set

# neutral probes
vertical_con_list = [
    {"prime":"le", "probe":"le", "congruency":"congruent", "correct_response":"n", "name":"vertical_con_1", "color":"neutral"},
    {"prime":"fel", "probe":"fel", "congruency":"congruent", "correct_response":"j", "name":"vertical_con_2", "color":"neutral"}
]
vertical_inc_list = [
    {"prime":"fel", "probe":"le", "congruency":"incongruent", "correct_response":"n", "name":"vertical_incon_1", "color":"neutral"},
    {"prime":"le", "probe":"fel", "congruency":"incongruent", "correct_response":"j", "name":"vertical_incon_2", "color":"neutral"}
]

horizontal_con_list = [
    {"prime": "bal", "probe": "bal", "congruency":"congruent", "correct_response":"f", "name": "horizontal_con_1", "color":"neutral"},
    {"prime": "jobb", "probe": "jobb", "congruency":"congruent", "correct_response":"g", "name": "horizontal_con_2", "color":"neutral"}
]
horizontal_incon_list = [
    {"prime": "bal", "probe": "jobb", "congruency":"incongruent", "correct_response":"g", "name": "horizontal_incon_1", "color":"neutral"},
    {"prime": "jobb", "probe": "bal", "congruency":"incongruent", "correct_response":"f", "name":"horizontal_incon_2", "color":"neutral"}
]

# red probes
red_vertical_con = [
    {"prime":"le", "probe":"le", "congruency":"congruent", "correct_response":"n", "name":"red_vertical_con_1", "color":"red"},
    {"prime":"fel", "probe":"fel", "congruency":"congruent", "correct_response":"j", "name":"red_vertical_con_2", "color":"red"}
]
red_vertical_incon = [
    {"prime":"fel", "probe":"le", "congruency":"incongruent", "correct_response":"n", "name":"red_vertical_incon_1", "color":"red"},
    {"prime":"le", "probe":"fel", "congruency":"incongruent", "correct_response":"j", "name":"red_vertical_incon_2", "color":"red"}
]

red_horizontal_con = [
    {"prime":"bal", "probe":"bal", "congruency":"congruent", "correct_response":"f", "name":"red_horizontal_con_1", "color":"red"},
    {"prime":"jobb", "probe":"jobb", "congruency":"congruent", "correct_response":"g", "name":"red_horizontal_con_2", "color":"red"}
]
red_horizontal_incon = [
    {"prime":"bal", "probe":"jobb", "congruency":"incongruent", "correct_response":"g", "name":"red_horizontal_incon_1", "color":"red"},
    {"prime":"jobb", "probe":"bal", "congruency":"incongruent", "correct_response":"f", "name":"red_horizontal_incon_2", "color":"red"}
]

# grouping congruent and incongruent stimuli together
vertical_group = [vertical_con_list, vertical_inc_list, red_vertical_con, red_vertical_incon]
horizontal_group = [horizontal_con_list, horizontal_incon_list, red_horizontal_con, red_horizontal_incon]

# trial counts
trial_rate = []
trial_count = 91

# neutral: 65 trials (33 congruent, 32 incongruent)
NEUTRAL_CON_REMAIN = 33
NEUTRAL_INC_REMAIN = 32

# red: 26 trials (13 congruent, 13 incongruent)
RED_CON_REMAIN = 13
RED_INC_REMAIN = 13

# functions

def stimulus_finder(group, color_tag):
    """Append one stimulus from group according to color_tag."""
    global stimulus_set
    global NEUTRAL_CON_REMAIN, NEUTRAL_INC_REMAIN, RED_CON_REMAIN, RED_INC_REMAIN

    if color_tag == "neutral":
        choices = []
        if NEUTRAL_CON_REMAIN > 0:
            choices.append((0, group[0]))  # congruent neutral
        if NEUTRAL_INC_REMAIN > 0:
            choices.append((1, group[1]))  # incongruent neutral
        if not choices:
            return False
        cong, lst = random.choice(choices)
        stimulus_set.append(random.choice(lst))
        if cong == 0:
            NEUTRAL_CON_REMAIN -= 1
        else:
            NEUTRAL_INC_REMAIN -= 1
        return True

    elif color_tag == "red":
        choices = []
        if RED_CON_REMAIN > 0:
            choices.append((2, group[2]))  # congruent red
        if RED_INC_REMAIN > 0:
            choices.append((3, group[3]))  # incongruent red
        if not choices:
            return False
        cong, lst = random.choice(choices)
        stimulus_set.append(random.choice(lst))
        if cong == 2:
            RED_CON_REMAIN -= 1
        else:
            RED_INC_REMAIN -= 1
        return True
    else:
        return False

def group_relay():
    """Pick horizontal or vertical group per relay, choose color according to remaining quotas."""
    global relay
    total_neutral = NEUTRAL_CON_REMAIN + NEUTRAL_INC_REMAIN
    total_red = RED_CON_REMAIN + RED_INC_REMAIN

    if total_neutral <= 0 and total_red <= 0:
        return False
    if total_neutral <= 0:
        color_tag = "red"
    elif total_red <= 0:
        color_tag = "neutral"
    else:
        color_tag = "neutral" if random.random() < (total_neutral/(total_neutral + total_red)) else "red"

    if relay == 0:
        group = horizontal_group
        relay = 1
    else:
        group = vertical_group
        relay = 0

    ok = stimulus_finder(group, color_tag)
    if not ok:
        other = "red" if color_tag == "neutral" else "neutral"
        stimulus_finder(group, other)
    return True

def set_factory(times):
    for _ in range(times):
        if (NEUTRAL_CON_REMAIN + NEUTRAL_INC_REMAIN + RED_CON_REMAIN + RED_INC_REMAIN) <= 0:
            break
        group_relay()

# creating an infinite loop to find a correct trial set
match_count = 0
while True:
    stimulus_set = []
    # reset quotas each block
    NEUTRAL_CON_REMAIN = 33
    NEUTRAL_INC_REMAIN = 32
    RED_CON_REMAIN = 13
    RED_INC_REMAIN = 13

    set_factory(trial_count)
    trial_block = pd.DataFrame(stimulus_set, columns=["prime", "probe", "congruency", "correct_response", "color"])
    trial_block["previous_congruency"] = trial_block["congruency"].shift(1)
    trial_block["con_pair"] = trial_block["previous_congruency"] + "-" + trial_block["congruency"]
    pair_counts = trial_block["con_pair"].value_counts()

    # ensure each pair occurs the expected number of times
    expected = {
        "congruent-congruent": 23,
        "congruent-incongruent": 23,
        "incongruent-congruent": 22,
        "incongruent-incongruent": 22
    }
    
    matches = all(pair_counts.get(k,0) == v for k,v in expected.items())
    if matches:
        match_count += 1
        print("Match found: {}".format(match_count))
        print("Correct paircount found, writing...")
    # check if all expected pairs exist
    path = "trials.json"
    try:
          with open(path, "r") as f:
                file_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
          file_data = {"trials": []}

    file_data["trials"].append(stimulus_set)

    with open(path, "w") as f:
            json.dump(file_data, f, indent=2)

    stimulus_set = []