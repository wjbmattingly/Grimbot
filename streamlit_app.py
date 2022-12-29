import streamlit as st
from itertools import combinations

# Create a text input field to specify the number of sides on each die
num_sides = st.sidebar.text_input("Number of sides on each die", "6")

# Convert the number of sides to an integer
num_sides = int(num_sides)

# Create a text input field to specify the target number for the hit roll
hit_target = st.sidebar.text_input("Target number for hit roll", "3")

# Convert the hit target to an integer
hit_target = int(hit_target)

# Create a text input field to specify the target number for the wound roll
wound_target = st.sidebar.text_input("Target number for wound roll", "4")

# Convert the wound target to an integer
wound_target = int(wound_target)

# Create a slider to specify the number of dice for the hit roll
num_hit_dice = st.sidebar.slider("Number of dice for hit roll", 1, 50, 3)

# Create a dropdown menu to select the type of save
save_types = [
    ("No save", 6),
    ("Armor save", 4),
    ("Invulnerable save", 3),
]
selected_save = st.sidebar.selectbox("Select save type", [s[0] for s in save_types])

# Find the target roll for the selected save
for save, save_target in save_types:
  if save == selected_save:
    break

# Create a text input field to specify the Armor Piercing (AP) save modifier
ap_modifier = st.sidebar.text_input("Armor Piercing (AP) save modifier", "0")

# Convert the AP modifier to an integer
ap_modifier = int(ap_modifier)

# Create a text input field to specify the damage done by the weapon
damage = st.sidebar.text_input("Damage done by weapon", "1")

# Convert the damage to an integer
damage = int(damage)

# Initialize counters for the number of successful hit rolls, wound rolls, and saves
successful_hit_rolls = 0
successful_wound_rolls = 0
successful_saves = 0

# Loop through all possible combinations of hit dice rolls
for hit_rolls in combinations(range(1, num_sides+1), num_hit_dice):
  # If the sum of the hit rolls is greater than or equal to the hit target,
  # increment the successful hit rolls counter
  if sum(hit_rolls) >= hit_target:
    successful_hit_rolls += 1
    # Loop through all possible combinations of wound dice rolls
    for wound_rolls in combinations(range(1, num_sides+1), num_hit_dice):
      # If the sum of the wound rolls is greater than or equal to the wound target,
      # increment the successful wound rolls counter
      if sum(wound_rolls) >= wound_target:
        successful_wound_rolls += 1
        
         # Loop through all possible combinations of save dice rolls
        for save_rolls in combinations(range(1, num_sides+1), num_hit_dice):
         # If the sum of the save rolls is less than the save target,
         # increment the successful saves counter
            if sum(save_rolls) < save_target:
                successful_saves += 1

# Create a dropdown menu to select the type of save
save_types = [
    ("No save", 6),
    ("Armor save", 4),
    ("Invulnerable save", 3),
]
selected_save = st.sidebar.selectbox("Select save type", [s[0] for s in save_types])

# Find the target roll for the selected save
for save, save_target in save_types:
  if save == selected_save:
    break

# Calculate the probability of making a successful hit roll
hit_probability = successful_hit_rolls / (num_sides ** num_hit_dice)

# Calculate the probability of making a successful wound roll, given a successful hit roll
wound_probability = successful_wound_rolls / (num_sides ** num_hit_dice)

# Calculate the probability of making a successful save, given a successful wound roll
save_probability = successful_saves / (num_sides ** num_hit_dice)

# Calculate the average number of successful hit rolls
average_successful_hit_rolls = hit_probability * num_hit_dice

# Calculate the average number of successful wound rolls, given a successful hit roll
average_successful_wound_rolls = wound_probability * num_hit_dice

# Calculate the average number of successful saves, given a successful wound roll
average_successful_saves = save_probability * num_hit_dice

# Calculate the average number of wounds caused, given a successful hit roll and failed save
average_wounds = (1 - save_probability) * damage

# Display the results
st.write(f"Probability of making a successful hit roll: {hit_probability:.3f}")
st.write(f"Probability of making a successful wound roll, given a successful hit roll: {wound_probability:.3f}")
st.write(f"Probability of making a successful save, given a successful wound roll: {save_probability:.3f}")
st.write(f"Average number of successful hit rolls: {average_successful_hit_rolls:.3f}")
st.write(f"Average number of successful wound rolls, given a successful hit roll: {average_successful_wound_rolls:.3f}")
st.write(f"Average number of successful saves, given a successful wound roll: {average_successful_saves:.3f}")
st.write(f"Average number of wounds caused, given a successful hit roll and failed save: {average_wounds:.3f}")
