'use strict';
// Shared pure presentation logic; consumed by the browser and Node regression tests.
const EvidenceView = {
  badge(release) {
    if (release.public_score != null) return 'SUBMITTED / SCORED';
    return release.status === 'submitted' ? 'SUBMITTED / SCORE UNAVAILABLE' : 'CANDIDATE / UNSCORED';
  },
  checkpoint(results) { return results.as_of || 'unavailable'; },
  pilot(results) {
    const v = results.validation || {};
    return `${v.real_pilot_runs ?? '—'} executed / ${v.real_pilot_runs_planned ?? '—'} planned / ${v.real_pilot_runs_graded ?? '—'} graded`;
  },
  submission(results) {
    const items = results.submission_updates || [];
    if (!items.length) return 'No newer submission recorded.';
    const r = items[items.length - 1];
    return `${r.id}: ${r.status_at_report} as reported ${r.reported_on}. This is a recorded checkpoint, not live status.`;
  }
};
if (typeof module !== 'undefined') module.exports = EvidenceView;
