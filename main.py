import random

random.seed(1)
GRID_SIZE = 4
states = [i for i in range(1, GRID_SIZE * GRID_SIZE + 1)]
actions = ['up', 'right', 'down', 'left']
action_moves = {
    'up': (1, 0),
    'right': (0, 1),
    'down': (-1, 0),
    'left': (0, -1)
}
alpha = 0.3
gamma = 0.1
epsilon = 0.5
max_iterations = 100000
living_reward = -0.1
goal_reward = 100
forbidden_reward = -100
input_data = input().split()
goal1 = int(input_data[0])
goal2 = int(input_data[1])
forbidden = int(input_data[2])
wall = int(input_data[3])
command = input_data[4]
if command == 'q':
    query_state = int(input_data[5])
Q = {}
for state in states:
    Q[state] = {action: 0.0 for action in actions}
def get_position(state):
    row = (state - 1) // GRID_SIZE
    col = (state - 1) % GRID_SIZE
    return (row, col)
def get_state(position):
    row, col = position
    return row * GRID_SIZE + col + 1
def is_valid_position(position):
    row, col = position
    return 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE
def move(state, action):
    if state in [goal1, goal2]:
        return state, 0
    if state == forbidden:
        return state, 0
    current_position = get_position(state)
    move_delta = action_moves[action]
    new_position = (current_position[0] + move_delta[0], current_position[1] + move_delta[1])
    if not is_valid_position(new_position):
        next_state = state
    else:
        next_state = get_state(new_position)
    if next_state == wall:
        next_state = state
    if next_state == goal1 or next_state == goal2:
        reward = goal_reward
    elif next_state == forbidden:
        reward = forbidden_reward
    else:
        reward = living_reward
    return next_state, reward
def choose_action(state, epsilon):
    if random.random() < epsilon:
        return random.choice(actions)
    else:
        max_q = max(Q[state].values())
        best_actions = [action for action in actions if Q[state][action] == max_q]
        return random.choice(best_actions)
iteration = 0
while iteration < max_iterations:
    state = 2
    while True:
        if state in [goal1, goal2, forbidden]:
            break
        action = choose_action(state, epsilon)
        next_state, reward = move(state, action)
        max_next_q = max(Q[next_state].values())
        Q[state][action] += alpha * (reward + gamma * max_next_q - Q[state][action])
        state = next_state
    iteration += 1
    if iteration == max_iterations:
        epsilon = 0
if command == 'p':
    for state in states:
        if state == wall:
            print(f"{state}\twall-square")
        elif state == forbidden:
            print(f"{state}\tforbid")
        elif state == goal1 or state == goal2:
            print(f"{state}\tgoal")
        else:
            max_q = max(Q[state].values())
            for action in actions:
                if Q[state][action] == max_q:
                    best_action = action
                    break
            print(f"{state}\t{best_action}")
elif command == 'q':
    state = query_state
    for action in actions:
        q_value = round(Q[state][action], 2)
        print(f"{action}\t{q_value}")
