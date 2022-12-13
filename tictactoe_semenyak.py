print("*" * 77)
print("Привет! Это игра 'Крестики - нолики'. Думаю, правила ты знаешь:) \nЕдинственный нюанс - тебе для того, чтобы поставить крестик или нолик в табличку, нужно использовать индекс этого места. \nПодсказки есть слева и сверху от самого игрового поля. \nСначала нужно указывать строчку, которую выбираете, а потом столбец. \nНапример, 01- это 1-ая строчка и 2-ой столбец. \nНадеюсь, вы разобрались:) Давайте попробуем!")
print("*" * 77)
A = input("Введите имя первого игрока, который будет использовать Крестики. ")
B = input("Введите имя второго игрока, который будет использовать Нолики. ")
print("*" * 77)
board = []
x = "-"
board.extend(x * 9)
d = {
   "00": 0,
   "01": 1,
   "02": 2,
   "10": 3,
   "11": 4,
   "12": 5,
   "20": 6,
   "21": 7,
   "22": 8,
}

def draw_board(board):
    print("  " + "0 " + "1 " + "2")
    for i in range(3):
        print(i, board[0+i*3], board[1+i*3], board[2+i*3])

def player_move(which, turn):
    t = True
    while t:
        print("Игрок", which, "ходит")
        on = input("Куда поставим " + turn + "? ")
        if on.isdigit():
            if on in d:
                if str(board[d[on]]) not in "xo":
                    board[d[on]] = turn
                    t = False
                else:
                    print("Клетка уже занята!")
            else:
                print("Вам нужно ввести индекс от 00 до 22. Давайте попробуем еще раз")
        else:
            print("Вы ввели не число")

def winner(board):
    vict_options = ((0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6))
    for a in vict_options:
        if board[a[0]] == board[a[1]] == board[a[2]] and board[a[0]] in "xo":
            return board[a[0]]
    return False

def final(board):
    score_1 = 0
    score_2 = 0
    player_choice = "да"
    while player_choice == "да":
        sum = 0
        win = False
        while not win:
            draw_board(board)
            if sum % 2 == 0:
                player_move(A, "x")
            else:
                player_move(B, "o")
            sum += 1
            if sum > 4:
                who = winner(board)
                if who:
                    draw_board(board)
                    if who == "x":
                        print("В этой партии выиграл игрок", A)
                        score_1 += 1
                    else:
                        print("В этой партии выиграл игрок", B)
                        score_2 += 1
                    win = True
            if sum == 9 and not who:
                draw_board(board)
                print("Ничья")
                break
        print("*" * 77)
        player_choice = input("Хотите сыграть еще раз? да/нет ")
        print("*" * 77)
        if player_choice == "да":
            for i in range(len(board)):
                board[i] = "-"
            continue
        elif player_choice == "нет":
            print("Это было круто:)")
            if score_1 > score_2:
                print("*" * 77)
                print("Игрок", A, "Выиграл по партиям со счетом: ", score_1, "-", score_2)
                print("*" * 77)
            elif score_1 < score_2:
                print("*" * 77)
                print("Игрок", B, "Выиграл по партиям со счетом: ", score_2, "-", score_1)
                print("*" * 77)
            else:
                print("*" * 77)
                print(A, "и", B, ",вы сыграли на равных. У вас ничья: ", score_1, "-", score_2)
                print("*" * 77)

final(board)




