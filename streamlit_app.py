import streamlit as st
from itertools import combinations

# Create a text input field to specify the number of sides on each die
sides = st.sidebar.number_input("Number of sides on each die", 6, key = "dice_sides_1")

unit_check = st.sidebar.checkbox("Damage Efficiency?")
if unit_check:
    unit_points = st.sidebar.number_input("Points per Unit", 1)

# Create a text input field to specify the target number for the hit roll
hit_target = st.sidebar.number_input("Target number for hit roll", 3, key = "hit_1")

six_check = st.sidebar.checkbox("Exploding Sixes?")
if six_check:
    double_exploding = st.sidebar.checkbox("Double Exploding Sixes?")

# Create a text input field to specify the target number for the wound roll
wound_target = st.sidebar.number_input("Target number for wound roll", 4, key = "wound_1")

# Create a slider to specify the number of dice for the hit roll
dice = st.sidebar.slider("Number of dice for hit roll", 1, 50, 3, key = "num_dice_1")

# Create a dropdown menu to select the type of save
save_types = [
    ("6", 6),
    ("5+", 5),
    ("4+", 4),
    ("3+", 3),
    ("2+", 2),
]

selected_save = st.sidebar.selectbox("Select save type", [s[0] for s in save_types], key = "save_types1")

# Find the target roll for the selected save
for save, save_target in save_types:
    if save == selected_save:
        break

# Create a text input field to specify the Armor Piercing (AP) save modifier
ap_modifier = st.sidebar.number_input("Armor Piercing (AP) save modifier", 0, key = "save_mod_1")

# Create a text input field to specify the damage done by the weapon
dmg = st.sidebar.number_input("Damage done by weapon", 1, key = "damage_mod")

def probability(sides, dice, target, hit=False, save=False, ap=0, esix=False):
    if save == True:
        six_hits = (sides+1)-(target+ap)
        six_prob = (six_hits/sides)
        six_likely = abs(six_prob*dice)
    wins = (sides+1)-(target+ap)
    losses = sides-wins
    prob = (wins/sides)
    likely = prob*dice
    if save==False:
        if hit==True:
            if esix==True:
                six_hit = (sides+1)-6
                six_prob = (six_hit/sides)*dice
                likely = six_prob+likely
                return prob, likely, six_prob
            else:
                return prob, likely
        else:
            return prob, likely
    elif save==True:
        return prob, likely, six_likely


def damage(dmg, dice, armor_break=0):
    return dmg*dice
exploding_six_chance = 0
if six_check:
    hit_prob, hit_likely, exploding_six_chance = probability(sides, dice, hit_target, hit=True, esix=True)
    if double_exploding:
        exploding_six_chance = exploding_six_chance*2
else:
    hit_prob, hit_likely = probability(sides, dice, hit_target, hit=True)

wound_prob, wound_likely = probability(sides, hit_likely, wound_target)

wound_likely = wound_likely+exploding_six_chance
save_prob, save_likely, six_likely = probability(sides,
                                            wound_likely,
                                            save_target,
                                            ap=ap_modifier,
                                            save=True)
if save_likely <= 0:
    dmg_res = wound_likely*dmg
    armor_broke = True
else:
    armor_broke = False
    dmg_res = damage(dmg, wound_likely-save_likely)
unit_res = ""
if unit_check:
    unit_res = dmg_res/unit_points

for save, save_target in save_types:
    if save == selected_save:
        break

# Display the results
if six_check:
    st.write(f"Probability of making a successful hit roll: {hit_prob:.3f} per dice with {hit_likely:.3f} dice hitting. The average number of exploding six is {exploding_six_chance:.3f}.")
else:
    st.write(f"Probability of making a successful hit roll: {hit_prob:.3f} per dice with {hit_likely:.3f} dice hitting.")
st.write(f"Probability of making a successful wound roll, given a successful hit roll: {wound_prob:.3f} per dice with {wound_likely:.3f} dice hitting.")
st.write(f"Probability of making a successful save, given a successful wound roll: {save_prob:.3f} per dice with {save_likely:.3f} dice saving.")
if armor_broke==True:
    st.write(f"Armor Broke")
st.write(f"Amount of damage enemy will take on average: {dmg_res:.3f}")
if unit_res != "":
    st.write(f"Damage Efficiency (Points per Wound): {unit_res:.3f}")
