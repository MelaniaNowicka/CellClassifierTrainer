import unittest
import filter
import example_data


class TestTraining(unittest.TestCase):

    # test filter_best_solutions
    def test_best(self):
        results, correct_output = example_data.create_example_best_solutions_instance()
        for i in range(len(filter.filter_best_solutions([3, 0], results))):
            self.assertListEqual(filter.filter_best_solutions([3, 0], results)[i].solutions_by_gate, correct_output[i])

    # test find_shortest_solutions
    def test_shortest(self):

        solution_list, correct_output = example_data.create_example_size_instance()
        self.assertListEqual(filter.filter_shortest_solutions(solution_list), correct_output)

    # test remove_symmetric_solutions
    def test_symmetry(self):

        solution_list, correct_output = example_data.create_example_symmetry_instance()
        self.assertListEqual(filter.filter_symmetric_solutions(solution_list), correct_output)


if __name__ == '__main__':
    unittest.main()
