'use strict';
(async function () {
  const error = document.querySelector('#data-error');
  try {
    const response = await fetch('pilot-data.json');
    if (!response.ok) throw new Error('HTTP ' + response.status);
    const data = await response.json();
    const select = document.querySelector('#threshold');
    const svgNS = 'http://www.w3.org/2000/svg';
    function el(name, attrs, text) {
      const node = document.createElementNS(svgNS, name);
      for (const [key, value] of Object.entries(attrs)) node.setAttribute(key, value);
      if (text !== undefined) node.textContent = text;
      return node;
    }
    function render() {
      const minimum = Number(select.value);
      const hospitals = data.hospitals.filter(h => Number.isFinite(h.discharge_percent) && Number.isFinite(h.completed_surveys) && h.completed_surveys >= minimum && (minimum === 0 || h.exposure_footnote === ''));
      const scores = hospitals.map(h => h.discharge_percent).sort((a, b) => a - b);
      const n = scores.length;
      const median = n % 2 ? scores[(n - 1) / 2] : (scores[n / 2 - 1] + scores[n / 2]) / 2;
      const summary = `${n} hospitals · median ${median}% · range ${scores[0]}–${scores[n - 1]}%`;
      document.querySelector('#chart-summary').textContent = summary;
      document.querySelector('#threshold-note').textContent = minimum === 0 ? 'Includes one hospital with 83 completed surveys and CMS caution footnote 6. All other hospitals have a blank discharge-score footnote.' : 'Includes only hospitals with a blank discharge-score footnote. This threshold changes sample reliability, not the meaning of the score or its causal interpretation.';
      const counts = new Map();
      scores.forEach(s => counts.set(s, (counts.get(s) || 0) + 1));
      const svg = el('svg', {viewBox: '0 0 900 270', 'aria-hidden': 'true'});
      const x = v => 35 + (v - 75) / 25 * 830;
      const baseline = 218;
      svg.append(el('line', {x1: 35, x2: 865, y1: baseline, y2: baseline, stroke: '#a4b4aa'}));
      for (let value = 75; value <= 100; value += 5) {
        svg.append(el('line', {x1: x(value), x2: x(value), y1: 12, y2: baseline, stroke: '#e2e7df'}));
        svg.append(el('text', {x: x(value), y: 246, 'text-anchor': 'middle', fill: '#586764', 'font-size': 14, 'font-family': 'sans-serif'}, String(value)));
      }
      for (const [score, count] of counts) {
        for (let i = 0; i < count; i++) svg.append(el('circle', {cx: x(score), cy: baseline - 12 - i * 17, r: 6, fill: '#103d3b'}));
      }
      const holder = document.querySelector('#distribution');
      holder.replaceChildren(svg);
      holder.setAttribute('aria-label', `${summary}. Each dot is one hospital. Horizontal score axis is zoomed from 75 to 100 percent. Data table follows.`);
      const table = document.querySelector('#distribution-table');
      table.replaceChildren();
      for (const [score, count] of counts) {
        const row = document.createElement('tr');
        const label = document.createElement('th'); label.scope = 'row'; label.textContent = score + '%';
        const cell = document.createElement('td'); cell.textContent = count;
        row.append(label, cell); table.append(row);
      }
    }
    select.addEventListener('change', render);
    render();
  } catch (e) {
    error.hidden = false;
    error.textContent = 'The interactive data could not load. The static findings and downloadable audit remain available. Serve this page over HTTP, or reload the published site.';
  }
})();
