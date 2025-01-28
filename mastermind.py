# Import of mm.py, Pygame and random
import mm
import pygame
import random

# Generates the secret code, choce randomly from the list "mm.TabCouleur"
def createSecret():
    secret = []
    for i in range(5):
        index = random.randrange(0, 8)
        secret.append(mm.TabCouleur[index])
    return secret

# Compares player's guess with the secret code
# Return a tuple (well_placed, badly_placed)
def gameResult(proposition: list, secret: list) -> tuple:
    well_placed = 0
    badly_placed = 0
    secret_copy = secret.copy()
    proposition_copy = proposition.copy()

    # For in loop checking for well placed 
    for i in range(len(proposition)):
        if proposition[i] == secret[i]:
            well_placed += 1
            secret_copy[i] = None
            proposition_copy[i] = None

    # For in loop checking badly placed
    for i in range(len(proposition_copy)):
        if proposition_copy[i] is not None and proposition_copy[i] in secret_copy:
            badly_placed += 1
            secret_copy[secret_copy.index(proposition_copy[i])] = None

    return (well_placed, badly_placed)

# Displays the end game screen
def endGame(screen, line, win):
    top_text = "Bravo ! Vous avez gagné !" if win else "Dommage ! Vous avez perdu !"
    end_text = f"Partie terminée en {line} essais"

    rect_x, rect_y = 150, 150
    rect_width, rect_height = 530, 200
    pygame.draw.rect(screen, mm.Noir, [rect_x, rect_y, rect_width, rect_height], 3)
    pygame.draw.rect(screen, mm.Marron, [rect_x + 3, rect_y + 3, rect_width - 6, rect_height - 6])

    myfont = pygame.font.SysFont("monospace", 30)
    top_label = myfont.render(top_text, 1, mm.Noir)
    end_label = myfont.render(end_text, 1, mm.Noir)
    screen.blit(top_label, (screen.get_width() // 2 - top_label.get_width() // 2, 200))
    screen.blit(end_label, (screen.get_width() // 2 - end_label.get_width() // 2, rect_y + rect_height // 2))

    pygame.display.update()

# Main game function
def main():
    # Initialization fo Pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 700))
    pygame.display.set_caption("Mastermind")
    clock = pygame.time.Clock()
    running = True

    # Initialization of the game's variables
    secret = createSecret()
    print(secret)
    line = 2
    playing = True
    win = False

    # Randering of the user-machine interface
    screen.fill(mm.Blanc)
    mm.afficherPlateau(screen)
    mm.afficherChoixCouleur(screen)

    # Main game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not playing:
            endGame(screen, line - 2, win)
            mm.afficherCombinaison(screen, secret, 0.5)
            continue # Continue the loop without executing the rest of the code

        # If the game is over, displays the end screen
        player_proposition = mm.construireProposition(screen, line)

        # Calculate the result of the guess with respect to the secret combination and display it
        res = gameResult(player_proposition, secret)
        mm.afficherResultat(screen, res, line)

        pygame.display.update()

        # Checks victory or defeat conditions
        if res[0] == 5: # All colors well placed -> Victory
            playing = False
            win = True
        elif line > 15: # More than 15 tries -> Defeat
            playing = False
            win = False

        line += 1 # Move on to the next test
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
