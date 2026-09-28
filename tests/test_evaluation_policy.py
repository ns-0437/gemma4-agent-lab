import unittest
from scripts.evaluation_policy import screening_order

class ScreeningTests(unittest.TestCase):
    def test_interleaving_and_input_order(self):
        rows=[dict(id=f'{r}{i}',repo=r,size='small') for r in ['alpha','zulu'] for i in range(8)]
        result=screening_order(rows,4)
        self.assertEqual([r['repo'] for r in result], ['alpha','zulu','alpha','zulu'])
        self.assertEqual(result,screening_order(list(reversed(rows)),4))
    def test_empty_zero_and_duplicate(self):
        self.assertEqual(screening_order([],4),[])
        row=dict(id='one',repo='r',size='small')
        self.assertEqual(screening_order([row],0),[])
        with self.assertRaises(ValueError): screening_order([row,row],4)
        with self.assertRaises(ValueError): screening_order([], -1)
