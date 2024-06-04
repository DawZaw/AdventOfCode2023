import os

path: str = os.path.dirname(__file__)
filepath: str = path + "\\input.txt"


from queue import PriorityQueue
from typing import TypeAlias


Point: TypeAlias = tuple[int, int]
State: TypeAlias = tuple[Point, Point | None, int]


def is_inbound(matrix: list[str], point: Point) -> bool:
    return 0 <= point[0] < len(matrix) and 0 <= point[1] < len(matrix[0])


def pathfind(matrix: list[str], start: Point, min_steps: int, max_steps: int) -> int:
    goal: Point = (len(matrix) - 1, len(matrix[0]) - 1)
    queue: PriorityQueue = PriorityQueue()

    cost: int = 0
    current_position: Point = start
    direction: Point | None = None
    consecutive: int = 0
    # Cost first to make sure we are getting state with lowest cost
    queue.put((cost, current_position, direction, consecutive))

    state: State = (start, direction, consecutive)
    visited: dict[State, int] = {state: cost}

    while not queue.empty():
        cost, current_position, direction, consecutive = queue.get()

        if current_position == goal:
            return cost

        next_states: list[State] = []
        # Direction is None means we are at the beginning, we can move only to the right or down
        if direction is None:
            for row, col in [(0, 1), (1, 0)]:
                neighbour: Point = (
                    current_position[0] + row,
                    current_position[1] + col,
                )
                n_direction: Point | None = (row, col)
                n_steps: int = 1
                n_state: State = (neighbour, n_direction, n_steps)
                next_states.append(n_state)
        else:
            # Consecutive step count is greater or equal to min_steps, we are allowed to turn
            # append clockwise and couterclockwise state in relation to current state
            if consecutive >= min_steps:
                cw_state: State = (
                    (
                        current_position[0] + direction[1],
                        current_position[1] - direction[0],
                    ),
                    (
                        direction[1],
                        -direction[0],
                    ),
                    1,
                )

                ccw_state: State = (
                    (
                        current_position[0] - direction[1],
                        current_position[1] + direction[0],
                    ),
                    (-direction[1], direction[0]),
                    1,
                )
                next_states.extend([ccw_state, cw_state])

            # Consecutive step count lesser than max_steps, we are allowed to move in same direction
            if consecutive < max_steps:
                next_states.append(
                    (
                        (
                            current_position[0] + direction[0],
                            current_position[1] + direction[1],
                        ),
                        direction,
                        consecutive + 1,
                    )
                )

        for next_state in next_states:
            neighbour, n_direction, n_steps = next_state
            if is_inbound(matrix, neighbour):
                new_cost: int = cost + int(matrix[neighbour[0]][neighbour[1]])
                if next_state not in visited or new_cost < visited[next_state]:
                    visited[next_state] = new_cost
                    queue.put((new_cost, neighbour, n_direction, n_steps))

    return -1


with open(filepath, "r") as file:
    data: list[str] = [line.strip() for line in file.readlines()]
    start: Point = (0, 0)

    # Part 1

    print(f"Part 1: {pathfind(data, start, 0, 3)}")

    # Part 2

    print(f"Part 2: {pathfind(data, start, 4, 10)}")
