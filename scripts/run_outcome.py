"""Classify termination evidence without turning unknown failures into infrastructure facts."""


def classify_run(*, errors=(), environment_error=False, provenance_ok=None,
                 cleanup_ok=None):
    """Candidate termination may continue; unknown or unsafe run state stops dispatch.

    Callers must supply independent environment/provenance/cleanup observations.
    A known candidate message never masks those observations or another unknown error.
    This portable helper does not modify the private Kaggle harness.
    """
    if environment_error or provenance_ok is False or cleanup_ok is False:
        return {"kind": "environment", "stop": True, "reason": "environment, provenance or cleanup failure"}
    if provenance_ok is not True or cleanup_ok is not True:
        return {"kind": "unobserved", "stop": True, "reason": "provenance or cleanup unconfirmed"}
    reasons = []
    for error in errors:
        if not error:
            continue
        message = str(error).lower()
        if "agent completed execution without calling submit_patch" in message:
            reasons.append("missing_submission")
        elif "exceeded turns budget" in message or "turn budget exhausted" in message:
            reasons.append("turn_budget")
        elif "contextwindowexceedederror" in message or "maximum context length" in message:
            reasons.append("context_limit")
        else:
            return {"kind": "unknown", "stop": True, "reason": str(error)}
    return {"kind": "candidate" if reasons else "completed", "stop": False,
            "reason": ", ".join(sorted(set(reasons)))}
