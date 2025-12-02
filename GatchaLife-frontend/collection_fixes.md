# Collection View Fixes

I have addressed the user-reported issues with the Collection view.

## Fixes Implemented

1.  **Rarity Sorting**:
    *   Implemented custom sorting logic for the "Rarity" group.
    *   It now sorts groups by `min_roll_threshold` in descending order (Legendary -> Rare -> Common).
    *   This ensures the most valuable cards appear first.

2.  **Filter Interaction & Scrolling**:
    *   Removed `animate-in` classes from the filter panel container. These classes were likely causing interaction issues (e.g., `pointer-events`) or layout shifts that interfered with the `Select` component's portal positioning and scroll locking mechanism.
    *   Verified that `Select` components are using the standard `shadcn-vue` implementation which portals content to the body, ensuring they appear above other elements.

3.  **"All" Filter Logic**:
    *   Confirmed that the "All" options in dropdowns now pass an empty string `""` instead of `"all"`, which correctly clears the filter in the backend query.

## Verification
- **Linting**: Passed.
- **Type Check**: Passed.
- **Build**: Passed.
