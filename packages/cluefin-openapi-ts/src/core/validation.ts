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

// NH PLUG 응답 봉투. 스펙(자산군 openapi.json)은 `message` 블록을 명세하지만 실서버는
// null 을 내려주고 `rsp_cd`/`rsp_msg` 로 응답하므로 셋 다 optional 로 둔다.
// `Output_0`, `Output_1`… 블록은 API 마다 객체/배열이 달라 passthrough 로 통과시킨다.
export const nhplugEnvelopeSchema = z
  .object({
    rsp_cd: z.string().optional(),
    rsp_msg: z.string().optional(),
    message: z.unknown().optional(),
  })
  .passthrough();
