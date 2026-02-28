import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();

const toCamelCase = (value) =>
  value
    .replace(/[-_]+([a-zA-Z0-9])/g, (_, captured) => captured.toUpperCase())
    .replace(/^[A-Z]/, (first) => first.toLowerCase());

const parseDefaultValue = (raw) => {
  const trimmed = raw.trim();
  if (trimmed === 'None') {
    return undefined;
  }
  if (trimmed === 'True') {
    return true;
  }
  if (trimmed === 'False') {
    return false;
  }
  if ((trimmed.startsWith('"') && trimmed.endsWith('"')) || (trimmed.startsWith("'") && trimmed.endsWith("'"))) {
    return trimmed.slice(1, -1);
  }
  if (/^-?\d+(\.\d+)?$/.test(trimmed)) {
    return Number(trimmed);
  }
  return trimmed;
};

const splitTopLevel = (input) => {
  const result = [];
  let buffer = '';
  let depth = 0;
  let quote = '';

  for (let i = 0; i < input.length; i += 1) {
    const ch = input[i];
    if (quote) {
      buffer += ch;
      if (ch === quote && input[i - 1] !== '\\') {
        quote = '';
      }
      continue;
    }

    if (ch === '"' || ch === "'") {
      quote = ch;
      buffer += ch;
      continue;
    }

    if (ch === '(' || ch === '[' || ch === '{') {
      depth += 1;
      buffer += ch;
      continue;
    }

    if (ch === ')' || ch === ']' || ch === '}') {
      depth -= 1;
      buffer += ch;
      continue;
    }

    if (ch === ',' && depth === 0) {
      const piece = buffer.trim();
      if (piece.length > 0) {
        result.push(piece);
      }
      buffer = '';
      continue;
    }

    buffer += ch;
  }

  const tail = buffer.trim();
  if (tail.length > 0) {
    result.push(tail);
  }
  return result;
};

const parseSignatureParams = (signature) => {
  const tokens = splitTopLevel(signature.replace(/\n/g, ' '));
  const params = [];

  for (const token of tokens) {
    const normalized = token.trim();
    if (!normalized || normalized === 'self') {
      continue;
    }

    const equalIndex = normalized.indexOf('=');
    const left = equalIndex >= 0 ? normalized.slice(0, equalIndex).trim() : normalized;
    const rawDefault = equalIndex >= 0 ? normalized.slice(equalIndex + 1).trim() : undefined;

    const colonIndex = left.indexOf(':');
    const name = (colonIndex >= 0 ? left.slice(0, colonIndex) : left).trim();

    if (!name || name === 'self') {
      continue;
    }

    const isRequired = rawDefault === undefined;
    const parameter = {
      name: toCamelCase(name),
      required: isRequired,
    };

    if (!isRequired) {
      const parsedDefault = parseDefaultValue(rawDefault);
      if (parsedDefault !== undefined) {
        parameter.defaultValue = parsedDefault;
      }
    }

    params.push(parameter);
  }

  return params;
};

const extractDictContent = (block, variableName) => {
  const assignIndex = block.indexOf(`${variableName} =`);
  if (assignIndex < 0) {
    return undefined;
  }

  const braceStart = block.indexOf('{', assignIndex);
  if (braceStart < 0) {
    return undefined;
  }

  let depth = 0;
  let quote = '';
  for (let i = braceStart; i < block.length; i += 1) {
    const ch = block[i];

    if (quote) {
      if (ch === quote && block[i - 1] !== '\\') {
        quote = '';
      }
      continue;
    }

    if (ch === '"' || ch === "'") {
      quote = ch;
      continue;
    }

    if (ch === '{') {
      depth += 1;
      continue;
    }

    if (ch === '}') {
      depth -= 1;
      if (depth === 0) {
        return block.slice(braceStart + 1, i);
      }
    }
  }

  return undefined;
};

const parseDictFromBlock = (block, variableName) => {
  const content = extractDictContent(block, variableName);
  if (!content) {
    return [];
  }

  const pairs = [...content.matchAll(/["']([^"']+)["']\s*:\s*([a-zA-Z_][a-zA-Z0-9_]*)/g)];
  return pairs.map((entry) => ({ key: entry[1], value: entry[2] }));
};

const extractMethods = (source) => {
  const methodRegex = /\n\s{4}def\s+([a-zA-Z0-9_]+)\s*\(([\s\S]*?)\)\s*(?:->[^\n:]+)?:\n([\s\S]*?)(?=\n\s{4}def\s+|$)/g;
  const methods = [];
  let match = methodRegex.exec(source);
  while (match) {
    const snakeName = match[1];
    if (snakeName === '__init__' || snakeName.startsWith('_')) {
      match = methodRegex.exec(source);
      continue;
    }

    methods.push({
      snakeName,
      methodName: toCamelCase(snakeName),
      signature: match[2],
      block: match[3],
    });
    match = methodRegex.exec(source);
  }
  return methods;
};

