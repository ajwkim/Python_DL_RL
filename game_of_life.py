import asyncio
L, D = '*-'


class Grid:
    def __init__(self, height, width):
        self.height, self.width = height, width
        self.rows = [[D for _ in range(self.width)] for _ in range(self.height)]

    def get(self, r, c):
        return self.rows[r % self.height][c % self.width]
    
    def set(self, r, c, state):
        self.rows[r % self.height][c % self.width] = state

    def __str__(self):
        return '\n'.join(''.join(row) for row in self.rows)
    

class ColumnPrinter:
    def __init__(self):
        self.columns = []
        self.h, self.w = 0, 0

    def append(self, x):
        l = len(self.columns)
        w = len(x.split('\n')[0])
        self.columns.append(f'{l:^{w}}\n' + x)

    def __str__(self):
        l = len(self.columns)
        h = len(self.columns[0].split('\n'))
        rows = []
        for i in range(h):
            row = ' | '.join(self.columns[j].split('\n')[i] for j in range(l))
            rows.append(row)
        return '\n'.join(rows)
    

def count_neighbors(r, c, get):     # get(r, c) method
    neighbor_states = [get(r+r_, c+c_) for r_ in (-1,0,1) 
                           for c_ in (-1,0,1) if r_ or c_]
    return neighbor_states.count(L)


async def game_logic(state, neighbors):
    if state == L:
        if neighbors < 2 or neighbors > 3: return D
    else:
        if neighbors == 3: return L
    return state


async def step_cell(r, c, get, set):
    state = get(r, c)
    neighbors = count_neighbors(r, c, get)
    next_state = await game_logic(state, neighbors)
    set(r, c, next_state)


async def simulate(grid):
    height, width = grid.height, grid.width
    next_grid = Grid(height, width)
    
    async with asyncio.TaskGroup() as tg:           # from 3.11
        for r in range(height):
            for c in range(width):
                tg.create_task(
                    step_cell(r, c, grid.get, next_grid.set))
    return next_grid
    
    # Effective Python
    tasks = [step_cell(r, c, grid.get, next_grid.set) for r in range(height) 
                                                      for c in range(width)]
    # tasks = []
    # for r in range(height):
    #     for c in range(width):
    #         task = step_cell(r, c, grid.get, next_grid.set)         # fan out
    #         tasks.append(task)

    await asyncio.gather(*tasks)                                    # fan in
    return next_grid


grid = Grid(5, 9)
grid.set(0, 3, L)
grid.set(1, 4, L)
grid.set(2, 2, L)
grid.set(2, 3, L)
grid.set(2, 4, L)

columns = ColumnPrinter()
for _ in range(5):
    columns.append(str(grid))

    grid = asyncio.run(simulate(grid))                              # run the event loop
print(columns)