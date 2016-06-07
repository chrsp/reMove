#
#
# author: Charles Pradob
#
# o algoritimo abaixo foi idealizado como projeto para a disciplina
# de matematica discreta da FAESA.
# O codigo utilizada os conceitos de busca em largura para solucionar o jogo
# Move: a brain shifting game (da empresa Nitako):
# http://www.nitako.com/wp/blog/projects/move/

class GameState:
    def __init__(self, board, path_size, pred, left_move, right_move, up_move, down_move):
        self.data_matrix = board
        self.path_size = path_size
        self.pred = pred
        self.left_move = left_move
        self.right_move = right_move
        self.up_move = up_move
        self.down_move = down_move
        self.visited = False

class Game:
    def __init__(self, initial_config, result):
        self.current_move = initial_config
        self.result = result

    def print_board(self, board):
        game_string = "\n"

        for line in board.data_matrix:
            game_string +="|"
            for cell in line:
                if cell == 1:
                    game_string += " O |"
                elif cell == 0:
                    game_string += "   |"
                elif cell == 2:
                    game_string += " X |"
            game_string += "\n"
        print(game_string)

    def get_left_move_simulation(self):
        result_move = [row[:] for row in self.current_move.data_matrix] 

        for line_idx, line in enumerate(result_move):
            for column_idx, cell_value in enumerate(line):
                if cell_value != 1: pass
                else:
                    # se a casa da esquerda nao existir, passa
                    if (column_idx == 0): pass
                    # se a casa da esquerda estiver ocupada, passa
                    elif (result_move[line_idx][column_idx - 1] > 0): pass
                    else:
                        result_move[line_idx][column_idx-1] = cell_value
                        result_move[line_idx][column_idx] = 0

        return result_move

    def get_right_move_simulation(self):
        result_move = [row[:] for row in self.current_move.data_matrix] 

        for line_idx, line in enumerate(result_move):
            for column_idx, cell_value in reversed(list(enumerate(line))):
                if cell_value != 1: pass
                else:
                    # se a casa da direita  nao existir, passa
                    if (column_idx == 2): pass
                    # se a casa da direita estiver ocupada, passa
                    elif (result_move[line_idx][column_idx + 1] > 0): pass
                    else:
                        result_move[line_idx][column_idx + 1] = cell_value
                        result_move[line_idx][column_idx] = 0
        return result_move

    def get_up_move_simulation(self):
        result_move = [row[:] for row in self.current_move.data_matrix] 

        for line_idx, line in enumerate(result_move):
            for column_idx, cell_value in enumerate(line):
                if cell_value != 1: pass
                else:
                    # se a casa de cima  nao existir, passa
                    if (line_idx == 0): pass
                    # se a casa de cima  estiver ocupada, passa
                    elif (result_move[line_idx - 1][column_idx] > 0): pass
                    else:
                        result_move[line_idx - 1][column_idx] = cell_value
                        result_move[line_idx][column_idx] = 0
        return result_move

    def get_down_move_simulation(self):
        result_move = [row[:] for row in self.current_move.data_matrix] 

        for line_idx, line in reversed(list(enumerate(result_move))):
            for column_idx, cell_value in enumerate(line):
                if cell_value != 1: pass
                else:
                    # se a casa de baixo  nao existir, passa
                    if (line_idx == 2): pass
                    # se a casa de baixo  estiver ocupada, passa
                    elif (result_move[line_idx + 1][column_idx] > 0): pass
                    else:
                        result_move[line_idx + 1][column_idx] = cell_value
                        result_move[line_idx][column_idx] = 0
        return result_move

