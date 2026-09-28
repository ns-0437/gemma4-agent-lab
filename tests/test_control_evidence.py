import unittest
import xml.etree.ElementTree as ET
from scripts.control_evidence import parse_junit

class JUnitTests(unittest.TestCase):
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
