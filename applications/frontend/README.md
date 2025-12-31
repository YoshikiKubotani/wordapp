# Oboe Experiment Frontend (React + TypeScript + Vite)

Production SPA for the oboe-experiment project. Implements Cognito Hosted UI authentication (Authorization Code + PKCE), React Router-based routing, and an API client that sends Authorization: Bearer <ID token> to the FastAPI backend.

Key files:
- Routing and guards: [applications/frontend/src/app/App.tsx](applications/frontend/src/app/App.tsx)
- App bootstrap (React Router): [applications/frontend/src/app/main.tsx](applications/frontend/src/app/main.tsx)
- Cognito OAuth + token exchange + refresh: [applications/frontend/src/shared/auth/cognito-service.ts](applications/frontend/src/shared/auth/cognito-service.ts)
- PKCE utilities (S256): [applications/frontend/src/shared/auth/pkce.ts](applications/frontend/src/shared/auth/pkce.ts)
- Auth callback page: [applications/frontend/src/pages/auth/AuthCallbackPage.tsx](applications/frontend/src/pages/auth/AuthCallbackPage.tsx)
- API client with Authorization header: [applications/frontend/src/shared/api/client.ts](applications/frontend/src/shared/api/client.ts)
- Env loader and validation: [applications/frontend/src/shared/config/env.ts](applications/frontend/src/shared/config/env.ts)
- Sample env file: [applications/frontend/environments/frontend.env.sample](applications/frontend/environments/frontend.env.sample)

## Features

- React 19 + Vite 6 + TypeScript
- React Router SPA routes with protected pages
- AWS Cognito Hosted UI (Authorization Code flow + PKCE S256)
- ID token stored client-side and attached to every API request
- Simple auth state via Jotai
- TailwindCSS UI utilities

## Authentication Overview (Cognito + SPA)

- Flow: User clicks “Sign In” → Hosted UI → redirect to /auth/callback with `code` → app exchanges `code + code_verifier` for tokens.
- PKCE: A `code_verifier` is generated on login and a `code_challenge` (S256) is sent to Cognito; on callback we send the original `code_verifier` to exchange tokens.
- Tokens:
  - ID token: sent to backend in the Authorization header
  - Access/Refresh token: stored for future refresh (optional auto-refresh wiring)
- Backend accepts only ID tokens (token_use == "id").

Related code:
- Login (generates PKCE and sends code_challenge): [applications/frontend/src/shared/auth/cognito-service.ts](applications/frontend/src/shared/auth/cognito-service.ts)
- PKCE helpers: [applications/frontend/src/shared/auth/pkce.ts](applications/frontend/src/shared/auth/pkce.ts)
- Callback handler: [applications/frontend/src/pages/auth/AuthCallbackPage.tsx](applications/frontend/src/pages/auth/AuthCallbackPage.tsx)

## Environment Variables

Configure via `.env` files (Vite reads VITE_* at build time). See [applications/frontend/src/shared/config/env.ts](applications/frontend/src/shared/config/env.ts).

Required:
- VITE_API_BASE_URL: Backend API base (e.g., https://d1234abcd.cloudfront.net/api)

Auth toggle:
- VITE_ENABLE_AUTH: "true" to require Cognito sign-in; "false" for local dev bypass

Cognito (required when auth is enabled):
- VITE_COGNITO_HOSTED_UI_URL: Cognito Hosted UI domain (e.g., https://example-domain.auth.ap-northeast-1.amazoncognito.com)
- VITE_COGNITO_CLIENT_ID: Cognito App Client ID
- VITE_COGNITO_REDIRECT_URI: SPA callback (must end with /auth/callback)
- VITE_COGNITO_LOGOUT_URI: SPA logout landing URL (usually "/")

Example for local development:
```env
# .env.local
VITE_API_BASE_URL=http://localhost:8000/api

# Toggle auth
VITE_ENABLE_AUTH=false

# If enabling auth locally, set these to your pool/app client:
# VITE_ENABLE_AUTH=true
# VITE_COGNITO_HOSTED_UI_URL=https://your-domain.auth.ap-northeast-1.amazoncognito.com
# VITE_COGNITO_CLIENT_ID=your-client-id
# VITE_COGNITO_REDIRECT_URI=http://localhost:5173/auth/callback
# VITE_COGNITO_LOGOUT_URI=http://localhost:5173/
```

Example for production (CloudFront default domain):
```env
VITE_API_BASE_URL=https://<cloudfront_domain_name>/api
VITE_ENABLE_AUTH=true
VITE_COGNITO_HOSTED_UI_URL=https://<your_pool>.auth.ap-northeast-1.amazoncognito.com
VITE_COGNITO_CLIENT_ID=<app_client_id>
VITE_COGNITO_REDIRECT_URI=https://<cloudfront_domain_name>/auth/callback
VITE_COGNITO_LOGOUT_URI=https://<cloudfront_domain_name>/
```

A sample is provided at:
- [applications/frontend/environments/frontend.env.sample](applications/frontend/environments/frontend.env.sample)

## Quick Start

1) Install dependencies
```bash
cd applications/frontend
yarn install
```

2) Configure env
- Create `.env.local` as shown above.

