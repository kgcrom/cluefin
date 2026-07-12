export interface Logger {
  debug(message: string, context?: Record<string, unknown>): void;
  warn(message: string, context?: Record<string, unknown>): void;
  error(message: string, context?: Record<string, unknown>): void;
}

export const consoleLogger: Logger = {
  debug: (message, context) => {
    console.debug(message, context ?? '');
  },
  warn: (message, context) => {
    console.warn(message, context ?? '');
  },
  error: (message, context) => {
    console.error(message, context ?? '');
  },
};

export const silentLogger: Logger = {
  debug: () => undefined,
  warn: () => undefined,
  error: () => undefined,
};
