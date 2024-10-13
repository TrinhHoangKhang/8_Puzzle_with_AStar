import numpy as np
import heapq
import copy
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
def swap_element(matrix, pos1, pos2):
    matrix[pos1], matrix[pos2] = matrix[pos2], matrix[pos1]
    return None

class State:
    def __init__(self, matrix: np.ndarray, blank_pos: tuple, g: int) -> None:
        self.matrix = matrix
        self.blank_pos = blank_pos
        self.g = g

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, State):
            return False
        return np.array_equal(self.matrix, value.matrix) and (self.blank_pos == value.blank_pos)

    def __lt__(self, other: object):
        return (self.heuristic() + self.g) < (other.heuristic() + other.g)

    def __hash__(self):
        return hash(str(self.matrix))

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

    def solvable(self):
        # Flatten the matrix
        # Count the each pair, if a pair is inverse then +1
        # If the result is even: solvable
        flat = self.matrix.flatten()
        n = len(flat)
        count = 0
        for i in range(n - 1):
            for j in range(i + 1, n):
                if flat[i] > flat[j]:
                    count += 1

        if (count % 2) == 0:
            return True
        else:
            return False

class Puzzle_Solver:
    def __init__(self, rows=3, cols=3) -> None:
        self.rows = rows
        self.cols = cols
        # Start state is random, 'space' is at the lower right corner
        # The state must be solvable
        self.randomize_start_state()
        # End state is ordered numbers, 'space' is at the lower right corner
        flat_nums = np.arange(1, 9)
        flat_nums = np.append(flat_nums, 0)
        end_matrix = flat_nums.reshape((3, 3))
        self.end = State(end_matrix, (2, 2), 0)

        # Flag
        self.solution_exist = False

    def randomize_start_state(self):
        while True:
            flat_nums = np.arange(1, 9)
            np.random.shuffle(flat_nums)
            flat_nums = np.append(flat_nums, 0)
            start_matrix = flat_nums.reshape((3, 3))
            self.start = State(start_matrix, (2, 2), 0)

            if self.start.solvable():
                logging.info("Solvable state found!")
                break
            logging.info("State not solvable, trying a new starting state...")

    # Base on current state, return valid neighbors state
    def get_valid_neighbors(self, curr_state: State, closed_set: set):
        curr_row, curr_col = curr_state.blank_pos

        next_poss = [(curr_row + 1, curr_col), (curr_row - 1, curr_col),
                     (curr_row, curr_col + 1), (curr_row, curr_col - 1)]

        results = []
        for new_pos in next_poss:
            if (
                0 <= new_pos[0] < self.rows and
                0 <= new_pos[1] < self.cols
            ):
                new_matrix = copy.deepcopy(curr_state.matrix)
                swap_element(new_matrix, curr_state.blank_pos, new_pos)
                new_state = State(new_matrix, new_pos, curr_state.g + 1)
                if new_state not in closed_set:
                    results.append(new_state)

        return results

    def get_path(self, parrent: dict):
        path = [self.end.blank_pos]
        curr = self.end

        while curr != self.start:
            curr = parrent[curr]
            path.append(curr.blank_pos)

        return path[::-1]

    def perform_search(self):
        priority_queue = []
        closed_set = set()
        parrent = {}

        # Push the first element to the queue
        heapq.heappush(
            priority_queue, self.start)

        while priority_queue:
            # Pop the top
            top_state = heapq.heappop(priority_queue)
            logging.info(f"State explored: {len(closed_set)}")
            logging.info(f'g: {top_state.g}, h: {top_state.heuristic()}')
            # Check if it is end state
            if top_state == self.end:
                self.solution_exist = True
                break
            # Push the state to the closed set
            closed_set.add(top_state)

            # Get the neighbors
            neighbors = self.get_valid_neighbors(top_state, closed_set)
            if neighbors:
                for neighbor in neighbors:
                    # Push the neighbor to the open_list
                    heapq.heappush(
                        priority_queue, neighbor)
                    # Update the parrent
                    parrent[neighbor] = top_state

        # Return the path
        if self.solution_exist:
            path = self.get_path(parrent)
            return path
        return None
