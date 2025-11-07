import random
import json
import pandas as pd

# global
TRIALS_PER_SET = 100
TOTAL_SETS = 500
RED_TRIALS = 30  

# defining the stimuli
vertical_con_list = [
    {"prime": "le\nle\nle", "probe": "le", "congruency": "congruent", "correct_response": "n", "name": "vertical_con_1", "color": "black"},
    {"prime": "fel\nfel\nfel", "probe": "fel", "congruency": "congruent", "correct_response": "j", "name": "vertical_con_2", "color": "black"}
]
vertical_inc_list = [
    {"prime": "fel\nfel\nfel", "probe": "le", "congruency": "incongruent", "correct_response": "n", "name": "vertical_incon_1", "color": "black"},
    {"prime": "le\nle\nle", "probe": "fel", "congruency": "incongruent", "correct_response": "j", "name": "vertical_incon_2", "color": "black"}
]
horizontal_con_list = [
    {"prime": "bal\nbal\nbal", "probe": "bal", "congruency": "congruent", "correct_response": "f", "name": "horizontal_con_1", "color": "black"},
    {"prime": "jobb\njobb\njobb", "probe": "jobb", "congruency": "congruent", "correct_response": "g", "name": "horizontal_con_2", "color": "black"}
]
horizontal_incon_list = [
    {"prime": "bal\nbal\nbal", "probe": "jobb", "congruency": "incongruent", "correct_response": "g", "name": "horizontal_incon_1", "color": "black"},
    {"prime": "jobb\njobb\njobb", "probe": "bal", "congruency": "incongruent", "correct_response": "f", "name": "horizontal_incon_2", "color": "black"}
]

# defining the red stimuli
red_vertical_con = [
    {"prime": "le\nle\nle", "probe": "le", "congruency": "congruent", "correct_response": "n", "name": "red_vertical_con_1", "color": "red"},
    {"prime": "fel\nfel\nfel", "probe": "fel", "congruency": "congruent", "correct_response": "i", "name": "red_vertical_con_2", "color": "red"}
]
red_vertical_incon = [
    {"prime": "fel\nfel\nfel", "probe": "le", "congruency": "incongruent", "correct_response": "n", "name": "red_vertical_incon_1", "color": "red"},
    {"prime": "le\nle\nle", "probe": "fel", "congruency": "incongruent", "correct_response": "i", "name": "red_vertical_incon_2", "color": "red"}
]
red_horizontal_con = [
    {"prime": "bal\nbal\nbal", "probe": "bal", "congruency": "congruent", "correct_response": "d", "name": "red_horizontal_con_1", "color": "red"},
    {"prime": "jobb\njobb\njobb", "probe": "jobb", "congruency": "congruent", "correct_response": "a", "name": "red_horizontal_con_2", "color": "red"}
]
red_horizontal_incon = [
    {"prime": "bal\nbal\nbal", "probe": "jobb", "congruency": "incongruent", "correct_response": "d", "name": "red_horizontal_incon_1", "color": "red"},
    {"prime": "jobb\njobb\njobb", "probe": "bal", "congruency": "incongruent", "correct_response": "a", "name": "red_horizontal_incon_2", "color": "red"}
]


# helping function to split 100 into halves
def half_split(n):
    return n // 2, n - n // 2


