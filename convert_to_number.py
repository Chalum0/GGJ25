import pickle

# ['-', ' ', 'P', 'W', '^', 'v', 'R', 'G', 'B', 'C']

# 09 : - : unreachable wall
# 00 :   : air
# 01 : P : player
# 02 : W : wall
# 03 : ^ : PIQUES VERS LE HAUT
# 04 : v : PIQUES VERS LE BAS
# 05 : R : red bubble
# 06 : G : green bubble
# 07 : B : blue bubble
# 08 : C : checkpoint

ids = {"-": 9,
       " ": 0,
       "P": 1,
       "W": 2,
       "^": 3,
       "v": 4,
       "R": 5,
       "G": 6,
       "B": 7,
       "C": 8}

def load(filename):
    with open(filename, "r") as file:
        lines = file.readlines()
        mp = []
        for line in lines:
            mp_ = []
            for c in line[:-1]:
                mp_.append(ids[c])
            mp.append(mp_)

    return mp


lvl = "1"
grid = load(f"levels/{lvl}.txt")
pickle.dump(grid, open(f"levels/{lvl}.pickle", "wb"))
print(grid)
