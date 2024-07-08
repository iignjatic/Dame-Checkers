import numpy as np
import copy
import time


player_possible_moves = {}

should_delete = { "W1": [], "W2": [], "W3": [], "W4": [], "W5": [], "W6": [],
    "W7": [], "W8": [], "W9": [], "W10": [], "W11": [], "W12": [],
     "B1": [], "B2": [], "B3": [], "B4": [], "B5": [], "B6": [],
    "B7": [], "B8": [], "B9": [], "B10": [], "B11": [], "B12": [],
    "KW1": [], "KW2": [], "KW3": [], "KW4": [], "KW5": [], "KW6": [],
    "KW7": [], "KW8": [], "KW9": [], "KW10": [], "KW11": [], "KW12": [],
     "KB1": [], "KB2": [], "KB3": [], "KB4": [], "KB5": [], "KB6": [],
    "KB7": [], "KB8": [], "KB9": [], "KB10": [], "KB11": [], "KB12": []}

def get_color_coded_background(i):
    return "\033[41m{:^8}\033[0m".format('')        #boji pozadinu u crveno


def print_matrix(matrix):                           #ispis table
    is_colored = -1
    for row in matrix:
        is_colored *= -1
        for cell in row:
            if cell == '':
                if is_colored == -1:
                    colored_cell = get_color_coded_background(cell)
                else:
                    colored_cell = ""
            else:
                colored_cell = cell

            is_colored *= -1    
            print("|{:^8}".format(colored_cell), end='')

        print("|")
        print("-"*73)


white_moves_map = {
    "W1": [], "W2": [], "W3": [], "W4": [], "W5": [], "W6": [],
    "W7": [], "W8": [], "W9": [], "W10": [], "W11": [], "W12": []
}

black_moves_map = {
    "B1": [], "B2": [], "B3": [], "B4": [], "B5": [], "B6": [],
    "B7": [], "B8": [], "B9": [], "B10": [], "B11": [], "B12": []
}

white_queens = {"KW1": [], "KW2": [], "KW3": [], "KW4": [], "KW5": [], "KW6": [],
    "KW7": [], "KW8": [], "KW9": [], "KW10": [], "KW11": [], "KW12": []}


black_queens = { "KB1": [], "KB2": [], "KB3": [], "KB4": [], "KB5": [], "KB6": [],
    "KB7": [], "KB8": [], "KB9": [], "KB10": [], "KB11": [], "KB12": []}


def find_coordinates_in_matrix( figure, matrix):
    for i in range(8):
        for j in range(8):
            if matrix[i][j] == figure:
                return [i, j]


