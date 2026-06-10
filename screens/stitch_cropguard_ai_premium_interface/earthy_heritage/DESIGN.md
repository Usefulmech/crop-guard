---
name: Earthy Heritage
colors:
  surface: '#fef9ef'
  surface-dim: '#dedad0'
  surface-bright: '#fef9ef'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f8f3e9'
  surface-container: '#f2ede3'
  surface-container-high: '#ede8de'
  surface-container-highest: '#e7e2d8'
  on-surface: '#1d1c16'
  on-surface-variant: '#41493f'
  inverse-surface: '#32302a'
  inverse-on-surface: '#f5f0e6'
  outline: '#72796e'
  outline-variant: '#c1c9bc'
  surface-tint: '#366935'
  primary: '#114616'
  on-primary: '#ffffff'
  primary-container: '#2b5e2b'
  on-primary-container: '#9dd696'
  inverse-primary: '#9cd595'
  secondary: '#7d562d'
  on-secondary: '#ffffff'
  secondary-container: '#ffca98'
  on-secondary-container: '#7a532a'
  tertiary: '#2e4300'
  on-tertiary: '#ffffff'
  tertiary-container: '#415c00'
  on-tertiary-container: '#aed563'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#b7f1af'
  primary-fixed-dim: '#9cd595'
  on-primary-fixed: '#002204'
  on-primary-fixed-variant: '#1e5120'
  secondary-fixed: '#ffdcbd'
  secondary-fixed-dim: '#f0bd8b'
  on-secondary-fixed: '#2c1600'
  on-secondary-fixed-variant: '#623f18'
  tertiary-fixed: '#c8f17a'
  tertiary-fixed-dim: '#add461'
  on-tertiary-fixed: '#131f00'
  on-tertiary-fixed-variant: '#364e00'
  background: '#fef9ef'
  on-background: '#1d1c16'
  surface-variant: '#e7e2d8'
typography:
  display-lg:
    fontFamily: Playfair Display
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Playfair Display
    fontSize: 32px
    fontWeight: '700'
    lineHeight: '1.2'
  headline-lg-mobile:
    fontFamily: Playfair Display
    fontSize: 28px
    fontWeight: '700'
    lineHeight: '1.2'
  headline-md:
    fontFamily: Playfair Display
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.3'
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.5'
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: '1.2'
rounded:
  sm: 0.5rem
  DEFAULT: 1rem
  md: 1.5rem
  lg: 2rem
  xl: 3rem
  full: 9999px
spacing:
  unit: 8px
  container-padding-mobile: 20px
  container-padding-desktop: 40px
  gutter: 16px
  stack-sm: 8px
  stack-md: 16px
  stack-lg: 32px
---

## Brand & Style

The design system is built for a friendly, localized agricultural companion. It prioritizes a "human-to-earth" connection, moving away from sterile medical aesthetics toward a warm, artisanal, and bespoke feel. The brand personality is knowledgeable yet approachable—like a seasoned gardener offering advice over a fence.

The visual style is **Soft-Organic Minimalism**. It utilizes heavy roundedness and a warm, cream-based palette to reduce the anxiety associated with plant disease. While the core is clean and professional, tactile details like dashed borders and terracotta accents provide a "handmade" quality that feels trustworthy and community-oriented.

## Colors

The color palette is derived from natural landscapes and traditional pottery.
- **Deep Green (Primary):** Representing healthy foliage and growth. Used for high-emphasis actions and navigation.
- **Terracotta (Secondary):** Evoking clay pots and sun-drenched earth. Used for accents, highlights, and specialized "care" notifications.
- **Cream (Background):** A softer alternative to pure white that reduces eye strain in outdoor settings and enhances the organic feel.
- **Olive (Tertiary):** Used for success states and secondary vegetation-related iconography.
- **Surface White:** Reserved for cards and interactive containers to ensure legibility and depth against the cream background.

## Typography

This design system uses a high-contrast typographic pairing to balance authority with utility.
- **Headlines (Playfair Display):** These bring an editorial, "bespoke" quality to the app. They should be used for page titles and section headers to evoke the feeling of a high-quality botanical journal.
- **Body & UI (Inter):** A neutral, highly legible sans-serif ensures that diagnostic data and instructions are crystal clear, even in bright sunlight.
- **Scale:** Larger line heights (1.5 - 1.6) are utilized for body text to ensure a comfortable reading experience for users who may be multitasking in a garden or field.

## Layout & Spacing

The layout philosophy follows a **Fluid-Fixed Hybrid** model. The main content is contained within a max-width of 1200px on desktop to maintain readability, while expanding to full width on mobile devices.

- **Spacing Rhythm:** Based on an 8px grid to ensure mathematical harmony.
- **Safe Areas:** Generous 20px margins on mobile prevent content from feeling cramped against the screen edges.
- **Reflow:** Cards should stack vertically on mobile and transition to a 2 or 3-column grid on tablet/desktop. 
- **Grouping:** Use the `stack-lg` (32px) for separating distinct sections and `stack-sm` (8px) for associating labels with input fields.

## Elevation & Depth

To maintain a soft and inviting atmosphere, this design system avoids heavy shadows. Depth is communicated through:
- **Tonal Layering:** Using the Cream background as the base, and White for "interactive" or "foreground" elements like cards and modals.
- **Soft Outlines:** Containers use 1px solid borders in a slightly darker cream or muted green (#E5E0D6) rather than harsh drop shadows.
- **Focused Elevation:** Only the primary action buttons and active modals may use a very subtle, low-opacity ambient shadow (Blur: 10px, Y: 4px, Color: Primary with 5% opacity) to signify they are "above" the organic surface.

## Shapes

The shape language is the defining characteristic of this design system. It uses an **extra-round** approach to feel safe and approachable.
- **Core Elements:** Buttons, cards, and input fields all utilize a baseline 24px (1.5rem) corner radius.
- **Small Elements:** Chips and tags should be fully pill-shaped (rounded-full).
- **Specialized States:** Upload zones and "empty state" containers use a dashed border with the same 24px radius to indicate an "active" or "awaiting" area for user input.

## Components

- **Primary Buttons:** High-contrast White text on Deep Green backgrounds. Always fully rounded or 24px.
- **Secondary Buttons:** Deep Green text on a transparent background with a 2px Deep Green border.
- **Cards:** White surface, 1px soft border, 24px corner radius. Used for diagnosis results and plant profiles.
- **Upload Zones:** Large, dashed-border containers in Terracotta or Muted Green. The dashed pattern should have a 4px dash and 4px gap.
- **Chips/Badges:** Small, pill-shaped markers in Terracotta for "Alerts" and Green for "Healthy" status.
- **Input Fields:** 24px rounded, White background, subtle border. Focus states should use a 2px Deep Green ring.
- **Diagnosis Progress:** Use a custom "growing" progress bar—a thicker, rounded track in light green with the primary green filling it.
- **Iconography:** Use "monoline" or "hand-drawn" style icons with rounded ends to match the soft typography and shapes.