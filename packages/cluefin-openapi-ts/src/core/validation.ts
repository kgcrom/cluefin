import { z } from 'zod';

import type { EndpointParamDefinition } from './types';

const flexibleScalar = z.union([z.string(), z.number(), z.boolean()]);

export const createInputSchema = (
  params: readonly EndpointParamDefinition[],
): z.ZodObject<Record<string, z.ZodTypeAny>> => {
  const shape: Record<string, z.ZodTypeAny> = {};

  for (const definition of params) {
    let schema: z.ZodTypeAny = flexibleScalar;
    if (definition.defaultValue !== undefined) {
      schema = schema.optional().default(definition.defaultValue);
    } else if (!definition.required) {
      schema = schema.optional();
    }
    shape[definition.name] = schema;
  }

  return z.object(shape).strict();
};

export const kisEnvelopeSchema = z
  .object({
    rt_cd: z.union([z.string(), z.number()]).optional(),
    msg_cd: z.string().optional(),
    msg1: z.string().optional(),
  })
  .passthrough();

export const kiwoomEnvelopeSchema = z
  .object({
    return_code: z.union([z.string(), z.number()]).optional(),
    return_msg: z.string().optional(),
  })
  .passthrough();
