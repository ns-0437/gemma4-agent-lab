import ast
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'scripts'))
from check_public_repo import violations,missing_markdown_links,tracked_files


class RepositoryTests(unittest.TestCase):
    def test_restricted_payloads_and_large_files_rejected(self):
        for path in ['reference/tasks.jsonl','weights.safetensors','notebooks/pilot.ipynb','.env','.kaggle/access_token']:
            with self.subTest(path=path): self.assertTrue(violations(path,b'fixture'))
        self.assertTrue(violations('docs/big.txt',b'x'*1_000_001))
        self.assertEqual(violations('docs/note.md',b'Ordinary documentation'),[])

    def test_detects_token_shapes_without_live_secret(self):
        fake=('gh'+'p_'+'x'*30).encode()
        self.assertIn('credential-shaped content',violations('docs/example.txt',fake))

    def test_tracked_tree_contains_only_allowed_files(self):
        for p in tracked_files():
            with self.subTest(path=p): self.assertEqual(violations(p,(ROOT/p).read_bytes()),[])

    def test_markdown_links_resolve(self):
        for p in tracked_files():
            if p.suffix=='.md':
                with self.subTest(path=p): self.assertEqual(missing_markdown_links(ROOT/p),[])

    def test_result_status_matches_release_manifest(self):
        results=json.loads((ROOT/'docs/results.json').read_text())
        manifest={r['id']:r for r in json.loads((ROOT/'releases/manifest.json').read_text())['releases']}
        for r in results['releases']:
            self.assertEqual(r['status'],manifest[r['id']]['status'])
            self.assertEqual(r['public_score'],manifest[r['id']]['public_score'])
            if r['status']!='submitted': self.assertIsNone(r['public_score'])

    def test_public_fixture_does_not_read_private_inputs(self):
        text=(ROOT/'scripts/public_fixtures.py').read_text()
        self.assertNotIn('reference/tasks.jsonl',text)
        self.assertNotIn('harness_src',text)
        source=(ROOT/'scripts/make_pilot_notebook.py').read_text()
        module=ast.parse(source)
        config=next(ast.literal_eval(n.value) for n in module.body
                    if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='CFG' for t in n.targets))
        dispatch=next(ast.literal_eval(n.value) for n in ast.parse(config).body
                      if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='DISPATCH_CONFIRM' for t in n.targets))
        self.assertIs(dispatch,False)


if __name__=='__main__': unittest.main()
