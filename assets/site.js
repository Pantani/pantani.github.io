/* The published site has static locale pages; JavaScript only enhances controls. */
(() => {
  const portuguese = document.documentElement.lang === 'pt-BR';

  function redirectLegacyLanguage() {
    const params = new URLSearchParams(location.search);
    const language = params.get('lang');
    if (!language) return false;
    const usePortuguese = ['pt', 'pt-BR', 'pt-br', 'ptbr', 'pt_br'].includes(language);
    const path = location.pathname.replace(/^\/pt(?=\/)/, '');
    params.delete('lang');
    const query = params.toString();
    const target = (usePortuguese ? '/pt' : '') + path;
    location.replace(target + (query ? '?' + query : '') + location.hash);
    return true;
  }

  function syncLanguageLink(link) {
    const target = new URL(link.href, location.href);
    const params = new URLSearchParams(location.search);
    params.delete('lang');
    target.search = params.toString();
    target.hash = location.hash;
    link.href = target.href;
  }

  function syncLanguageLinks() {
    document.querySelectorAll('.lang-button').forEach(syncLanguageLink);
  }

  function resetCopyLabel(label) {
    label.textContent = portuguese ? 'Copiar e-mail' : 'Copy email';
    label.classList.remove('copied');
  }

  async function copyEmail(label) {
    try {
      await navigator.clipboard.writeText('danpantani@gmail.com');
      label.textContent = portuguese ? 'Copiado ✓' : 'Copied ✓';
      label.classList.add('copied');
    } catch (_) {
      label.textContent = 'danpantani@gmail.com';
    }
    setTimeout(() => resetCopyLabel(label), 2400);
  }

  function setupCopyEmail() {
    const button = document.getElementById('copyEmailBtn');
    if (!button) return;
    const label = button.querySelector('span');
    button.addEventListener('click', () => copyEmail(label));
  }

  function setupSharePreview() {
    const button = document.getElementById('shareBtn');
    if (!button) return;
    button.addEventListener('click', () => {
      const target = document.getElementById('sharePreview');
      target.classList.add('is-revealed');
      const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      target.scrollIntoView({ behavior: reduced ? 'auto' : 'smooth', block: 'start' });
    });
  }

  if (redirectLegacyLanguage()) return;
  syncLanguageLinks();
  window.addEventListener('hashchange', syncLanguageLinks);
  setupCopyEmail();
  setupSharePreview();
})();
