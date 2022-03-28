import sys
import pygame
import math
import PrimaryColors
import PrimaryFonts

class Window:
    def __init__(self):
        # Initialize Set of Colors and Fonts
        self.primaryColors = PrimaryColors.Colors()
        self.primaryFonts = PrimaryFonts.Fonts()

        # Initialize Screen Size
        self.displayWidth = 800
        self.displayHeight = 600

        # Initialize Window
        pygame.init()
        self.screen = pygame.display.set_mode([self.displayWidth, self.displayHeight])

    def AddPrompt(self, promptList, buttonList):
        # Initialize fonts, texts
        promptFont = pygame.font.SysFont(self.primaryFonts.promptFont, 15)
        buttonFont = pygame.font.SysFont(self.primaryFonts.buttonFont, 25)
        buttonText = [buttonFont.render(button, True, self.primaryColors.white) for button in buttonList]

        # Useful attributes to handle variable number of buttons
        numButtons = len(buttonList)
        buttonWidth = 150
        buttonHeight = 50
        buttonStartPos = math.floor((self.displayWidth - (buttonWidth * numButtons)) / 2)
        
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
                        if (((buttonStartPos) + (150 * i)) <= mouse[0] <= (buttonStartPos + (150 * (i + 1)))) and ((self.displayHeight / 2) <= mouse[1] <= ((self.displayHeight / 2) + buttonHeight)):
                            self.screen.fill(self.primaryColors.black)
                            return buttonList[i]
            # Draw each button's rectangle and text
            for i in range(numButtons):
                pygame.draw.rect(self.screen, self.primaryColors.magenta, [buttonStartPos + (150 * i), (self.displayHeight / 2), 150, buttonHeight])
                self.screen.blit(buttonText[i], [buttonStartPos + 10 + (150 * i), math.floor((self.displayHeight / 2) + (buttonHeight / 4))])

            # Draw Prompt Text if provided
            for i in range(len(promptList)):
                self.screen.blit(promptFont.render(promptList[i], True, self.primaryColors.white), [10, 20 * i])

            # Update Window's Display
            pygame.display.update()

    def Quit(self):
        pygame.quit()