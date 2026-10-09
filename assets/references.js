/* Public evidence augments the canonical CV without changing its claims. */
(() => {
  const enabled = new URLSearchParams(location.search).get('references') === '1';
  const copy = {
    en: {
      show: 'With references', hide: 'Without references', label: 'References',
      title: 'Follow the work, claim by claim',
      intro: 'Public pull requests and code changes are linked below the work they support. This is a curated evidence map, not a complete history of every contribution. PRs document implementation; they do not establish leadership, production deployment or business impact. The PDF download keeps the compact CV.',
      missing: 'No public references identified for this role.',
      checked: 'Links checked', commit: 'Commit',
    },
    pt: {
      show: 'Com referências', hide: 'Sem referências', label: 'Referências',
      title: 'Confira as entregas, item por item',
      intro: 'Os pull requests públicos e as alterações de código estão ligados às entregas que sustentam. Este é um mapeamento de evidências selecionadas, não o histórico completo de contribuições. PRs documentam implementação; não comprovam liderança, publicação em produção ou impacto de negócio. O download do PDF mantém o CV compacto.',
      missing: 'Nenhuma referência pública identificada para esta experiência.',
      checked: 'Links verificados', commit: 'Commit',
    },
  };

  function element(tag, className, text) {
    const node = document.createElement(tag);
    node.className = className;
    node.textContent = text;
    return node;
  }

  function referenceLink(source, labels) {
    const path = new URL(source.url).pathname.split('/');
    const repository = `${path[1]}/${path[2]}`;
    const number = source.kind === 'pr' ? `#${path[4]}` : `${labels.commit} ${path[4].slice(0, 7)}`;
    const link = element('a', 'reference-link', `${repository} ${number} — ${source.title}`);
    link.href = source.url;
    link.target = '_blank';
    link.rel = 'noopener noreferrer';
    return link;
  }

  function referenceList(sources, labels) {
    const details = element('details', 'reference-details', '');
    details.open = true;
    details.append(element('summary', '', `${labels.label} (${sources.length})`));
    const list = element('ul', 'reference-list', '');
    sources.forEach((source) => {
      const item = element('li', '', '');
      item.append(referenceLink(source, labels));
      list.append(item);
    });
    details.append(list);
    return details;
  }

  function renderClaim(key, claim, language) {
    const target = document.querySelector(`[data-i18n-html="${key}"], [data-i18n="${key}"]`);
    if (!target) return;
    const block = element('div', 'claim-references references-only', '');
    if (claim.sources.length) block.append(referenceList(claim.sources, copy[language]));
    if (claim.note) block.append(element('p', 'reference-note', claim.note[language]));
    target.append(block);
  }

  function renderMissing(labels) {
    document.querySelectorAll('.job-card').forEach((card) => {
      if (card.querySelector('.claim-references')) return;
      card.append(element('p', 'reference-note references-only', labels.missing));
    });
  }

  function renderIntro(labels) {
    const intro = element('aside', 'references-intro references-only', '');
    intro.append(element('h3', '', labels.title));
    intro.append(element('p', '', labels.intro));
    intro.append(element('p', 'reference-note', `${labels.checked}: ${CV_REFERENCES.checkedOn}`));
    document.querySelector('.experience').before(intro);
  }

  function renderToggle(labels) {
    const toggle = document.getElementById('referencesToggle');
    const url = new URL(location.href);
    if (enabled) url.searchParams.delete('references');
    else url.searchParams.set('references', '1');
    toggle.href = url.pathname + url.search + url.hash;
    toggle.textContent = enabled ? labels.hide : labels.show;
    toggle.classList.toggle('is-active', enabled);
  }

  function render() {
    const language = document.documentElement.lang === 'pt-BR' ? 'pt' : 'en';
    const labels = copy[language];
    document.querySelectorAll('.references-only').forEach((node) => node.remove());
    renderToggle(labels);
    if (!enabled) return;
    renderIntro(labels);
    Object.entries(CV_REFERENCES.claims).forEach(([key, claim]) => renderClaim(key, claim, language));
    renderMissing(labels);
  }

  document.addEventListener('cv:languagechange', render);
  window.addEventListener('hashchange', () => {
    const language = document.documentElement.lang === 'pt-BR' ? 'pt' : 'en';
    renderToggle(copy[language]);
  });
  render();
})();
