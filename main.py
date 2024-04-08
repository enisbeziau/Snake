import pygame
import random
import math


pygame.init()

POLICE = pygame.font.Font('freesansbold.ttf', 25)

LONGUEUR = 800
LARGEUR = 800
COULEUR_FOND = (38, 82, 99)


PX_DEPLACEMENT = 20
COTE = 25
DELAI_ENTRE_LES_COUPS = 50
AUGMENTATION = 4


class Game:
    def __init__(self):
        self.fen = pygame.display.set_mode((LONGUEUR, LARGEUR))
        self.running = True
        self.nouvelle_pos = None
        self.longueur, self.pommes = 0, 0
        self.x, self.y = LONGUEUR // 2, LARGEUR // 2
        self.tab_pos: list[tuple[int, int]] = []
        self.commandes = {
            pygame.K_UP: (0, -PX_DEPLACEMENT),
            pygame.K_DOWN: (0, PX_DEPLACEMENT),
            pygame.K_RIGHT: (PX_DEPLACEMENT, 0),
            pygame.K_LEFT: (-PX_DEPLACEMENT, 0)
        }
        self.fen.fill(COULEUR_FOND)

    @staticmethod
    def distance(a: tuple[int, int], b: tuple[int, int]) -> float:
        """Renvoie la distance entre les points a et b"""
        return math.sqrt((b[0] - a[0]) * (b[0] - a[0]) + (b[1] - a[1]) * (b[1] - a[1]))

    def dessiner(self, pos: tuple[int, int], couleur: str = 'white') -> None:
        """Dessine sur le plateau un carré de coin supérieur gauche pos et de couleur spécifiée"""
        pygame.draw.rect(self.fen, couleur, (*pos, COTE, COTE))
        return None

    def supprimer(self, pos: tuple[int, int]) -> None:
        """Supprime le carré de coin supérieur gauche pos en redessinant un carré de couleur COULEUR_FOND """
        pygame.draw.rect(self.fen, COULEUR_FOND, (*pos, COTE, COTE))
        return None

    def generer_pomme(self) -> tuple[int, int]:
        """
        Génère la pomme du jeu et renvoie ses coordonnées sous la forme d'un tuple d'int
        pour que les coordonnées soient valides, il faut que celles-ci ne tombent pas sur le serpent
        """
        while True:
            x, y = random.randint(100, LARGEUR - 100), random.randint(100, LONGUEUR - 100)
            if (x, y) not in self.tab_pos:
                break
        self.dessiner((x, y), 'red')
        return x, y

    def verif_prochain_coup(self, prochaine_pos: tuple[int, int]) -> bool:
        """
        Renvoie un boolean indiquant si le prochain déplacement est légal
        Les déplacements illégaux sont :
            - dépasser les limites du terrain définies par LONGUEUR et LARGEUR
            - toucher une partie du corps du serpent
        """
        futur_x = prochaine_pos[0] + self.x
        futur_y = prochaine_pos[1] + self.y
        return (2 <= futur_x <= LARGEUR - 2 and 2 <= futur_y <= LONGUEUR - 2) and (futur_x, futur_y) not in self.tab_pos

    def deplacer(self, pos: tuple[int, int]) -> None:
        """Fonction de gestion d'un tour"""

        if self.verif_prochain_coup(pos):

            if len(self.tab_pos) > self.longueur:
                self.supprimer(self.tab_pos.pop(0))

            self.x, self.y = self.x + pos[0], self.y + pos[1]
            self.tab_pos.append((self.x, self.y))

            for pos in self.tab_pos:
                self.dessiner((pos[0], pos[1]))

        else:
            self.running = False
        return None

    def afficher_score(self) -> None:
        """Affiche le nbr de pommes en haut à droite de l'écran"""
        self.fen.fill(COULEUR_FOND, (LARGEUR - 300, 0, 300, 50))
        txt = POLICE.render(
            f"Nombre de pommes ramassées : {self.pommes}",
            True,
            'white', 'black')
        txt.set_colorkey((0, 0, 0))
        zone_de_txt = txt.get_rect()
        zone_de_txt.center = (LARGEUR - 250, 20)
        self.fen.blit(txt, zone_de_txt)
        return None

    def run(self) -> None:
        """Fonction contenant la boucle interne du jeu"""
        self.dessiner((self.x, self.y))
        self.tab_pos.append((self.x, self.y))
        x_pomme, y_pomme = self.generer_pomme()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key in self.commandes.keys():
                    self.nouvelle_pos = self.commandes.get(event.key)

            self.afficher_score()

            distance_pomme = self.distance((self.x, self.y), (x_pomme, y_pomme))
            if distance_pomme < COTE:
                self.supprimer((x_pomme, y_pomme))
                self.longueur += AUGMENTATION
                self.pommes += 1
                x_pomme, y_pomme = self.generer_pomme()

            if self.nouvelle_pos is not None:
                self.deplacer(self.nouvelle_pos)

            pygame.time.delay(DELAI_ENTRE_LES_COUPS)
            pygame.display.flip()


if __name__ == '__main__':
    game = Game()
    game.run()
