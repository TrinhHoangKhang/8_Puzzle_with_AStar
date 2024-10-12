import numpy as np
import heapq
import copy

def swap_element(matrix, pos1, pos2):
    rows, cols = matrix.shape
    if not (0 <= pos2[0] < rows and 0 <= pos2[1] < cols):
        raise ValueError("Invalid move: position out of bounds")

    matrix = copy.copy(matrix)
    matrix[pos1], matrix[pos2] = matrix[pos2], matrix[pos1]
    return matrix

class State:
    def __init__(self, matrix: np.ndarray, blank_pos: tuple) -> None:
        self.matrix = matrix
        self.blank_pos = blank_pos

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, State):
            return False
        return np.array_equal(self.matrix, value.matrix) and (self.blank_pos == value.blank_pos)

    def __lt__(self, other: object):
        return self.heuristic() < other.heuristic()

    def heuristic(self):
        total_distance = 0
        for row in range(self.matrix.shape[0]):
            for col in range(self.matrix.shape[1]):
                if (row, col) != self.blank_pos:
                    value = self.matrix[row, col]
                    true_row, true_col = divmod(
                        value - 1, self.matrix.shape[0])
                    total_distance += abs(row - true_row) + abs(col - true_col)
        return total_distance

class Puzzle_Solver:
    def __init__(self, rows=3, cols=3) -> None:
        self.rows = rows
        self.cols = cols
        # Start state is random, 'space' is at the lower right corner
        # flat_nums = np.arange(1, 9)
        # np.random.shuffle(flat_nums)
        # flat_nums = np.append(flat_nums, 0)
        flat_nums = np.array([1, 2, 3, 4, 5, 6, 7, 0, 8])
        start_matrix = flat_nums.reshape((3, 3))
        self.start = State(start_matrix, (2, 1))
        # End state is ordered numbers, 'space' is at the lower right corner
        flat_nums = np.arange(1, 9)
        flat_nums = np.append(flat_nums, 0)
        end_matrix = flat_nums.reshape((3, 3))
        self.end = State(end_matrix, (2, 2))

        # Flag
        self.solution_exist = False

    # Base on current state, return valid neighbors state
    def get_valid_neighbors(self, curr_state: State, closed_set: set):
        curr_matrix = copy.deepcopy(curr_state.matrix)

        curr_row, curr_col = curr_state.blank_pos

        next_poss = [(curr_row + 1, curr_col), (curr_row - 1, curr_col),
                     (curr_row, curr_col + 1), (curr_row, curr_col - 1)]

        results = []
        for pos in next_poss:
            try:
                next_matrix = swap_element(
                    curr_matrix, curr_state.blank_pos, pos)

                if tuple(next_matrix.flatten()) in closed_set:
                    continue

                results.append(State(next_matrix, pos))
            except:
                continue

        return results

    def get_path(self, parrent: dict):
        path = [self.end.blank_pos]
        curr = self.end

        while curr != self.start:
            curr = parrent[tuple(curr.matrix.flatten())]
            path.append(curr.blank_pos)

        return path[::-1]

    def perform_search(self):
        priority_queue = []
        closed_set = set()
        parrent = {}

        heapq.heappush(
            priority_queue, self.start)

        while priority_queue:
            # Pop the top
            top_state = heapq.heappop(priority_queue)
            # Check if it is end state
            if top_state == self.end:
                self.solution_exist = True
                break
            # Push the flatten of the matrix to set
            closed_set.add(tuple(top_state.matrix.flatten()))

            # Get the neighbors
            neighbors = self.get_valid_neighbors(top_state, closed_set)
            if neighbors:
                for neighbor in neighbors:
                    # Push the neighbor to the open_list
                    heapq.heappush(
                        priority_queue, neighbor)
                    # Update the parrent
                    parrent[tuple(neighbor.matrix.flatten())] = top_state

        # Return the path
        if self.solution_exist:
            path = self.get_path(parrent)
            return path
        return None


solver = Puzzle_Solver()
path = solver.perform_search()
print(path)
