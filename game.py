from game_resources import GameResources
from game_result import GameResult
from game_state_types import GameStateTypes
from command import ICommand
from command_manager import CommandManager
from game_skills import GameSkills
from game_timer import GameTimer
from game_victory_condition import GameVictoryCondition
from lemming_manager import LemmingManager
from object_manager import ObjectManager
from trigger_manager import TriggerManager
from lemmings_sprite import LemmingsSprite
from level import Level
from mask_provider import MaskProvider
from particle_table import ParticleTable
from skill_panel_sprites import SkillPanelSprites
from event_handler import EventHandler
from log_handler import LogHandler
from display_image import DisplayImage
from game_display import GameDisplay
from game_gui import GameGui

class Game:
    def __init__(self, level, masks, lem_sprite, skill_panel_sprites):
        self.log = LogHandler('Game')
        self.level = level
        self.triggerManager = TriggerManager()
        self.lemmingManager = None
        self.objectManager = None
        self.gameVictoryCondition = None
        self.gameGui = None
        self.guiDisplay = None
        self.display = None
        self.gameDisplay = None
        self.gameTimer = None
        self.commandManager = None
        self.skills = None
        self.showDebug = False
        self.onGameEnd = EventHandler()
        self.finalGameState = GameStateTypes.UNKNOWN
        self.gameTimer = GameTimer(self.level)
        self.skills = GameSkills(self.level)
        self.gameVictoryCondition = GameVictoryCondition(self.level)
        self.commandManager = CommandManager(self, self.gameTimer)
        self.gameTimer.onGameTick.on(self.onGameTimerTick)
        self.triggerManager.addRange(self.level.triggers)
        particleTable = ParticleTable(self.level.colorPalette)
        self.lemmingManager = LemmingManager(self.level, lem_sprite, self.triggerManager, self.gameVictoryCondition, masks, particleTable)
        self.gameGui = GameGui(self, skill_panel_sprites, self.skills, self.gameTimer, self.gameVictoryCondition)
        if self.guiDisplay:
            self.gameGui.setGuiDisplay(self.guiDisplay)
        self.objectManager = ObjectManager(self.gameTimer)
        self.objectManager.addRange(self.level.objects)
        self.gameDisplay = GameDisplay(self, self.level, self.lemmingManager, self.objectManager, self.triggerManager)
        if self.display:
            self.gameDisplay.setGuiDisplay(self.display)

    def setGameDisplay(self, display):
        self.display = display
        if not self.gameDisplay:
            return
        self.gameDisplay.setGuiDisplay(display)
        if self.level:
            self.display.setScreenPosition(self.level.screenPositionX, 0)

    def setGuiDisplay(self, display):
        self.guiDisplay = display
        if self.gameGui:
            self.gameGui.setGuiDisplay(display)

    @staticmethod
    async def loadLevel(gameResources, levelGroupIndex, levelIndex):
        level = await gameResources.getLevel(levelGroupIndex, levelIndex)
        if not level:
            return None
        maskPromise = gameResources.getMasks()
        lemPromise = gameResources.getLemmingsSprite(level.colorPalette)
        results = await Promise.all([maskPromise, lemPromise])
        skillPanelSprites = await gameResources.getSkillPanelSprite(level.colorPalette)
        return Game(level, results[0], results[1], skillPanelSprites)

    def start(self):
        self.gameTimer.continue()

    def stop(self):
        if self.gameTimer:
            self.gameTimer.stop()
        self.onGameEnd.dispose()

    def getGameTimer(self):
	return self.gameTimer

def cheat(self):
    if not self.skills:
        return
    self.skills.cheat()

def getGameSkills(self):
    return self.skills

def getLemmingManager(self):
    return self.lemmingManager

def getVictoryCondition(self):
    return self.gameVictoryCondition

def getCommandManager(self):
    return self.commandManager

def queueCommand(self, newCommand):
    if not self.commandManager:
        return
    self.commandManager.queueCommand(newCommand)

def setDebugMode(self, value):
    self.showDebug = value

def onGameTimerTick(self):
    self.runGameLogic()
    self.checkForGameOver()
    self.render()

def getGameState(self):
    if not self.gameTimer or not self.gameVictoryCondition:
        return GameStateTypes.UNKNOWN
    if self.finalGameState != GameStateTypes.UNKNOWN:
        return self.finalGameState
    hasWon = self.gameVictoryCondition.getSurvivorsCount() >= self.gameVictoryCondition.getNeedCount()
    if self.gameVictoryCondition.getLeftCount() <= 0 and self.gameVictoryCondition.getOutCount() <= 0:
        if hasWon:
            return GameStateTypes.SUCCEEDED
        else:
            return GameStateTypes.FAILED_LESS_LEMMINGS
    if self.gameTimer.getGameLeftTime() <= 0:
        if hasWon:
            return GameStateTypes.SUCCEEDED
        else:
            return GameStateTypes.FAILED_OUT_OF_TIME
    return GameStateTypes.RUNNING

def checkForGameOver(self):
    if not self.gameVictoryCondition:
        return
    if self.finalGameState != GameStateTypes.UNKNOWN:
        return
    state = self.getGameState()
    if state != GameStateTypes.RUNNING and state != GameStateTypes.UNKNOWN:
        self.gameVictoryCondition.doFinalize()
        self.finalGameState = state
        self.onGameEnd.trigger(GameResult(self))

def runGameLogic(self):
    if not self.lemmingManager:
        self.log.log('level not loaded!')
        return
    self.lemmingManager.tick()

def render(self):
    if self.gameDisplay:
        self.gameDisplay.render()
        if self.showDebug:
            self.gameDisplay.renderDebug()
    if self.gameGui:
        self.gameGui.render()
    if self.guiDisplay:
        self.guiDisplay.redraw()
