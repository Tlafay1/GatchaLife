# Collection View Fixes - Round 2

I have addressed the runtime error and further refined the Collection view.

## Fixes Implemented

1.  **Runtime Error Fix**:
    *   Changed `<SelectItem value="">` to `<SelectItem value="all">` in all dropdowns. The `reka-ui` library (used by `shadcn-vue`) requires non-empty string values for items.
    *   Updated the `filters` ref to default to `'all'` instead of `''`.

2.  **API Filtering Logic**:
    *   Implemented a computed property `apiFilters` that automatically transforms `'all'` values back to `''` (empty string) before sending them to the API. This ensures the backend receives the correct query parameters (e.g., `?rarity=` instead of `?rarity=all`), satisfying the user's requirement to "remove the string from the parameter".

## Verification
- **Linting**: Passed.
- **Type Check**: Passed.
- **Build**: Passed.
