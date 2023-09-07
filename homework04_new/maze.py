from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(
    grid: List[List[Union[str, int]]], coord: Tuple[int, int]
) -> List[List[Union[str, int]]]:
    """
    :param grid:
    :param coord:
    :return:
    """
    y, x = coord
    direction = randint(0, 1)
    if direction:
        if x + 1 != len(grid[0]) - 1:
            grid[y][x + 1] = " "
        elif y != 1:
            grid[y - 1][x] = " "
    else:
        if y != 1:
            grid[y - 1][x] = " "
        elif x + 1 != len(grid[0]) - 1:
            grid[y][x + 1] = " "

    return grid


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True):
    """
    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """

    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    # 1. выбрать любую клетку
    # 2. выбрать направление: наверх или направо.
    # Если в выбранном направлении следующая клетка лежит за границами поля,
    # выбрать второе возможное направление
    # 3. перейти в следующую клетку, сносим между клетками стену
    # 4. повторять 2-3 до тех пор, пока не будут пройдены все клетки

    for index, i in enumerate(empty_cells):
        grid = remove_wall(grid, i)

    if random_exit:
        x_begin, x_end = randint(0, rows - 1), randint(0, rows - 1)
        y_begin = randint(0, cols - 1) if x_begin in (0, rows - 1) else choice((0, cols - 1))
        y_end = randint(0, cols - 1) if x_end in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_begin, y_begin = 0, cols - 2
        x_end, y_end = rows - 1, 1

    grid[x_begin][y_begin], grid[x_end][y_end] = "X", "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """
    :param grid:
    :return:
    """

    exits_coord = []
    for y, line in enumerate(grid):
        x_in_line = line.count("X")
        if x_in_line:
            coordinate = y, line.index("X")
            exits_coord.append(coordinate)

    return exits_coord


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """
    :param grid:
    :param k:
    :return:
    """

    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if grid[x][y] == k:
                if x != len(grid) - 1 and grid[x + 1][y] == 0:
                    grid[x + 1][y] = k + 1
                if x != 0 and grid[x - 1][y] == 0:
                    grid[x - 1][y] = k + 1
                if y != len(grid[0]) - 1 and grid[x][y + 1] == 0:
                    grid[x][y + 1] = k + 1
                if y != 0 and grid[x][y - 1] == 0:
                    grid[x][y - 1] = k + 1
    return grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coordinate: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:

    path_way = [exit_coordinate]
    x = exit_coordinate[0]
    y = exit_coordinate[1]
    shortest = grid[x][y]
    k = int(shortest)
    while k > 1:
        if x != len(grid) - 1 and grid[x + 1][y] == k - 1:
            x += 1
            path_way.append((x, y))
        if y != len(grid[0]) - 1 and grid[x][y + 1] == k - 1:
            y += 1
            path_way.append((x, y))
        if x != 0 and grid[x - 1][y] == k - 1:
            x -= 1
            path_way.append((x, y))
        if y != 0 and grid[x][y - 1] == k - 1:
            y -= 1
            path_way.append((x, y))
        k -= 1
    return path_way


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """
    :param grid:
    :param coord:
    :return:
    """

    x, y = coord[0], coord[1]
    if x == 0:
        if grid[x + 1][y] == "■":
            return True
    elif x == len(grid) - 1:
        if grid[x - 1][y] == "■":
            return True
    elif y == 0:
        if grid[x][y + 1] == "■":
            return True
    elif y == len(grid[0]) - 1:
        if grid[x][y - 1] == "■":
            return True
    return False


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:

    new_exit = get_exits(grid)

    if encircled_exit(grid, new_exit[0]) or encircled_exit(grid, new_exit[1]):
        return grid, None

    begin, end = new_exit
    grid[begin[0]][begin[1]], grid[end[0]][end[1]] = 1, 0
    for x, row in enumerate(grid):
        for y in range(len(row)):
            if grid[x][y] == " ":
                grid[x][y] = 0

    k = 0
    while grid[end[0]][end[1]] == 0:
        k += 1
        make_step(grid, k)
    return grid, shortest_path(grid, end)


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:

    if path:
        for x, row in enumerate(grid):
            for y in range(len(row)):
                if grid[x][y] != "■":
                    grid[x][y] = " "
                if (x, y) in path:
                    grid[x][y] = "X"
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(5, 5)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(_, PATH)
    print(pd.DataFrame(MAZE))
