import json

# Load the JSON file with the key mapping of digital buttons
with open('digital_keys.json') as f:
    key_mapping = json.load(f)

# Define constants using the key mapping
X = key_mapping.get("x", 0)
CIRCLE = key_mapping.get("circle", 1)
SQUARE = key_mapping.get("square", 2)
TRIANGLE = key_mapping.get("triangle", 3)
SHARE = key_mapping.get("share", 4)
PS = key_mapping.get("PS", 5)
OPTIONS = key_mapping.get("options", 6)
LEFT_STICK_CLICK = key_mapping.get("left_stick_click", 7)
RIGHT_STICK_CLICK = key_mapping.get("right_stick_click", 8)
L1 = key_mapping.get("L1", 9)
R1 = key_mapping.get("R1", 10)
UP_ARROW = key_mapping.get("up_arrow", 11)
DOWN_ARROW = key_mapping.get("down_arrow", 12)
LEFT_ARROW = key_mapping.get("left_arrow", 13)
RIGHT_ARROW = key_mapping.get("right_arrow", 14)
TOUCHPAD = key_mapping.get("touchpad", 15)



# Load the JSON file with the key mapping of analog buttons
with open('analog_keys.json') as f:
    key_mapping = json.load(f)

# Add analog keys
LEFT_ANALOG_HORIZONTAL = key_mapping.get("Left analog horizonal", 0)
LEFT_ANALOG_VERTICAL = key_mapping.get("Left analog vertical", 1)
RIGHT_ANALOG_HORIZONTAL = key_mapping.get("Right analog horizonal", 2)
RIGHT_ANALOG_VERTICAL = key_mapping.get("Right analog vertical", 3)
L2 = key_mapping.get("L2", 4)
R2 = key_mapping.get("R2", 5)

#Threshold for the analog keys to be considered active
JOYSTICK_THRESHOLD = 0.5  # Threshold for the joystick to be considered active (goes from )