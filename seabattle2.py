from random import choice
from random import randint
import time


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Ваши координаты выходят за пределы доски"


class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы сюда уже стреляли"


class BoardWrongShipException(BoardException):
    pass


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Dot({self.x}, {self.y})"


class Ship:
    def __init__(self, fore, length, orientation):
        self.fore = fore
        self.length = length
        self.orientation = orientation
        self.lives = length

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.length):
            coordinate_x = self.fore.x
            coordinate_y = self.fore.y

            if self.orientation == 0:
                coordinate_x += i

            elif self.orientation == 1:
                coordinate_y += i

            ship_dots.append(Dot(coordinate_x, coordinate_y))

        return ship_dots

    def shooten(self, shot):
        return shot in self.dots


class Board:
    def __init__(self, hide=False, size=6):
        self.hide = hide
        self.size = size

        self.count = 0

        self.field = [["·"] * size for i in range(size)]

        self.busy = []
        self.ships = []

    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "●"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, 1), (0, 0), (0, -1),
            (1, 1), (1, 0), (1, -1),
        ]
        for d in ship.dots:
            for dx, dy in near:
                coordinate = Dot(d.x + dx, d.y + dy)
                if not(self.out(coordinate)) and coordinate not in self.busy:
                    if verb:
                        self.field[coordinate.x][coordinate.y] = "X"
                    self.busy.append(coordinate)

    def contour_2(self, ship, verb=False):
        for d in ship.dots:
            coordinate = Dot(d.x, d.y)
            if not (self.out(coordinate)):
                if verb:
                    self.field[coordinate.x][coordinate.y] = "†"

    def __str__(self):

        res = "  | 1 | 2 | 3 | 4 | 5 | 6 | "
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " | "
        if self.hide:
            res = res.replace("●", "·")

        return res

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)

        for ship in self.ships:
            if ship.shooten(d):
                ship.lives -= 1
                self.field[d.x][d.y] = "◯"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    self.contour_2(ship, verb=True)
                    print("Убит")
                    return True
                else:
                    print("ранен")
                    return True
        self.field[d.x][d.y] = "X"
        print("Мимо")
        return False

    def begin(self):
        self.busy = []

    def defeat(self):
        return self.count == len(self.ships)

class Radar:
    def __init__(self):
        self.weight = [[1] * 6 for i in range(6)]

    def recalculate(self, field):
        #перерасчет self.weight для параметра field
        for x in range(6):
            for y in range(6):
                if field[x][y] == "X" or "†":
                    self.weight[x][y] = 0
                if field[x][y] == "◯":
                    self.weight[x][y] = 0
                    if x - 1 >= 0:
                        self.weight[x - 1][y] *= 50
                        if y - 1 >= 0:
                            self.weight[x-1][y-1] = 0
                        if y + 1 <= 5:
                            self.weight[x-1][y+1] = 0
                    if x + 1 <= 5:
                        self.weight[x + 1][y] *= 50
                        if y - 1 >= 0:
                            self.weight[x+1][y-1] = 0
                        if y + 1 <= 5:
                            self.weight[x+1][y+1] = 0
                    if y + 1 <= 5:
                        self.weight[x][y+1] *= 50
                    if y - 1 >= 5:
                        self.weight[x][y-1] *= 50

    @property
    def best_dots(self):
        weights = {}
        max_weight = 0
        for x in range(6):
            for y in range(6):
                if self.weight[x][y] > max_weight:
                    max_weight = self.weight[x][y]
                weights.setdefault(self.weight[x][y], []).append((x, y))
        return weights[max_weight]








class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def __init__(self, weight):
        super().__init__()
        self.weight = weight
        self.radar = Radar()

    def ask(self):
        self.radar.recalculate(self.board.field)
        x, y = choice(self.radar.best_dots)
        d = Dot(x, y)
        print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
        return d


class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()

            if len(cords) != 2:
                print("Введите 2 координаты!")
                continue

            x, y = cords

            if not(x.isdigit()) or not(y.isdigit()):
                print("Введите числа!")
                continue

            x, y = int(x), int(y)

            return Dot(x-1, y-1)


class Game:

    def try_board(self):
        board = Board(size=self.size)
        attempts = 0
        for length in self.lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), length, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass

        board.begin()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()

        return board

    def __init__(self, size=6):

        self.radar = Radar()
        self.lens = [3, 2, 2, 1, 1, 1, 1]
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hide = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def greet(self):
        print("*" * 77)
        print("Привет, это игра 'Морской бой'")
        print("Координаты задаются через пробел: x y")
        print("Например: 3 2 - это третья строчка и второй столбец")
        print("Ну что же, поехали)")
        print("*" * 77)
        self.a = input("Введите имя игрока: ")
        self.b = input("Придумайте имя компьютеру, против которого будете играть: ")
        print("Расставляем корабли...")
        time_ = 10
        while time_ > 0:
            print(time_)
            time.sleep(0.3)
            time_ -= 1
        print("*" * 77)

    def print_boards(self):
        us_board = str(self.us.board).split("\n")
        ai_board = str(self.ai.board).split("\n")
        for row in range(self.size + 1):
            print(us_board[row], ' ' * 10, ai_board[row])

    def loop(self):
        player_1 = 0
        player_2 = 0
        try_again = "да"

        while try_again == "да":
            num = 0
            win = False
            while not win:
                self.print_boards()
                if num % 2 == 0:
                    print("Ходит ", self.a)
                    repeat = self.us.move()
                else:
                    print("Компьютер думает над своим ходом")
                    time.sleep(1.5)
                    repeat = self.ai.move()
                if repeat:
                    num -= 1
                num += 1
                if self.ai.board.defeat() or self.us.board.defeat():
                    self.print_boards()
                    if self.ai.board.defeat():
                        print(self.a, "в этой партии выиграл")
                        player_1 += 1
                    else:
                        print(self.b, "в этой партии выиграл")
                        player_2 += 1
                    win = True

                    try_again = input("Хотите сыграть еще?")
                    if try_again == "да":
                        self.__init__()
                        print("расставляем корабли...")
                        time_ = 10
                        while time_ > 0:
                            print(time_)
                            time.sleep(0.3)
                            time_ -= 1
                        continue
                    else:
                        print("Это было интересно!")
                        if player_1 > player_2:
                            print(self.a, "выиграл со счетом: ", player_1, "-", player_2)

                        elif player_2 > player_1:
                            print(self.b, "выиграл со счетом: ", player_2, "-", player_1)
                        else:
                            print("У вас ничья: ", player_1, ":", player_2)

    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()
