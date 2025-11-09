from collections import deque

# 0: UF  1: UR  2: UB  3: UL  4: DF  5: DR  6: DB  7: DL
# 8: FR  9: BR  10:BL  11:FL
# 12:UFR  13:URB  14:UBL  15:ULF
# 16:DRF  17:DBR  18:DLB  19:DFL

class Solver:
    def __init__(self):
        self.phase_moves = (0b111111111111111111, 0b111111010010111111,
                            0b010010010010111111, 0b010010010010010010, 1)
        self.encoded_turns = (
            (3, 2, 1, 0, 3, 2, 1, 0),    # U
            (4, 5, 6, 7, 4, 5, 6, 7),    # D
            (0, 8, 4, 11, 3, 0, 4, 7),   # F
            (2, 10, 6, 9, 1, 2, 6, 5),   # B
            (3, 11, 7, 10, 2, 3, 7, 6),  # L
            (1, 9, 5, 8, 0, 1, 5, 4),    # R
        )
        self.phase = 0

    def applyMove(self, move, state):
        turns = move % 3 + 1
        face = move // 3
        new_state = state.copy()

        for i in range(turns):
            old_state = state.copy()
            for j in range(8):
                target = self.encoded_turns[face][j] + (i>3)*12
                replacement = self.encoded_turns[face][j+3 if j%4==0 else j-1] + (i>3)*12
                orientDelta = 0
                if j < 4:
                    orientDelta = face in (2, 3)
                else:
                    orientDelta = 0 if (face < 2) else (1 + j%2)
                new_state[target] = old_state[replacement]
                new_state[target+20] = old_state[replacement+20] + orientDelta
                if i == turns-1:
                    new_state[target+20] %= 2 + (i>3)
        return state
    
    def inverse(self, move):
        return move + 2 - 2*(move%3)
    
    def id(self, state):
        if self.phase < 2:
            return tuple(state[20:32])
        
        if self.phase < 3:
            result = state[31:40]
            result[0] |= sum(((state[e] // 8) << e) for e in range(12))
            return str(result)
        
        if self.phase < 4:
            result = [0, 0, 0]
            for e in range(12):
                result[0] |= (2 if (state[e] > 7) else (state[e] & 1)) << (2 * e)
            for c in range(8):
                result[1] |= ((state[c + 12] - 12) & 5) << (3 * c)
            for i in range(12, 20):
                for j in range(i+1, 20):
                    result[2] ^= state[i] > state[j]
            return str(result)
    
    def main(self, argv):
        goal = ("UF", "UR", "UB", "UL", "DF", "DR", "DB", "DL", "FR", "FL", "BR", "BL",
            "UFR", "URB", "UBL", "ULF", "DRF", "DFL", "DLB", "DBR" )
        
        currentState = [0 for _ in range(40)]
        goalState = [0 for _ in range(40)]
        for i in range(20):
            goalState[i] = i

            cubie = argv[i+1]
            while True:
                currentState[i] = (20 if cubie not in goal else goal.index(cubie))
                if (currentState[i] != 20): break
                cubie = cubie[1:] + cubie[0]
                currentState[i+20] += 1
            
        while True:
            self.phase += 1
            if self.phase >= 5: break

            currentId = id(currentState)
            goalId = id(goalState)
            if currentId == goalId:
                continue

            q = deque([(currentState, currentId), (goalState, goalId)])

            predecessor = {}
            direction = {}
            lastMove = {}
            direction[currentId] = 1
            direction[goalId] = 2

            while True:
                if not q:
                    print("Phase", self.phase, "failed to connect search trees.")
                    break
                oldState, oldId = q.popleft()
                oldId = id(oldState)
                
                for move in range(18):
                    if self.phase_moves[self.phase] & (1 << move):
                        newState = self.applyMove(move, oldState.copy())
                        newId = id(newState)

                        if newId in direction and direction[newId] != direction[oldId]:
                            if direction[oldId] > 1:
                                newId, oldId = oldId, newId
                                move = self.inverse(move)
                            
                            algorithm = [move]
                            while oldId != currentId:
                                algorithm.insert(0, lastMove[oldId])
                                oldId = predecessor[oldId]
                            while newId != goalId:
                                algorithm.append(self.inverse(lastMove[newId]))
                                newId = predecessor[newId]

                            for i, m in enumerate(algorithm):
                                print("UDFBLR"[algorithm[i] // 3] + str(algorithm[i] % 3 + 1), end='')
                                currentState = self.applyMove(algorithm[i], currentState.copy())
                            break

                        if newId not in direction:
                            q.append((newState, id(newState)))
                            direction[newId] = direction[oldId]
                            lastMove[newId] = move
                            predecessor[newId] = oldId
                else:
                    continue
                break

import sys
args = []
for arg in sys.argv[1:]:
    args.append(arg)        
s = Solver()
s.main([""]+args)

# main([20, 'UF', 'UR', 'UB', 'UL', 'DF', 'DR', 'DB', 'DL', 'FR', 'FL', 'BR', 'BL', 'UFR', 'URB', 'UBL', 'ULF', 'DRF', 'DFL', 'DLB', 'DBR'])
# main([""] + args)

