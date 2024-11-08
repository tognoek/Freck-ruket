import pygame
from models.game_entities.entity import Entity
from models.game_entities.character import Character

class Fire_90(Entity):
    def __init__(self, name, pos, images, sound, flip, volume, frame, size_frame = 5, type_entity = 1, z_index = 1, data = None):
        super().__init__(name, pos, images, sound, flip, volume, frame, size_frame, type_entity, z_index)
        self.data = data
        self.is_active = True
        self.count_active = 0
        self.size_frame_fire = 5
        self.index_frame_fire = 0
        self.range = [2, 3, 6, 7]
        self.range_f = [0, 1, 4, 5]

    def collision_player(self, player : Character):
        if self.is_active:
            frame = int(self.frame / self.size_frame)
            if self.flip[0]:
                x = self.get_pos()[0]
                x_f = x + 16
            else:
                x = self.get_pos()[0] + self.data[self.action][frame][0][0]
                x_f = x - 16
            y = self.get_pos()[1] + self.data[self.action][frame][0][1]
            w = self.data[self.action][frame][1][0]
            h = self.data[self.action][frame][1][1]
            w_f = w - 16
            other_rect = pygame.Rect((x, y),(w, h))
            other_rect_fire = pygame.Rect((x_f, y),(w_f, h))
            player_rect = player.rect()
            if self.type_entity == 1:
                if self.action == "On":
                    for i in self.range_f:
                        if player.collision_tognoek(other_rect_fire, player.data[player.action][i]):
                            player.type_entity = 3
                            return
                for i in self.range:
                     if player.collision_tognoek(other_rect, player.data[player.action][i]): 
                        if self.action == "On":
                            if (i < 4 and not self.flip[0]) or (i > 4 and self.flip[0]):
                                player.type_entity = 3
                                return
                if player.speed[0] > 0:
                    if player.collision_tognoek(other_rect, player.data[player.action][2]):
                        player_rect.right = other_rect.left + (player_rect.width - player.data[player.action][2][0])
                        player.collisions["right"] = True
                        if not self.flip[0]:
                             self.set_action("Hit")
                    if player.collision_tognoek(other_rect, player.data[player.action][3]):
                        player_rect.right = other_rect.left + (player_rect.width - player.data[player.action][2][0])
                        player.collisions["right"] = True
                        if not self.flip[0]:
                             self.set_action("Hit")
                if player.speed[0] < 0:
                    if player.collision_tognoek(other_rect, player.data[player.action][6]):
                        player_rect.left = other_rect.right - player.data[player.action][6][0] - 1
                        player.collisions["left"] = True
                        if self.flip[0]:
                             self.set_action("Hit")
                    if player.collision_tognoek(other_rect, player.data[player.action][7]):
                        player_rect.left = other_rect.right - player.data[player.action][7][0] - 1
                        player.collisions["left"] = True
                        if self.flip[0]:
                             self.set_action("Hit")
                
                player.pos = (player_rect.x, player.pos[1])
            player_rect = player.rect()
            if self.type_entity == 1:
                if player.speed[1] < 0:
                    if player.collision_tognoek(other_rect, player.data[player.action][0]):
                            player_rect.top = other_rect.bottom - player.data[player.action][0][1] - 1
                            player.collisions["up"] = True
                    if player.collision_tognoek(other_rect, player.data[player.action][1]):
                            player_rect.top = other_rect.bottom - player.data[player.action][1][1] - 1
                            player.collisions["up"] = True
                if player.speed[1] > 0:
                    if player.collision_tognoek(other_rect, player.data[player.action][4]):
                            player_rect.bottom = other_rect.top + (player_rect.height - player.data[player.action][4][1])
                            player.collisions["down"] = True
                    if player.collision_tognoek(other_rect, player.data[player.action][5]):
                            player_rect.bottom = other_rect.top + (player_rect.height - player.data[player.action][5][1])
                            player.collisions["down"] = True
                player.pos = (player.pos[0], player_rect.y)

    def update(self, loop=False):
        self.frame += 1
        if self.frame >= len(self.images[self.action]) * self.size_frame:
            self.frame = 0
            if self.action == "On":
                self.index_frame_fire += 1
            if self.index_frame_fire > self.size_frame_fire:
                self.index_frame_fire = 0
                self.set_action("Idle")
            if self.action == "Hit":
                self.set_action("On")
