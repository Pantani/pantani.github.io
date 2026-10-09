// Run with Playwright available on NODE_PATH and the site served on port 8879.
const { test, before, after } = require('node:test');
const assert = require('node:assert/strict');
const { chromium } = require('playwright');

let browser;
let page;
const base = process.env.CV_TEST_URL || 'http://127.0.0.1:8879';

before(async () => {
  browser = await chromium.launch({ channel: 'chrome', headless: true });
  page = await browser.newPage();
});
after(async () => { await browser?.close(); });

test('regular CV links to a shareable references view', async () => {
  await page.goto(base);
  assert.equal(await page.locator('.claim-references').count(), 0);
  assert.equal(await page.locator('#referencesToggle').count(), 1);
  await page.locator('#referencesToggle').click();
  assert.equal(new URL(page.url()).searchParams.get('references'), '1');
  await page.reload();
  const atomone = page.locator('[data-i18n-html="exp.ignite.b3"]');
  assert.equal(await atomone.locator('a[href="https://github.com/atomone-hub/atomone-sdk/pull/10"]').count(), 1);
  assert.match(await atomone.textContent(), /Nakamoto Bonus/);
});

test('language changes retain references without duplicates and preserve the URL', async () => {
  await page.goto(`${base}/?references=1&lang=en#experience-title`);
  const count = await page.locator('.claim-references a').count();
  assert.ok(count > 50);
  await page.locator('[data-lang="pt"]').click();
  assert.equal(new URL(page.url()).searchParams.get('references'), '1');
  assert.equal(new URL(page.url()).searchParams.get('lang'), 'pt-BR');
  assert.equal(await page.locator('.claim-references a').count(), count);
  assert.match(await page.locator('#referencesToggle').textContent(), /Sem referências/);
  await page.locator('[data-lang="en"]').click();
  assert.equal(await page.locator('.claim-references a').count(), count);
});

test('unsupported claims are explicit and do not borrow unrelated PRs', async () => {
  await page.goto(`${base}/?references=1&lang=en`);
  const abi = page.locator('[data-i18n-html="exp.hermez.b3"]');
  assert.equal(await abi.locator('a').count(), 0);
  assert.match(await abi.textContent(), /no specific public PR identified/);
  const energi = page.locator('.job-card').filter({ has: page.locator('[data-i18n-html="exp.energi.b1"]') });
  assert.match(await energi.textContent(), /No public references identified/);
});

test('return to regular CV preserves the selected language and anchor', async () => {
  await page.goto(`${base}/?references=1&lang=pt-BR#experience-title`);
  await page.locator('#referencesToggle').click();
  assert.equal(new URL(page.url()).searchParams.has('references'), false);
  assert.equal(new URL(page.url()).searchParams.get('lang'), 'pt-BR');
  assert.equal(new URL(page.url()).hash, '#experience-title');
  assert.equal(await page.locator('.claim-references').count(), 0);
});

test('toggle preserves anchors selected after the page loads', async () => {
  await page.goto(`${base}/?lang=en`);
  await page.locator('a.cta[href="#experience-title"]').click();
  await page.locator('#referencesToggle').click();
  assert.equal(new URL(page.url()).hash, '#experience-title');
});

test('mobile references fit the viewport and standard print stays compact', async () => {
  await page.setViewportSize({ width: 375, height: 812 });
  await page.goto(`${base}/?references=1&lang=pt-BR`);
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth > innerWidth);
  assert.equal(overflow, false);
  assert.equal(await page.locator('#referencesToggle').isVisible(), true);
  await page.emulateMedia({ media: 'print' });
  assert.equal(await page.locator('.claim-references').first().isVisible(), false);
  assert.match(await page.locator('#downloadPdfBtn').getAttribute('href'), /cv-pt-br\.pdf$/);
  await page.emulateMedia({ media: 'screen' });
});
