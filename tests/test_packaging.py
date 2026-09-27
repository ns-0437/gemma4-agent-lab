import hashlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT/'scripts'))
from verify_releases import archive_bytes


class PackagingTests(unittest.TestCase):
    def test_frozen_release_hashes(self):
        records = json.loads((ROOT/'releases/manifest.json').read_text())['releases']
        for r in records:
            with self.subTest(release=r['id']):
                self.assertEqual(hashlib.sha256(archive_bytes(ROOT/r['directory'])).hexdigest(), r['sha256'])

    def test_archive_metadata_and_order(self):
        payload = archive_bytes(ROOT/'releases/pilot_A')
        with zipfile.ZipFile(io.BytesIO(payload)) as z:
            self.assertEqual(z.namelist(), sorted(z.namelist()))
            self.assertTrue(all(i.date_time == (1980,1,1,0,0,0) for i in z.infolist()))
            self.assertTrue(all(i.create_system == 0 for i in z.infolist()))
            self.assertIsNone(z.testzip())

    def test_candidate_delta_is_only_thinking(self):
        a,b = ROOT/'releases/pilot_A',ROOT/'releases/pilot_B'
        aa={p.relative_to(a).as_posix():p.read_bytes() for p in a.rglob('*') if p.is_file()}
        bb={p.relative_to(b).as_posix():p.read_bytes() for p in b.rglob('*') if p.is_file()}
        self.assertEqual(aa.keys(),bb.keys())
        for name,data in aa.items():
            self.assertEqual(data.replace(b'include_thoughts: false',b'include_thoughts: true')
                             if name=='configs/sampling.yaml' else data, bb[name])

    def test_missing_root_and_binary_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)
            with self.assertRaises(ValueError): archive_bytes(p)
            (p/'agent.yaml').write_text('name: fixture')
            (p/'weight.bin').write_bytes(b'invented fixture')
            with self.assertRaises(ValueError): archive_bytes(p)

    def test_validator_rejects_include_escape(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);sub=p/'sub';sub.mkdir()
            (p/'outside.md').write_text('outside')
            (sub/'agent.yaml').write_text('name: fixture\nmodel: gemma-4-31b-it-qat-w4a16-ct\ninstruction: !include ../outside.md\n')
            result=subprocess.run([sys.executable,str(ROOT/'scripts/validate_and_zip.py'),str(sub),'--no-zip'],capture_output=True,text=True)
            self.assertNotEqual(result.returncode,0)
            self.assertIn('escapes submission root',result.stdout)

    def test_submit_notebook_preserves_exact_zip(self):
        spec=importlib.util.spec_from_file_location('submit_builder',ROOT/'scripts/make_submit_notebook.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        old=sys.argv
        with tempfile.TemporaryDirectory() as tmp:
            module.OUT=Path(tmp)/'notebook'
            sys.argv=['builder','--version','fixture','--source',str(ROOT/'releases/v2')]
            try: module.main()
            finally: sys.argv=old
            nb=json.loads((module.OUT/'submit.ipynb').read_text())
            code=''.join(nb['cells'][1]['source'])
            output=Path(tmp)/'submission.zip'
            code=code.replace('/kaggle/working/submission.zip',output.as_posix())
            exec(compile(code,'<generated packaging cell>','exec'),{})
            self.assertEqual(output.read_bytes(),archive_bytes(ROOT/'releases/v2'))


if __name__=='__main__': unittest.main()
