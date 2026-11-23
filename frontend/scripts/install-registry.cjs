#!/usr/bin/env node
/** 递归拉取 assistant-ui registry 组件并落盘(绕过 Node fetch 直连超时,统一走 curl)。 */
const { execFileSync } = require("node:child_process");
const fs = require("node:fs");
const path = require("node:path");

const ROOT = process.cwd();
const CACHE = path.join(ROOT, ".registry-cache");
const STYLE_BASE = "https://r.assistant-ui.com/styles/base-nova";
const BASE = "https://r.assistant-ui.com/base";
const SHADCN_UI = "https://ui.shadcn.com/r/styles/new-york-v4";

const fetched = new Set();
const npmDeps = new Set();
const written = [];

function curlJson(url) {
  const file = path.join(CACHE, url.replace(/[^a-z0-9]+/gi, "_") + ".json");
  if (!fs.existsSync(file)) {
    execFileSync("curl", ["-s", "--max-time", "60", url, "-o", file], { stdio: "inherit" });
  }
  try {
    return JSON.parse(fs.readFileSync(file, "utf8"));
  } catch {
    return null; // 404 页面等
  }
}

const SHADCN_PRIMS = new Set([
  "utils", "button", "skeleton", "tooltip", "spinner", "scroll-area",
]);

function resolveUrl(name) {
  if (name.startsWith("http")) return name;
  if (SHADCN_PRIMS.has(name)) {
    return `https://ui.shadcn.com/r/styles/new-york-v4/${name}.json`;
  }
  return `${STYLE_BASE}/${name}.json`;
}

function resolveFallbackUrl(name) {
  // assistant-ui 风格路径没有的(通常是 shadcn 原语),回退 shadcn 官方 registry
  return `https://ui.shadcn.com/r/styles/new-york-v4/${name}.json`;
}

function install(nameOrUrl) {
  let url = resolveUrl(nameOrUrl);
  if (fetched.has(url)) return;
  let item = curlJson(url);
  if (!item && !nameOrUrl.startsWith("http")) {
    const fb = resolveFallbackUrl(nameOrUrl);
    if (!fetched.has(fb)) {
      item = curlJson(fb);
      if (item) url = fb;
    }
  }
  if (!item) {
    console.error("SKIP (404 both registries):", nameOrUrl);
    return;
  }
  fetched.add(url);
  console.log("fetched:", item.name || url);

  (item.dependencies || []).forEach((d) => npmDeps.add(d));
  for (const f of item.files || []) {
    const target = f.targetPath || f.path || f.target;
    const dest = path.join(ROOT, target);
    fs.mkdirSync(path.dirname(dest), { recursive: true });
    fs.writeFileSync(dest, f.content, "utf8");
    written.push(target);
  }
  for (const dep of item.registryDependencies || []) {
    install(dep);
  }
}

const targets = process.argv.slice(2);
if (!targets.length) {
  console.error("usage: node scripts/install-registry.js <component...>");
  process.exit(1);
}
fs.mkdirSync(CACHE, { recursive: true });
targets.forEach(install);

fs.writeFileSync(
  path.join(CACHE, "deps.json"),
  JSON.stringify({ npm: [...npmDeps], files: written }, null, 2),
);
console.log("\nfiles written:", written.length);
console.log("npm deps:", [...npmDeps].join(" "));
