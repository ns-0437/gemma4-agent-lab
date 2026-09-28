'use strict';
const list = document.querySelector('#release-list');
const detail = document.querySelector('#detail');
const status = document.querySelector('#load-status');
const theme = document.querySelector('#theme');
let releases = [], manifest = new Map(), selected = 'v2', filter = 'all', checkpoint = 'unavailable';
theme.addEventListener('click', () => {
  const dark = document.body.classList.toggle('dark');
  theme.setAttribute('aria-pressed', String(dark));
});
function el(tag, text, className) {
  const node = document.createElement(tag);
  if (text !== undefined) node.textContent = text;
  if (className) node.className = className;
  return node;
}
function render() {
  const visible = releases.filter(r => filter === 'all' || r.status === filter);
  if (!visible.some(r => r.id === selected)) selected = visible[0]?.id;
  list.replaceChildren();
  for (const release of visible) {
    const button = el('button', undefined, 'release');
    button.type = 'button'; button.setAttribute('aria-pressed', String(release.id === selected));
    button.setAttribute('aria-label', `Inspect ${release.id}, ${release.status}`);
    const label = el('span'); label.append(el('strong', release.id), el('small', release.label));
    button.append(label, el('span', release.public_score === null ? 'UNMEASURED' : release.public_score.toFixed(2), release.public_score === null ? 'pending' : 'score'));
    button.addEventListener('click', () => { selected = release.id; render(); });
    list.append(button);
  }
  status.textContent = `${visible.length} releases Â· selected: ${selected || 'none'} Â· checkpoint ${checkpoint}`;
  const r = visible.find(x => x.id === selected);
  detail.replaceChildren();
  if (!r) { detail.append(el('p','No releases match this filter.')); return; }
  const record = manifest.get(r.id);
  detail.append(el('span', EvidenceView.badge(r), `badge${r.status === 'submitted' ? '' : ' pending'}`), el('h3',r.id), el('p',r.label), el('h4','HYPOTHESIS'), el('p',r.hypothesis), el('h4','OBSERVED RESULT'), el('p',r.outcome));
  if (record) {
    detail.append(el('h4','REPRODUCIBLE ARCHIVE SHA-256'), el('code',record.sha256,'hash'));
    const copy = el('button','Copy hash','copy'); copy.type='button';
    copy.addEventListener('click',async () => {
      try { await navigator.clipboard.writeText(record.sha256); copy.textContent='Copied'; }
      catch { copy.textContent='Select the hash above to copy'; }
    }); detail.append(copy);
    if (record.submitted_archive_sha256) {
      detail.append(el('h4','HISTORICAL UPLOAD SHA-256'),el('code',record.submitted_archive_sha256,'hash'),el('p',record.note,'disclaimer'));
    }
  }
  detail.append(el('p', r.public_score != null ? 'Public score evidence: owner-provided Kaggle screenshot. No hidden per-task results are available.' : 'No public score is recorded. Pilot and replay observations are described above; neither is a leaderboard score.', 'disclaimer'));
}
document.querySelector('#filters').addEventListener('change',event => { filter=event.target.value; render(); });
Promise.all([fetch('../results.json'),fetch('../../releases/manifest.json')])
  .then(async responses => {
    if (responses.some(r => !r.ok)) throw new Error('Manifest could not be loaded');
    return Promise.all(responses.map(r => r.json()));
  }).then(([results,artifacts]) => {
    checkpoint=EvidenceView.checkpoint(results);
    document.querySelector('#pilot-summary').textContent=EvidenceView.pilot(results);
    document.querySelector('#submission-summary').textContent=EvidenceView.submission(results);
    document.querySelector('#checkpoint').textContent=checkpoint;
    releases=results.releases; manifest=new Map(artifacts.releases.map(r => [r.id,r])); render();
  }).catch(() => { status.textContent='Could not load evidence. Serve the repository over HTTP or read docs/results.json in GitHub.'; });
