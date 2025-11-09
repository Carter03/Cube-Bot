from collections import deque

applicableMoves = (0, 262143, 259263, 74943, 74898)
affectedCubies = (
    ( 0, 1, 2, 3, 0, 1, 2, 3 ),   # U
    ( 4, 7, 6, 5, 4, 5, 6, 7 ),   # D
    ( 0, 9, 4, 8, 0, 3, 5, 4 ),   # F
    ( 2, 10, 6, 11, 2, 1, 7, 6 ), # B
    ( 3, 11, 7, 9, 3, 2, 6, 5 ),  # L
    ( 1, 8, 5, 10, 1, 0, 4, 7 ),  # R
)


def applyMove(move, state):
    turns = move % 3 + 1
    face = move // 3

    for j in range(turns):
        oldState = state.copy()
        for i in range(8):
            isCorner = i > 3
            target = affectedCubies[face][i] + isCorner*12
            killer = affectedCubies[face][i-3 if (i & 3) == 3 else i+1] + isCorner*12
            orientationDelta = (1 if (face > 1 and face < 4) else 0) if (i < 4) else (0 if (face < 2) else (2 - (i & 1)))

            state[target] = oldState[killer]
            state[target+20] = oldState[killer+20] + orientationDelta
            
            if j == turns-1:
                state[target + 20] %= 2 + isCorner
    return state

def inverse(move):
    return move + 2 - 2*(move % 3)

phase = 0

def id(state):
    if phase < 2:
        return tuple(state.copy()[20:32])

    if phase < 3:
        result = state.copy()[31:40]
        result[0] |= sum(((state[e] // 8) << e) for e in range(12))
        return tuple(result)
    
    if phase < 4:
        result = [0, 0, 0]
        result[0] |= sum((2 if (state[e] > 7) else (state[e] & 1)) << (2 * e) for e in range(12))
        result[1] |= sum(((state[c + 12] - 12) & 5) << (3 * c) for c in range(8))
        for i in range(12, 20):
            for j in range(i+1, 20):
                result[2] ^= state[i] > state[j]
        return tuple(result)
    
    return tuple(state)

def main(argv):
    global phase

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
        phase += 1
        if phase >= 5: break

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
                print("Phase", phase, "failed to connect search trees.")
                break
            oldState, oldId = q.popleft()
            oldId = id(oldState)
            
            for move in range(18):
                if applicableMoves[phase] & (1 << move):
                    newState = applyMove(move, oldState.copy())
                    newId = id(newState)

                    if newId in direction and direction[newId] != direction[oldId]:
                        if direction[oldId] > 1:
                            newId, oldId = oldId, newId
                            move = inverse(move)
                        
                        algorithm = [move]
                        while oldId != currentId:
                            algorithm.insert(0, lastMove[oldId])
                            oldId = predecessor[oldId]
                        while newId != goalId:
                            algorithm.append(inverse(lastMove[newId]))
                            newId = predecessor[newId]

                        for i, m in enumerate(algorithm):
                            print("UDFBLR"[algorithm[i] // 3] + str(algorithm[i] % 3 + 1), end='')
                            currentState = applyMove(algorithm[i], currentState.copy())
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
# main([20, 'UF', 'UR', 'UB', 'UL', 'DF', 'DR', 'DB', 'DL', 'FR', 'FL', 'BR', 'BL', 'UFR', 'URB', 'UBL', 'ULF', 'DRF', 'DFL', 'DLB', 'DBR'])
main([""] + args)