def create_moves(matrix, figure, coordinates):           #obicno kretanje
    add_coordinate = [0,0]
    which_player = 1
    if figure in black_moves_map:
        which_player = -1               #ako je u pitanju crni igrac redovi se povecavaju kada se krece
    

    if figure not in black_queens and figure not in white_queens:        #ako nisu u pitanju dame
        if coordinates[1] -1 >=0 and coordinates[0]+(-1)*which_player>-1 and coordinates[0]+(-1)*which_player<8:        
            if matrix[coordinates[0]+(-1)*which_player, coordinates[1]-1] == "" :   #uslov za kretanje ukoso i to lijevo   
                add_coordinate[0] = coordinates[0] +(- 1)*which_player
                add_coordinate[1] = coordinates[1] - 1
                if figure in white_moves_map:
                    white_moves_map[figure].append([add_coordinate[0],add_coordinate[1]])
                else:
                    black_moves_map[figure].append([add_coordinate[0],add_coordinate[1]])

        if coordinates[1] +1 <8 and coordinates[0]+(-1)*which_player>-1 and coordinates[0]+(-1)*which_player<8: 
                if matrix[coordinates[0]+(-1)*which_player, coordinates[1] +1] == "" :          #desno
                    add_coordinate[0] = coordinates[0] +(- 1)*which_player
                    add_coordinate[1] = coordinates[1] + 1
                    if figure in white_moves_map:
                        white_moves_map[figure].append([add_coordinate[0],add_coordinate[1]])
                    else:
                        black_moves_map[figure].append([add_coordinate[0],add_coordinate[1]])

    else:               #u pitanju su dame
        if coordinates[0] -1 >=0 and coordinates[1]-1>=0:        
            if matrix[coordinates[0]-1, coordinates[1]-1] == "" :  
                #uslov za kretanje ukoso i to gore lijevo   
                add_coordinate[0] = coordinates[0] - 1
                add_coordinate[1] = coordinates[1] - 1
                if figure in white_queens:
                    white_queens[figure].append([add_coordinate[0],add_coordinate[1]])
                else:
                    black_queens[figure].append([add_coordinate[0],add_coordinate[1]])
                #gore desno
        if coordinates[0] -1 >=0 and coordinates[1]+1<8:        
            if matrix[coordinates[0]-1, coordinates[1]+1] == "":     
                add_coordinate[0] = coordinates[0] - 1
                add_coordinate[1] = coordinates[1] + 1
                if figure in white_queens:
                    white_queens[figure].append([add_coordinate[0],add_coordinate[1]])
                else:
                    black_queens[figure].append([add_coordinate[0],add_coordinate[1]])

        if coordinates[0] +1 <8 and coordinates[1]-1>=0:
            if matrix[coordinates[0]+1, coordinates[1] -1] == "" :          #dole lijevo
                add_coordinate[0] = coordinates[0] + 1
                add_coordinate[1] = coordinates[1] - 1
                if figure in white_queens:
                    white_queens[figure].append([add_coordinate[0],add_coordinate[1]])
                else:
                    black_queens[figure].append([add_coordinate[0],add_coordinate[1]])

        if coordinates[0] +1 <8 and coordinates[1]+1<8:
            if matrix[coordinates[0]+1, coordinates[1] +1] == "" :          #desno dole
                add_coordinate[0] = coordinates[0] + 1
                add_coordinate[1] = coordinates[1] + 1
                if figure in white_queens:
                    white_queens[figure].append([add_coordinate[0],add_coordinate[1]])
                else:
                    black_queens[figure].append([add_coordinate[0],add_coordinate[1]])        


            
def eat_left(matrix, figure, coordinates):            #vraca koordinate poteza na kog mogu staviti igraca
    which_player = 1
    if figure in black_moves_map:
        which_player = -1

    if figure not in white_queens and figure not in black_queens:    

        if coordinates[0]+(-2)*which_player>-1 and coordinates[0]+(-2)*which_player<8 and coordinates[1]-2>-1 and coordinates[1]-2<8 :
            if matrix[coordinates[0]+(-2)*which_player, coordinates[1]-2] == "":
                if(matrix[coordinates[0]+(-1)*which_player, coordinates[1]-1] in black_moves_map and figure in white_moves_map
                or matrix[coordinates[0]+(-1)*which_player, coordinates[1]-1] in black_queens and figure in white_moves_map
                or matrix[coordinates[0]+(-1)*which_player, coordinates[1]-1] in white_moves_map and figure  in black_moves_map
                or matrix[coordinates[0]+(-1)*which_player, coordinates[1]-1] in white_queens and figure  in black_moves_map):  
                    #ako je protivnicki igrac ukoso
                    should_delete[figure].append([coordinates[0]+(-1)*which_player, coordinates[1]-1])
                    #should_delete.append([coordinates[0]+(-1)*which_player, coordinates[1]-1])
                    coordinates[0] = coordinates[0] +(-2)*which_player
                    coordinates[1] -= 2
                    if figure in white_moves_map:

                        white_moves_map[figure].append(coordinates)
                    else:
                        black_moves_map[figure].append(coordinates)
                    
                    return eat_left(matrix, figure, coordinates)
                
  

def eat_right(matrix, figure, coordinates):
    which_player = 1

    if figure in black_moves_map:
        which_player = -1

    if figure not in white_queens and figure not in black_queens:    
        if coordinates[0]+(-2)*which_player>-1 and coordinates[0]+(-2)*which_player<8 and coordinates[1]+2>-1 and coordinates[1]+2<8 :

            if matrix[coordinates[0]+(-2)*which_player, coordinates[1]+2] == "":
                if(matrix[coordinates[0]+(-1)*which_player, coordinates[1]+1] in black_moves_map and figure  in white_moves_map
                or matrix[coordinates[0]+(-1)*which_player, coordinates[1]+1] in black_queens and figure  in white_moves_map
                or matrix[coordinates[0]+(-1)*which_player, coordinates[1]+1] in white_moves_map and figure  in black_moves_map
                or matrix[coordinates[0]+(-1)*which_player, coordinates[1]+1] in white_queens and figure  in black_moves_map):  
                    should_delete[figure].append([coordinates[0]+(-1)*which_player, coordinates[1]+1])
                    #should_delete.append([coordinates[0]+(-1)*which_player, coordinates[1]+1])
                    coordinates[0] = coordinates[0] +(-2)*which_player
                    coordinates[1] += 2
                    if figure in white_moves_map:
                        white_moves_map[figure].append(coordinates)
                    else:
                        black_moves_map[figure].append(coordinates)
                    
                    return eat_right(matrix, figure, coordinates)  
                                

