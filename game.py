import pyxel


class SpaceShip:
    def __init__(self):
        self.x: int = 100
        self.y: int = 100
        self.shots: list[Tir] = []
        self._can_shoot = False
        self._can_hit = True
        self.cooldown = 1
        self.lives = 3
        self.speed = 2

    def move(self):
        if pyxel.btn(pyxel.KEY_Z):
            self.y -= self.speed
        if pyxel.btn(pyxel.KEY_S):
            self.y += self.speed
        if pyxel.btn(pyxel.KEY_Q):
            self.x -= self.speed
        if pyxel.btn(pyxel.KEY_D):
            self.x += self.speed

        if self.x > 256:
            self.x = 256
        if self.y > 256:
            self.y = 256
        if self.x < 0:
            self.x = 0
        if self.y < 0:
            self.y = 0

    def shoot(self):
        if not self._can_shoot:
            self._can_shoot = pyxel.frame_count % (self.cooldown*30) == 0
            return None

        if pyxel.btnp(pyxel.KEY_SPACE, repeat=False):
            self.shots.append(Tir(self.x, self.y))
            self._can_shoot = False

    def draw_ship(self):
        pyxel.blt(self.x-4, self.y+3, 0, 0, 10, 16, 12, 5)

    def move_shoots(self):
        del_shots = []
        for shot in self.shots:
            shot.y -= 5
            if shot.y <= 0:
                del_shots.append(shot)

        for shot in del_shots:
            del_shots.remove(shot)

    def check_collision_shoots(self, enemies):
        to_del = []
        for shot in self.shots:
            if shot.collision(enemies):
                to_del.append(shot)

        for shot in to_del:
            self.shots.remove(shot)

    def collision_spaceship(self, enemies):
        for e in enemies:
            if e == (self.x, self.y):
                self.lives -= 1
        if self.lives < 1:
            #TODO
            pass

    def collision_bonus_spaceship(self, enemies):
        for e in enemies:
            if e == (self.x, self.y):
                self.lives += 1

    def draw_shoots(self):
        for shot in self.shots:
            pyxel.blt(shot.x, shot.y, 0, 48, 73, 8, 7, 5)

    def draw_lives(self):
        pyxel.text(5, 5, f"Vies : {self.lives}", 8)


class Tir:
    """Stocke les tirs"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def collision(self, enemie):
        # TODO
        for e in enemie:
            if (e.x - self.x < 5 or e.x - self.x > 5) and (e.y - self.y > 5 or e.y - self.y < 5):
                e.pv -= 2
                return True
        return False


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
        for i in range(len(self.obstacles)):
            self.obstacles[i][1][1] += 1



class Game:
    def __init__(self):
        width = 256
        height = 256
        pyxel.init(width, height, title="Nuit du Code")
        self.spaceship = SpaceShip()
        pyxel.load("1.pyxres")
        pyxel.run(self.update, self.draw)
        self.mastermind = Donjon()

    def update(self):
        """
        Gère l'actualisation des variables chaque seconde.
        :return: Nothing.
        """
        pyxel.cls(0)
        self.pause.mettre_pause()
        if self.spaceship.vie():
            return
        if self.pause.pause:
            etage = self.mastermind.niveau_courant.etage
            self.spaceship.move()
            self.spaceship.shoot()
            self.spaceship.move_shoots()
            self.spaceship.check_collision_shoots(self.mastermind.niveau_courant.obstacles)
            self.spaceship.collision_spaceship(self.mastermind.niveau_courant.obstacles)
            self.spaceship.collision_bonus_spaceship(self.mastermind.niveau_courant.bonus)
            self.spaceship.speed = 2 if etage < 4 else 4
            self.background.defilement = etage * 1.1 if etage * 1.1 < 6 else 6
            self.background.out()
            self.background.add()
            self.background.defiler()

    def draw(self):
        pyxel.cls(0)
        self.spaceship.draw_lives()
        self.spaceship.draw_bonus()
        
        if self.spaceship.vie():
            return
        if not self.pause.verif_pause
            self.background.draw_background()
            self.spaceship.draw_ship()
            self.spaceship.draw_shoots()
            self.mastermind.gerer_scroll()
            self.spaceship.draw_lives()



if __name__ == '__main__':
    game = Game()
