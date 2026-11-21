/* Progressive enhancement: tool cards remain available without JavaScript. */
(() => {
  'use strict';
  const grid = document.getElementById('tool-grid');
  if (!grid) return;
  const cards = [...grid.querySelectorAll('.tool-card')];
  const search = document.getElementById('search');
  const tabs = [...document.querySelectorAll('button.tab[data-category]')];
  const sort = document.getElementById('sort');
  const countLabel = document.getElementById('result-count');
  const empty = document.getElementById('empty-state');
  let category = 'all';
  function update() {
    const query = search.value.trim().toLocaleLowerCase();
    let visible = 0;
    cards.forEach(card => {
      const matchesCategory = category === 'all' || card.dataset.category === category;
      const matchesQuery = !query || card.dataset.search.includes(query);
      card.hidden = !matchesCategory || !matchesQuery;
      if (!card.hidden) visible++;
    });
    const sorted = [...cards].sort((a,b) => {
      if (sort.value === 'name') return a.dataset.name.localeCompare(b.dataset.name);
      const order = Number(a.dataset.day)-Number(b.dataset.day);
      return sort.value === 'oldest' ? order : -order;
    });
    sorted.forEach(card => grid.append(card));
    countLabel.textContent = visible === cards.length ? `Showing all ${cards.length} tools` : `Showing ${visible} of ${cards.length} tools`;
    empty.hidden = visible !== 0;
  }
  search.addEventListener('input',update);
  sort.addEventListener('change',update);
  tabs.forEach(tab => tab.addEventListener('click', () => {
    category = tab.dataset.category;
    tabs.forEach(t => { const active = t === tab; t.classList.toggle('active',active); t.setAttribute('aria-pressed',String(active)); });
    update();
  }));
  document.getElementById('reset-filters').addEventListener('click', () => {
    search.value = ''; sort.value = 'newest'; tabs.find(t => t.dataset.category === 'all').click(); search.focus();
  });
  document.addEventListener('click', event => {
    const a = event.target.closest('a[data-track-tool],a[data-track-source]');
    if (!a) return;
    const slug = a.dataset.trackTool || a.dataset.trackSource;
    window.BuildifulAnalytics?.track(a.dataset.trackTool ? 'tool_open' : 'source_open', slug);
  });
  update();
})();
