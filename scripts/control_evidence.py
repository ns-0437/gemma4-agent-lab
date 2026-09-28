"""Portable JUnit and evidence helpers; no competition data or sandbox dependencies."""
import xml.etree.ElementTree as ET

def parse_junit(text):
    """Fail closed on malformed XML or ambiguous identities; preserve failure detail."""
    root=ET.fromstring(text)
    nodes={}
    for case in root.iter('testcase'):
        identity=(case.get('classname','')+'::'+case.get('name','')).strip(':')
        if not identity or identity in nodes:
            raise ValueError('missing or duplicate JUnit test identity')
        kinds={child.tag for child in case}
        outcome=next((value for tag,value in [('error','errored'),('failure','failed'),('skipped','skipped')]
                      if tag in kinds),'passed')
        detail=[{'kind':child.tag,'message':child.get('message',''),'text':''.join(child.itertext())}
                for child in case if child.tag in {'error','failure','skipped'}]
        nodes[identity]={'outcome':outcome,'details':detail}
    return nodes
