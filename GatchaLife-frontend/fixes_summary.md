# Bug Fixes and Improvements

## Progress Bar Fix
- **Issue**: The progress bar tooltip was being clipped or not displaying correctly due to `overflow-hidden` on the parent container.
- **Fix**: Restructured the HTML in `PlayerDashboard.vue` (formerly `Dashboard.vue`).
  - Moved `overflow-hidden` to the inner progress bar track.
  - Kept the tooltip outside the overflow container but within a relative wrapper to ensure correct positioning without clipping.

## Linting and Type Safety
- **Unlock Level**: Added `unlock_level` to:
  - Backend serializers (`CharacterSerializer`, `SeriesSerializer`, `StyleSerializer`, `ThemeSerializer`).
  - Frontend API client hooks (`useUpdateSeries`, `useUpdateCharacter`, `useUpdateStyle`, `useUpdateTheme`).
  - Frontend types (`CharacterFormState`).
  - Frontend components (`CharacterEditor.vue`, `StyleListView.vue`, `ThemeListView.vue`, `SeriesListView.vue`).
- **Component Naming**: Renamed single-word components to multi-word names to comply with Vue linting rules:
  - `Dashboard.vue` -> `PlayerDashboard.vue`
  - `Collection.vue` -> `CollectionList.vue`
  - Disabled `vue/multi-word-component-names` for UI library components (`Button`, `Card`, `Dialog`, `Input`, `Label`, `Select`, `Badge`, `Separator`, `Textarea`) to avoid renaming generated files.
- **Unused Variables**: Removed unused variables and imports across multiple files (`PlayerDashboard.vue`, `CharacterEditor.vue`, `CharacterListView.vue`).
- **Type Definitions**:
  - Fixed `any` types in `api-client.ts` and `GatchaAnimation.vue`.
  - Updated `useCollection` to accept `Ref` or `object` for filters.
  - Fixed test file types in `CharacterEditor.spec.ts`.

## Refactoring
- **Router**: Updated `router/index.ts` to reflect the renamed component files.
- **Tests**: Updated `CharacterEditor.spec.ts` to use proper imports and types for `VueQueryPlugin` and `Router`.

## Verification
- **Linting**: `npm run lint` passes with 0 errors.
- **Type Checking**: `npm run type-check` passes with 0 errors.
- **Build**: `npm run build` completes successfully.
