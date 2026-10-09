const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const source = () => fs.readFileSync('assets/site.js', 'utf8');

function run(url, language = 'en') {
  const links = [{ href: 'https://pantani.xyz/', dataset: { lang: 'en' } },
    { href: 'https://pantani.xyz/pt/', dataset: { lang: 'pt' } }];
  const current = new URL(url);
  const redirects = [];
  const events = {};
  const document = {
    documentElement: { lang: language },
    querySelectorAll: () => links,
    getElementById: () => null,
  };
  const location = { href: url, pathname: current.pathname, search: current.search,
    hash: current.hash, replace: (value) => redirects.push(value) };
  const window = { addEventListener: (name, fn) => { events[name] = fn; } };
  vm.runInNewContext(source(), { document, location, window, URL, URLSearchParams });
  return { links, redirects, events };
}

test('language navigation preserves references and the selected section', () => {
  const result = run('https://pantani.xyz/?references=1#experience-title');
  assert.equal(result.links[1].href, 'https://pantani.xyz/pt/?references=1#experience-title');
  assert.equal(result.redirects.length, 0);
});

test('legacy Portuguese URLs redirect to a static locale path', () => {
  const result = run('https://pantani.xyz/?lang=pt-BR&references=1#experience-title');
  assert.equal(result.redirects[0], '/pt/?references=1#experience-title');
});

test('legacy English URLs on Portuguese pages return to English', () => {
  const result = run('https://pantani.xyz/pt/?lang=en#main', 'pt-BR');
  assert.equal(result.redirects[0], '/#main');
});

test('default English stays deterministic without stored preferences', () => {
  const result = run('https://pantani.xyz/');
  assert.equal(result.redirects.length, 0);
  assert.equal(result.links[0].href, 'https://pantani.xyz/');
});