def queen_top_left(matrix, figure, coordinates):
    if figure in white_queens or figure in black_queens:
        if coordinates[0]-2>-1 and coordinates[1]-2>-1:
            if matrix[coordinates[0]-2, coordinates[1]-2] == "":
                if(matrix[coordinates[0]-1, coordinates[1]-1] in black_moves_map and figure in white_queens
                   or matrix[coordinates[0]-1, coordinates[1]-1] in black_queens and figure  in white_queens
                or matrix[coordinates[0]-1, coordinates[1]-1] in white_moves_map and figure  in black_queens
                or matrix[coordinates[0]-1, coordinates[1]-1] in white_queens and figure  in black_queens):  
                    #ako je protivnicki igrac ukoso
                    should_delete[figure].append([coordinates[0]-1, coordinates[1]-1])
                    #should_delete.append([coordinates[0]-1, coordinates[1]-1])
                    coordinates[0] = coordinates[0] -2
                    coordinates[1] -= 2
                    if figure in white_queens:
                        white_queens[figure].append(coordinates)
                    else:
                        black_queens[figure].append(coordinates)
                    
                    return queen_top_left(matrix, figure, coordinates)


def queen_top_right(matrix, figure, coordinates):
    if figure in white_queens or figure in black_queens:
        if coordinates[0]-2>-1 and coordinates[1]+2<8:
            if matrix[coordinates[0]-2, coordinates[1]+2] == "":
                if(matrix[coordinates[0]-1, coordinates[1]+1] in black_moves_map and figure in white_queens
                   or matrix[coordinates[0]-1, coordinates[1]+1] in black_queens and figure  in white_queens
                or matrix[coordinates[0]-1, coordinates[1]+1] in white_moves_map and figure  in black_queens
                or matrix[coordinates[0]-1, coordinates[1]+1] in white_queens and figure  in black_queens):  
                    #ako je protivnicki igrac ukoso
                    should_delete[figure].append([coordinates[0]-1, coordinates[1]+1])

                    #should_delete.append([coordinates[0]-1, coordinates[1]+1])
                    coordinates[0] = coordinates[0] -2
                    coordinates[1] += 2
                    if figure in white_queens:
                        white_queens[figure].append(coordinates)
                    else:
                        black_queens[figure].append(coordinates)
                    
                    return queen_top_left(matrix, figure, coordinates)
                

def queen_bottom_left(matrix, figure, coordinates):
    if figure in white_queens or figure in black_queens:
        if coordinates[0]+2<8 and coordinates[1]-2>-1:
            if matrix[coordinates[0]+2, coordinates[1]-2] == "":
                if(matrix[coordinates[0]+1, coordinates[1]-1] in black_moves_map and figure in white_queens
                   or matrix[coordinates[0]+1, coordinates[1]-1] in black_queens and figure  in white_queens
                or matrix[coordinates[0]+1, coordinates[1]-1] in white_moves_map and figure  in black_queens
                or matrix[coordinates[0]+1, coordinates[1]-1] in white_queens and figure  in black_queens):  
                    #ako je protivnicki igrac ukoso
                    should_delete[figure].append([coordinates[0]+1, coordinates[1]-1])

                    #should_delete.append([coordinates[0]+1, coordinates[1]-1])
                    coordinates[0] = coordinates[0] +2
                    coordinates[1] -= 2
                    if figure in white_queens:
                        white_queens[figure].append(coordinates)
                    else:
                        black_queens[figure].append(coordinates)
                    
                    return queen_top_left(matrix, figure, coordinates)

        
