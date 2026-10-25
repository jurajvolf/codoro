# Codoro Interface System

Codoro keeps its recognizable world: mineral light surfaces, forest emerald accents, rolling green hills, the Codo mascot, and a hands-on Python studio. The visual direction is a careful refinement of this identity, with clearer hierarchy, steadier spacing, quieter borders, and touch-first navigation on phones.

## Visual foundation

- **Canvas:** pale mineral green (`#F3F7F5`) with white working surfaces.
- **Brand:** Codoro emerald (`#008767`) and deeper hover/pressed states; use mint as a supporting surface, not as a competing accent.
- **Ink:** forest charcoal (`#111C18`), readable secondary green-gray (`#4B5E57`), and restrained muted text (`#788B83`).
- **Dark theme:** deep forest (`#0D1512`) with lifted evergreen surfaces, clear borders, and luminous emerald accents.
- **Typography:** Plus Jakarta Sans for headings and Inter for interface text; JetBrains Mono for code and aligned numeric values.
- **Radii:** 8px controls, 12px nested elements, 16–20px principal surfaces, and pills only for compact controls or status.
- **Elevation:** subtle, short shadows for layered surfaces. Avoid stacked, oversized shadows and decorative gradients.

## Product expression

- Keep the landscape, existing Codoro and Codo assets, and the familiar page structure.
- Let the learning map, real Python editor, test feedback, Socratic Codo guidance, Doros, and classroom quests carry the product story.
- Keep teaching controls and student progress information legible and calm. Use emerald for the next action and completed learning states.
- Preserve existing Slovak and English content, routes, and workflows.
- Give phones a compact top bar and a four-item student navigation dock. Reflow the learning map into a readable vertical itinerary instead of shrinking the desktop zigzag.

## Interaction and accessibility

- Use 80ms feedback, 150ms control transitions, and 250–350ms panel transitions with an exponential ease-out curve. Name the properties being animated; never use `transition: all`.
- Make controls at least 40px on desktop and 44px on touch screens. Keep keyboard focus visible and preserve the platform's browser, keyboard, and screen-reader behavior.
- Maintain WCAG AA contrast for text and controls, balanced display wrapping, and a comfortable reading measure.
- Respect `prefers-reduced-motion`; reserve movement for clear feedback and spatial continuity.
- Keep numeric totals tabular and code in a consistent monospace face.

## Source of truth

`static/css/codoro.css` contains the existing component system. `static/css/codoro-polish.css` contains focused refinements and responsive presentation rules. Keep new styles in that layer unless a component needs structural markup or behavior changes.
