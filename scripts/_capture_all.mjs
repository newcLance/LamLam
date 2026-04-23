/**
 * Batch full-page screenshot capture for Tier 3 games.
 * Usage: node scripts/_capture_all.mjs
 * Requires: npx playwright install chromium (one-time)
 */
import { chromium } from 'playwright';
import { existsSync, mkdirSync } from 'fs';
import path from 'path';

const SCREENSHOT_DIR = path.resolve('D:/ecnalClaw/output/game-platform-analysis/screenshots');
const TIMEOUT = 20000; // 20s per page max

const GAMES = [
  { slug: 'stellar-blade', name: 'Stellar Blade', url: 'https://www.yourstellarblade.com/' },
  { slug: 'resident-evil-village', name: 'Resident Evil Village', url: 'https://www.residentevil.com/village/' },
  { slug: 'hogwarts-legacy', name: 'Hogwarts Legacy', url: 'https://www.hogwartslegacy.com/' },
  { slug: 'cyberpunk-2077', name: 'Cyberpunk 2077', url: 'https://www.cyberpunk.net/' },
  { slug: 'marvels-spider-man-remastered', name: "Marvel's Spider-Man Remastered", url: 'https://insomniac.games/game/marvels-spider-man-remastered/' },
  { slug: 'inscryption', name: 'Inscryption', url: 'https://www.inscryption.com/' },
  { slug: 'dave-the-diver', name: 'DAVE THE DIVER', url: 'https://mintrocket.net/davethediver/' },
  { slug: 'signalis', name: 'SIGNALIS', url: 'https://signalis.info/' },
  { slug: 'split-fiction', name: 'Split Fiction', url: 'https://www.ea.com/games/split-fiction' },
  { slug: 'days-gone', name: 'Days Gone', url: 'https://www.bendstudio.com/game/days-gone/' },
  { slug: 'balatro', name: 'Balatro', url: 'https://www.playbalatro.com/' },
  { slug: 'vampire-survivors', name: 'Vampire Survivors', url: 'https://poncle.games/' },
  { slug: 'cult-of-the-lamb', name: 'Cult of the Lamb', url: 'https://www.cultofthelamb.com/' },
  { slug: 'pizza-tower', name: 'Pizza Tower', url: 'https://www.pizzatowergame.com/' },
  { slug: 'dredge', name: 'DREDGE', url: 'https://www.dredge.game/' },
  { slug: 'lethal-company', name: 'Lethal Company', url: 'https://www.lethalcompany.com/' },
  { slug: 'satisfactory', name: 'Satisfactory', url: 'https://www.satisfactorygame.com/' },
  { slug: 'teardown', name: 'Teardown', url: 'https://www.teardowngame.com/' },
  { slug: 'dyson-sphere-program', name: 'Dyson Sphere Program', url: 'https://store.steampowered.com/app/1366540/Dyson_Sphere_Program/' },
  { slug: 'the-planet-crafter', name: 'The Planet Crafter', url: 'https://www.theplanetcrafter.com/' },
];

// Common cookie/popup dismiss selectors
const DISMISS_SELECTORS = [
  // Cookie consent
  '[id*="cookie"] button[class*="accept"]',
  '[id*="cookie"] button[class*="agree"]',
  '[class*="cookie"] button[class*="accept"]',
  '[class*="cookie"] button[class*="agree"]',
  '#onetrust-accept-btn-handler',
  '.cc-btn.cc-dismiss',
  '[data-testid="cookie-accept"]',
  'button[data-cookiefirst-action="accept"]',
  '#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll',
  '#didomi-notice-agree-button',
  '.osano-cm-accept-all',
  'button.accept-cookies',
  '[class*="CookieConsent"] button:first-child',
  // GDPR
  '[class*="gdpr"] button[class*="accept"]',
  // Generic popups
  '[class*="popup"] [class*="close"]',
  '[class*="modal"] [class*="close"]',
  '[class*="overlay"] [class*="close"]',
  // Age gate - try accept/enter buttons
  '[class*="age"] button',
  '[class*="age-gate"] button',
  '[id*="age-gate"] button',
  'button[class*="enter"]',
  // Specific sites
  '.evidon-banner-acceptbutton',
  '#truste-consent-button',
];

async function dismissPopups(page) {
  for (const sel of DISMISS_SELECTORS) {
    try {
      const btn = page.locator(sel).first();
      if (await btn.isVisible({ timeout: 500 })) {
        await btn.click({ timeout: 2000 });
        await page.waitForTimeout(500);
      }
    } catch { /* ignore */ }
  }
}

async function captureGame(browser, game) {
  const dir = path.join(SCREENSHOT_DIR, game.slug);
  const outFile = path.join(dir, 'home-1.webp');
  
  // Skip if already has screenshots
  if (existsSync(outFile)) {
    console.log(`  SKIP ${game.slug}: home-1.webp already exists`);
    return 'skipped';
  }

  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });

  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    locale: 'en-US',
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
  });
  const page = await context.newPage();
  
  try {
    console.log(`  Navigating to ${game.url}...`);
    await page.goto(game.url, { waitUntil: 'networkidle', timeout: TIMEOUT });
    
    // Wait for content to load
    await page.waitForTimeout(2000);
    
    // Dismiss popups
    await dismissPopups(page);
    await page.waitForTimeout(1000);
    
    // Take full page screenshot as WebP
    await page.screenshot({
      path: outFile,
      fullPage: true,
      type: 'png', // We'll convert to WebP later, or use WebP directly
    });
    
    // Actually, Playwright supports WebP natively? No - only png/jpeg.
    // Let's save as PNG first, then we'll convert with the slice script.
    // Wait - the file extension is .webp but content is PNG. Let me fix this.
    
    // Save as PNG, will be processed by slice script
    const pngFile = path.join(dir, 'home-1.png');
    if (existsSync(outFile)) {
      // Remove the wrongly-named file
      const fs = await import('fs/promises');
      await fs.unlink(outFile);
    }
    
    await page.screenshot({
      path: pngFile,
      fullPage: true,
      type: 'png',
    });
    
    const fs = await import('fs/promises');
    const stat = await fs.stat(pngFile);
    const sizeKB = Math.round(stat.size / 1024);
    console.log(`  ✓ ${game.slug}: home-1.png (${sizeKB} KB)`);
    
    return 'captured';
  } catch (err) {
    console.log(`  ✗ ${game.slug}: ${err.message.substring(0, 100)}`);
    return 'failed';
  } finally {
    await context.close();
  }
}

async function main() {
  console.log('=== Batch Screenshot Capture ===');
  console.log(`Target: ${GAMES.length} games`);
  console.log(`Output: ${SCREENSHOT_DIR}\n`);

  const browser = await chromium.launch({ headless: true });
  
  const results = { captured: 0, skipped: 0, failed: 0, failedGames: [] };

  for (const game of GAMES) {
    console.log(`\n[${GAMES.indexOf(game) + 1}/${GAMES.length}] ${game.name}`);
    const result = await captureGame(browser, game);
    results[result]++;
    if (result === 'failed') results.failedGames.push(game.slug);
  }

  await browser.close();

  console.log('\n=== Results ===');
  console.log(`Captured: ${results.captured}`);
  console.log(`Skipped:  ${results.skipped}`);
  console.log(`Failed:   ${results.failed}`);
  if (results.failedGames.length > 0) {
    console.log(`Failed games: ${results.failedGames.join(', ')}`);
  }
  console.log('\nNext: run `python scripts/slice-fullpage.py --all` to slice + convert to WebP');
}

main().catch(console.error);
