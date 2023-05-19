# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 15:30:00 2023

@author: matthew
"""

import random
from itertools import cycle
import pygame

# Define board dimensions and cell size
board_width, board_height = 5, 6
cell_size = 50

# Initialize Pygame
pygame.init()

# Create window
screen = pygame.display.set_mode(((board_width+1) * cell_size, (board_height+1) * cell_size))
screen.fill((255,255,255))

# Create font object for text display
font = pygame.font.SysFont('Arial', 20)

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)

# Define board as a list of lists
board = [[[] for _ in range(board_width)] for _ in range(board_height)]

#Start
#Input Player names
p1name = str(input('Please input Player 1 name.'))
p2name = str(input('Please input Player 2 name.'))
players = {'b':None,'w':None}
if random.choice([True, False]):
    players['b'] = p1name
    players['w'] = p2name
else:
    players['b'] = p2name
    players['w'] = p1name
colors = cycle(['b','w'])

#Set initial pieces
for i in range(5):
    board[0][i] = ['w']
    board[5][i] = ['b']

def drawboard():
    # Draw board cells and labels
    for row in range(board_height):
        for col in range(board_width):
            # Get cell value
            cell = board[row][col]

            # Calculate cell position
            cell_x = (col + 1) * cell_size
            cell_y = (row + 1) * cell_size
            cell_center = (cell_x + cell_size // 2, cell_y + cell_size)

            # Draw cell background
            pygame.draw.rect(screen, (220, 220, 220), (cell_x, cell_y, cell_size, cell_size))

            # Calculate circle size and spacing
            circle_radius = cell_size // 4
            circle_spacing = circle_radius // 2

            # Draw circles for each item in the cell
            for i, item in enumerate(cell):
                circle_color = white if item == 'w' else black
                circle_y = cell_y + circle_radius * 2 - i * (0.2 * circle_radius + circle_spacing)

                # Draw circle
                pygame.draw.circle(screen, circle_color, (cell_center[0], circle_y), circle_radius)

                # Draw portion of circle underneath
                if i < 2:
                    pygame.draw.circle(screen, circle_color, (cell_center[0], circle_y + circle_spacing), circle_radius)

            # Draw cell borders
            pygame.draw.rect(screen, black, (cell_x, cell_y, cell_size, cell_size), 1)

    # Draw row labels
    for row in range(board_height):
        label_surface = font.render(str(row), True, black)
        label_rect = label_surface.get_rect(center=(cell_size // 2, (row + 1.5) * cell_size))
        screen.blit(label_surface, label_rect)

    # Draw column labels
    for col in range(board_width):
        label_surface = font.render(str(col), True, black)
        label_rect = label_surface.get_rect(center=((col + 1.5) * cell_size, cell_size // 2))
        screen.blit(label_surface, label_rect)

    # Update screen
    pygame.display.flip()

# Display initial board
drawboard()
# Create the clock object
clock = pygame.time.Clock()

# Main game loop
running = True

while running:    
    # Limit the frame rate
    clock.tick(10)
    
    # Quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    #Turn Flows
    turn = next(colors)
    currentplayer = players[turn]
    
    #Check Player Turn
    print('Now is the turn of '+currentplayer+'. You are {}.'.format('black' if turn == 'b' else 'white'))

    #Choose piece to move
    positions = [(i, j) for i in range(board_height)
                 for j in range(board_width)
                 if len(board[i][j]) > 0 and board[i][j][-1] == turn]

    # Print the matching positions
    print('You have the following pieces to move:')
    print(positions)

    #Return legal move
    ##Get input
    while True:
        choosepiece = input('Please input position of piece to move. e.g. 50\n')
        ##Check if in positions
        if choosepiece.isdigit() and len(choosepiece) == 2:
            choosepiece = (int(str(choosepiece)[0]), int(str(choosepiece)[1]))
            if choosepiece in positions:
                break
            print('Invalid input. No movable piece.')
            print('You have the following pieces to move:')
            print(positions)
        else:
            print('Invalid input. Please type in 2 digits.')

        ##Return all possible moves
    legalmoves = []

    for i in range(choosepiece[0] - 1, choosepiece[0] + 2):
        for j in range(choosepiece[1] - 1, choosepiece[1] + 2):
            if i == choosepiece[0] and j == choosepiece[1]:
                continue  # Skip current position
            if i < 0 or i >= len(board) or j < 0 or j >= len(board[0]):
                continue  # Skip positions outside the board
            if len(board[i][j]) <= 2:
                legalmoves.append((i, j))

    # Print the list of possible moves
    print('You can move to these positions:')
    print(legalmoves)

    ##Get input
    while True:
        choosemove = input('Please input position to move to. e.g. 50\n')
        ##Check if in positions
        if choosemove.isdigit() and len(choosemove) == 2:
            choosemove = (int(str(choosemove)[0]), int(str(choosemove)[1]))
            if choosemove in legalmoves:
                break
            print('Invalid input. No movable piece.')
            print('You can move to these positions:')
            print(legalmoves)
        else:
            print('Invalid input. Please type in 2 digits.')

    #Delete old piece and add new piece
    movepiece = board[choosepiece[0]][choosepiece[1]]
    movepiece.pop(-1)
    movetarget = board[choosemove[0]][choosemove[1]]
    movetarget.append(turn)

    #check win condition
    for i in range(5):
        if board[0][i] == ['b']:
            print('Black has won.')
            winmsg_surface = font.render('Black has WON!!', True, black)
            winmsg_rect = winmsg_surface.get_rect(center=(3*cell_size, 5*cell_size))
            screen.blit(winmsg_surface, winmsg_rect)
            running = False
            
        if board[5][i] == ['w']:
            print('White has won.')
            winmsg_surface = font.render('White has WON!!', True, black)
            winmsg_rect = winmsg_surface.get_rect(center=(3*cell_size, 5*cell_size))
            screen.blit(winmsg_surface, winmsg_rect)
            running = False
            
                
    drawboard()
    
# Quit Pygame
#pygame.quit()