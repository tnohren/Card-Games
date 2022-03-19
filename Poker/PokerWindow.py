import sys
import pygame

# Global set of colors - to make standardization easier
class Colors:
    def __init__(self):
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.magenta = (60, 25, 60)

# Global set of fonts - to make standardization easier
class Fonts:
    def __init__(self):
        self.buttonFont = "Corbel"
        self.promptFont = "Corbel"

# Game Window and Functions to update its state
class Window:
    def __init__(self):
        # Structs and constants
        self.colors = Colors()
        self.fonts = Fonts()
        self.displayWidth = 800
        self.displayHeight = 600

        # Initialize pygame and display window
        pygame.init()
        self.surface = pygame.display.set_mode([self.displayWidth, self.displayHeight])

    def AddPrompt(self, prompt, buttonList):
        # Initialize fonts and texts
        buttonFont = pygame.font.SysFont(self.fonts.buttonFont, 25)
        buttonText = [buttonFont.render(button, True, self.colors.white) for button in buttonList]
        if prompt != '':
            promptFont = pygame.font.SysFont(self.fonts.promptFont, 25)
            promptText = promptFont.render(prompt, True, self.colors.white)
        numButtons = len(buttonList)
        
        # Continue until button is clicked
        while True:
            # Get mouse position
            mouse = pygame.mouse.get_pos()
            for ev in pygame.event.get():
                # quit on QUIT event
                if ev.type == pygame.QUIT:
                    pygame.quit()
                # If screen is clicked in one of our button's spaces, then return that button back
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    for i in range(numButtons):
                        if (((self.displayWidth / numButtons) + (150 * (i - 1))) <= mouse[0] <= (self.displayWidth / numButtons + (150 * i))) and ((self.displayHeight / 2) <= mouse[1] <= ((self.displayHeight / 2) + 50)):
                            self.surface.fill(self.colors.black)
                            return buttonList[i]
            # Draw each button's rectangle and text
            for i in range(numButtons):
                pygame.draw.rect(self.surface, self.colors.magenta, [(self.displayWidth / numButtons) + (150 * (i - 1)), (self.displayHeight / 2), 150, 50])
                self.surface.blit(buttonText[i], [(self.displayWidth / numButtons) + 10 + (150 * (i - 1)), (self.displayHeight / 2)])

            # Draw Prompt Text if provided
            if prompt != '':
                self.surface.blit(promptText, [10, 10])

            # Update Window's Display
            pygame.display.update()

    def Quit(self):
        pygame.quit()