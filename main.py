from checkers import *

if __name__ == "__main__":
    matrix = np.array([             #np za bojenje u crveno
        ['B1', '', 'B2', '', 'B3', '', 'B4', ''],
        ['', 'B5', '', 'B6', '', 'B7', '', 'B8'],
        ['B9', '', 'B10', '', 'B11', '', 'B12', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', 'W1', '', 'W2', '', 'W3', '', 'W4'],
        ['W5', '', 'W6', '', 'W7', '', 'W8', ''],
        ['', 'W9', '', 'W10', '', 'W11', '', 'W12']
    ], dtype=object)
    print("Izaberite rezim: ")
    print("1. Biranje poteza")
    print("2. Obavezno jedenje")
    mode = input("Unesite 1 ili 2: ")

    print_matrix(matrix)

    while True:
        matrix = choose_move(matrix, mode)
    