class Player:
    def __init__(self, game):
        self.game = game
        self.current_move = game.current_move
        self.queue = [game.current_move]

    def solve_game(self):
        result_array = []
        for i in self.queue:
            if i.visited == False:
                self.game.current_move = i

                self.register_l_movement()
                self.register_d_movement()
                self.register_r_movement()
                self.register_u_movement()

                i.visited = True

                # se resultado for encontrado
                if (self.game.current_move.data_matrix == self.game.result.data_matrix):
                    result_array.append(self.game.current_move)

                    # criando array do resultado obtido
                    for i in result_array:
                        if (i.pred == None): break
                        elif (i.pred not in result_array):
                            result_array.append(i.pred)

                    # printando visualmente o resultado obtido
                    for i in reversed(result_array):
                        self.game.print_board(i)

                    break

    def register_l_movement(self):
        if (self.game.current_move.left_move == "fim"):
            return

        elif (self.game.get_left_move_simulation() == self.game.current_move.data_matrix):
            self.game.current_move.left_move = "fim"
            return

        else:
            for g in self.queue:
                if (g.data_matrix == self.game.get_left_move_simulation()):
                    if (g.path_size < self.current_move.path_size + 1):
                        self.game.current_move.left_move == "fim"
                        return
                    else:
                        if (g.pred.left_move == g):
                            g.pred.left_move = "fim"
                        elif(g.pred.right_move == g):
                            g.pred.right_move = "fim"
                        elif(g.pred.up_move == g):
                            g.pred.up_move = "fim"
                        elif(g.pred.down_move == g):
                            g.pred.down_move == "fim"

            left_move_game_state = GameState(self.game.get_left_move_simulation(), self.game.current_move.path_size + 1, self.game.current_move, None, "fim", None, None)
            self.game.current_move.left_move = left_move_game_state
            self.queue.append(left_move_game_state)

    def register_r_movement(self):
        if (self.game.current_move.right_move == "fim"):
            return

        elif (self.game.get_right_move_simulation() == self.game.current_move.data_matrix):
            self.game.current_move.right_move = "fim"
            return

        else:
            for g in self.queue:
                if (g.data_matrix == self.game.get_right_move_simulation()):
                    if (g.path_size < self.current_move.path_size + 1):
                        self.game.current_move.right_move == "fim"
                        return
                    else:
                        if (g.pred.left_move == g):
                            g.pred.left_move = "fim"
                        elif(g.pred.right_move == g):
                            g.pred.right_move = "fim"
                        elif(g.pred.up_move == g):
                            g.pred.up_move = "fim"
                        elif(g.pred.down_move == g):
                            g.pred.down_move == "fim"

            right_move_game_state = GameState(self.game.get_right_move_simulation(), self.game.current_move.path_size + 1, self.game.current_move, "fim", None, None, None)
            self.game.current_move.right_move = right_move_game_state
            self.queue.append(right_move_game_state)

    def register_u_movement(self):
        if (self.game.current_move.up_move == "fim"):
            return

        elif (self.game.get_up_move_simulation() == self.game.current_move.data_matrix):
            self.game.current_move.up_move = "fim"
            return

        else:
            for g in self.queue:
                if (g.data_matrix == self.game.get_up_move_simulation()):
                    if (g.path_size < self.current_move.path_size + 1):
                        self.game.current_move.up_move == "fim"
                        return
                    else:
                        if (g.pred.left_move == g):
                            g.pred.left_move = "fim"
                        elif(g.pred.right_move == g):
                            g.pred.right_move = "fim"
                        elif(g.pred.up_move == g):
                            g.pred.up_move = "fim"
                        elif(g.pred.down_move == g):
                            g.pred.down_move == "fim"

            up_move_game_state = GameState(self.game.get_up_move_simulation(), self.game.current_move.path_size + 1, self.game.current_move, None, None, None, "fim")
            self.game.current_move.up_move = up_move_game_state
            self.queue.append(up_move_game_state)


    def register_d_movement(self):
        if (self.game.current_move.down_move == "fim"):
            return

        elif (self.game.get_down_move_simulation() == self.game.current_move.data_matrix):
            self.game.current_move.down_move = "fim"
            return

        else:
            for g in self.queue:
                if (g.data_matrix == self.game.get_down_move_simulation()):
                    if (g.path_size < self.current_move.path_size + 1):
                        self.game.current_move.right_move == "fim"
                        return
                    else:
                        if (g.pred.left_move == g):
                            g.pred.left_move = "fim"
                        elif(g.pred.right_move == g):
                            g.pred.right_move = "fim"
                        elif(g.pred.up_move == g):
                            g.pred.up_move = "fim"
                        elif(g.pred.down_move == g):
                            g.pred.down_move == "fim"

            down_move_game_state = GameState(self.game.get_down_move_simulation(), self.game.current_move.path_size + 1, self.game.current_move, None, None, "fim", None)
            self.game.current_move.down_move = down_move_game_state
            self.queue.append(down_move_game_state)

#################################################################################
# MAIN
#################################################################################
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--matriz_tabuleiro_inicial", help="Matriz com a configuracao inicial de jogo", required=True)
parser.add_argument("-r", "--matriz_resultado", help="Matriz 3x3 com o resultado", required=True)
parser.add_argument("-s", "--only_show", help="Se esta opcao for igual a 1 apenas mostra o jogo sem resolver.")
args = parser.parse_args()

def to3x3matrix(list):
    if len(list) < 9:
        print ("ERRO: Informe uma sequencia de 12 digitos correspondendo \
               a uma matrix 3x3 (os 3 primeiros sao a primeira linha, os 3 \
               proximos a linha do meio, os 3 ultimos a ultima linha)")
    else:
        matrix = [[],[],[]]
        c = 0
        for i in list:
            if c < 3: matrix[0].append(i)
            elif c < 6: matrix[1].append(i)
            else : matrix[2].append(i)
            c +=1
        return matrix

def main():
    initial_config = to3x3matrix([int(item) for item in args.matriz_tabuleiro_inicial.split(',')] )
    result = to3x3matrix([int(item) for item in args.matriz_resultado.split(',')] )

    a_game = Game(GameState(initial_config, 0,  None, None, None, None, None), GameState(result, 0, None, None, None, None, None))
    solver = Player(a_game)

    print("\nCONFIGURACAO DE JOGO INICIAL:")
    a_game.print_board(a_game.current_move)
    print("RESULTADO DESEJADO:")
    a_game.print_board(a_game.result)

    if (args.only_show !="1" and args.only_show != None):
        print("SOLUCAO ENCONTRADA: ")
        solver.solve_game()

if __name__ == '__main__':
    main()