def queen_bottom_right(matrix, figure, coordinates):
    if figure in white_queens or figure in black_queens:
        if coordinates[0]+2<8 and coordinates[1]+2<8:
            if matrix[coordinates[0]+2, coordinates[1]+2] == "":
                if(matrix[coordinates[0]+1, coordinates[1]+1] in black_moves_map and figure in white_queens
                   or matrix[coordinates[0]+1, coordinates[1]+1] in black_queens and figure  in white_queens
                or matrix[coordinates[0]+1, coordinates[1]+1] in white_moves_map and figure  in black_queens
                or matrix[coordinates[0]+1, coordinates[1]+1] in white_queens and figure  in black_queens):  
                    #ako je protivnicki igrac ukoso
                    should_delete[figure].append([coordinates[0]+1, coordinates[1]+1])

                    #should_delete.append([coordinates[0]+1, coordinates[1]+1])
                    coordinates[0] = coordinates[0] +2
                    coordinates[1] += 2
                    if figure in white_queens:
                        white_queens[figure].append(coordinates)
                    else:
                        black_queens[figure].append(coordinates)
                    
                    return queen_top_left(matrix, figure, coordinates)
                
def empty_map(map):
    empty = True
    for key in map:
        if map[key] != []:
            empty = False
            break
    return empty    

                

def show_moves(matrix, figure, coordinates, mode):     #pokazuje moguce opcije poteza
    if figure in white_moves_map:
        white_moves_map[figure] = []
    elif figure in black_moves_map:
        black_moves_map[figure] = []
    elif figure in white_queens:
        white_queens[figure] = []
    else:
        black_queens[figure] = []    

    #copy_coordinates = [coordinates[0], coordinates[1]]    

          
    create_moves(matrix, figure, coordinates)
    eat_left(matrix,figure, coordinates)
    eat_right(matrix,figure, coordinates)
    queen_top_left(matrix, figure, coordinates)
    queen_bottom_left(matrix, figure, coordinates)
    queen_bottom_right(matrix, figure, coordinates)
    queen_top_right(matrix, figure, coordinates)

    counter = 1

    if figure in white_moves_map or figure in white_queens:
        if figure in white_moves_map:
            white_moves_map[figure] = [list(t) for t in set(tuple(move) for move in white_moves_map[figure])]
            #uklanjam duplikate
            for move in white_moves_map[figure]:
                matrix[move[0], move[1]] = str(counter)
                player_possible_moves[counter] = move
                counter += 1   

        if figure in white_queens: 
            white_queens[figure] = [list(t) for t in set(tuple(move) for move in white_queens[figure])]
            #uklanjam duplikate
            for move in white_queens[figure]:
                matrix[move[0], move[1]] = str(counter)
                player_possible_moves[counter] = move
                counter += 1          


    print_matrix(matrix)    


def get_possible_moves(matrix, minmax, mode):     #funkcija za sve poteze
        possible_moves = {}
        
        for i in range(8):
            for j in range(8):
                if matrix[i][j] != '':
                        if matrix[i][j][0] == minmax or matrix[i][j][1] == minmax:
                            eat_left(matrix, matrix[i][j],[i,j])
                            eat_right(matrix, matrix[i][j],[i,j])
                            queen_bottom_left(matrix, matrix[i][j],[i,j])
                            queen_bottom_right(matrix, matrix[i][j],[i,j])
                            queen_top_left(matrix, matrix[i][j],[i,j])
                            queen_top_right(matrix, matrix[i][j],[i,j])

                            if mode == '1':
                                create_moves(matrix, matrix[i][j],[i,j])

                            if minmax == 'B':
                                if matrix[i][j] in black_moves_map: 
                                    possible_moves[matrix[i][j]] = black_moves_map[matrix[i][j]] 
                                elif matrix[i][j] in black_queens:
                                    possible_moves[matrix[i][j]] = black_queens[matrix[i][j]]

                            if minmax == 'W':
                                if matrix[i][j] in white_moves_map: 
                                    possible_moves[matrix[i][j]] = white_moves_map[matrix[i][j]] 
                                elif matrix[i][j] in white_queens:
                                    possible_moves[matrix[i][j]] = white_queens[matrix[i][j]]    

        if mode == '2':
            if minmax == 'B':
                global_maps = [black_moves_map, black_queens]

                if all(not val for maps in global_maps for val in maps.values()):
                    for i in range(8):
                        for j in range(8):
                            if matrix[i][j] != '':
                                    
                                if matrix[i][j][0] == minmax or matrix[i][j][1] == minmax:
                                    create_moves(matrix, matrix[i][j], [i,j])

                                    if minmax == 'B':

                                        if matrix[i][j] in black_moves_map: 
                                            possible_moves[matrix[i][j]] = black_moves_map[matrix[i][j]] 
                                        elif matrix[i][j] in black_queens:
                                            possible_moves[matrix[i][j]] = black_queens[matrix[i][j]]        

            else:
                global_maps = [white_moves_map, white_queens]

                if all(not val for maps in global_maps for val in maps.values()):
                    for i in range(8):
                        for j in range(8):
                            if matrix[i][j] != '':
                                if matrix[i][j][0] == minmax or matrix[i][j][1] == minmax:
                                    create_moves(matrix, matrix[i][j], [i,j])   

                                    if minmax == 'W':
                                        if matrix[i][j] in white_moves_map: 
                                            possible_moves[matrix[i][j]] = white_moves_map[matrix[i][j]] 
                                        elif matrix[i][j] in white_queens:
                                            possible_moves[matrix[i][j]] = white_queens[matrix[i][j]]

                                     

        
        return possible_moves


