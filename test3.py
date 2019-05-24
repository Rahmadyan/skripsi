board = []
for i in range(6): # create a list with nested lists
    board.append([])
    for n in range(6):
        board[i].append("O")
print(board)