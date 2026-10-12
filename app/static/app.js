'use strict';
const $ = (id) => document.getElementById(id);
const workRefreshHint = $('work-refresh-note').textContent;
let auth = '',
  facilities = [],
  activeRun = null,
  activeDecision = null,
  polling = null,
  evaluationKey = null,
  decisionKey = null;
function node(tag, text, className) {
  const e = document.createElement(tag);
  if (text !== undefined) e.textContent = String(text);
  if (className) e.className = className;
  return e;
}
function status(message, error = false, state = 'info') {
  $('status').textContent = error ? friendlyError(message) : message;
  $('status').className = error ? 'error' : '';
  $('status').dataset.state = error ? 'error' : state;
  $('status').setAttribute('role', error ? 'alert' : 'status');
  if (error) $('status').scrollIntoView({ block: 'nearest' });
}
function link(label, url) {
  const a = node('a', label);
  try {
    const u = new URL(url, location.origin);
    if (
      u.origin === location.origin ||
      [
        'https://api.weather.gov',
        'https://www.weather.gov',
        'https://air-quality-api.open-meteo.com',
        'https://open-meteo.com',
        'https://www.airnow.gov',
      ].includes(u.origin)
    ) {
      a.href = u.href;
      a.target = '_blank';
      a.rel = 'noopener';
      if (u.origin === location.origin && u.pathname.startsWith('/api/'))
        a.onclick = async (event) => {
          event.preventDefault();
          try {
            const response = await fetch(u.href, { headers: { Authorization: auth } });
            if (!response.ok) throw Error(`Export failed: HTTP ${response.status}`);
            const blob = await response.blob(),
              objectUrl = URL.createObjectURL(blob),
              download = node('a');
            download.href = objectUrl;
            download.download =
              u.pathname.endsWith('/export') && u.pathname.includes('/notifications/')
                ? 'prototype-draft.eml'
                : u.pathname.endsWith('/memo')
                  ? 'closurecall-decision-memo.html'
                  : 'closurecall-record.json';
            download.click();
            setTimeout(() => URL.revokeObjectURL(objectUrl), 1000);
          } catch (error) {
            status(error.message, true);
          }
        };
    }
  } catch {}
  return a;
}
async function api(path, options = {}) {
  const response = await fetch('/api' + path, {
    ...options,
    headers: {
      Authorization: auth,
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
  });
  if (!response.ok) {
    let b;
    try {
      b = await response.json();
    } catch {}
    const detail = b?.detail;
    throw Error(
      typeof detail === 'string'
        ? detail
        : Array.isArray(detail)
          ? detail.map((item) => item.msg || 'Invalid input').join('; ')
          : `HTTP ${response.status}`,
    );
  }
  return response.json();
}
function pretty(value) {
  return String(value ?? 'Not recorded')
    .replaceAll('_', ' ')
    .replace(/\b\w/g, (c) => c.toUpperCase());
}
function friendlyError(message) {
  const text = String(message);
  if (text.includes('Work period must be positive'))
    return 'Check your work hours: the end must be after the start, and the period must be no longer than 24 hours.';
  if (text.includes('Override requires'))
    return 'To choose a different outcome, select how the facility should operate and explain your reason.';
  if (text.includes('Reject requires'))
    return 'Explain why you are rejecting this assessment before saving.';
  if (text.includes('Timing posture requires'))
    return 'Choose the arrival or dismissal time and explain why that time is appropriate.';
  if (text.includes('Confirmed timing must be inside'))
    return 'The arrival or dismissal time must fall between the selected work start and end.';
  return text;
}
function outcome(value) {
  return (
    {
      normal: 'Normal operations',
      closure: 'Facility closure',
      telework: 'Telework',
      delayed_arrival: 'Delayed arrival',
      early_dismissal: 'Early dismissal',
    }[value] || pretty(value)
  );
}
function reviewLabel(value) {
  return (
    {
      ready_for_manager: 'Ready for your review',
      data_incomplete: 'More information needed',
      unsupported_hazard: 'No automatic rule for this hazard',
    }[value] || pretty(value)
  );
}
function workflow(snapshot, decision) {
  const busy = ['collecting', 'evaluating'].includes(activeRun?.status) && !decision,
    step = decision ? 4 : busy || snapshot ? 2 : 1;
  for (let n = 1; n <= 4; n++) {
    const item = $('step-' + n);
    item.dataset.state = n === step ? 'current' : 'idle';
    if (n === step) item.setAttribute('aria-current', 'step');
    else item.removeAttribute('aria-current');
  }
  $('step-3').href = decision
    ? '#brief-card'
    : snapshot && !busy
      ? '#human-panel'
      : '#controls-card';
  $('guide-label').textContent = decision
    ? 'Saved decision · historical replay'
    : snapshot?.test_evidence_label
      ? 'Synthetic test · no provider or model call'
      : busy
        ? 'Checking conditions'
        : 'Next step';
  $('guide-title').textContent = decision
    ? decision.status === 'rejected'
      ? 'Assessment rejected — nothing queued'
      : 'Decision saved. Review the employee drafts.'
    : busy
      ? 'Preparing your recommendation…'
      : snapshot
        ? snapshot.assessment.review_status === 'ready_for_manager'
          ? 'Review the conditions before deciding'
          : 'More review is needed before a decision'
        : 'Choose a facility and work hours';
  $('guide-text').textContent = decision
    ? 'You are viewing the original saved record, not current weather. Review the reason, recipient routes and drafts. For a new decision, return to work hours and choose an upcoming period.'
    : busy
      ? 'Wait for collection and review to finish. No manager decision or notification has been recorded.'
      : snapshot
        ? snapshot.assessment.review_status === 'ready_for_manager'
          ? 'Read the recommendation and its source evidence. Then approve it, choose a different outcome with a reason, or reject the assessment.'
          : 'This assessment cannot be approved as a recommendation. Check missing information and local conditions; record an explicit override with a reason, or reject the assessment.'
        : 'Work start and end describe the shift affected by your decision. The app checks weather and air quality; you retain the final decision.';
  $('guide-action').textContent = decision
    ? 'Review employee drafts →'
    : snapshot && !busy
      ? 'Read recommendation →'
      : busy
        ? 'View collected evidence →'
        : 'Choose work hours →';
  $('guide-action').href = decision
    ? '#outbox-card'
    : snapshot && !busy
      ? '#brief-card'
      : busy
        ? '#evidence-card'
        : '#controls-card';
}
function pill(text, state) {
  const e = node('span', text, 'state-pill');
  e.dataset.state = state;
  return e;
}
function displayTime(value, zone) {
  if (!value) return 'Not recorded';
  const date = new Date(value);
  if (!Number.isFinite(date.getTime())) return String(value);
  try {
    return new Intl.DateTimeFormat('en-US', {
      timeZone: zone,
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: 'numeric',
      minute: '2-digit',
      timeZoneName: 'short',
    }).format(date);
  } catch {
    return String(value);
  }
}
function displayWindow(start, end, zone) {
  const a = new Date(start),
    b = new Date(end);
  if (!Number.isFinite(a.getTime()) || !Number.isFinite(b.getTime())) return `${start} → ${end}`;
  const day = new Intl.DateTimeFormat('en-US', {
      timeZone: zone,
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    }),
    time = new Intl.DateTimeFormat('en-US', {
      timeZone: zone,
      hour: 'numeric',
      minute: '2-digit',
      timeZoneName: 'short',
    });
  return day.format(a) === day.format(b)
    ? `${day.format(a)} · ${time.format(a)} → ${time.format(b)}`
    : `${displayTime(start, zone)} → ${displayTime(end, zone)}`;
}
function retrievalAge(value) {
  if (!value) return 'Retrieval time not recorded';
  const seconds = Math.floor((Date.now() - new Date(value).getTime()) / 1000);
  if (!Number.isFinite(seconds)) return 'Retrieval time not recorded';
  if (seconds < 0) return 'Future timestamp — review source timing';
  if (seconds < 60) return 'Retrieval age at display: less than 1 min';
  if (seconds < 3600) return `Retrieval age at display: ${Math.floor(seconds / 60)} min`;
  return `Retrieval age at display: ${Math.floor(seconds / 3600)} h ${Math.floor((seconds % 3600) / 60)} min`;
}
function timeDatum(parent, label, value, zone) {
  datum(parent, label, displayTime(value, zone));
  if (value) parent.lastChild.lastChild.append(node('small', value + ' · original timestamp'));
}
function busyButton(button, busy, label) {
  if (!button.dataset.restingLabel) button.dataset.restingLabel = button.textContent.trim();
  button.disabled = busy;
  button.setAttribute('aria-busy', String(busy));
  button.textContent = busy ? label : button.dataset.restingLabel;
  if (['evaluate-button', 'decision-button'].includes(button.id))
    $('refresh-work-hours').disabled = busy;
}
function context(snapshot = null, decision = null, historical = false) {
  const f = snapshot?.facility || selected();
  if (!f) return;
  $('context-facility').textContent = f.display_name;
  $('context-location').textContent =
    `${f.latitude.toFixed(4)}, ${f.longitude.toFixed(4)} · ${f.timezone}`;
  const w = snapshot?.work_period;
  $('context-window').textContent = w
    ? displayWindow(w.start, w.end, f.timezone)
    : `${$('start').value.replace('T', ' ')} → ${$('end').value.replace('T', ' ')}`;
  $('context-zone').textContent =
    `${f.timezone}${w?.special_shift || (!snapshot && $('special').checked) ? ' · synthetic special shift' : ''}`;
  $('context-capture').textContent = snapshot
    ? displayTime(snapshot.collected_at_utc, f.timezone)
    : 'Not collected';
  $('context-age').textContent = historical
    ? 'Saved evidence · not current weather'
    : snapshot?.test_evidence_label ||
      (snapshot ? retrievalAge(snapshot.collected_at_utc) : 'Evaluate to collect sources.');
  $('context-decision').textContent = decision
    ? decision.status === 'rejected'
      ? 'Assessment rejected'
      : `${outcome(decision.posture)} · ${pretty(decision.status)}`
    : snapshot
      ? 'Awaiting manager review'
      : 'Not recorded';
  $('context-detail').textContent = decision
    ? `${decision.actor} · ${displayTime(decision.approved_at, f.timezone)}`
    : 'You make the final decision. Nothing is sent.';
  workflow(snapshot, decision);
}
function decisionHint() {
  const action = $('action').value,
    timed =
      action !== 'reject' && ['delayed_arrival', 'early_dismissal'].includes($('posture').value);
  $('timing-field').hidden = $('timing-basis-field').hidden = !timed;
  const label =
    action === 'approve'
      ? 'Approve recommendation & prepare drafts'
      : action === 'override'
        ? 'Save override & prepare drafts'
        : 'Record rejection — no notices';
  $('decision-button').dataset.restingLabel = label;
  if ($('decision-button').getAttribute('aria-busy') !== 'true')
    $('decision-button').textContent = label;
  $('action-help').textContent =
    action === 'approve'
      ? 'Accept the recommendation shown above. A reason is optional for approval; drafts are prepared, never sent.'
      : action === 'override'
        ? 'Choose how the facility should operate and explain why. This records your override; it does not send notifications.'
        : 'Explain why this assessment should not be used. A rejection queues no operating notice.';
  $('reason').setAttribute('aria-required', String(action !== 'approve'));
}
$('action').addEventListener('change', decisionHint);
$('posture').addEventListener('change', decisionHint);
['start', 'end', 'special'].forEach((id) =>
  $(id).addEventListener('change', () => {
    if (!activeRun && !activeDecision) context();
  }),
);
function selected() {
  return facilities.find((f) => f.facility_id === $('facility').value);
}
function datetimeLocal(date, timezone) {
  const parts = new Intl.DateTimeFormat('sv-SE', {
    timeZone: timezone,
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false,
  }).format(date);
  return parts.replace(' ', 'T');
}
function offsetDate(value, zone = selected().timezone) {
  if (!value) throw Error('Choose a date and time');
  const target = new Date(value + 'Z');
  let candidate = target;
  for (let i = 0; i < 3; i++) {
    const local = new Date(datetimeLocal(candidate, zone) + 'Z');
    candidate = new Date(candidate.getTime() + target.getTime() - local.getTime());
  }
  if (datetimeLocal(candidate, zone) !== value)
    throw Error('Invalid local time for this timezone; choose another time');
  return candidate.toISOString();
}
function workDefaults() {
  const facility = selected();
  if (!facility) return;
  $('work-refresh-note').textContent = workRefreshHint;
  const now = new Date();
  $('start').value = datetimeLocal(new Date(now.getTime() + 15 * 60000), facility.timezone);
  $('end').value = datetimeLocal(new Date(now.getTime() + 135 * 60000), facility.timezone);
  $('timezone').textContent =
    `All work and decision times use ${facility.timezone}. Location: ${facility.latitude.toFixed(4)}, ${facility.longitude.toFixed(4)}. Synthetic office; no real employee data.`;
  if (!activeRun && !activeDecision) context();
}
async function loadFacilities(id) {
  facilities = await api('/facilities');
  $('facility').replaceChildren(
    ...facilities.map((f) => {
      const o = node('option', f.display_name);
      o.value = f.facility_id;
      return o;
    }),
  );
  if (id) $('facility').value = id;
  workDefaults();
}
$('facility').addEventListener('change', workDefaults);
$('refresh-work-hours').addEventListener('click', () => {
  const facility = selected();
  if (!facility) return;
  let duration = 2 * 60 * 60000;
  try {
    const previous =
      new Date(offsetDate($('end').value)).getTime() -
      new Date(offsetDate($('start').value)).getTime();
    if (Number.isFinite(previous) && previous > 0 && previous <= 24 * 60 * 60000)
      duration = previous;
  } catch {}
  const start = new Date(Date.now() + 15 * 60000);
  $('start').value = datetimeLocal(start, facility.timezone);
  $('end').value = datetimeLocal(new Date(start.getTime() + duration), facility.timezone);
  $('timezone').textContent =
    `Form facility: ${facility.display_name}. Work times use ${facility.timezone}. Location: ${facility.latitude.toFixed(4)}, ${facility.longitude.toFixed(4)}. Synthetic office; no real employee data.`;
  $('work-refresh-note').textContent =
    `Form updated: starts ${displayTime(start, facility.timezone)}; shift length ${duration / 60000} min. Click Check conditions to evaluate this period. Existing evidence and saved decisions are unchanged.`;
  if (!activeRun && !activeDecision) context();
});
$('login').addEventListener('submit', async (event) => {
  event.preventDefault();
  busyButton($('login').querySelector('button'), true, 'Opening manager desk…');
  auth =
    'Basic ' + btoa(unescape(encodeURIComponent($('username').value + ':' + $('password').value)));
  const loginAbort = new AbortController(),
    loginTimer = setTimeout(() => loginAbort.abort(), 15000);
  try {
    const config = await api('/config', { signal: loginAbort.signal });
    clearTimeout(loginTimer);
    $('password').value = '';
    $('login-panel').hidden = true;
    $('workspace').hidden = false;
    status('Loading facilities and saved decisions…', false, 'busy');
    $('deployment').textContent =
      `${config.deployment} · ${config.environment} · ${config.build} · AI ${config.ai_mode}`;
    await loadFacilities();
    await history();
    status('Manager desk ready. Select the affected work period.');
    const id = sessionStorage.getItem('closurecall-run');
    if (id) await poll(id);
  } catch (error) {
    auth = '';
    $('workspace').hidden = true;
    $('login-panel').hidden = false;
    status(
      error.name === 'AbortError'
        ? 'Sign-in timed out. Check manager credentials or connectivity, then retry.'
        : error.message,
      true,
    );
  } finally {
    clearTimeout(loginTimer);
    busyButton($('login').querySelector('button'), false, '');
  }
});
$('logout').onclick = () => {
  auth = '';
  clearTimeout(polling);
  $('workspace').hidden = true;
  $('login-panel').hidden = false;
  $('mode').textContent = 'SIGNED OUT';
  $('mode').dataset.state = 'idle';
  status('Signed out.');
};
function datum(parent, label, value) {
  const row = node('div', undefined, 'datum');
  row.append(node('span', label), node('strong', value ?? 'Missing'));
  parent.append(row);
}
function evidence(snapshot) {
  const box = $('evidence');
  box.replaceChildren();
  box.className = '';
  const weather = snapshot.nws,
    aq = snapshot.air_quality,
    zone = snapshot.facility.timezone,
    historical = $('mode').textContent === 'REPLAY';
  if (snapshot.test_evidence_label) box.append(node('p', snapshot.test_evidence_label, 'warning'));
  if (historical)
    box.append(
      node(
        'p',
        'Historical evidence — source availability and validity are shown as saved. This view does not fetch current conditions.',
        'draft-notice',
      ),
    );
  const weatherBox = node('div', undefined, 'source-block'),
    head = node('div', undefined, 'source-heading');
  head.append(
    node('h3', 'National Weather Service'),
    pill(
      `${pretty(weather.status)}${historical ? ' at capture' : ''}`,
      weather.status === 'available' ? 'available' : 'unavailable',
    ),
  );
  weatherBox.append(
    head,
    node(
      'p',
      historical
        ? 'Saved NWS retrieval · not a current freshness check'
        : retrievalAge(weather.fetched_at_utc),
      'source-caption',
    ),
  );
  timeDatum(weatherBox, 'Retrieved', weather.fetched_at_utc, zone);
  datum(
    weatherBox,
    'HTTP / returned alerts',
    `${weather.response_status ?? 'Unavailable'} / ${weather.alerts.length}`,
  );
  const source = link('Open NWS source request ↗', weather.source_url);
  source.className = 'source-link';
  weatherBox.append(source);
  if (!weather.alerts.length)
    weatherBox.append(
      node(
        'p',
        weather.status === 'available'
          ? 'Valid empty feed: zero alerts returned. This does not verify local safety.'
          : 'Feed unavailable: missing evidence, not a zero-alert result.',
        weather.status === 'available' ? 'note' : 'warning',
      ),
    );
  for (const a of weather.alerts) {
    const item = node('div', undefined, 'alert-item'),
      meta = node('div', undefined, 'alert-meta');
    item.append(node('h3', a.event), node('p', a.headline || a.area_desc));
    [
      ['Severity', a.severity],
      ['Certainty', a.certainty],
      ['Urgency', a.urgency],
    ].forEach(([k, v]) => meta.append(node('span', `${k}: ${v ?? 'Unknown'}`)));
    item.append(meta);
    timeDatum(item, 'Issued', a.sent, zone);
    timeDatum(item, 'Effective', a.effective || a.onset, zone);
    timeDatum(item, 'Expires', a.expires, zone);
    if (a.ends) timeDatum(item, 'Event ends', a.ends, zone);
    datum(item, 'Saved applicability', a.applicability_status);
    item.append(
      node('p', a.applicability_reason),
      node('p', a.instruction || 'No instruction field provided.'),
    );
    const detail = node('details');
    detail.append(
      node('summary', 'Alert text and identifier'),
      node('p', a.description),
      node('p', a.alert_id),
    );
    item.append(detail);
    weatherBox.append(item);
  }
  const aqBox = node('div', undefined, 'source-block'),
    aqHead = node('div', undefined, 'source-heading');
  aqHead.append(
    node('h3', 'Modeled air quality'),
    pill(
      `${pretty(aq.status)}${historical ? ' at capture' : ''}`,
      aq.status === 'available' ? 'available' : 'unavailable',
    ),
  );
  aqBox.append(aqHead, node('p', 'Open-Meteo / CAMS · modeled grid estimate', 'source-caption'));
  datum(
    aqBox,
    historical ? 'US AQI at capture (unrounded)' : 'Current US AQI (unrounded)',
    aq.us_aqi,
  );
  datum(
    aqBox,
    'PM2.5',
    aq.pm2_5 === null || aq.pm2_5 === undefined
      ? 'Missing'
      : `${aq.pm2_5}${aq.units?.pm2_5 ? ' ' + aq.units.pm2_5 : ''}`,
  );
  timeDatum(aqBox, 'Model valid time', aq.valid_at_utc, zone);
  timeDatum(aqBox, 'Retrieved', aq.fetched_at_utc, zone);
  datum(
    aqBox,
    'Returned grid',
    aq.returned_grid_location
      ? `${aq.returned_grid_location.latitude}, ${aq.returned_grid_location.longitude}`
      : 'Missing',
  );
  const aqLink = link('Open-Meteo source request ↗', aq.source_url);
  aqLink.className = 'source-link';
  aqBox.append(
    aqLink,
    node(
      'p',
      `${aq.attribution}. Not a building sensor or indoor measurement. Retrieval time is separate from model valid time.`,
      'note',
    ),
  );
  box.append(weatherBox, aqBox);
}
function brief(snapshot, ai) {
  const box = $('brief');
  box.replaceChildren();
  box.className = '';
  const a = snapshot.assessment,
    summary = node('div', undefined, 'recommendation');
  summary.dataset.posture = a.recommended_posture || 'incomplete';
  summary.append(
    node('span', 'Original recommendation · prototype rules', 'recommendation-label'),
    node(
      'div',
      a.recommended_posture
        ? outcome(a.recommended_posture)
        : a.review_status === 'data_incomplete'
          ? 'Not enough data to recommend'
          : 'Manager judgment needed',
      'big-posture',
    ),
  );
  const badges = node('div', undefined, 'brief-badges');
  badges.append(
    pill(
      reviewLabel(a.review_status),
      a.review_status === 'ready_for_manager' ? 'ready' : 'review',
    ),
    pill(
      `${pretty(a.confidence_label)} confidence`,
      a.confidence_label === 'low' ? 'low' : 'confidence',
    ),
  );
  summary.append(
    badges,
    node(
      'p',
      'Confidence reflects how complete and applicable the evidence is. It is not a guarantee of safety or a probability. You still make the decision.',
      'confidence-note',
    ),
  );
  if (!$('human-panel').hidden) {
    const next = node('a', 'Make your decision →', 'guide-action');
    next.href = '#human-panel';
    summary.append(next);
  }
  box.append(summary);
  datum(box, 'Review requirement', reviewLabel(a.review_status));
  datum(box, 'Policy version', a.policy_version);
  box.append(node('p', a.rationale_text), node('p', a.protective_action_notice, 'warning'));
  for (const r of a.matched_rules) {
    const card = node('div', undefined, 'rule-card');
    card.append(node('h3', r.id));
    datum(card, 'Rule version', r.version);
    if (r.categorical_match_reason) datum(card, 'Saved applicability', r.categorical_match_reason);
    datum(
      card,
      'Observed / prototype threshold',
      `${r.observed_value} / ${r.threshold ?? 'category match'}`,
    );
    datum(
      card,
      'Exceedance',
      r.exceedance === null ? 'No numeric exceedance' : `${r.exceedance} ${r.units}`,
    );
    card.append(
      node('p', r.prototype_mapping_reason),
      link('Reference evidence anchor', r.reference_source_url),
    );
    box.append(card);
  }
  for (const [title, values] of [
    ['Missing inputs', a.missing_inputs],
    ['What could change the recommendation?', a.what_would_change],
    ['Why this confidence level?', [...a.assumptions, ...a.confidence_basis]],
  ]) {
    const d = node('details');
    d.append(node('summary', `${title}${title === 'Missing inputs' ? ` (${values.length})` : ''}`));
    if (!values.length) d.append(node('p', 'No entries recorded.'));
    values.forEach((v) => d.append(node('p', v)));
    box.append(d);
  }
  const aiDetail = node('details');
  aiDetail.append(
    node(
      'summary',
      `Strands evidence brief · ${pretty(ai.status)}${$('mode').textContent === 'REPLAY' ? ' · saved' : ''}`,
    ),
    node('p', ai.narrative || `Deterministic result retained. ${ai.safe_error_code || ''}`),
  );
  box.append(aiDetail);
}
function timeline(snapshot, trace, decision) {
  $('timeline').replaceChildren();
  const entries = [
    `Source capture${decision ? ' (historical)' : snapshot.test_evidence_label ? ' (synthetic test)' : ''}: ${snapshot.collected_at_utc}`,
    `Policy ${snapshot.policy.version}: ${snapshot.assessment.review_status}`,
    ...trace.map(
      (t) =>
        `${t.step_number}. ${t.tool_name} · ${t.status} · ${t.duration_ms}ms · ${t.output_summary || t.safe_error_code || ''}`,
    ),
  ];
  if (!trace.length) entries.push('No verified Strands tool invocation for this run.');
  if (decision)
    entries.push(
      `Manager ${decision.actor}: ${decision.status} / ${decision.posture || 'rejected'} at ${decision.approved_at}`,
      'Notification drafts stored in demo outbox',
      'Historical replay reads frozen records only',
    );
  entries.forEach((t) => $('timeline').append(node('li', t)));
}
function renderRun(run) {
  if (activeRun?.id !== run.id) {
    $('reason').value = '';
    $('timing').value = '';
    $('timing-basis').value = '';
  }
  activeRun = run;
  activeDecision = null;
  $('mode').textContent = run.snapshot?.test_evidence_label
    ? 'TEST'
    : run.snapshot
      ? 'LIVE'
      : 'COLLECTING';
  $('mode').dataset.state = run.snapshot?.test_evidence_label ? 'test' : 'live';
  context(run.snapshot);
  $('human-panel').hidden = !['ready', 'incomplete'].includes(run.status);
  $('people').className = 'placeholder';
  $('people').replaceChildren(
    node(
      'p',
      'Manager decision pending. Recipient routing will be frozen when a human records a decision.',
      'placeholder',
    ),
  );
  $('exports').replaceChildren();
  $('counts').textContent = '12 SYNTHETIC EMPLOYEES';
  if (run.snapshot) {
    showFrozenWindow(run.snapshot, false);
    evidence(run.snapshot);
    brief(run.snapshot, run.ai || { status: 'running' });
    timeline(run.snapshot, run.trace || []);
    const a = run.snapshot.assessment;
    if (a.recommended_posture) $('posture').value = a.recommended_posture;
    $('approval-note').textContent =
      `Reviewing ${displayWindow(run.snapshot.work_period.start, run.snapshot.work_period.end, run.snapshot.facility.timezone)}. ${run.snapshot.work_period.special_shift ? 'SYNTHETIC SPECIAL SHIFT. ' : ''}Approval binds this snapshot hash. Stale, superseded, or incomplete evidence requires an explicit reasoned override.`;
    $('action').value = a.review_status === 'ready_for_manager' ? 'approve' : 'override';
    decisionHint();
  } else {
    $('evidence').replaceChildren(
      node(
        'p',
        'Waiting for this evaluation’s live source collection. Previous evidence is cleared.',
        'placeholder',
      ),
    );
    $('brief').replaceChildren(node('p', 'No current-run assessment yet.', 'placeholder'));
    $('timeline').replaceChildren(
      node('li', 'Waiting for current-run evidence; no tool result yet.'),
    );
  }
}
async function poll(id) {
  clearTimeout(polling);
  try {
    const run = await api('/evaluations/' + id);
    const busy = ['collecting', 'evaluating'].includes(run.status);
    busyButton(
      $('evaluate-button'),
      busy,
      run.status === 'collecting' ? 'Collecting source evidence…' : 'Preparing decision brief…',
    );
    if (run.decision_id) {
      renderReplay(await api(`/decisions/${run.decision_id}/replay`));
      return;
    }
    renderRun(run);
    status(
      `Evaluation: ${run.status}${run.error ? ' · ' + run.error : ''}`,
      run.status === 'failed',
      busy ? 'busy' : 'info',
    );
    if (busy) polling = setTimeout(() => poll(id), 2000);
    else evaluationKey = null;
  } catch (error) {
    status(error.message, true);
    busyButton($('evaluate-button'), false, '');
  }
}
$('evaluate').addEventListener('submit', async (event) => {
  event.preventDefault();
  busyButton($('evaluate-button'), true, 'Starting evaluation…');
  try {
    const payload = {
      facility_id: $('facility').value,
      start: offsetDate($('start').value),
      end: offsetDate($('end').value),
      special_shift: $('special').checked,
    };
    evaluationKey = evaluationKey || crypto.randomUUID();
    const run = await api('/evaluations', {
      method: 'POST',
      headers: { 'Idempotency-Key': evaluationKey },
      body: JSON.stringify(payload),
    });
    sessionStorage.setItem('closurecall-run', run.run_id);
    decisionKey = null;
    await poll(run.run_id);
  } catch (error) {
    status(error.message, true);
    busyButton($('evaluate-button'), false, '');
    evaluationKey = null;
  }
});
function people(pack, id) {
  $('counts').textContent = Object.entries(pack.counts)
    .sort(
      ([a], [b]) =>
        ['included', 'excluded', 'deferred'].indexOf(a) -
        ['included', 'excluded', 'deferred'].indexOf(b),
    )
    .map(([k, v]) => `${v} ${k}`)
    .join(' · ');
  $('people').replaceChildren();
  $('people').className = '';
  for (const p of pack.recipients) {
    const item = node('div', undefined, 'person'),
      top = node('div', undefined, 'person-top');
    item.dataset.route = p.routing_status;
    item.dataset.essential = String(p.essential);
    top.append(
      node('strong', p.name + (p.essential ? ' · Essential' : '')),
      pill(pretty(p.routing_status), p.routing_status),
    );
    item.append(top, node('p', p.reason));
    const meta = node('div', undefined, 'person-meta');
    meta.append(
      node(
        'span',
        `Channel: ${{ app_inbox: 'App inbox', voice_accessible: 'Accessible voice draft', none: 'None' }[p.channel] || pretty(p.channel || 'none')}`,
      ),
      pill(
        p.notification_status === 'queued_demo'
          ? 'Demo outbox draft · not sent'
          : 'Draft · not sent',
        'draft',
      ),
    );
    item.append(meta);
    if (p.follow_up) item.append(node('p', `Manual follow-up: ${p.follow_up}`, 'follow-up'));
    const d = node('details');
    d.append(
      node('summary', 'Read draft message'),
      node('div', p.message, 'message'),
      link('Export prototype .eml', `/api/decisions/${id}/notifications/${p.employee_id}/export`),
    );
    item.append(d);
    $('people').append(item);
  }
}
function renderReplay(record) {
  activeDecision = record.decision;
  showFrozenWindow(record.snapshot);
  $('mode').textContent = 'REPLAY';
  $('mode').dataset.state = 'replay';
  $('human-panel').hidden = true;
  busyButton($('evaluate-button'), false, '');
  context(record.snapshot, record.decision, true);
  evidence(record.snapshot);
  brief(record.snapshot, record.ai);
  const panel = node('div', undefined, 'recorded-decision');
  panel.dataset.state = record.decision.status;
  panel.append(
    node('span', 'Recorded manager decision', 'recommendation-label'),
    node(
      'div',
      record.decision.status === 'rejected'
        ? 'Assessment rejected'
        : outcome(record.decision.posture),
      'decision-posture',
    ),
    pill(pretty(record.decision.status), record.decision.status),
  );
  datum(panel, 'Decision actor', record.decision.actor);
  timeDatum(panel, 'Recorded', record.decision.approved_at, record.snapshot.facility.timezone);
  datum(
    panel,
    'Affected work period',
    displayWindow(
      record.decision.effective_window.start,
      record.decision.effective_window.end,
      record.snapshot.facility.timezone,
    ),
  );
  if (record.decision.timing_at) {
    timeDatum(
      panel,
      'Confirmed timing',
      record.decision.timing_at,
      record.snapshot.facility.timezone,
    );
    datum(panel, 'Timing evidence / assumption', record.decision.timing_basis);
  }
  panel.append(node('p', record.decision.reason));
  const next = node('a', 'Review employee drafts →', 'source-link');
  next.href = '#outbox-card';
  panel.append(next);
  $('brief').insertBefore(panel, $('brief').children[1]);
  timeline(record.snapshot, record.trace, record.decision);
  people(record.notifications, record.decision.decision_id);
  $('exports').replaceChildren(
    link('Export frozen decision package', `/api/decisions/${record.decision.decision_id}/export`),
    link('Download decision memo (HTML)', `/api/decisions/${record.decision.decision_id}/memo`),
  );
  status(
    `Historical replay · collected ${displayTime(record.snapshot.collected_at_utc, record.snapshot.facility.timezone)}. Bundle integrity verified. No sources or model called for replay.`,
  );
}
$('decision').addEventListener('submit', async (event) => {
  event.preventDefault();
  busyButton($('decision-button'), true, 'Saving decision & drafts…');
  try {
    const payload = {
      snapshot_hash: activeRun.snapshot_hash,
      action: $('action').value,
      posture: $('action').value === 'reject' ? null : $('posture').value,
      reason: $('reason').value,
      timing_at: $('timing').value
        ? offsetDate($('timing').value, activeRun.snapshot.facility.timezone)
        : null,
      timing_basis: $('timing-basis').value,
    };
    decisionKey = decisionKey || crypto.randomUUID();
    const record = await api(`/evaluations/${activeRun.id}/decision`, {
      method: 'POST',
      headers: { 'Idempotency-Key': decisionKey },
      body: JSON.stringify(payload),
    });
    renderReplay(record);
    await history();
  } catch (error) {
    status(error.message, true);
    decisionKey = null;
  } finally {
    busyButton($('decision-button'), false, '');
  }
});
async function history() {
  const records = await api('/decisions');
  $('history').replaceChildren();
  if (!records.length) $('history').append(node('p', 'No stored manager decisions yet.'));
  records.forEach((r) => {
    const row = node('div', undefined, 'history-row'),
      button = node('button', 'Open saved decision', 'quiet');
    button.onclick = async () => {
      clearTimeout(polling);
      try {
        renderReplay(await api(`/decisions/${r.decision_id}/replay`));
      } catch (e) {
        status(e.message, true);
      }
    };
    row.append(
      node(
        'p',
        `${r.status === 'rejected' ? 'Assessment rejected' : outcome(r.posture) + ' · ' + pretty(r.status)}\nRecorded ${displayTime(r.approved_at, selected()?.timezone || 'UTC')}`,
      ),
      button,
    );
    $('history').append(row);
  });
}
$('refresh-history').onclick = async () => {
  busyButton($('refresh-history'), true, 'Refreshing…');
  try {
    await history();
  } catch (e) {
    status(e.message, true);
  } finally {
    busyButton($('refresh-history'), false, '');
  }
};
$('explore').onclick = async () => {
  busyButton($('explore'), true, 'Finding active warnings…');
  try {
    status('Fetching national live warnings…');
    const data = await api('/live-alerts');
    $('explorer').replaceChildren(
      node(
        'p',
        `${data.status} · fetched ${data.fetched_at_utc} · national feed ${data.national_total} alerts · up to 50 supported warnings shown`,
      ),
    );
    for (const a of data.alerts) {
      const item = node('div', undefined, 'alert-item'),
        button = node('button', 'Create verified synthetic site', 'quiet');
      button.disabled = !a.geometry;
      button.onclick = async () => {
        button.disabled = true;
        try {
          const f = await api('/facilities/demo-site', {
            method: 'POST',
            body: JSON.stringify({ alert_id: a.alert_id }),
          });
          await loadFacilities(f.facility_id);
          status('Synthetic site verified by NWS point endpoint; review work period.');
        } catch (e) {
          status(e.message, true);
        } finally {
          button.disabled = !a.geometry;
        }
      };
      item.append(node('p', `${a.event} · ${a.area_desc}`), button);
      $('explorer').append(item);
    }
    status('Explorer ready; sites are synthetic and require point confirmation.');
  } catch (e) {
    status(e.message, true);
  } finally {
    busyButton($('explore'), false, '');
  }
};

function showFrozenWindow(snapshot, historical = true) {
  $('work-refresh-note').textContent = workRefreshHint;
  const f = snapshot.facility;
  if (facilities.some((item) => item.facility_id === f.facility_id))
    $('facility').value = f.facility_id;
  $('start').value = datetimeLocal(new Date(snapshot.work_period.start), f.timezone);
  $('end').value = datetimeLocal(new Date(snapshot.work_period.end), f.timezone);
  $('special').checked = snapshot.work_period.special_shift;
  $('timezone').textContent =
    `${historical ? 'Historical' : 'Evaluation'} facility: ${f.display_name}. All work times use ${f.timezone}. Location: ${f.latitude.toFixed(4)}, ${f.longitude.toFixed(4)}. Synthetic office and shift.`;
}
