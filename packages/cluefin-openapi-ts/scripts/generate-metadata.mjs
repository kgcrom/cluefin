import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const scriptPath = fileURLToPath(import.meta.url);
const scriptDir = path.dirname(scriptPath);
const packageRoot = path.resolve(scriptDir, '..');
const workspaceRoot = path.resolve(packageRoot, '..', '..');

const resolveWithinRoot = (rootDir, relativePath) => {
  const resolved = path.resolve(rootDir, relativePath);
  const relative = path.relative(rootDir, resolved);
  if (relative.startsWith('..') || path.isAbsolute(relative)) {
    throw new Error(`Path escapes root: ${relativePath}`);
  }
  return resolved;
};

const toCamelCase = (value) =>
  value
    .replace(/_+$/, '') // 파이썬 예약어 회피용 트레일링 언더스코어 (예: next_)
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
      snakeName: name,
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

  const entries = [];
  for (const rawPiece of splitTopLevel(content)) {
    const piece = rawPiece
      .split('\n')
      .filter((line) => !line.trim().startsWith('#'))
      .join('\n')
      .trim();
    const match = piece.match(/^["']([^"']+)["']\s*:\s*([\s\S]+)$/);
    if (!match) {
      continue;
    }
    entries.push({ key: match[1], expression: match[2].trim() });
  }
  return entries;
};

// dict 리터럴 밖에서 조건부로 넣는 항목: `body["key"] = value` / `params["key"] = value`
const parseDictAssignments = (block, variableName) => {
  const pattern = new RegExp(`${variableName}\\[["']([^"']+)["']\\]\\s*=\\s*([^\\n]+)`, 'g');
  return [...block.matchAll(pattern)].map((entry) => ({ key: entry[1], expression: entry[2].trim() }));
};

const IDENTIFIER_ONLY = /^[a-zA-Z_][a-zA-Z0-9_]*$/;
const STRING_LITERAL = /^["']([^"']*)["']$/;

