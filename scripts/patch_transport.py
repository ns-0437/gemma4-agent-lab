"""Normalize patch transport bytes without changing the original evidence."""
import hashlib


def prepare_patch(text):
    if not isinstance(text, str):
        raise TypeError('patch must be text')
    raw = text.encode('utf-8')
    applied = raw + b'\n' if raw and not raw.endswith(b'\n') else raw
    digest = lambda data: hashlib.sha256(data).hexdigest()
    return applied, dict(original_bytes=len(raw), original_sha256=digest(raw),
                        applied_bytes=len(applied), applied_sha256=digest(applied),
                        added_final_newline=applied != raw)
