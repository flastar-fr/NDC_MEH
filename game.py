import pyxel


class SpaceShip:
    """Gère tout ce qui est lié au vaisseau."""
    def __init__(self):
        self.x: int = 100
        self.y: int = 100
        self.shots: list[Tir] = []
        self._can_shoot = False
        self._can_hit = True
        self.cooldown = 1
        self.lives = 3
        self.speed = 2
        self.compteur = 45

    def move(self):
        """Permet de bouger le vaisseau."""
        if pyxel.btn(pyxel.KEY_Z):
            self.y -= self.speed
        if pyxel.btn(pyxel.KEY_S):
            self.y += self.speed
        if pyxel.btn(pyxel.KEY_Q):
            self.x -= self.speed
        if pyxel.btn(pyxel.KEY_D):
            self.x += self.speed

        if self.x > 246:
            self.x = 246
        if self.y > 246:
            self.y = 246
        if self.x < 0:
            self.x = 0
        if self.y < 0:
            self.y = 0

    def shoot(self):
        """Permet de tirer."""
        if not self._can_shoot:
            self._can_shoot = pyxel.frame_count % (self.cooldown*30) == 0
            return None

        if pyxel.btnp(pyxel.KEY_SPACE, repeat=False):
            self.shots.append(Tir(self.x, self.y))
            pyxel.play(2, 3)
            self._can_shoot = False

    def draw_ship(self):
        """Affiche le vaisseau."""
        pyxel.blt(self.x-4, self.y+3, 0, 0, 10, 16, 12, 5)

    def vie(self):
        """Pour connaître si le joueur n'a plus de vie."""
        return self.lives < 1

    def move_shoots(self):
        """Déplace les tirs."""
        del_shots = []
        for shot in self.shots:
            shot.y -= 5
            if shot.y <= 0:
                del_shots.append(shot)

        for shot in del_shots:
            del_shots.remove(shot)

    def check_collision_shoots(self, enemies):
        """Permet de détecter les collisions entre les tirs et les ennemis."""
        to_del = []
        for shot in self.shots:
            if shot.collision(enemies):
                to_del.append(shot)

        for shot in to_del:
            self.shots.remove(shot)

    def collision_spaceship(self, enemies):
        """Permet de détecter les colisions entre le vaisseau et les ennemis."""
        if self._can_hit:
            for e in enemies:
                if type(e) is not Bonus:
                    if (e.x - self.x < 8 and e.x - self.x > -8) and (e.y - self.y > -8 and e.y - self.y < 8):
                        self.lives -= 1
                        pyxel.play(3, 5)
                        self._can_hit = False
        else:
            self.compteur -= 1
            if self.compteur <= 0:
                self.compteur = 60
                self._can_hit = True

    def collision_bonus_spaceship(self, bonus):
        """Détecte les collisions entre les bonus et le vaisseau."""
        for e in bonus:
            if (e.x - self.x < 10 and e.x - self.x > -10) and (e.y - self.y > -10 and e.y - self.y < 10):
                self.lives += 1
                e.consummed = True
                pyxel.play(1, 4)

    def draw_shoots(self):
        """Affiche les tirs."""
        for shot in self.shots:
            pyxel.blt(shot.x, shot.y, 0, 48, 73, 8, 7, 5)

    def draw_lives(self):
        """Affiche le nombre de vies restantes."""
        pyxel.text(5, 5, f"Vies : {self.lives}", 8)


class Tir:
    """Stocke les tirs."""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def collision(self, enemie):
        for e in enemie:
            if (e.x - self.x < 10 and e.x - self.x > -10) and (e.y - self.y > -10 and e.y - self.y < 10):
                if type(e) is Enemmi:
                    e.pv -= 1
                if type(e) is Bonus:
                    return False
                return True
        return False


class Donjon:
    """
    Classe permettant de contrôler l'enemble des ennemis et fonctions liées à l'avancement du joueur.
    Il n'existe toujours qu'on objet Donjon car il repésente la partie en cours.
    """
    def __init__(self):
        self.etage = 1
        self.niveau_courant = Niveau(1)

    def niveau_superieur(self):
        """
        Permet de savoir si l'étage en cours est arrivé à son terme ou non.
        :return: Nothing.
        """
        if self.niveau_courant.gerer_fin():
            self.etage += 1
            self.niveau_courant = Niveau(self.etage)
            pyxel.play(3, 2)

    def gerer_scroll(self):
        """
        Permet de gérer le scrolling des obstacles ainsi que l'avancée du niveau à chaque seconde.
        :return: Nothing.
        """
        self.niveau_courant.scroll()
        self.niveau_courant.draw_ennemis()
        self.niveau_courant.verify_hp()
        self.niveau_superieur()