def game_over(matrix):
    white_figures_left = any(cell.startswith('W') for row in matrix for cell in row)
    black_figures_left = any(cell.startswith('B') for row in matrix for cell in row)
    return not (white_figures_left and black_figures_left )

def evaluate(matrix, player):       #vrijednost table, heuristika
    ''' score = [
       [5, 0, 10, 0, 10, 0, 10, 0],
        [0, 3, 0, 3, 0, 3, 0, 10],
        [10, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 10],
        [10, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 10],
        [0, 1000, 0, 1000, 0, 0, 0, 700],
        [30, 0, 50, 0, 50, 0, 50, 0]

]'''

    my_score = 0
    opponent_score = 0
    my_value = 0
    opponent_value = 0
    my_figures = 0
    opponent_figures = 0
    my_kings = 0
    opponent_kings = 0
    my_protected_figures = 0
    opponent_protected_figures = 0

 

    for i in range(8):
        for j in range(8):
            if matrix[i][j] != "":
                if matrix[i][j][0] == player:
                    #my_score += score[i][j]
                    my_figures += 2
                    if matrix[i][j][0] == 'K':
                        #my_score += 200
                        my_kings += 3
                else:
                    #opponent_score += score[i][j]
                    opponent_figures += 2
                    if matrix[i][j][0] == 'K':
                        #opponent_score += 200
                        opponent_kings += 3

                if i == 7 and matrix[i][j][0] == player :
                    my_score += 100               

                elif i == 0 and matrix[i][j][0] != player:
                    opponent_score += 100

                if j == 0 and matrix[i][j] == player:
                    my_score += 60

                elif j == 0 and matrix[i][j] != player:
                    opponent_score += 60  

                elif i == 0 and matrix[i][j][0] != player:
                    opponent_score += 100

                elif j == 7 and matrix[i][j] == player:
                    my_score += 60

                elif j == 7 and matrix[i][j] != player:
                    opponent_score += 60           

                if matrix[i][j] != player:
                        if 2 < i < 5 and 1 < j < 6:  # kontrola centra
                            opponent_value += 50
                        elif i < 4:
                            opponent_value += 45
                        else:
                            opponent_value += 40

                if matrix[i][j] == player:
                        if 2 < i < 5 and 1 < j < 6:  
                            my_value += 50
                        elif i > 3:
                            my_value += 45
                        else:
                            my_value += 40

                if matrix[i][j][0] == player:       #da ne smije biti pojeden
                    if i+1<8 and j+1<8:
                        if matrix[i+1][j+1] in white_moves_map:
                            if i-1>-1 and j-1>-1:
                                if matrix[i-1][j-1] == "":
                                    my_protected_figures = -300

                    if i+1<8 and j-1>-1:
                        if matrix[i+1][j-1] in white_moves_map:
                            if i-1>-1 and j+1<8:
                                if matrix[i-1][j+1] == "":
                                    my_protected_figures -= 300   

                if matrix[i][j][0] == player:       #da ne smije biti pojeden
                    if i-1>-1 and j+1<8:
                        if matrix[i-1][j+1] in black_moves_map:
                            if i-1>-1 and j-1>-1:
                                if matrix[i-1][j-1] == "":
                                    opponent_protected_figures -= 300

                else:
                    if i-1>-1 and j-1>-1:
                        if matrix[i-1][j-1] in white_moves_map:
                            if i-1>-1 and j+1<8:
                                if matrix[i-1][j+1] == "":
                                    opponent_protected_figures -= 300                                    

            

    score_matrix =  (my_figures - opponent_figures)*10 + (my_kings - opponent_kings) *300 + (my_score-opponent_score) + (my_value-opponent_value) +(my_protected_figures-opponent_protected_figures)*2

    return score_matrix



