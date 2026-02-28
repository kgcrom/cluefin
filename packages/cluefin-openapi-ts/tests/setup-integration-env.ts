import { loadProjectRootEnv } from './setup-env';

loadProjectRootEnv(process.env, {
  envFiles: ['.env.test', '.env'],
});