class Niveau:
    """Classe représentant un niveau, notamment les obstacles qui le composent.
    Elle dépend de l'étage, c'est-à-dire de l'avancée du joueur."""
    def __init__(self, etage):
        self.etage = etage
        self.nb_obstacle_to_generate = etage * 5
        self.obstacle_line = []
        for i in range(25):
            self.obstacle_line += [i + 1] * (25 - i)
        self.obstacles = self.generate_level()
        # Liste de listes. Chaque sous-liste représente un obstacle :
        # [ Numéro de l'ennemi (son id), [Son x, son y]]
        # Les x et y sont le coin bas droite de l'image

    def scroll(self):
        """
        Permet l'avcancée des obstacles et le déplacement des monstres du niveau, chaque seconde.
        """
        for obstacle in self.obstacles:
            speed = self.etage * 1.05 if self.etage * 1.05 < 6 else 6
            obstacle.y += speed
            if type(obstacle) is Enemmi:
                if obstacle.is_going_right:
                    obstacle.x += 1
                    if obstacle.x >= 248:
                        obstacle.is_going_right = False
                else:
                    obstacle.x -= 1
                    if obstacle.x <= 0:
                        obstacle.is_going_right = True

    def verify_hp(self):
        """

        :return:
        """
        for b in self.bonus:
            if b.consummed:
                self.obstacles.remove(b)
        for enemi in self.enemies:
            if enemi.pv <= 0:
                self.obstacles.remove(enemi)
                pyxel.play(1, 1)
                self.obstacles.append(Bonus(enemi.x, -5))
        to_del = []
        for obstacle in self.obstacles:
            if obstacle.y >= 256:
                to_del.append(obstacle)

        for obstacle in to_del:
            self.obstacles.remove(obstacle)

    def generate_level(self):
        """
        Génère l'étage en cours.
        :return: Les obstacles sous forme de liste de listes.
        """
        obstacles = []

        for i in range(self.nb_obstacle_to_generate):
            obstacles += self.generer_etage(i)

        return obstacles

    def generer_etage(self, iteration: int):
        """
        Génère une ligne d'obstacles constituant un étage.
        :param iteration: Le nombre d'obstacles à générer.
        :return: La ligne sous forme de liste d'objets Enemmi et Obstacle.
        """
        random_int = pyxel.rndi(0, len(self.obstacle_line)-1)

        nb_obstacle = self.obstacle_line[random_int]
        if nb_obstacle == 1:
            return [Enemmi(self.etage, pyxel.rndi(0, 8), -10-iteration*50, 1)]

        line = []
        random_x = pyxel.rndi(0, 256-10*nb_obstacle)
        for i in range(nb_obstacle):
            line.append(Obstacle(self.etage, random_x+10*i, -10-iteration*50))

        return line

    def gerer_fin(self):
        """
        Permet de savoir si un étage est terminé ou non.
        :return: Un booléen.
        """
        return len(self.obstacles) == 0

    def draw_ennemis(self):
        """
        Représente les ennemis, obstacles et bonus à l'écran.
        :return:
        """
        for o in self.obstacles:
            if type(o) is Bonus:
                pyxel.blt(o.x, o.y, 0, o.affichage[0], o.affichage[1], o.affichage[2], o.affichage[3], 5)
            else:
                pyxel.blt(o.x, o.y, 0, o.affichage[1][0], o.affichage[1][1], o.affichage[1][2], o.affichage[1][3], 5)

    @property
    def enemies(self) -> list:
        """ Méthode property pour avoir accès facilement aux ennemies du niveau """
        return [o for o in self.obstacles if type(o) is Enemmi]

    @property
    def bonus(self) -> list:
        """ Méthode property pour avoir accès facilement aux bonus du niveau """
        return [o for o in self.obstacles if type(o) is Bonus]


class Obstacle:
    """
    Classe repésentant un obstacle à l'écran.
    """
    def __init__(self, type_obstacle: int, x, y):
        self.affichage = [type_obstacle, self.img_coordinates(type_obstacle)]
        self.x = x
        self.y = y

    def img_coordinates(self, type):
        """
        Cette fonction permet de savoir l'image associée à l'obstacle en fonction de son type.
        :param type: Le type de l'ennemi, c'est-à-dire l'image voulue.
        :return:
        """
        if type == 1:
            return [19, 107, 11, 11]
        elif type == 2:
            return [35, 107, 11, 11]
        elif type == 3:
            return [51, 107, 11, 11]
        elif type == 4:
            return [3, 123, 11, 11]
        elif type == 5:
            return [24, 72, 7, 7]
        elif type == 6:
            return [16, 72, 7, 7]
        else:
            return [8, 72, 7, 7]


