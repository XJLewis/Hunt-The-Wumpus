# game_state.py

import random
from config import NUM_PITS, NUM_BATS, START_ARROWS


class GameState:
    def __init__(self):
        self.start_room = 0  # Start in room 0
        self.reset()

    def reset(self):
        """Reset the game state"""
        self.rooms = list(range(20))

        self.tunnels = {
            0: [1, 4, 5], 1: [0, 2, 7], 2: [1, 3, 9],
            3: [2, 4, 11], 4: [0, 3, 13], 5: [0, 6, 14],
            6: [5, 7, 15], 7: [1, 6, 16], 8: [9, 16, 17],
            9: [2, 8, 18], 10: [11, 12, 18], 11: [3, 10, 19],
            12: [10, 13, 14], 13: [4, 12, 19], 14: [5, 12, 15],
            15: [6, 14, 16], 16: [7, 8, 15], 17: [8, 18, 19],
            18: [9, 10, 17], 19: [11, 13, 17]
        }

        self.player_room = 0
        self.room_contents = ["empty"] * 20

        self.arrows = START_ARROWS
        self.game_over = False
        self.win = False
        self.message = ""
        self.show_hazards = False

        self.place_wumpus_closer()
        self.place_pits()
        self.place_bats()
        self.get_warnings()

    def place_wumpus_closer(self):
        """Place the wumpus in a room 2-3 steps away"""
        distance_2_rooms = set()
        for adjacent_room in self.tunnels[self.player_room]:
            for r in self.tunnels[adjacent_room]:
                if r != self.player_room:
                    distance_2_rooms.add(r)

        distance_3_rooms = set()
        for room_2_away in distance_2_rooms:
            for r in self.tunnels[room_2_away]:
                if r != self.player_room and r not in distance_2_rooms:
                    distance_3_rooms.add(r)

        possible_rooms = (
            list(distance_3_rooms) if distance_3_rooms
            else list(distance_2_rooms)
        )

        if possible_rooms:
            self.wumpus_room = random.choice(possible_rooms)
        else:
            exclude_rooms = [self.player_room] + self.tunnels[self.player_room]
            possible_rooms = [r for r in self.rooms if r not in exclude_rooms]
            self.wumpus_room = random.choice(possible_rooms)

        self.room_contents[self.wumpus_room] = "wumpus"

    def place_pits(self):
        """Place pits in random rooms"""
        for _ in range(NUM_PITS):
            exclude_rooms = [self.player_room, self.wumpus_room]
            exclude_rooms += self.tunnels[self.player_room]
            exclude_rooms += [
                i for i, content in enumerate(self.room_contents)
                if content != "empty"
            ]
            possible_rooms = [r for r in self.rooms if r not in exclude_rooms]
            if possible_rooms:
                pit_room = random.choice(possible_rooms)
                self.room_contents[pit_room] = "pit"

    def place_bats(self):
        """Place bats in random rooms"""
        for _ in range(NUM_BATS):
            exclude_rooms = [self.player_room, self.wumpus_room]
            exclude_rooms += self.tunnels[self.player_room]
            exclude_rooms += [
                i for i, content in enumerate(self.room_contents)
                if content != "empty"
            ]
            possible_rooms = [r for r in self.rooms if r not in exclude_rooms]
            if possible_rooms:
                bat_room = random.choice(possible_rooms)
                self.room_contents[bat_room] = "bat"

    def move_player(self, tunnel_index):
        """Move the player through the specified tunnel"""
        if (
            self.game_over
            or tunnel_index < 0
            or tunnel_index >= len(self.tunnels[self.player_room])
        ):
            return

        self.player_room = self.tunnels[self.player_room][tunnel_index]
        self.check_hazards()
        self.get_warnings()

    def check_hazards(self):
        """Check if the player encountered any hazards"""
        room_content = self.room_contents[self.player_room]

        if room_content == "wumpus":
            self.game_over = True
            self.win = False
            self.message = "Game Over! The Wumpus got you!"

        elif room_content == "pit":
            self.game_over = True
            self.win = False
            self.message = "Game Over! You fell into a bottomless pit!"

        elif room_content == "bat":
            self.message = "Giant bats carried you to another room!"
            exclude_rooms = [self.player_room]
            exclude_rooms += [
                i for i, content in enumerate(self.room_contents)
                if content in ["wumpus", "pit"]
            ]
            possible_rooms = [r for r in self.rooms if r not in exclude_rooms]
            if possible_rooms:
                self.player_room = random.choice(possible_rooms)
            else:
                self.player_room = random.choice(
                    [r for r in self.rooms if r != self.player_room]
                )
            self.check_hazards()

    def get_warnings(self):
        """Get warnings about nearby hazards"""
        if self.game_over:
            return

        warnings = []

        for adjacent_room in self.tunnels[self.player_room]:
            room_content = self.room_contents[adjacent_room]
            if room_content == "wumpus":
                warnings.append("You smell something terrible nearby.")
            elif room_content == "pit":
                warnings.append("You feel a draft.")
            elif room_content == "bat":
                warnings.append("You hear rustling.")

        self.message = " ".join(warnings) if warnings else ""

    def shoot_arrow(self, path):
        """Shoot an arrow through a sequence of tunnels"""
        if self.game_over or self.arrows <= 0 or not path:
            return

        self.arrows -= 1
        current_room = self.player_room

        for i, tunnel_index in enumerate(path[:5]):
            if (
                tunnel_index < 0
                or tunnel_index >= len(self.tunnels[current_room])
            ):
                self.message = "Your arrow flies off into the darkness."
                break

            current_room = self.tunnels[current_room][tunnel_index]

            if current_room == self.wumpus_room:
                self.game_over = True
                self.win = True
                self.message = "You killed the Wumpus! You win!"
                return

            elif i > 0 and random.random() < 0.1:
                if self.wumpus_room in self.tunnels[current_room]:
                    self.game_over = True
                    self.win = True
                    self.message = (
                        "Your arrow ricocheted and hit the Wumpus! Lucky shot!"
                    )
                    return

        self.message = "Your arrow missed."

        if random.random() < 0.5:
            self.wake_wumpus()

        if self.arrows <= 0 and not self.win:
            self.game_over = True
            self.message = "Game Over! You're out of arrows!"

    def wake_wumpus(self):
        """Chance for wumpus to move to an adjacent room"""
        self.room_contents[self.wumpus_room] = "empty"
        possible_moves = self.tunnels[self.wumpus_room]

        if self.player_room in possible_moves and random.random() < 0.2:
            self.wumpus_room = self.player_room
        else:
            possible_moves = [
                r for r in possible_moves if r != self.player_room
            ]
            self.wumpus_room = random.choice(possible_moves)

        self.room_contents[self.wumpus_room] = "wumpus"

        if self.wumpus_room == self.player_room:
            self.game_over = True
            self.win = False
            self.message = (
                "The wumpus was disturbed by your arrow and found you! "
                "Game Over!"
            )
