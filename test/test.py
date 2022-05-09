import json
pastes_fd = open("pastes.json", "r")
# Reads the pastes json file and loads it into a dict
pastes = json.load(pastes_fd)
pastes_fd.close()
print(pastes["CZ7TA7JWIQ"])
