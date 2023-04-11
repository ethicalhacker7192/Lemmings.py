from typing import List
from resources.file.file_container import FileContainer
from resources.file.file_provider import FileProvider
from resources.level import Level
from resources.level_loader import LevelLoader
from resources.lemmings.color_palette import ColorPalette
from resources.lemmings.lemmings_sprite import LemmingsSprite
from resources.main_image_sprites import MainImageSprites
from resources.mask_provider import MaskProvider
from resources.skill_panel_sprites import SkillPanelSprites
from resources.sound.audio_player import AudioPlayer
from resources.sound.sound_image_manager import SoundImageManager
from resources.sound.sound_image_player import SoundImagePlayer
from utilities.config_reader import GameConfig


class GameResources:
    def __init__(self, file_provider: FileProvider, config: GameConfig):
        self.file_provider = file_provider
        self.config = config
        self.music_player = None
        self.sound_player = None
        self.sound_image = None
        self.main_dat = None

    def dispose(self):
        self.stop_music()
        self.stop_sound()
        self.sound_image

    def get_main_dat(self) -> FileContainer:
        if self.main_dat:
            return self.main_dat

        data = self.file_provider.load_binary(self.config.path, "MAIN.DAT")
        self.main_dat = FileContainer(data)
        return self.main_dat

    async def get_lemmings_sprite(self, color_palette: ColorPalette) -> LemmingsSprite:
        container = await self.get_main_dat()
        return LemmingsSprite(container.get_part(0), color_palette)

    async def get_skill_panel_sprite(self, color_palette: ColorPalette) -> SkillPanelSprites:
        container = await self.get_main_dat()
        return SkillPanelSprites(container.get_part(2), container.get_part(6), color_palette)

    async def get_masks(self) -> MaskProvider:
        container = await self.get_main_dat()
        return MaskProvider(container.get_part(1))

    async def get_main_image_sprites(self) -> MainImageSprites:
        container = await self.get_main_dat()
        return MainImageSprites(container.get_part(3), container.get_part(4))

    def get_level(self, level_mode: int, level_index: int) -> Level:
        level_reader = LevelLoader(self.file_provider, self.config)
        return level_reader.get_level(level_mode, level_index)

    def get_level_groups(self) -> List[str]:
        return self.config.level.groups

    async def init_sound_image(self) -> SoundImageManager:
        if self.sound_image:
            return self.sound_image

        data = self.file_provider.load_binary(self.config.path, "ADLIB.DAT")
        container = FileContainer(data)
        sound_image = SoundImageManager(container.get_part(0), self.config.audio_config)
        self.sound_image = sound_image
        return sound_image

    def stop_music(self):
        if not self.music_player:
            return
        self.music_player.stop()
        self.music_player = None

    async def get_music_player(self, song_index: int) -> AudioPlayer:
        self.stop_music()
        sound_image = await self.init_sound_image()
        adlib_src = sound_image.get_music_track(song_index)
        self.music_player = AudioPlayer(adlib_src)
        return self.music_player

    def stop_sound(self):
        if not self.sound_player:
            return
        self.sound_player.stop()
        self.sound_player = None

    async def get_sound_player(self, sound_index: int) -> AudioPlayer:
        self.stop_sound()
        sound_image = await self.init_sound_image()
        adlib_src = sound_image.get_sound_track(sound_index)
        self.sound_player = AudioPlayer(adlib_src)
	return self.sound_player
