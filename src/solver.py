from collections import deque

class Solver:
    def __init__(self):
        self.APPLICABLE_MOVES = (0, 262143, 259263, 74943, 74898)
        self.AFFECTED_CUBIES = (
            ( 0, 1, 2, 3, 0, 1, 2, 3 ),   # U
            ( 4, 7, 6, 5, 4, 5, 6, 7 ),   # D
            ( 0, 9, 4, 8, 0, 3, 5, 4 ),   # F
            ( 2, 10, 6, 11, 2, 1, 7, 6 ), # B
            ( 3, 11, 7, 9, 3, 2, 6, 5 ),  # L
            ( 1, 8, 5, 10, 1, 0, 4, 7 ),  # R
        )
        self.phase = 0


    def apply_move(self, move, state):
        turns = move % 3 + 1
        face = move // 3

        for j in range(turns):
            old_state = state.copy()
            for i in range(8):
                is_corner = i > 3
                target = self.AFFECTED_CUBIES[face][i] + is_corner*12
                killer = self.AFFECTED_CUBIES[face][i-3 if (i & 3) == 3 else i+1] + is_corner*12
                orientation_delta = (1 if (face > 1 and face < 4) else 0) if (i < 4) else (0 if (face < 2) else (2 - (i & 1)))

                state[target] = old_state[killer]
                state[target+20] = old_state[killer+20] + orientation_delta
                
                if j == turns-1:
                    state[target + 20] %= 2 + is_corner
        return state

    def inverse(self, move):
        return move + 2 - 2*(move % 3)

    def id(self, state):
        if self.phase < 2:
            return tuple(state.copy()[20:32])

        if self.phase < 3:
            result = state.copy()[31:40]
            result[0] |= sum(((state[e] // 8) << e) for e in range(12))
            return tuple(result)
        
        if self.phase < 4:
            result = [0, 0, 0]
            result[0] |= sum((2 if (state[e] > 7) else (state[e] & 1)) << (2 * e) for e in range(12))
            result[1] |= sum(((state[c + 12] - 12) & 5) << (3 * c) for c in range(8))
            for i in range(12, 20):
                for j in range(i+1, 20):
                    result[2] ^= state[i] > state[j]
            return tuple(result)
        
        return tuple(state)

    def solve(self, string_state):
        goal = ("UF", "UR", "UB", "UL", "DF", "DR", "DB", "DL", "FR", "FL", "BR", "BL",
            "UFR", "URB", "UBL", "ULF", "DRF", "DFL", "DLB", "DBR" )
        
        current_state = [0 for _ in range(40)]
        goal_state = [0 for _ in range(40)]
        for i in range(20):
            goal_state[i] = i

            cubie = string_state[i]
            while True:
                current_state[i] = (20 if cubie not in goal else goal.index(cubie))
                if (current_state[i] != 20): break
                cubie = cubie[1:] + cubie[0]
                current_state[i+20] += 1
            
        while True:
            self.phase += 1
            if self.phase >= 5: break

            current_id = id(current_state)
            goal_id = id(goal_state)
            if current_id == goal_id:
                continue

            q = deque([(current_state, current_id), (goal_state, goal_id)])


            predecessor = {}
            direction = {}
            last_move = {}
            direction[current_id] = 1
            direction[goal_id] = 2

            soln_string = ""

            while True:
                if not q:
                    print("self.phase", self.phase, "failed to connect search trees.")
                    break
                old_state, oldId = q.popleft()
                oldId = id(old_state)
                
                for move in range(18):
                    if self.APPLICABLE_MOVES[self.phase] & (1 << move):
                        new_state = self.apply_move(move, old_state.copy())
                        new_id = id(new_state)

                        if new_id in direction and direction[new_id] != direction[oldId]:
                            if direction[oldId] > 1:
                                new_id, oldId = oldId, new_id
                                move = self.inverse(move)
                            
                            algorithm = [move]
                            while oldId != current_id:
                                algorithm.insert(0, last_move[oldId])
                                oldId = predecessor[oldId]
                            while new_id != goal_id:
                                algorithm.append(self.inverse(last_move[new_id]))
                                new_id = predecessor[new_id]

                            for i, m in enumerate(algorithm):
                                soln_string += "UDFBLR"[algorithm[i] // 3] + str(algorithm[i] % 3 + 1)
                                current_state = self.apply_move(algorithm[i], current_state.copy())
                            break

                        if new_id not in direction:
                            q.append((new_state, id(new_state)))
                            direction[new_id] = direction[oldId]
                            last_move[new_id] = move
                            predecessor[new_id] = oldId
                else:
                    continue
                break
        return soln_string
