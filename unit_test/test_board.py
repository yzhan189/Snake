from unittest import TestCase

from model.board import Board


class TestBoard(TestCase):
    def test_new_food(self):
        my_board = Board(20, 60)
        self.assertEquals(my_board.new_food([[10, 10]]), True)