class Enemmi:
    """
    Représente un ennemi. Il est caractérisé par ses coordonnées x et y, par ses points de vie et par son type.
    """
    def __init__(self, stage_type: int, x, y, pv):
        self.affichage = [stage_type, self.image_coordinates(stage_type)]
        self.x = x
        self.y = y
        self.pv = pv
        self.is_going_right = True

    def image_coordinates(self, stage_type):
        """
        Permet de connaître l'image associée à l'ennemi en fonction du stage-type.
        :param stage_type: Le type de l'ennemi.
        :return:
        """
        match stage_type:
            case 1:
                return [52, 59, 9, 9]
            case 2:
                return [36, 59, 9, 9]
            case 3:
                return [20, 59, 9, 9]
            case 4:
                return [4, 59, 9, 9]
            case 5:
                return [4, 43, 9, 9]
            case 6:
                return [20, 43, 9, 9]
            case 7:
                return [36, 43, 9, 9]
            case _:
                return [52, 43, 9, 9]


class Bonus:
    """
    Représente un Bonus,notamment grâce à ses coordonnées x et y.
    """
    def __init__(self, x, y):
        self.affichage = [41, 81, 6, 4]
        self.x = x
        self.y = y
        self.type = pyxel.rndi(0, 1)
        self.consummed = False


class Background:
    """Permet d'afficher un fond étoilé."""
    def __init__(self):
        """Génere le fond étoilé."""
        self.quotas = 50
        self.li = [[pyxel.rndi(10, 246), pyxel.rndi(10, 246)] for _ in range(self.quotas)]
        self.defilement = 1

    def add(self):
        """Ajoute aléatoirement des étoiles en haut de la fenêtre."""
        while len(self.li) < self.quotas:
            self.li.append([pyxel.rndi(10, 246), -10])

    def out(self):
        """Supprime les étoiles en dehors de la fenêtre."""
        li = self.li.copy()
        for k in li:
            if k[1] > 256:
                self.li.remove(k)

    def draw_background(self):
        """Affiche le fond étoilé."""
        for star in self.li:
            pyxel.rect(star[0], star[1], 1, 1, 7)

    def defiler(self):
        """Permet de faire défiler le fond."""
        for star in self.li:
            star[1] += self.defilement


class Pause:
    """Cette classe permet de gérer le menu pause."""
    def __init__(self):
        self.pause = True

    def mettre_pause(self):
        """Permet de mettre en pause le jeu."""
        if pyxel.btnp(pyxel.KEY_P):
            if self.pause:
                self.pause = False
            else:
                self.pause = True


class Game:
    """C'est la classe principale qui incarne la session du joueur."""
    def __init__(self):
        width = 256
        height = 256
        pyxel.init(width, height, title="Nuit du Code")
        self.spaceship = SpaceShip()
        self.mastermind = Donjon()
        self.background = Background()
        self.pause = Pause()
        self.game_over_frame = 0
        pyxel.load("1.pyxres")
        pyxel.playm(0, loop=True)
        pyxel.run(self.update, self.draw)

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
            self.background.defilement = etage * 1.05 if etage * 1.05 < 6 else 6
            self.background.out()
            self.background.add()
            self.background.defiler()

    def draw(self):
        """éxecute les méthodes pour afficher les élements à l'écran."""
        pyxel.cls(0)
        self.spaceship.draw_lives()
        pyxel.text(120,5,str(f"Etage : {self.mastermind.niveau_courant.etage}"), 7)
        if self.spaceship.vie():
            pyxel.text(115,115, "Game Over", 7)
            self.game_over_frame = pyxel.frame_count if self.game_over_frame == 0 else self.game_over_frame
            if pyxel.frame_count - self.game_over_frame >= 60:
                self.spaceship = SpaceShip()
                self.mastermind = Donjon()
                self.background = Background()
                self.pause = Pause()
                self.game_over_frame = 0
            return
        if self.pause.pause:
            self.background.draw_background()
            self.spaceship.draw_ship()
            self.spaceship.draw_shoots()
            self.mastermind.gerer_scroll()
            self.spaceship.draw_lives()
        else:
            pyxel.text(115, 115, "Pause", 7)


if __name__ == '__main__':
    game = Game()
