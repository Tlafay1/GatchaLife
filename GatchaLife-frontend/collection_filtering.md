# Collection Filtering System

I have implemented a complete filtering system for the Collection view in the frontend.

## Features

1.  **Advanced Filters**:
    *   **Search**: Filter by character name (case-insensitive partial match).
    *   **Rarity**: Filter by card rarity (Common, Rare, Legendary, etc.).
    *   **Theme**: Filter by card theme (e.g., Cyberpunk, Fantasy).
    *   **Style**: Filter by art style (e.g., Chibi, Realistic).
    *   **Series**: Filter by character series.

2.  **Dynamic UI**:
    *   The filters are populated dynamically from the backend (fetching available themes, styles, series, and rarities).
    *   Used `shadcn-vue` components (`Select`, `Input`, `Button`) for a polished look.
    *   Added a "Reset Filters" button to quickly clear all selections.

3.  **Backend Support**:
    *   Updated `CollectionViewSet` in `gatchalife/gamification/views.py` to handle the new query parameters: `theme`, `style`, `series`, and `character`.

## Technical Details

- **Frontend**: Updated `CollectionList.vue` to use `useCollection` with reactive filters. Added API hooks for fetching metadata lists (`useThemesList`, etc.).
- **Backend**: Overrode `filter_queryset` in `CollectionViewSet` to apply the filters.

## Verification
- **Linting**: Passed.
- **Type Check**: Passed.
- **Build**: Passed.