3) Run dev server
```bash
yarn dev
# Visit http://localhost:5173
```

4) Build and preview
```bash
yarn build
yarn preview
```

## Routing

- React Router is initialized in [applications/frontend/src/app/main.tsx](applications/frontend/src/app/main.tsx).
- Route configuration and guards live in [applications/frontend/src/app/App.tsx](applications/frontend/src/app/App.tsx).
- Auth callback route is handled at `/auth/callback` by [applications/frontend/src/pages/auth/AuthCallbackPage.tsx](applications/frontend/src/pages/auth/AuthCallbackPage.tsx).

When `VITE_ENABLE_AUTH=true`, protected routes redirect unauthenticated users to the Hosted UI login.

## API Client and Authorization Header

All outbound requests to the backend API use the Authorization header with the ID token when authentication is enabled.

- Implementation: [applications/frontend/src/shared/api/client.ts](applications/frontend/src/shared/api/client.ts)

The same header is also applied to streaming/SSE endpoints to support authenticated streams.

## Local Development Modes

- With Auth disabled (`VITE_ENABLE_AUTH=false`):
  - The app simulates a local user and does not perform Cognito login.
  - Backend may also be configured to bypass auth (ENABLE_AUTH=false) for end-to-end local testing.

- With Auth enabled (`VITE_ENABLE_AUTH=true`):
  - You must configure Hosted UI URL, Client ID, Redirect and Logout URIs.
  - Ensure the Cognito App Client’s allowed callback/logout URLs include your local values.

## Deployment Notes

- The SPA is hosted on S3 behind CloudFront. No custom domain is required (default CloudFront domain works).
- Cognito callback must be `/auth/callback` (already wired in the app). Ensure the User Pool App Client settings and Terraform match this path.

See project-wide deployment docs:
- [DEPLOYMENT.md](DEPLOYMENT.md)
- [AWS_ARCHITECTURE.md](AWS_ARCHITECTURE.md)
- Infra overview: [infra/README.md](infra/README.md)

## Troubleshooting

- TypeScript “Cannot find module 'react' or 'jotai'” in editors:
  - Run `yarn install` to get node_modules; build will succeed with dependencies present.
- 401 Unauthorized from API:
  - Verify the Authorization header is present (check devtools), and that `VITE_ENABLE_AUTH` is set as expected.
  - When auth is enabled, confirm Cognito callback/logout URIs exactly match the SPA’s origin and path.
- Callback loop:
  - Ensure `/auth/callback` is registered in Cognito App Client and that `VITE_COGNITO_REDIRECT_URI` matches exactly.
- CORS:
  - Confirm backend CORS includes the SPA origin and that CloudFront forwards Authorization headers for `/api/*`.

## Scripts

From [applications/frontend/package.json](applications/frontend/package.json):
- `yarn dev` — Start Vite dev server
- `yarn build` — Type-check and build production bundle
- `yarn preview` — Preview production build
- `yarn lint` / `yarn format` — Linting and formatting

## Project Structure

```
applications/frontend/
├── src/
│   ├── app/
│   │   ├── App.tsx                 # SPA routes + guards
│   │   └── main.tsx                # App bootstrap (React Router)
│   │
│   ├── pages/
│   │   └── auth/
│   │       ├── index.ts            # Auth pages barrel
│   │       └── AuthCallbackPage.tsx# Cognito callback: code → tokens (PKCE)
│   │
│   └── shared/
│       ├── api/
│       │   └── client.ts           # API client (adds Authorization: Bearer <ID token>)
│       │
│       ├── auth/
│       │   ├── cognito-service.ts  # OAuth endpoints: authorize/token/refresh
│       │   └── pkce.ts             # PKCE helpers (code_verifier/challenge storage)
│       │
│       └── config/
│           └── env.ts              # VITE_* env loader and validation
│
├── environments/
│   └── frontend.env.sample         # Sample VITE_* configuration
│
└── package.json
```

Key implementation files:
- Routing and guards: [applications/frontend/src/app/App.tsx](applications/frontend/src/app/App.tsx)
- React Router bootstrap: [applications/frontend/src/app/main.tsx](applications/frontend/src/app/main.tsx)
- Cognito OAuth + token exchange + refresh: [applications/frontend/src/shared/auth/cognito-service.ts](applications/frontend/src/shared/auth/cognito-service.ts)
- PKCE utilities (S256): [applications/frontend/src/shared/auth/pkce.ts](applications/frontend/src/shared/auth/pkce.ts)
- Auth callback page: [applications/frontend/src/pages/auth/AuthCallbackPage.tsx](applications/frontend/src/pages/auth/AuthCallbackPage.tsx)
- API client with Authorization header: [applications/frontend/src/shared/api/client.ts](applications/frontend/src/shared/api/client.ts)
- Env loader and validation: [applications/frontend/src/shared/config/env.ts](applications/frontend/src/shared/config/env.ts)
