import pygame
from config import *
from tile import *
from dief import Player
from cavaleiro import Cavaleiro
from chave import Chave
from bau import Bau
#from pygameZoom import PygameZoom


class Level:
    def __init__(self):
        # "superficie" a ser exibida
        self.display_surface = pygame.display.get_surface()
        # grupos de sprite
        self.visible_sprites = YSortCameraGroup()  # pygame.sprite.Group()
        self.obstacles_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

    def create_map(self):
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                Y = row_index * TILESIZE
                if col == "x":
                    Tile((x, Y), [self.visible_sprites, self.obstacles_sprites])
                '''if col == "y":
                    x = x * 3
                    Y = Y * 3
                    Tile2((x, Y), [self.visible_sprites, self.obstacles_sprites])
                if col == "z":
                    x = x * 3
                    Y = Y * 3
                    Tile3((x, Y), [self.visible_sprites, self.obstacles_sprites])'''
                if col == "p":
                    self.player = Player((x, Y), [self.visible_sprites],self.obstacles_sprites)
                if col == "c":
                    Cavaleiro((x,Y),[self.visible_sprites, self.obstacles_sprites])
                if col == "k":
                    Chave((x,Y),[self.visible_sprites,self.obstacles_sprites])
                if col == "b":
                    Bau((x,Y),[self.visible_sprites,self.obstacles_sprites])

    def run(self):
        # atualiza e desenha o jogo
        self.visible_sprites.custom_draw(self.player)  # draw(self.display_surface)
        self.visible_sprites.update()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        #criando o chao
        self.floor_surf = pygame.image.load('tile_fixed.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

    def custom_draw(self, player):
        # fazendo o recorte
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        #desenhando o chao
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf,floor_offset_pos)

        #for sprite in self.sprites():
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            #self.display_surface.blit(pygame.transform.scale(sprite.image,(100,120)), offset_pos)
            self.display_surface.blit(sprite.image, offset_pos)