// dict 엔트리(key: expression)를 requestMap 쌍과 추가 params로 분해한다.
// - 값이 kwarg 식별자면 그대로 매핑
// - 값이 문자열 리터럴이면: 같은 이름의 kwarg가 있으면 그 kwarg로 매핑, 없으면
//   상수 기본값을 가진 선택 파라미터를 합성해 매핑 (예: KIS의 "CTX_AREA_NK30": "")
// - 그 외 표현식이면 표현식 안에서 가장 긴 kwarg 이름을 찾아 매핑
const resolveDictEntries = (entries, signatureParams, context) => {
  const paramNames = new Set(signatureParams.map((p) => p.name));
  const mappings = [];
  const syntheticParams = [];

  for (const { key, expression } of entries) {
    if (IDENTIFIER_ONLY.test(expression)) {
      mappings.push([key, toCamelCase(expression)]);
      continue;
    }

    const literalMatch = expression.match(STRING_LITERAL);
    if (literalMatch) {
      const camelKey = toCamelCase(key.toLowerCase());
      if (!paramNames.has(camelKey)) {
        syntheticParams.push({ name: camelKey, required: false, defaultValue: literalMatch[1] });
        paramNames.add(camelKey);
      }
      mappings.push([key, camelKey]);
      continue;
    }

    // 복합 표현식: 표현식 안에 등장하는 시그니처 kwarg 중 가장 긴 것을 채택
    const candidates = signatureParams
      .map((p) => p.snakeName)
      .filter((snake) => new RegExp(`\\b${snake}\\b`).test(expression))
      .sort((a, b) => b.length - a.length);
    if (candidates.length > 0) {
      mappings.push([key, toCamelCase(candidates[0])]);
      continue;
    }

    console.warn(`  [warn] ${context}: could not resolve dict value for key "${key}" (${expression.slice(0, 60)})`);
  }

  return { mappings, syntheticParams };
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

// 파이썬 소스에서 정규식으로 못 뽑는 케이스(f-string 루프 등)의 수동 보정.
// 재생성해도 유지되도록 여기에 둔다. symbolName.methodName -> 추가 requestMap 엔트리
const MANUAL_REQUEST_MAP_OVERRIDES = {
  // 관심종목(멀티종목) 시세조회: 슬롯 1~30을 헬퍼+루프로 조립해 dict 리터럴이 없다
  'domesticMarketAnalysisEndpoints.getWatchlistMultiQuote': Object.fromEntries(
    Array.from({ length: 30 }, (_, i) => i + 1).flatMap((slot) => [
      [`FID_COND_MRKT_DIV_CODE_${slot}`, `fidCondMrktDivCode${slot}`],
      [`FID_INPUT_ISCD_${slot}`, `fidInputIscd${slot}`],
    ]),
  ),
};

const stripInternalFields = (params) => params.map(({ snakeName, ...rest }) => rest);

const applyOverrides = (symbolName, methodName, requestMap) => {
  const override = MANUAL_REQUEST_MAP_OVERRIDES[`${symbolName}.${methodName}`];
  return override ? { ...requestMap, ...override } : requestMap;
};

const buildKisMetadata = (sourceRelativePath, symbolName) => {
  const sourcePath = resolveWithinRoot(workspaceRoot, sourceRelativePath);
  const source = fs.readFileSync(sourcePath, 'utf8');
  const methods = extractMethods(source);

  return methods.map((method) => {
    const trId = (method.block.match(/["']tr_id["']\s*:\s*["']([^"']+)["']/) || [])[1];
    const getPathMatch = method.block.match(/_get\(\s*["']([^"']+)["']/);
    const postPathMatch = method.block.match(/_post\(\s*["']([^"']+)["']/);
    const endpointPath = getPathMatch?.[1] ?? postPathMatch?.[1] ?? '';
    const signatureParams = parseSignatureParams(method.signature);
    const entries = parseDictFromBlock(method.block, 'params')
      .concat(parseDictFromBlock(method.block, 'body'))
      .concat(parseDictAssignments(method.block, 'params'))
      .concat(parseDictAssignments(method.block, 'body'));
    const { mappings, syntheticParams } = resolveDictEntries(entries, signatureParams, method.methodName);

    return {
      methodName: method.methodName,
      method: postPathMatch ? 'POST' : 'GET',
      path: endpointPath,
      trId,
      requestMap: applyOverrides(symbolName, method.methodName, Object.fromEntries(mappings)),
      params: stripInternalFields(signatureParams).concat(syntheticParams),
    };
  });
};

const buildKiwoomMetadata = (sourceRelativePath, symbolName) => {
  const sourcePath = resolveWithinRoot(workspaceRoot, sourceRelativePath);
  const source = fs.readFileSync(sourcePath, 'utf8');
  const methods = extractMethods(source);
  const classPath = (source.match(/self\.path\s*=\s*"([^"]+)"/) || [])[1] ?? '';

  return methods.map((method) => {
    const apiId = (method.block.match(/["']api-id["']\s*:\s*["']([^"']+)["']/) || [])[1] ?? '';
    const signatureParams = parseSignatureParams(method.signature);
    const bodyEntries = parseDictFromBlock(method.block, 'body').concat(parseDictAssignments(method.block, 'body'));
    const { mappings, syntheticParams } = resolveDictEntries(bodyEntries, signatureParams, method.methodName);
    const headerPairs = parseDictFromBlock(method.block, 'headers');

    const headerParamMap = Object.fromEntries(
      headerPairs
        .filter((pair) => ['cont-yn', 'cond-yn', 'con-yn', 'next-key'].includes(pair.key))
        .filter((pair) => IDENTIFIER_ONLY.test(pair.expression))
        .map((pair) => [pair.key, toCamelCase(pair.expression)]),
    );

    return {
      methodName: method.methodName,
      path: classPath,
      apiId,
      bodyMap: applyOverrides(symbolName, method.methodName, Object.fromEntries(mappings)),
      headerParamMap,
      params: stripInternalFields(signatureParams).concat(syntheticParams),
    };
  });
};

const buildNhplugMetadata = (sourceRelativePath, symbolName) => {
  const sourcePath = resolveWithinRoot(workspaceRoot, sourceRelativePath);
  const source = fs.readFileSync(sourcePath, 'utf8');
  const methods = extractMethods(source);

  return methods.map((method) => {
    // 키움은 클래스 레벨 self.path 하나를 쓰지만, NH PLUG 는 호출마다 경로를 넘긴다.
    const endpointPath = (method.block.match(/client\.post\(\s*["']([^"']+)["']/) || [])[1] ?? '';
    const signatureParams = parseSignatureParams(method.signature);
    const bodyEntries = parseDictFromBlock(method.block, 'body').concat(parseDictAssignments(method.block, 'body'));
    const { mappings, syntheticParams } = resolveDictEntries(bodyEntries, signatureParams, method.methodName);

    if (!endpointPath) {
      console.warn(`  [warn] ${symbolName}.${method.methodName}: could not extract endpoint path`);
    }

    return {
      methodName: method.methodName,
      path: endpointPath,
      bodyMap: applyOverrides(symbolName, method.methodName, Object.fromEntries(mappings)),
      // 연속조회는 시그니처에 cts kwarg 가 있는지로 판단한다 (헤더는 클라이언트가 조립).
      supportsCts: /\bcts\b/.test(method.signature),
      params: stripInternalFields(signatureParams).concat(syntheticParams),
    };
  });
};

const toPascalCase = (camel) => camel.charAt(0).toUpperCase() + camel.slice(1);

const writeTs = (targetRelativePath, symbolName, importPath, data) => {
  const fullPath = resolveWithinRoot(workspaceRoot, targetRelativePath);
  const typeName = `${toPascalCase(symbolName.replace(/Endpoints$/, ''))}MethodName`;
  const methodNames = data.map((ep) => ep.methodName);
  const unionLiteral = methodNames.map((n) => `'${n}'`).join('\n  | ');
  const content =
    `import type { ${importPath} } from '../../core/types';\n\n` +
    `export const ${symbolName}: ${importPath}[] = ${JSON.stringify(data, null, 2)};\n\n` +
    `export type ${typeName} =\n  | ${unionLiteral};\n`;
  fs.mkdirSync(path.dirname(fullPath), { recursive: true });
  fs.writeFileSync(fullPath, content);
};

const tasks = [
  {
    sourcePath: 'packages/cluefin-openapi/src/cluefin_openapi/kis/_domestic_account.py',
    targetPath: 'packages/cluefin-openapi-ts/src/kis/metadata/domestic-account.ts',
    symbolName: 'domesticAccountEndpoints',
    kind: 'kis',
  },
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
    sourcePath: 'packages/cluefin-openapi/src/cluefin_openapi/kis/_domestic_ranking_analysis.py',
    targetPath: 'packages/cluefin-openapi-ts/src/kis/metadata/domestic-ranking-analysis.ts',
    symbolName: 'domesticRankingAnalysisEndpoints',
    kind: 'kis',
  },
  {
    sourcePath: 'packages/cluefin-openapi/src/cluefin_openapi/kis/_domestic_market_analysis.py',
    targetPath: 'packages/cluefin-openapi-ts/src/kis/metadata/domestic-market-analysis.ts',
    symbolName: 'domesticMarketAnalysisEndpoints',
    kind: 'kis',
  },
  {
    sourcePath: 'packages/cluefin-openapi/src/cluefin_openapi/kis/_domestic_issue_other.py',
    targetPath: 'packages/cluefin-openapi-ts/src/kis/metadata/domestic-issue-other.ts',
    symbolName: 'domesticIssueOtherEndpoints',
    kind: 'kis',
  },
  {
    sourcePath: 'packages/cluefin-openapi/src/cluefin_openapi/kis/_overseas_basic_quote.py',
    targetPath: 'packages/cluefin-openapi-ts/src/kis/metadata/overseas-basic-quote.ts',
    symbolName: 'overseasBasicQuoteEndpoints',
    kind: 'kis',
  },
  {
    sourcePath: 'packages/cluefin-openapi/src/cluefin_openapi/kis/_onmarket_bond_basic_quote.py',
    targetPath: 'packages/cluefin-openapi-ts/src/kis/metadata/onmarket-bond-basic-quote.ts',
    symbolName: 'onmarketBondBasicQuoteEndpoints',
    kind: 'kis',
  },
  {
    sourcePath: 'packages/cluefin-openapi/src/cluefin_openapi/kis/_overseas_account.py',
    targetPath: 'packages/cluefin-openapi-ts/src/kis/metadata/overseas-account.ts',
    symbolName: 'overseasAccountEndpoints',
    kind: 'kis',
  },
  {
    sourcePath: 'packages/cluefin-openapi/src/cluefin_openapi/kis/_overseas_market_analysis.py',
    targetPath: 'packages/cluefin-openapi-ts/src/kis/metadata/overseas-market-analysis.ts',
    symbolName: 'overseasMarketAnalysisEndpoints',
    kind: 'kis',
  },
  {
    sourcePath: 'packages/cluefin-openapi/src/cluefin_openapi/kiwoom/_domestic_account.py',
    targetPath: 'packages/cluefin-openapi-ts/src/kiwoom/metadata/domestic-account.ts',
    symbolName: 'domesticAccountEndpoints',
    kind: 'kiwoom',
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
  {
    sourcePath: 'packages/cluefin-openapi/src/cluefin_openapi/kiwoom/_domestic_etf.py',
    targetPath: 'packages/cluefin-openapi-ts/src/kiwoom/metadata/domestic-etf.ts',
    symbolName: 'domesticEtfEndpoints',
    kind: 'kiwoom',
  },
  {
    sourcePath: 'packages/cluefin-openapi/src/cluefin_openapi/kiwoom/_domestic_sector.py',
    targetPath: 'packages/cluefin-openapi-ts/src/kiwoom/metadata/domestic-sector.ts',
    symbolName: 'domesticSectorEndpoints',
    kind: 'kiwoom',
  },
  {
    sourcePath: 'packages/cluefin-openapi/src/cluefin_openapi/kiwoom/_domestic_theme.py',
    targetPath: 'packages/cluefin-openapi-ts/src/kiwoom/metadata/domestic-theme.ts',
    symbolName: 'domesticThemeEndpoints',
    kind: 'kiwoom',
  },
  {
    sourcePath: 'packages/cluefin-openapi/src/cluefin_openapi/kiwoom/_domestic_foreign.py',
    targetPath: 'packages/cluefin-openapi-ts/src/kiwoom/metadata/domestic-foreign.ts',
    symbolName: 'domesticForeignEndpoints',
    kind: 'kiwoom',
  },
  {
    sourcePath: 'packages/cluefin-openapi/src/cluefin_openapi/kiwoom/_domestic_market_condition.py',
    targetPath: 'packages/cluefin-openapi-ts/src/kiwoom/metadata/domestic-market-condition.ts',
    symbolName: 'domesticMarketConditionEndpoints',
    kind: 'kiwoom',
  },
  {
    sourcePath: 'packages/cluefin-openapi/src/cluefin_openapi/kiwoom/_domestic_order.py',
    targetPath: 'packages/cluefin-openapi-ts/src/kiwoom/metadata/domestic-order.ts',
    symbolName: 'domesticOrderEndpoints',
    kind: 'kiwoom',
  },
  {
    sourcePath: 'packages/cluefin-openapi/src/cluefin_openapi/nhplug/_common.py',
    targetPath: 'packages/cluefin-openapi-ts/src/nhplug/metadata/common.ts',
    symbolName: 'commonEndpoints',
    kind: 'nhplug',
  },
  {
    sourcePath: 'packages/cluefin-openapi/src/cluefin_openapi/nhplug/_krstock_order.py',
    targetPath: 'packages/cluefin-openapi-ts/src/nhplug/metadata/krstock-order.ts',
    symbolName: 'krstockOrderEndpoints',
    kind: 'nhplug',
  },
  {
    sourcePath: 'packages/cluefin-openapi/src/cluefin_openapi/nhplug/_krstock_inquiry.py',
    targetPath: 'packages/cluefin-openapi-ts/src/nhplug/metadata/krstock-inquiry.ts',
    symbolName: 'krstockInquiryEndpoints',
    kind: 'nhplug',
  },
  {
    sourcePath: 'packages/cluefin-openapi/src/cluefin_openapi/nhplug/_krstock_quote.py',
    targetPath: 'packages/cluefin-openapi-ts/src/nhplug/metadata/krstock-quote.ts',
    symbolName: 'krstockQuoteEndpoints',
    kind: 'nhplug',
  },
  {
    sourcePath: 'packages/cluefin-openapi/src/cluefin_openapi/nhplug/_overseas_stock_order.py',
    targetPath: 'packages/cluefin-openapi-ts/src/nhplug/metadata/overseas-stock-order.ts',
    symbolName: 'overseasStockOrderEndpoints',
    kind: 'nhplug',
  },
  {
    sourcePath: 'packages/cluefin-openapi/src/cluefin_openapi/nhplug/_overseas_stock_inquiry.py',
    targetPath: 'packages/cluefin-openapi-ts/src/nhplug/metadata/overseas-stock-inquiry.ts',
    symbolName: 'overseasStockInquiryEndpoints',
    kind: 'nhplug',
  },
  {
    sourcePath: 'packages/cluefin-openapi/src/cluefin_openapi/nhplug/_overseas_stock_quote.py',
    targetPath: 'packages/cluefin-openapi-ts/src/nhplug/metadata/overseas-stock-quote.ts',
    symbolName: 'overseasStockQuoteEndpoints',
    kind: 'nhplug',
  },
];

const builders = {
  kis: buildKisMetadata,
  kiwoom: buildKiwoomMetadata,
  nhplug: buildNhplugMetadata,
};

const importTypes = {
  kis: 'KisEndpointDefinition',
  kiwoom: 'KiwoomEndpointDefinition',
  nhplug: 'NhplugEndpointDefinition',
};

for (const task of tasks) {
  const data = builders[task.kind](task.sourcePath, task.symbolName);
  const importType = importTypes[task.kind];
  writeTs(task.targetPath, task.symbolName, importType, data);
  console.log(`${task.symbolName}: ${data.length}`);
}
