import unittest
import xml.etree.ElementTree as ET
from scripts.control_evidence import parse_junit

class JUnitTests(unittest.TestCase):
    def test_namespaced_reports_preserve_setup_errors(self):
        text='<testsuites xmlns="urn:example:junit"><testsuite><testcase classname="demo" name="target"><error message="fixture">setup failed</error></testcase></testsuite></testsuites>'
        nodes=parse_junit(text)
        self.assertEqual(nodes['demo::target']['outcome'],'errored')
        self.assertEqual(nodes['demo::target']['details'][0]['text'],'setup failed')

    def test_classname_alone_is_not_a_test_identity(self):
        for xml in ('<testcase classname="demo"/>','<testcase classname="demo" name=" "/>'):
            with self.assertRaises(ValueError): parse_junit(xml)

    def test_outcomes_and_unicode(self):
        text='<testsuites><testsuite><testcase classname="c" name="a[1]"><failure message="bad">rocket 🚀</failure></testcase><testcase classname="c" name="b"><error>fixture</error></testcase><testcase name="skip"><skipped/></testcase><testcase name="ok"/></testsuite></testsuites>'
        nodes=parse_junit(text)
        self.assertEqual(nodes['c::a[1]']['outcome'],'failed')
        self.assertEqual(nodes['c::b']['outcome'],'errored')
        self.assertEqual(nodes['skip']['outcome'],'skipped')
        self.assertEqual(nodes['ok']['outcome'],'passed')
        self.assertEqual(nodes['c::a[1]']['details'][0]['text'],'rocket 🚀')
    def test_ambiguous_and_malformed(self):
        with self.assertRaises(ValueError): parse_junit('<testsuite><testcase name="x"/><testcase name="x"/></testsuite>')
        with self.assertRaises(ValueError): parse_junit('<testsuite><testcase/></testsuite>')
        with self.assertRaises(ET.ParseError): parse_junit('not xml')
        self.assertEqual(parse_junit('<testsuite/>'),{})


from pathlib import Path
import tempfile, json, hashlib
from scripts.control_evidence import write_arm
class PersistenceTests(unittest.TestCase):
    def test_complete_bytes_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'arm'
            record=write_arm(path,{'reached_pytest':True,'pytest_exit':0},stdout='🚀',junit='<testsuite/>')
            self.assertEqual(json.loads((path/'arm.json').read_text(encoding='utf-8')),record)
            for name,digest in record['artifact_sha256'].items():
                self.assertEqual(hashlib.sha256((path/name).read_bytes()).hexdigest(),digest)
            with self.assertRaises(FileExistsError):write_arm(path,{'reached_pytest':False})
    def test_setup_failure_and_missing_xml_differ(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'setup'
            write_arm(path,{'reached_pytest':False,'exception':'setup failed'},traceback_text='trace')
            self.assertTrue((path/'NO_PYTEST_RUN.txt').exists())
            self.assertFalse((path/'junit.xml').exists())
            second=Path(tmp)/'interrupted'
            write_arm(second,{'reached_pytest':True,'pytest_exit':-1})
            self.assertTrue((second/'MISSING_JUNIT.txt').exists())
            with self.assertRaises(ValueError):write_arm(Path(tmp)/'bad',{'reached_pytest':False},junit='fake')
