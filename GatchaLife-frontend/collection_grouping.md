# Collection Filtering & Grouping Update

I have refined the collection view with advanced grouping, filtering, and UX improvements.

## Key Changes

1.  **Grouping System**:
    *   Added a "Group By" feature allowing users to organize their collection by **Series** (default), **Rarity**, **Theme**, or **Style**.
    *   Implemented visual headers for each group with card counts.
    *   Added "No Grouping" option to view a flat grid.

2.  **UX Improvements**:
    *   **Collapsible Filters**: The filter panel is now hidden by default to focus on the collection. A "Filters & Sorting" toggle button reveals it.
    *   **"All" Filter Fix**: Changed the "All" option in dropdowns to send an empty string `""` instead of `"all"`, ensuring the backend correctly ignores the filter.

3.  **Backend Updates**:
    *   Updated `CardSerializer` to include `series_name`, enabling grouping by series in the frontend.

## Technical Details

- **Frontend**:
    - Used `computed` property `groupedCollection` to dynamically restructure the data based on the selected `groupBy` key.
    - Added `series_name` to the grouping logic.
    - Used `v-if` and animations for the collapsible filter panel.
- **Backend**:
    - Added `series_name` field to `CardSerializer` in `gatchalife/gamification/serializers.py`.

## Verification
- **Linting**: Passed.
- **Type Check**: Passed.
- **Build**: Passed.
