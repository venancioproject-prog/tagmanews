---
name: Tagma Editorial
colors:
  surface: '#fcf9f8'
  surface-dim: '#dcd9d9'
  surface-bright: '#fcf9f8'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f6f3f2'
  surface-container: '#f0eded'
  surface-container-high: '#eae7e7'
  surface-container-highest: '#e5e2e1'
  on-surface: '#1c1b1b'
  on-surface-variant: '#414940'
  inverse-surface: '#313030'
  inverse-on-surface: '#f3f0ef'
  outline: '#727970'
  outline-variant: '#c1c9be'
  surface-tint: '#3a6840'
  primary: '#001c06'
  on-primary: '#ffffff'
  primary-container: '#003311'
  on-primary-container: '#6d9e71'
  inverse-primary: '#a0d3a2'
  secondary: '#934b00'
  on-secondary: '#ffffff'
  secondary-container: '#fd9337'
  on-secondary-container: '#683300'
  tertiary: '#320417'
  on-tertiary: '#ffffff'
  tertiary-container: '#4c192c'
  on-tertiary-container: '#c57e93'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#bbf0bd'
  primary-fixed-dim: '#a0d3a2'
  on-primary-fixed: '#002109'
  on-primary-fixed-variant: '#21502b'
  secondary-fixed: '#ffdcc4'
  secondary-fixed-dim: '#ffb781'
  on-secondary-fixed: '#301400'
  on-secondary-fixed-variant: '#703800'
  tertiary-fixed: '#ffd9e2'
  tertiary-fixed-dim: '#ffb1c7'
  on-tertiary-fixed: '#38091c'
  on-tertiary-fixed-variant: '#6e3448'
  background: '#fcf9f8'
  on-background: '#1c1b1b'
  surface-variant: '#e5e2e1'
  editorial-green-deep: '#003311'
  editorial-green-muted: '#004d1a'
  surface-off-white: '#fcfcfc'
  section-culture: '#c36'
  section-tech: '#0693e3'
  section-finance: '#fcb900'
  border-subtle: '#e0e0e0'
typography:
  headline-xl:
    fontFamily: Hanken Grotesk
    fontSize: 64px
    fontWeight: '800'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Hanken Grotesk
    fontSize: 42px
    fontWeight: '700'
    lineHeight: '1.2'
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Hanken Grotesk
    fontSize: 32px
    fontWeight: '700'
    lineHeight: '1.2'
  headline-sm:
    fontFamily: Hanken Grotesk
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.3'
  body-lg:
    fontFamily: Literata
    fontSize: 20px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Literata
    fontSize: 17px
    fontWeight: '400'
    lineHeight: '1.6'
  body-sm:
    fontFamily: Literata
    fontSize: 14px
    fontWeight: '400'
    lineHeight: '1.5'
  label-bold:
    fontFamily: IBM Plex Sans
    fontSize: 12px
    fontWeight: '700'
    lineHeight: '1'
    letterSpacing: 0.05em
  meta:
    fontFamily: IBM Plex Sans
    fontSize: 13px
    fontWeight: '400'
    lineHeight: '1.4'
spacing:
  container-max: 1280px
  gutter: 32px
  margin-mobile: 16px
  stack-sm: 8px
  stack-md: 24px
  stack-lg: 48px
  stack-xl: 80px
---

## Brand & Style

This design system is built for an authoritative news portal that balances traditional journalistic integrity with modern digital consumption. The brand personality is **sober, robust, and intellectual**, designed to evoke a sense of deep-dive reporting and institutional trust.

The visual style follows a **Corporate Minimalism** approach with **Brutalist** structural undertones. It prioritizes content hierarchy through heavy-weight typography and a high-contrast palette. The interface uses sharp edges and a strict grid to reinforce a sense of order and precision, avoiding frivolous decoration in favor of functional clarity.

## Colors

The palette is anchored by "Forest Deep" (#003311), used for primary brand touchpoints, headers, and high-emphasis UI elements. This is complemented by a "Pure White" surface for maximum legibility. 

A set of semantic category colors is utilized for editorial wayfinding, allowing readers to distinguish between "Tendências" (Culture), "Notícias" (General News), and "Negócios" (Finance) through subtle accent bars or category tags. Grayscale usage is disciplined: #1a1a1a for primary body text to reduce eye strain while maintaining high contrast, and #666 for secondary metadata.

## Typography

The typography system uses a pairing of a robust neo-grotesque for impact and a modern serif for long-form reading. 

- **Headlines:** Hanken Grotesk provides a technical, authoritative "newsroom" feel. Use the ExtraBold weight for main headlines to establish a strong visual anchor.
- **Body:** Literata is used for all article content. It is optimized for screen reading with generous x-heights and open counters, ensuring comfort during extended reading sessions.
- **Labels/UI:** IBM Plex Sans is utilized for navigation, timestamps, and category tags to provide a functional, systematic contrast to the editorial content.

## Layout & Spacing

This design system employs a **Fixed Grid** model for desktop to maintain editorial control over line lengths, which are critical for readability. 

- **Desktop:** 12-column grid with a 1280px max-width. Gutters are wide (32px) to provide significant breathing room between news cards.
- **Article View:** A centered 720px column for the body text to ensure an optimal 65-75 characters per line.
- **Rhythm:** Vertical spacing follows a strict "Stack" scale. Use `stack-lg` to separate major sections (e.g., "Trending" vs "Latest News") and `stack-md` for elements within a single module.

## Elevation & Depth

To maintain a "flat" journalistic aesthetic, this design system avoids traditional shadows. Depth is conveyed through **Tonal Layers** and **Border Work**:

- **Primary Surface:** White (#FFFFFF).
- **Secondary Surface:** Off-white (#FCFCFC) used for sidebars or "read next" modules to create subtle separation.
- **Separators:** 1px solid lines (#E0E0E0) are the primary tool for defining content boundaries.
- **Interaction:** No elevation increase on hover; instead, use a subtle background tint change or a 2px color-accented border-bottom to indicate interactivity.

## Shapes

The shape language is strictly **Sharp (0px)**. 

All buttons, image containers, input fields, and article cards utilize 90-degree corners. This reflects the "Tagma" logotype's blocky, stable nature and mimics the traditional cut of physical broadsheet newspapers. Circular shapes are only permitted for user avatars to distinguish human elements from content elements.

## Components

- **Buttons:** Sharp-edged, solid "Forest Deep" background with white text for primary actions. Ghost buttons with 1px borders are used for secondary navigation.
- **Article Cards:** No borders or shadows. Titles are placed directly above or below images with a `stack-sm` gap. Metadata (Author/Date) uses the `meta` typography token in #666.
- **Category Chips:** Rectangular tags with a 1px border or solid light-gray background. Each chip uses a small vertical 4px bar of the semantic category color on its left edge.
- **Inputs:** Minimalist bottom-border only or a full 1px border in #666. Focus state changes the border to "Forest Deep" and adds a 1px inner stroke.
- **News Ticker:** A full-width bar at the top of the viewport using a "Forest Deep" background and white typography for breaking news notifications.