const buildKisMetadata = (sourcePath) => {
  const source = fs.readFileSync(sourcePath, 'utf8');
  const methods = extractMethods(source);

  return methods.map((method) => {
    const trId = (method.block.match(/["']tr_id["']\s*:\s*["']([^"']+)["']/) || [])[1];
    const getPathMatch = method.block.match(/_get\(\s*["']([^"']+)["']/);
    const postPathMatch = method.block.match(/_post\(\s*["']([^"']+)["']/);
    const endpointPath = getPathMatch?.[1] ?? postPathMatch?.[1] ?? '';
    const requestPairs = parseDictFromBlock(method.block, 'params').concat(parseDictFromBlock(method.block, 'body'));

    const requestMap = Object.fromEntries(requestPairs.map((pair) => [pair.key, toCamelCase(pair.value)]));

    return {
      methodName: method.methodName,
      method: postPathMatch ? 'POST' : 'GET',
      path: endpointPath,
      trId,
      requestMap,
      params: parseSignatureParams(method.signature),
    };
  });
};

const buildKiwoomMetadata = (sourcePath) => {
  const source = fs.readFileSync(sourcePath, 'utf8');
  const methods = extractMethods(source);
  const classPath = (source.match(/self\.path\s*=\s*"([^"]+)"/) || [])[1] ?? '';

  return methods.map((method) => {
    const apiId = (method.block.match(/["']api-id["']\s*:\s*["']([^"']+)["']/) || [])[1] ?? '';
    const bodyPairs = parseDictFromBlock(method.block, 'body');
    const headerPairs = parseDictFromBlock(method.block, 'headers');

    const bodyMap = Object.fromEntries(bodyPairs.map((pair) => [pair.key, toCamelCase(pair.value)]));
    const headerParamMap = Object.fromEntries(
      headerPairs
        .filter((pair) => ['cont-yn', 'cond-yn', 'con-yn', 'next-key'].includes(pair.key))
        .map((pair) => [pair.key, toCamelCase(pair.value)]),
    );

    return {
      methodName: method.methodName,
      path: classPath,
      apiId,
      bodyMap,
      headerParamMap,
      params: parseSignatureParams(method.signature),
    };
  });
};

const writeTs = (targetPath, symbolName, importPath, data) => {
  const fullPath = path.join(ROOT, targetPath);
  const content =
    `import type { ${importPath} } from '../../core/types';\n\n` +
    `export const ${symbolName}: ${importPath}[] = ${JSON.stringify(data, null, 2)};\n`;
  fs.writeFileSync(fullPath, content);
};

const tasks = [
  {
    sourcePath: 'packages/cluefin-openapi/src/cluefin_openapi/kis/_domestic_basic_quote.py',
    targetPath: 'packages/cluefin-openapi-ts/src/kis/metadata/domestic-basic-quote.ts',
    symbolName: 'domesticBasicQuoteEndpoints',
    kind: 'kis',
  },
  {
    sourcePath: 'packages/cluefin-openapi/src/cluefin_openapi/kis/_domestic_stock_info.py',
    targetPath: 'packages/cluefin-openapi-ts/src/kis/metadata/domestic-stock-info.ts',
    symbolName: 'domesticStockInfoEndpoints',
    kind: 'kis',
  },
  {
    sourcePath: 'packages/cluefin-openapi/src/cluefin_openapi/kiwoom/_domestic_chart.py',
    targetPath: 'packages/cluefin-openapi-ts/src/kiwoom/metadata/domestic-chart.ts',
    symbolName: 'domesticChartEndpoints',
    kind: 'kiwoom',
  },
  {
    sourcePath: 'packages/cluefin-openapi/src/cluefin_openapi/kiwoom/_domestic_stock_info.py',
    targetPath: 'packages/cluefin-openapi-ts/src/kiwoom/metadata/domestic-stock-info.ts',
    symbolName: 'domesticStockInfoEndpoints',
    kind: 'kiwoom',
  },
  {
    sourcePath: 'packages/cluefin-openapi/src/cluefin_openapi/kiwoom/_domestic_rank_info.py',
    targetPath: 'packages/cluefin-openapi-ts/src/kiwoom/metadata/domestic-rank-info.ts',
    symbolName: 'domesticRankInfoEndpoints',
    kind: 'kiwoom',
  },
];

for (const task of tasks) {
  const data = task.kind === 'kis' ? buildKisMetadata(task.sourcePath) : buildKiwoomMetadata(task.sourcePath);
  const importType = task.kind === 'kis' ? 'KisEndpointDefinition' : 'KiwoomEndpointDefinition';
  writeTs(task.targetPath, task.symbolName, importType, data);
  console.log(`${task.symbolName}: ${data.length}`);
}
