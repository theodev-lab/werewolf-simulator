import unittest
from types import SimpleNamespace

from game.suspicion import SuspicionManager


class SuspicionManagerTest(unittest.TestCase):
    def test_locked_innocence_is_immune_to_debate_and_grudge(self):
        suspicion = SuspicionManager(2)
        suspicion.lock_cell(0, 1, 0)

        suspicion.apply_influence(0, 1, 0.75)
        suspicion.apply_grudge(
            [SimpleNamespace(id=0, memory={1: [1]}, paranoia=1)],
            current_day=2,
        )

        self.assertEqual(suspicion.suspicion[0][1], 0)
        self.assertEqual(suspicion.grudge[0][1], 0)
        self.assertEqual(suspicion.get_accusation_scores(0)[1], 0)

    def test_locked_guilt_is_immune_to_negative_debate(self):
        suspicion = SuspicionManager(2)
        suspicion.lock_cell(0, 1, 1)

        suspicion.apply_influence(0, 1, -0.75)

        self.assertEqual(suspicion.suspicion[0][1], 1)
        self.assertEqual(suspicion.get_accusation_scores(0)[1], 1)

    def test_only_binary_values_can_be_locked(self):
        suspicion = SuspicionManager(2)

        with self.assertRaises(ValueError):
            suspicion.lock_cell(0, 1, 0.5)


if __name__ == "__main__":
    unittest.main()