def reset_global_maps():            #podesava hash mape na pocetno stanje bez mogucih poteza
    global white_moves_map, black_moves_map, white_queens, black_queens
    
    for key in white_moves_map:
        white_moves_map[key] = []

    for key in black_moves_map:
        black_moves_map[key] = []

    for key in white_queens:
        white_queens[key] = []

    for key in black_queens:
        black_queens[key] = []


transposition_table = {}

def minimax_alpha_beta(matrix, depth, maximizing_player, alpha, beta, mode):
    matrix_tuple = tuple(map(tuple, matrix))
    if matrix_tuple in transposition_table:
        return transposition_table[matrix_tuple]
    
    if depth == 0 :
        return evaluate(matrix, 'B')
    
    reset_global_maps()
    if maximizing_player:
        max_eval = float('-inf')
        possible_moves = get_possible_moves(matrix, 'B', mode)
        for figure in possible_moves.keys():
            for move in possible_moves[figure]:
              #  if time.time() - start_time > time_limit:
               #     break
                new_matrix, does_eat = make_move(matrix, figure, move, 'B', should_delete)
                eval = minimax_alpha_beta(new_matrix, depth - 1, False, alpha, beta, mode)
                if does_eat:
                        eval += 1000
                        if mode == '2':
                            eval += 100000000000
                else:    
                        eval -= 1000
                        if mode == '2':
                            eval -= 100000000000

                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
           # if time.time() - start_time > time_limit:
            #    break
        transposition_table[matrix_tuple] = max_eval
        return max_eval
    else:
        min_eval = float('inf')
        possible_moves = get_possible_moves(matrix, 'W', mode)
        for figure in possible_moves.keys():
            for move in possible_moves[figure]:
           #     if time.time() - start_time > time_limit:
            #        break
                new_matrix, does_eat = make_move(matrix, figure, move, 'W', should_delete)
                eval = minimax_alpha_beta(new_matrix, depth - 1, True, alpha, beta, mode)
                if does_eat:
                        eval -= 1000
                        if mode == '2':
                            eval -= 100000000000
                else:    
                        eval += 1000
                        if mode == '2':
                            eval += 100000000000

                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
           # if time.time() - start_time > time_limit:
            #    break
        transposition_table[matrix_tuple] = min_eval
        return min_eval

    

def choose_move(matrix, mode):        #odigravanje
    global should_delete
    global player_possible_moves

    counter = 1

    while True:
        figure = input("Izaberite figuru: ")
        figure = figure.upper()

        if figure in white_moves_map or figure in white_queens:
            break

        


    new_coordinates = find_coordinates_in_matrix(figure, matrix)

    should_delete[figure] = []

    if mode == '2':
        get_possible_moves(matrix, 'W', mode)
        if figure in white_moves_map:
            white_moves_map[figure] = [list(t) for t in set(tuple(move) for move in white_moves_map[figure])]
            #uklanjam duplikate
            for move in white_moves_map[figure]:
                matrix[move[0], move[1]] = str(counter)
                player_possible_moves[counter] = move
                counter += 1   

        if figure in white_queens: 
            white_queens[figure] = [list(t) for t in set(tuple(move) for move in white_queens[figure])]
            #uklanjam duplikate
            for move in white_queens[figure]:
                matrix[move[0], move[1]] = str(counter)
                player_possible_moves[counter] = move
                counter += 1          


        print_matrix(matrix)  

    else:
        show_moves(matrix, figure, new_coordinates, mode)


    while True:
        if no_figures(matrix) == True:
            exit()

        if mode == '1':
            if all(not val for val in player_possible_moves.values()):
                print("Vi ste izgubili")
                exit()    

        option = input("Izaberite opciju ili kliknite x za nazad: ")
        if option == 'x':
            break
        if figure in white_moves_map:
            if white_moves_map[figure] == []:
                print("Ova figura nema poteza")
                option = 'x'
                break 

        if figure in white_queens:
            if white_queens[figure] == []:
                print("Ova figura nema poteza")
                option = 'x'
                break     

        if int(option) in player_possible_moves:
            break



    if option == 'x':
        for i in range(8):
            for j in range(8):
                if matrix[i][j] not in white_moves_map and matrix[i][j] not in black_moves_map and matrix[i][j] not in white_queens and matrix[i][j] not in black_queens:
                    matrix[i][j] = ''
        print_matrix(matrix)
        return matrix

 
    matrix, does_eat = make_move(matrix, figure, option, '', should_delete)

    print_matrix(matrix)

    print( '='*70)

    matrix = computer_move(matrix, mode)

    return matrix


