from collections import deque
from board_methods import *
from time import time
import heapq
import sys


def bfs():
    max_nodes = 0
    start_time = time()
    queue = deque()
    queue.appendleft([board_inicial])
    visited = set()
    while queue:
        max_nodes = max(max_nodes, len(queue))
        path = queue.pop()
        node = path[-1]
        if node == board_goal:
            end_time = time()
            return path, end_time - start_time, max_nodes
        if str(node) in visited:
            continue
        visited.add(str(node))
        for succesor in generate_descendente(node):
            new_path = path + [succesor]
            queue.appendleft(new_path)
    return None


def dfs():
    max_nodes = 0
    start_time = time()
    stack = deque()
    stack.append([board_inicial])
    visited = set()
    while stack:
        max_nodes = max(max_nodes, len(stack))
        path = stack.pop()
        node = path[-1]
        if node == board_goal:
            end_time = time()
            return path, end_time - start_time, max_nodes
        if str(node) in visited:
            continue
        visited.add(str(node))
        for successor in generate_descendente(node):
            new_path = path + [successor]
            stack.append(new_path)
    return None


def a_star(heuristic):
    max_nodes = 0
    start_time = time()
    minheap = []
    heapq.heappush(minheap, (heuristic(board_inicial), board_inicial, [board_inicial]))
    visited = set()
    while minheap:
        max_nodes = max(max_nodes, len(minheap))
        heuristic_value, node, path = heapq.heappop(minheap)
        if node == board_goal:
            end_time = time()
            return path, end_time - start_time, max_nodes
        if str(node) in visited:
            continue
        visited.add(str(node))
        for successor in generate_descendente(node):
            heapq.heappush(minheap, (len(path) + heuristic(successor), successor, path + [successor]))
    return None


def greedy(heuristic):
    max_nodes = 0
    start_time = time()
    minheap = []
    heapq.heappush(minheap, (heuristic(board_inicial), board_inicial, [board_inicial]))
    visited = set()
    while minheap:
        max_nodes = max(max_nodes, len(minheap))
        heuristic_value, node, path = heapq.heappop(minheap)
        if node == board_goal:
            end_time = time()
            return path, end_time - start_time, max_nodes
        if str(node) in visited:
            continue
        visited.add(str(node))
        for successor in generate_descendente(node):
            heapq.heappush(minheap, (heuristic(successor), successor, path + [successor]))
    return None

def iterative_deepening_search(max_depth):
    start_time = time()
    for depth_limit in range(max_depth):
        result = depth_limited_search(board_inicial, board_goal, depth_limit)
        if result is not None:
            path, max_nodes = result
            end_time = time()
            return path, end_time - start_time,max_nodes
    return None


def depth_limited_search(board_inicial, board_goal, depth_limit):
    max_nodes = 0
    stack = deque()
    stack.append([board_inicial])
    visited = set()
    while stack:
        max_nodes = max(max_nodes, len(stack))
        path = stack.pop()
        node = path[-1]
        if node == board_goal:
            return path,max_nodes
        if str(node) in visited or len(path) > depth_limit:
            continue
        visited.add(str(node))
        for successor in generate_descendente(node):
            new_path = path + [successor]
            stack.append(new_path)
    return None
    

def heuristicadistancia(board):
    distancia = 0
    for i in range(4):
        for j in range(4):
            peca = board[i][j]
            if peca != 0:
                linha_objetivo = (peca - 1) // 4
                coluna_objetivo = (peca - 1) % 4
                distancia += abs(i - linha_objetivo) + abs(j - coluna_objetivo)
    return distancia


def heuristicalugar(board):
    n_errados = 0
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] != board_goal[i][j]:
                n_errados += 1
    return n_errados
