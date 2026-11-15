import { readFileSync } from 'node:fs';

// The requirement mapping page has two tables that must say the same thing: the requirements and the sections
// of the evidence pack that support each, and the sections and the requirements each supports. The Martian
// backend's tests hold the evidence pack and its own guide to the same identifiers; this check holds the page
// to itself, and to the statements it must keep: the page is partial, and a label says relevant, not met.
const page = 'src/content/docs/evidence/requirement-mapping.mdx';
const text = readFileSync(page, 'utf8');
const coverage = JSON.parse(readFileSync('quality/coverage.json', 'utf8'));
const failures = [];

const identifier = /^[a-z0-9]+(?:-[a-z0-9]+)*:[a-z0-9]+(?:-[a-z0-9]+)*$/;
const section = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const requirements = new Map(); // identifier -> the sections its row lists
const sections = new Map(); // section id -> the identifiers its row lists
for (const line of text.split('\n')) {
  if (!line.startsWith('|')) continue;
  const cells = line.trim().replace(/^\||\|$/g, '').split('|').map((cell) => cell.trim());
  const first = cells[0].match(/^`([^`]+)`$/)?.[1];
  if (!first) continue;
  const codes = (cell) => [...cell.matchAll(/`([^`]+)`/g)].map((match) => match[1]);
  if (identifier.test(first)) {
    if (requirements.has(first)) failures.push(`${first}: defined twice`);
    requirements.set(first, new Set(cells.slice(1).flatMap(codes).filter((code) => section.test(code))));
  } else if (section.test(first)) {
    if (sections.has(first)) failures.push(`${first}: section listed twice`);
    sections.set(first, new Set(cells.slice(1).flatMap(codes).filter((code) => identifier.test(code))));
  }
}
if (!requirements.size || !sections.size) failures.push('no mapping tables found');

for (const [name, supports] of sections) {
  for (const id of supports) if (!requirements.has(id)) failures.push(`section ${name} supports ${id}, which no requirement row defines`);
}
for (const [id, listed] of requirements) {
  const supporting = [...sections].filter(([, supports]) => supports.has(id)).map(([name]) => name);
  if (!supporting.length) failures.push(`${id}: no section supports it`);
  for (const name of supporting) if (!listed.has(name)) failures.push(`${id}: its row does not list section ${name}, which supports it`);
  for (const name of listed) if (!sections.has(name) || !sections.get(name).has(id)) failures.push(`${id}: its row lists ${name}, which does not support it`);
}

const guide = coverage.guides.find((entry) => entry.id === 'evidence/requirement-mapping');
if (!guide) failures.push('the page is absent from quality/coverage.json');
else if (guide.qualification !== 'partial') failures.push(`the page is ${guide.qualification}, and must stay partial until an exported pack has been walked through`);
if (!/<GuideMeta id="evidence\/requirement-mapping" \/>/.test(text)) failures.push('the page does not show its qualification (GuideMeta)');
for (const required of ['does not say that a system meets the requirement', 'legal advice', 'What the product does not cover', 'Sections of the pack']) {
  if (!text.includes(required) && !text.toLowerCase().includes(required.toLowerCase())) failures.push(`the page no longer says: ${required}`);
}
for (const claim of [/(?<!not )compliant/i, /certified/i, /guarantee/i, /ensures? compliance/i, /satisf(?:y|ies) (?:the )?(?:requirement|article)/i]) {
  if (claim.test(text)) failures.push(`claim language the page must not use (a label says relevant, not met): ${claim}`);
}

console.log(JSON.stringify({ requirements: requirements.size, sections: sections.size, unmappedSections: [...sections].filter(([, supports]) => !supports.size).map(([name]) => name), failures }, null, 2));
if (failures.length) process.exitCode = 1;