def no_figures(matrix):
    count = 0
    for row in matrix:
        for cell in row:
            if cell in white_moves_map or cell in white_queens:
                count += 1    

    return count == 0            


def computer_move(matrix,mode):
    global player_possible_moves
    #igra kompjuter
    #start_time = time.time() 
    #time_limit = 3
    best_eval = float('-inf')
    best_move = None
    best_figure = None
    possible_moves = get_possible_moves(matrix, 'B', mode)
    count_moves = 0
    
    for key in possible_moves.keys():
        for move in possible_moves[key]:
            count_moves += 1

    if mode == '2':        
        depth = 5
        if count_moves < 5:
                depth = 6
        if count_moves > 10:
                depth = 5 

    else:
        depth = 5
        if count_moves < 5:
                depth = 6
        if count_moves > 10:
                depth = 4


    local_should_delete = copy.deepcopy(should_delete)
    for figure in possible_moves.keys():
        for move in possible_moves[figure]:
           # if time.time() - start_time > time_limit:
            #    break
            new_matrix, _ = make_move(matrix, figure, move, 'B', should_delete)
            eval = minimax_alpha_beta(new_matrix, depth, False, float('-inf'), float('inf'), mode)
            if move[1] == 7 and figure not in black_queens:
                eval += 25000
            if eval >= best_eval:
                best_eval = eval
                best_move = move
                best_figure = figure
        #if time.time() - start_time > time_limit:
         #   break          

    if best_figure is None:
        if all(not val for val in possible_moves.values()):
            print("Kompjuter nema vise poteza")
            exit()
       # else:
       #     for figure in possible_moves.keys():
       #         if possible_moves[figure]:
       #             matrix, _ = make_move(matrix, figure, possible_moves[figure][0], 'B', local_should_delete)
       #             print("Kompjuter je odigrao sa " + figure)
    else:
        matrix, _ = make_move(matrix, best_figure, best_move, 'B', local_should_delete)
        print("Kompjuter je odigrao sa " + best_figure)

    print_matrix(matrix)

    if all(not val for val in player_possible_moves.values()):
            print("Vi ste izgubili")
            exit()

    reset_global_maps()
    player_possible_moves = {}
    

    return matrix


