#!/usr/bin/env node

/** Verify that a standalone skill install never exposes a fake "vunknown" version. */

const assert = require('assert');
const fs = require('fs');
const http = require('http');
const net = require('net');
const os = require('os');
const path = require('path');
const { spawn } = require('child_process');

const SERVER_PATH = path.join(__dirname, '../skills/brainstorm/scripts/server.cjs');
const TOKEN = 'standalone-branding-test-token-0123456789';

function findFreePort() {
  return new Promise((resolve, reject) => {
    const probe = net.createServer();
    probe.once('error', reject);
    probe.listen(0, '127.0.0.1', () => {
      const { port } = probe.address();
      probe.close((error) => error ? reject(error) : resolve(port));
    });
  });
}

function fetchPage(port) {
  return new Promise((resolve, reject) => {
    const request = http.get(
      `http://127.0.0.1:${port}/`,
      { headers: { Cookie: `brainstorm-key-${port}=${TOKEN}` } },
      (response) => {
        let body = '';
        response.on('data', (chunk) => { body += chunk; });
        response.on('end', () => resolve({ status: response.statusCode, body }));
      }
    );
    request.on('error', reject);
  });
}

async function waitForStartup(server) {
  return new Promise((resolve, reject) => {
    let stdout = '';
    let stderr = '';
    const timeout = setTimeout(
      () => reject(new Error(`server startup timed out: ${stderr}`)),
      5000
    );

    server.stdout.on('data', (chunk) => {
      stdout += chunk.toString();
      const line = stdout.split('\n').find((entry) => entry.includes('server-started'));
      if (!line) return;
      clearTimeout(timeout);
      resolve(JSON.parse(line));
    });
    server.stderr.on('data', (chunk) => { stderr += chunk.toString(); });
    server.on('error', (error) => {
      clearTimeout(timeout);
      reject(error);
    });
  });
}

async function main() {
  // The actual repository intentionally has no Superpowers package manifest,
  // matching a selected-skill installation rather than the full plugin tree.
  const sessionDir = fs.mkdtempSync(path.join(os.tmpdir(), 'brainstorm-branding-'));
  const port = await findFreePort();
  const server = spawn(process.execPath, [SERVER_PATH], {
    env: {
      ...process.env,
      BRAINSTORM_DIR: sessionDir,
      BRAINSTORM_HOST: '127.0.0.1',
      BRAINSTORM_PORT: String(port),
      BRAINSTORM_TOKEN: TOKEN,
      BRAINSTORM_OWNER_PID: ''
    }
  });

  try {
    const startup = await waitForStartup(server);
    const response = await fetchPage(startup.port);
    assert.strictEqual(response.status, 200);
    assert(response.body.includes('Superpowers Brainstorming'));
    assert(!response.body.includes('Superpowers vunknown'));
    console.log('PASS standalone branding uses a meaningful unversioned fallback');
  } finally {
    if (server.exitCode === null && server.signalCode === null) {
      server.kill();
      await new Promise((resolve) => server.once('exit', resolve));
    }
    fs.rmSync(sessionDir, { recursive: true, force: true });
  }
}

main().catch((error) => {
  console.error('FAIL standalone branding:', error.message);
  process.exit(1);
});
