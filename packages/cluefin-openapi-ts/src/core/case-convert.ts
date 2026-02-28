import type { JsonArray, JsonObject } from './types';

const CAMEL_SEGMENT = /[-_]+([a-zA-Z0-9])/g;

export const toCamelCase = (value: string): string => {
  if (value.length === 0) {
    return value;
  }
  return value
    .trim()
    .replace(CAMEL_SEGMENT, (_, captured: string) => captured.toUpperCase())
    .replace(/^[A-Z]/, (first) => first.toLowerCase());
};

export const toSnakeCase = (value: string): string =>
  value
    .replace(/([a-z0-9])([A-Z])/g, '$1_$2')
    .replace(/[-\s]+/g, '_')
    .toLowerCase();

const transformArray = (value: JsonArray): JsonArray => value.map((entry) => camelizeKeys(entry));

const transformObject = (value: JsonObject): JsonObject => {
  const transformed: JsonObject = {};
  for (const [rawKey, rawValue] of Object.entries(value)) {
    const nextKey = toCamelCase(rawKey);
    transformed[nextKey] = camelizeKeys(rawValue);
  }
  return transformed;
};

export const camelizeKeys = <T>(value: T): T => {
  if (Array.isArray(value)) {
    return transformArray(value as JsonArray) as T;
  }
  if (value !== null && typeof value === 'object') {
    return transformObject(value as JsonObject) as T;
  }
  return value;
};

export const normalizeHeaders = (headers: Headers): Record<string, string> => {
  const result: Record<string, string> = {};
  for (const [key, value] of headers.entries()) {
    result[toCamelCase(key)] = value;
  }
  return result;
};
