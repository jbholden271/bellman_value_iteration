"""bellman_value_iteration.py: Performs and prints Bellman Value Iteration on an MDP up to a certain depth."""


def printBoard(board):
    """Print a formatted board to console."""
    for i in board:
        print("[", end="")
        for j in i:
            print("{:5.2f}".format(j), end=",")
        print("]")
    print("-" * (len(board[0]) * 6 + 2))


def getDir(board, protected, r, c, dir):
    """Return the utility of a direction from a coordinate respecting out-of-bounds and protected coordinates.

    Keyword arguments:
        board -- Matrix representing current MDP
        protected -- List of tuples representing protected states.
        r -- Origin state row
        c -- Origin state column
        dir -- Direction as a integer-valued pair/tuple.
    """
    d = dir
    newDir = (r+d[0], c+d[1])
    if newDir in protected or newDir[0] >= len(board) or newDir[1] >= len(board[r]) or newDir[0] < 0 or newDir[1] < 0:
        d = (0, 0)
    return board[r+d[0]][c+d[1]]


def maxDir(noise, board, protected, r, c):
    """Return the maximum utility of moving to any neighboring state for a given state.

    Keyword arguments:
        noise -- Floating point representing how likely any state is to deviate from the intended direction, split evenly
        board -- Matrix representing current MDP
        protected -- List of tuples representing protected states
        r -- Origin state row
        c -- Origin state column
    """
    dirs = {}
    dirs[(0, 1)] = [(1, 0), (-1, 0)]
    dirs[(1, 0)] = [(0, 1), (0, -1)]
    dirs[(0, -1)] = [(1, 0), (-1, 0)]
    dirs[(-1, 0)] = [(0, 1), (0, -1)]
    vals = [0, 0, 0, 0]
    for i, dir in enumerate(dirs):
        vals[i] += getDir(board, protected, r, c, dir) * (1-noise)
        for subDir in dirs[dir]:
            vals[i] += getDir(board, protected, r, c, subDir) * (noise/2)
    return max(vals)

def bellman(noise, decay, cost, board, protected, terminal):
    """Print and return a single iteration of Bellman's value iteration.

    Keyword arguments:
        noise -- Floating point representing how likely any state is to deviate from the intended direction, split evenly
        decay -- Floating point representing how quickly the utility from previous iterations decays
        cost --- Floating point representing the utility of of existing in a non-terminal state
        board -- Matrix representing current MDP
        protected -- List of tuples representing protected states
        terminal -- List of tuples representing terminal states
    """
    newBoard = [[0 for _ in row] for row in board]
    for r, row in enumerate(newBoard):
        for c, element in enumerate(row):
            if (r, c) in terminal:
                newBoard[r][c] = board[r][c]
            elif (r, c) not in protected:
                newBoard[r][c] += cost + decay * maxDir(noise, board, protected, r, c)
    printBoard(newBoard)
    return newBoard


if __name__=="__main__":
    b = [
        [0, 0, 1, -1],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
    p = [(1, 1)]
    t = [(0, 2), (0, 3)]
    printBoard(b)
    for i in range(4):
        print("Iteration", i+1)
        b = bellman(0.2, 0.9, -0.05, b, p, t)