def make_move(matrix, figure, move, who_plays, should_delete):     #prikaz poteza
    if (game_over(matrix) == False and player_possible_moves):

        does_eat = False

        #global should_delete 

        new_matrix = copy.deepcopy(matrix)

        old_coordinates = find_coordinates_in_matrix(figure, matrix)

        which_player = 1       
        if figure in black_moves_map:
            which_player = -1

        if who_plays == 'B' or who_plays == 'W':
            coordinates = move
        else:    
            coordinates = player_possible_moves[int(move)]

        for i in range(8):
            for j in range(8):
                if (new_matrix[i][j] not in white_moves_map.keys() and new_matrix[i][j] not in black_moves_map.keys() 
                    and new_matrix[i][j] not in white_queens.keys() and new_matrix[i][j] not in black_queens.keys()):
                    new_matrix[i][j] = ""   #brisanje brojeva poteza


        if figure in should_delete:         
            if figure not in white_queens and figure not in black_queens:
                if ([coordinates[0]-(-1)*which_player, coordinates[1]+1] in should_delete[figure]
                        or [coordinates[0]-(-1)*which_player, coordinates[1]-1] in should_delete[figure]): 
                    for delete in should_delete[figure]:
                        does_eat = True
                        if delete == [coordinates[0]-(-1)*which_player, coordinates[1]+1]:
                            new_matrix[delete[0], delete[1]] = ""
                        if delete == [coordinates[0]-(-1)*which_player, coordinates[1]-1]:
                            new_matrix[delete[0], delete[1]] = ""
                        if delete == [coordinates[0]-(3)*which_player, coordinates[1]+1]:
                            new_matrix[delete[0], delete[1]] = ""
                        if delete == [coordinates[0]-(-3)*which_player, coordinates[1]-1]:
                            new_matrix[delete[0], delete[1]] = ""    
                        if delete == [coordinates[0]-(3)*which_player, coordinates[1]+3]:
                            new_matrix[delete[0], delete[1]] = ""
                        if delete == [coordinates[0]-(-3)*which_player, coordinates[1]-3]:
                            new_matrix[delete[0], delete[1]] = ""        
                        if delete == [coordinates[0]-(-1)*which_player, coordinates[1]+3]:
                            new_matrix[delete[0], delete[1]] = ""
                        if delete == [coordinates[0]-(-1)*which_player, coordinates[1]-3]:
                            new_matrix[delete[0], delete[1]] = ""    

            else:
                    if ([coordinates[0]-1, coordinates[1]+1] in should_delete[figure]
                        or [coordinates[0]-1, coordinates[1]-1] in should_delete[figure]
                        or [coordinates[0]+1, coordinates[1]-1] in should_delete [figure]
                        or [coordinates[0]+1, coordinates[1]+1] in should_delete[figure]): 
                        does_eat = True
                        for delete in should_delete[figure]:
                            if delete == [coordinates[0]-1, coordinates[1]+1]:
                                new_matrix[delete[0], delete[1]] = ""
                            if delete == [coordinates[0]-1, coordinates[1]-1]:
                                new_matrix[delete[0], delete[1]] = ""
                            if delete == [coordinates[0]+1, coordinates[1]+1]:
                                new_matrix[delete[0], delete[1]] = ""
                            if delete == [coordinates[0]+1, coordinates[1]-1]:
                                new_matrix[delete[0], delete[1]] = ""
                            if delete == [coordinates[0]-1, coordinates[1]+3]:
                                new_matrix[delete[0], delete[1]] = ""
                            if delete == [coordinates[0]-1, coordinates[1]-3]:
                                new_matrix[delete[0], delete[1]] = ""
                            if delete == [coordinates[0]+1, coordinates[1]+3]:
                                new_matrix[delete[0], delete[1]] = ""
                            if delete == [coordinates[0]+1, coordinates[1]-3]:
                                new_matrix[delete[0], delete[1]] = ""   
                            if delete == [coordinates[0]-3, coordinates[1]+1]:
                                new_matrix[delete[0], delete[1]] = ""
                            if delete == [coordinates[0]+3, coordinates[1]-1]:
                                new_matrix[delete[0], delete[1]] = ""
                            if delete == [coordinates[0]+3, coordinates[1]+3]:
                                new_matrix[delete[0], delete[1]] = ""
                            if delete == [coordinates[0]+3, coordinates[1]-3]:
                                new_matrix[delete[0], delete[1]] = ""     


        #should_delete = []

        should_delete[figure] = []

            
        if figure in white_moves_map:
            if coordinates[0] == 0:
                if 'K' + figure in white_queens:
                    #white_moves_map.pop(figure)
                    white_moves_map[figure] = []
                    figure = 'K'+figure
                    white_queens[figure] = []
        else:
            if coordinates[0] == 7:
                if 'K' + figure in black_queens :
                    #black_moves_map.pop(figure)
                    black_moves_map[figure] = []
                    figure = 'K'+figure
                    black_queens[figure] = []


                 

        new_matrix[coordinates[0],coordinates[1]] = figure
        new_matrix[old_coordinates[0],old_coordinates[1]] = ""

        return new_matrix, does_eat
    
    else:
        does_eat = False
        return matrix, does_eat
        print("Igra je gotova.")



