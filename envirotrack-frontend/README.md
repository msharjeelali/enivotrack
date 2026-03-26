# EnviroTrack Frontend

Refactored from the original single-file prototype into a Vite + React + TypeScript frontend with:

- React Router based navigation
- auth provider and protected routes
- reusable UI components
- mock service layer ready to swap with real APIs
- dedicated pages for dashboard, violations, challans, warnings, cameras, vehicles, users, and settings

## Demo login

- username: `admin`
- password: `admin123`

## Run

```bash
npm install
npm run dev
```

## Notes

- The data layer is currently mock-backed.
- Replace files in `src/services/api` with real backend calls once your API contracts are ready.
- The UI structure aligns with the EnviroTrack report's admin dashboard scope.
