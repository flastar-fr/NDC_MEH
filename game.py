import pyxel


class SpaceShip:
    def __init__(self):
        self.x = 0
        self.y = 0

    def move(self):
        if pyxel.btn(pyxel.KEY_Z):
            self.y -= 1
        if pyxel.btn(pyxel.KEY_S):
            self.y += 1
        if pyxel.btn(pyxel.KEY_Q):
            self.x -= 1
        if pyxel.btn(pyxel.KEY_D):
            self.x += 1

        if self.x > 256:
            self.x = 256
        if self.y > 256:
            self.y = 256

    def tire(self):
        pass

    def draw(self):
        pyxel.blt(self.x, self.y, 1, 0, 10, 15, 10)

class Donjon:
    def __init__(self):
        self.etage = 1
        self.niveau_courant = []


    def niveau_superieur(self):
        self.etage += 1
        self.niveau_courant = Niveau(self.etage)


class Niveau:
    def __init__(self, etage):
        self.obstacles = [[0, [-12, 10]]]
        # Liste de listes. Chaque sous-liste représente un obstacle :
        # [ Numéro de l'ennemi (son id), [Son x, son y]]

    def scroll(self):
        pass



class Game:
    def __init__(self):
        pyxel.init(256, 256, title="Nuit du Code")
        self.spaceship = SpaceShip()
        pyxel.run(self.update, self.draw)
        self.mastermind = Donjon()

    def update(self):
        self.spaceship.move()

    def draw(self):
        self.spaceship.draw()


if __name__ == '__main__':
    game = Game()
