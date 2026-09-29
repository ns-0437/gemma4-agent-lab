"""Portable JUnit and evidence helpers; no competition data or sandbox dependencies."""
import xml.etree.ElementTree as ET

def parse_junit(text):
    """Fail closed on malformed XML or ambiguous identities; preserve failure detail."""
    root=ET.fromstring(text)
    # Some JUnit producers attach a namespace to every element.
    # Normalize tags before looking for tests, failures or setup errors.
    for element in root.iter():
        element.tag = element.tag.rsplit('}', 1)[-1]
    nodes={}
    for case in root.iter('testcase'):
        if not (case.get('name') or '').strip():
            raise ValueError('missing JUnit test name')
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


from pathlib import Path
import hashlib
import json

def write_arm(directory, metadata, *, stdout='', stderr='', traceback_text='', junit=None):
    """Write a new evidence directory. Call from finally, before sandbox cleanup.

    Existing directories are rejected to prevent accidental overwrites and stale XML.
    arm.json is written last and identifies the exact bytes persisted.
    """
    if type(metadata.get('reached_pytest')) is not bool:
        raise ValueError('reached_pytest must be explicit')
    if not metadata['reached_pytest'] and junit is not None:
        raise ValueError('cannot attach JUnit to an unexecuted pytest run')
    directory=Path(directory)
    directory.mkdir(parents=True,exist_ok=False)
    payload={'stdout.txt':stdout,'stderr.txt':stderr,'traceback.txt':traceback_text}
    if junit is not None: payload['junit.xml']=junit
    elif metadata['reached_pytest']: payload['MISSING_JUNIT.txt']='Pytest started but no JUnit was retrieved.\n'
    else: payload['NO_PYTEST_RUN.txt']='Pytest was not reached.\n'
    hashes={}
    for name, text in payload.items():
        raw=text.encode('utf-8');(directory/name).write_bytes(raw)
        hashes[name]=hashlib.sha256(raw).hexdigest()
    record={**metadata,'artifact_sha256':hashes}
    (directory/'arm.json').write_text(json.dumps(record,indent=2,ensure_ascii=False),encoding='utf-8')
    return record
