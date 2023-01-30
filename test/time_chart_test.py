import unittest
import json
from src import time_chart


class TestTimeChart(unittest.TestCase):
    def test_time_chart(self):
        # Dummy response data
        response = type('', (object,), {'data': [
            type('', (object,), {'created_at': '2022-01-01 10:00:00'}),
            type('', (object,), {'created_at': '2022-01-01 11:00:00'}),
            type('', (object,), {'created_at': '2022-01-01 12:00:00'})
        ]})
        self.maxDiff = None
        # Call the function
        result = time_chart.time_chart(response)

        # Check the result
        expected = json.dumps([
            {'hour': 0, 'tweet': 0},
            {'hour': 1, 'tweet': 0},
            {'hour': 2, 'tweet': 0},
            {'hour': 3, 'tweet': 0},
            {'hour': 4, 'tweet': 0},
            {'hour': 5, 'tweet': 0},
            {'hour': 6, 'tweet': 0},
            {'hour': 7, 'tweet': 0},
            {'hour': 8, 'tweet': 0},
            {'hour': 9, 'tweet': 0},
            {'hour': 10, 'tweet': 1},
            {'hour': 11, 'tweet': 1},
            {'hour': 12, 'tweet': 1},
            {'hour': 13, 'tweet': 0},
            {'hour': 14, 'tweet': 0},
            {'hour': 15, 'tweet': 0},
            {'hour': 16, 'tweet': 0},
            {'hour': 17, 'tweet': 0},
            {'hour': 18, 'tweet': 0},
            {'hour': 19, 'tweet': 0},
            {'hour': 20, 'tweet': 0},
            {'hour': 21, 'tweet': 0},
            {'hour': 22, 'tweet': 0},
            {'hour': 23, 'tweet': 0}
        ])  # si, devi scrivere tutto
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
