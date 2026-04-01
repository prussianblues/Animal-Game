# Author: Andy Kim
# GitHub username: prussianblues
# Date: 3/13/2026 (tweaked names, some piece placements)
# Description: Unit tests for portfolio project (Animal Game). Tests that pieces move
# only valid distances, directions. Tests that sliding pieces are blocked by interrupting
# pieces and jumping pieces are not. Tests that captures are handled correctly, that turn order
# is handled correctly. Tests that get_game_state() correctly reports game state.
import unittest
from AnimalGame import AnimalGame, Piece, Pika, Trilobite, Wombat, Beluga

class TestAnimalGame (unittest.TestCase):
    """
    Contains unit tests for AnimalGame project
    """
    # Test that pieces move valid distances (sliding pieces can move less than their full range, jumping pieces cannot)
    # testing pika pieces
    def test_pika_distance(self):
        game = AnimalGame()

        # test moving invalid distances for tangerine pika
        self.assertFalse(game.make_move('a1', 'a6')) # too far
        self.assertFalse(game.make_move('a1', 'a1')) #didn't move at all
        # test moving a valid distance
        self.assertTrue(game.make_move('a1', 'a5')) # max mvmt for tangerine pika

        # test moving invalid distances for amethyst pika
        self.assertFalse(game.make_move('a7', 'a2')) # too big of a distance
        self.assertFalse(game.make_move('a7', 'a7'))

        #test moving other valid distances
        self.assertTrue(game.make_move('a7', 'a6')) # shorter movmt for amethyst pika
        self.assertTrue(game.make_move('a5', 'b5')) # shorter mvmt for tangerine pika
        self.assertTrue(game.make_move('a6','e6')) # max movmt for amethyst pika

    def test_trilobite_distance(self):
        """testing trilobite distances"""
        game = AnimalGame()
        # test moving invalid distances for tangerine trilobite
        self.assertFalse(game.make_move('b1', 'e4'))  # too far
        self.assertFalse(game.make_move('b1', 'b1'))  # didn't move at all
        # test moving a valid distance
        self.assertTrue(game.make_move('b1', 'd3'))  # max mvmt for tangerine trilobite

        # test moving invalid distances for amethyst trilobite
        self.assertFalse(game.make_move('b7', 'e4'))  # too big of a distance
        self.assertFalse(game.make_move('b7', 'b7'))

        # test moving other valid distances
        self.assertTrue(game.make_move('b7', 'c6'))  # shorter movmt for amethyst trilobite
        self.assertTrue(game.make_move('d3', 'e4'))  # shorter mvmt for tangerine trilobite
        self.assertTrue(game.make_move('c6', 'a4'))  # max movmt for amethyst trilobite

    def test_wombat_distance(self):
        """testing wombat distances"""
        game = AnimalGame()
        # test moving invalid distances for tangerine wombat
        self.assertFalse(game.make_move('c1', 'c3'))  # too far
        self.assertFalse(game.make_move('c1', 'c1'))  # didn't move at all
        # test moving a valid distance
        self.assertTrue(game.make_move('c1', 'c2'))  # valid mvmt for tangerine wombat

        # test moving invalid distances for amethyst wombat
        self.assertFalse(game.make_move('c7', 'c5'))  # too big of a distance
        self.assertFalse(game.make_move('c7', 'c7'))

        # test moving other valid distances
        self.assertTrue(game.make_move('c7', 'c6'))  # valid movmt for amethyst wombat


    def test_beluga_distance(self):
        """testing beluga distances"""
        #testing beluga pieces
        game = AnimalGame()
        # test moving invalid distances for tangerine wombat
        self.assertFalse(game.make_move('d1', 'e2'))  # short
        self.assertFalse(game.make_move('d1', 'd1'))  # didn't move

        # test moving a valid distance
        self.assertTrue(game.make_move('d1', 'g4'))  # valid mvmt for tangerine beluga

        # test moving invalid distances for amethyst wombat
        self.assertFalse(game.make_move('d7', 'e6'))  # short
        self.assertFalse(game.make_move('d7', 'd7')) #didn't move

        # test moving other valid distances
        self.assertTrue(game.make_move('d7', 'a4'))  # valid movmt for amethyst beluga

    # Test that pieces only move valid directions (diagonal pieces can also move one square orthogonally, and orthogonal pieces can also move one square diagonally)
    def test_pika_direction(self):
        """testing pika direction"""
        game = AnimalGame()
        #invalid directions
        self.assertFalse(game.make_move('a1', 'c3')) # not allowed, too far diagonal
        self.assertTrue(game.make_move('a1','a3')) #down
        game.make_move('e7', 'e6') #filler amethyst move
        self.assertTrue(game.make_move('a3', 'b3')) # side/right
        game.make_move('e6', 'e5') #filler amethyst move
        self.assertTrue(game.make_move('b3', 'b2')) #up
        game.make_move('e5', 'e4')  # filler amethyst move
        self.assertTrue(game.make_move('b2', 'c3'))  # diagonal test
        game.make_move('e4', 'e3')  # filler amethyst move
        self.assertTrue(game.make_move('c3', 'b3'))  # left
        game.make_move('e3', 'd3')  # filler amethyst move

    def test_trilobite_direction(self):
        """testing trilobite direction"""
        game = AnimalGame()
        #invalid direction
        self.assertFalse(game.make_move('b1','b3')) # too far orthogonal
        self.assertTrue(game.make_move('b1','d3')) # valid low right diagonal
        game.make_move('b7','d5') #filler

        self.assertTrue(game.make_move('d3','c4')) # valid low left diagonal
        game.make_move('c7','c6') #filler

        self.assertTrue(game.make_move('c4','c5')) # valid orthogonal
        game.make_move('c6', 'b6')  # filler

        self.assertTrue(game.make_move('c5','d4')) #valid top right diagonal
        game.make_move('b6', 'a6')  # filler

        self.assertTrue(game.make_move('d4','c3')) #valid top left diagonal

    def test_wombat_direction(self):
        """testing wombat direction"""
        game = AnimalGame()
        #invalid direction
        self.assertFalse(game.make_move('c1','c3')) # too far orthogonal

        #valid
        self.assertTrue(game.make_move('c1','c2')) #moving 1 down
        game.make_move('c7','c6') #filler amethyst

        #valid orthogonal jumps
        self.assertTrue(game.make_move('c2','d2')) # move 1 right
        game.make_move('c6', 'c5') #filler amethyst

        self.assertTrue(game.make_move('d2', 'c2'))  # move 1 left
        game.make_move('e7', 'e6')  # filler amethyst

        self.assertTrue(game.make_move('c2', 'c1'))  # move 1 top
        game.make_move('e6', 'f6')  # filler amethyst

        self.assertTrue(game.make_move('c1','d2'))   #valid diagonal
        game.make_move('c5','c4') #filler

        # invalid test again
        self.assertFalse(game.make_move('d2','f4'))  #too far diagonal

    def test_beluga_direction(self):
        """testing beluga direction"""
        game = AnimalGame()

        # invalid orthogonal
        self.assertFalse(game.make_move('d1','d3')) #too far and orthogonal

        #valid diagonal jump
        self.assertTrue(game.make_move('d1','g4')) #bottom right jump
        game.make_move('d7','a4')

        #valid 1 square orthogonal movement
        self.assertTrue(game.make_move('g4','g5'))
        game.make_move('a4', 'b4')

        #invalid diagonal
        self.assertFalse(game.make_move('g5','f6'))

        # more valid diagonal jump directions
        self.assertTrue(game.make_move('g5','d2'))# top left jump
        game.make_move('e7', 'e6')

        self.assertTrue(game.make_move('d2', 'a5'))  # bottom left jump
        game.make_move('e6', 'f6')

        self.assertTrue(game.make_move('a5', 'd2'))  # top right jump

    # Test that sliding pieces are blocked by intervening pieces, jumping pieces are not
    def test_blocking(self):
        game = AnimalGame()
        # test sliding pieces
        game.make_move('a1','a3')
        game.make_move('a7','a5') #amethyst pika interrupting path

        self.assertFalse(game.make_move('a3','a6'))
        self.assertTrue(game.make_move('a3','a4'))

        game.make_move('e7','e6')
        game.make_move('a4','b5')
        game.make_move('d7','a4')
        # test jumping pieces
        self.assertTrue(game.make_move('d1','g4'))

    # Test that captures are handled correctly, including that players cannot capture their own pieces
    def test_captures(self):
        game = AnimalGame()
        # test tangerine captures
        #invalid
        self.assertFalse(game.make_move('a1','c1')) # tangerine trying to capture own wombat

        game.make_move('a1','a5')
        game.make_move('e7', 'e6') #amethyst turn
        game.make_move('a5','a7') #tangerine captures enemy pika
        self.assertIn("Pika",game.get_tangerine_captures())

        # test amethyst
        self.assertFalse(game.make_move('g7', 'd7')) # amethyst trying to capture own beluga
        game.make_move('g7', 'g3') # amethyst move
        game.make_move('e1', 'e2') # filler tangerine move
        game.make_move('g3', 'g1')
        self.assertIn("Pika", game.get_amethyst_captures())

    # Test that turn order is handled correctly
    def test_turn(self):
        game = AnimalGame()
        self.assertEqual(game.get_turn(), "Tangerine")
        game.make_move('d1', 'g4')
        self.assertEqual(game.get_turn(), "Amethyst")
        game.make_move('a7', 'a5')
        self.assertEqual(game.get_turn(), "Tangerine")
        game.make_move('g4', 'd7')
        self.assertEqual(game.get_turn(), "Amethyst")

    # Test that game_state() method correctly reports the game state
    def test_unfinished_state(self):
        game = AnimalGame()
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        game.make_move('d1', 'g4')
        game.make_move('a7', 'a5')
        self.assertEqual(game.get_game_state(), "UNFINISHED")

    def test_tangerine_win(self):
        game = AnimalGame()
        game.make_move('d1', 'g4')
        game.make_move('a7', 'a5')
        game.make_move('g4', 'd7')
        self.assertEqual(game.get_game_state(), "TANGERINE_WON")

    def test_amethyst_win(self):
        game = AnimalGame()
        game.make_move('a1', 'a3')
        game.make_move('d7', 'g4')
        game.make_move('a3', 'a5')
        game.make_move('g4', 'd1')
        self.assertEqual(game.get_game_state(), "AMETHYST_WON")


