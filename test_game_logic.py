import unittest
from game_state import GameState


class TestGameState(unittest.TestCase):

    def setUp(self):
        """Set up the test environment."""
        self.game_state = GameState()
        self.game_state.reset()  # Initialize game state

    def test_player_movement(self):
        """Test the player's ability to move between rooms."""
        initial_room = self.game_state.player_room
        # Move to a connected room (assume room 1 is a valid move)
        self.game_state.move_player(1)  # Move to room 1
        self.assertNotEqual(self.game_state.player_room, initial_room)

    def test_arrow_shooting(self):
        """Test the arrow shooting functionality."""
        self.game_state.player_room = 0  # Start in room 0
        self.game_state.arrows = 3  # Ensure the player has arrows to shoot
        # Define an arrow path
        arrow_path = [1, 2]
        self.game_state.shoot_arrow(arrow_path)
        # Arrows should decrease after shooting
        self.assertEqual(self.game_state.arrows, 2)

    def test_game_over(self):
        """Test if the game properly detects a game over condition."""
        # Set the player in a pit room (assuming room 0 has a pit for testing)
        self.game_state.room_contents[0] = "pit"
        self.game_state.player_room = 0
        self.game_state.check_hazards()  # Check for hazards
        self.assertTrue(self.game_state.game_over)


if __name__ == "__main__":
    unittest.main()