# generating a single trial block
def generate_trial_block(trial_count=TRIALS_PER_SET):
    random.seed()  # ensure fresh randomness each time

    red_total = RED_TRIALS
    non_red_total = trial_count - red_total
    vertical_total = trial_count // 2
    horizontal_total = trial_count - vertical_total

    # red distribution
    red_con_total = red_total // 2
    red_inc_total = red_total - red_con_total
    red_vertical_total = red_total // 2
    red_horizontal_total = red_total - red_vertical_total

    v_red_con = red_con_total // 2
    h_red_con = red_con_total - v_red_con
    v_red_inc = red_vertical_total - v_red_con
    h_red_inc = red_horizontal_total - h_red_con

    # neutral (black) distribution
    non_red_vertical_total = vertical_total - red_vertical_total
    non_red_horizontal_total = horizontal_total - red_horizontal_total

    non_red_con_total, non_red_inc_total = half_split(non_red_total)

    v_non_con = int(non_red_con_total * (non_red_vertical_total / non_red_total))
    v_non_inc = int(non_red_inc_total * (non_red_vertical_total / non_red_total))
    h_non_con = non_red_con_total - v_non_con
    h_non_inc = non_red_inc_total - v_non_inc

    # fix rounding drift
    while (v_non_con + v_non_inc) != non_red_vertical_total:
        v_non_inc += 1 if (v_non_con + v_non_inc) < non_red_vertical_total else -1
    while (h_non_con + h_non_inc) != non_red_horizontal_total:
        h_non_inc += 1 if (h_non_con + h_non_inc) < non_red_horizontal_total else -1

    # sample trials (with replacement)
    red_trials = (
        random.choices(red_vertical_con, k=v_red_con) +
        random.choices(red_vertical_incon, k=v_red_inc) +
        random.choices(red_horizontal_con, k=h_red_con) +
        random.choices(red_horizontal_incon, k=h_red_inc)
    )

    non_red_trials = (
        random.choices(vertical_con_list, k=v_non_con) +
        random.choices(vertical_inc_list, k=v_non_inc) +
        random.choices(horizontal_con_list, k=h_non_con) +
        random.choices(horizontal_incon_list, k=h_non_inc)
    )

    # combine and shuffle everything
    all_trials = red_trials + non_red_trials
    random.shuffle(all_trials)

    # ensure no two red trials are consecutive
    for i in range(1, len(all_trials)):
        if all_trials[i]["color"] == "red" and all_trials[i - 1]["color"] == "red":
            for j in range(i + 1, len(all_trials)):
                if all_trials[j]["color"] != "red" and (j == len(all_trials) - 1 or all_trials[j + 1]["color"] != "red"):
                    all_trials[i], all_trials[j] = all_trials[j], all_trials[i]
                    break

    # adding one guaranteed black trial at the beginning
    first_black_trial = random.choice(
        vertical_con_list + vertical_inc_list + horizontal_con_list + horizontal_incon_list
    )
    all_trials.insert(0, first_black_trial)

    return all_trials


# double checking the balance of a trial block
def check_balance(trials):
    df = pd.DataFrame(trials)
    red_df = df[df.get("color") == "red"]
    non_red_df = df[df.get("color") != "red"]

    def count_df(sub_df):
        return {
            "congruent": (sub_df["congruency"] == "congruent").sum(),
            "incongruent": (sub_df["congruency"] == "incongruent").sum(),
            "vertical": sub_df["name"].str.contains("vertical").sum(),
            "horizontal": sub_df["name"].str.contains("horizontal").sum()
        }

    return {"red": count_df(red_df), "non_red": count_df(non_red_df)}


# saving to json and generating the file if not found
def save_trials_to_json(all_sets, file_path="trials.json"):
    try:
        with open(file_path, "r") as f:
            file_data = json.load(f)
        if "trials" not in file_data:
            file_data = {"trials": []}
    except (FileNotFoundError, json.JSONDecodeError):
        file_data = {"trials": []}
    file_data["trials"].extend(all_sets)
    with open(file_path, "w") as f:
        json.dump(file_data, f, indent=2)


# generating all the trial sets
all_trial_sets = []
for i in range(TOTAL_SETS):
    block = generate_trial_block()
    stats = check_balance(block)
    all_trial_sets.append(block)
    print(f"Set {i+1}:")
    print(f"   Red:    Cong={stats['red']['congruent']}, Incon={stats['red']['incongruent']}, "
          f"V/H={stats['red']['vertical']}/{stats['red']['horizontal']}")
    print(f"   Neutral: Cong={stats['non_red']['congruent']}, Incon={stats['non_red']['incongruent']}, "
          f"V/H={stats['non_red']['vertical']}/{stats['non_red']['horizontal']}")

save_trials_to_json(all_trial_sets)
print(f"\nDone, {len(all_trial_sets)} sets saved to trials.json")
