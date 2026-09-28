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


from scripts.evaluation_policy import classify_controls
class ClassificationTests(unittest.TestCase):
    def pair(self):
        base=dict(import_in_checkout=True,patch_rc=0,test_patch_rc=0,pytest_exit=1,
                  nodes={f't{i}':'failed' for i in range(37)})
        ref={**base,'pytest_exit':0,'nodes':{n:'passed' for n in base['nodes']}}
        return base,ref
    def test_all_targets_and_review_gate(self):
        result=classify_controls(*self.pair())
        self.assertTrue(result['mechanically_eligible'])
        self.assertEqual(len(result['target_nodes']),37)
        self.assertEqual(result['failure_relevance'],'review_required')
    def test_errors_exit_and_missing_patch(self):
        for field,value in [('pytest_exit',2),('patch_rc',None),('exception','setup failed')]:
            base,ref=self.pair();base[field]=value
            self.assertFalse(classify_controls(base,ref)['mechanically_eligible'])
        base,ref=self.pair();base['nodes']['fixture']='errored'
        self.assertFalse(classify_controls(base,ref)['mechanically_eligible'])
        base,ref=self.pair();ref['pytest_exit']=1
        self.assertFalse(classify_controls(base,ref)['mechanically_eligible'])


from scripts.evaluation_policy import allocate
class AllocationTests(unittest.TestCase):
    def test_quotas_and_studied_exclusion(self):
        rows=[dict(id=f'{r}{i}',repo=r,size='small') for r in ['a','b'] for i in range(8)]
        result=allocate(rows,{'a':3,'b':1},2,2,studied={'a0','b0'})
        self.assertEqual(len(result['dev']),2);self.assertEqual(len(result['holdout']),2)
        self.assertFalse(set(result['holdout']) & {'a0','b0'})
        self.assertFalse(set(result['dev']) & set(result['holdout']))
        self.assertEqual(result['quota_shortfall'],{'a':0,'b':0})
        self.assertEqual(result['unused_valid'],12)
    def test_shortage_is_not_padded(self):
        rows=[dict(id='a',repo='r',size='small')]
        result=allocate(rows,{'r':2},1,1,studied={'a'})
        self.assertEqual(result['holdout'],[])
        self.assertEqual(result['capacity_shortfall'],{'dev':0,'holdout':1})
