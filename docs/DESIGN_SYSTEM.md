# Frontend Design System
## Smart Matter Opportunity Detector

**Version:** 1.0
**Last Updated:** November 4, 2025
**Framework:** React + shadcn/ui + Tailwind CSS

---

## Overview

This design system ensures consistency, accessibility, and maintainability across the frontend application. All components must follow these guidelines.

---

## Core Principles

### 1. Component Standards
- ✅ **Use ONLY shadcn/ui components** - No custom component libraries
- ✅ **Import pattern:** `import { Component } from '@/components/ui/component'`
- ✅ **Composition over creation** - Build complex UIs from shadcn primitives

### 2. Styling Standards
- ✅ **Tailwind utility classes ONLY** - No custom CSS files or styled-components
- ✅ **No inline styles** - Use Tailwind classes exclusively
- ✅ **No CSS modules** - Keep styling declarative with utilities

---

## Spacing System

### Consistent Spacing Scale

```typescript
// Card/Container padding
className="p-6"

// Section gaps
className="gap-4"    // Small gaps
className="gap-6"    // Medium gaps

// Form field spacing
className="space-y-4"

// Section margins
className="mb-4"     // Small margin
className="mb-6"     // Medium margin
className="mb-8"     // Large margin

// Flex/Grid gaps
className="gap-4"    // Default gap
className="gap-2"    // Tight gap for badges/small items
```

---

## Typography System

### Text Sizes

```typescript
// Labels
className="text-sm font-medium"

// Body text
className="text-base"

// Descriptions
className="text-sm text-muted-foreground"

// Headings
className="text-lg font-semibold"   // Card titles
className="text-xl font-bold"       // Section headings
className="text-3xl font-bold"      // Page headings
```

### Font Weights

```typescript
font-medium      // Labels (400-500)
font-semibold    // Subheadings (600)
font-bold        // Main headings (700)
```

---

## Color System

### Theme Colors (CSS Variables)

**NEVER use hardcoded colors like `bg-gray-50` or `text-black`**

#### Backgrounds
```typescript
bg-background      // Main app background
bg-card            // Card/panel backgrounds
bg-muted           // Subtle backgrounds (disabled, placeholders)
bg-popover         // Popover/dropdown backgrounds
```

#### Text Colors
```typescript
text-foreground             // Primary text
text-muted-foreground       // Secondary/helper text
text-card-foreground        // Text on cards
text-popover-foreground     // Text in popovers
```

#### Accent Colors
```typescript
bg-primary         // Primary buttons, main actions
bg-secondary       // Secondary actions
bg-accent          // Hover states, highlights
bg-destructive     // Errors, delete actions
```

#### Borders
```typescript
border-border      // Standard borders
border-input       // Input field borders
```

### Dark Mode Support

All components must support dark mode using `dark:` variants:

```typescript
// ✅ CORRECT - Theme-aware
className="bg-card text-foreground dark:bg-gray-800"

// ✅ CORRECT - Using semantic colors
className="bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200"

// ❌ WRONG - Hardcoded without dark mode
className="bg-white text-black"
```

### Accessibility

- Maintain **WCAG AA standards** (4.5:1 contrast ratio minimum)
- Test with dark mode enabled
- Use semantic color names for meaning

---

## Layout Patterns

### Responsive Design (Mobile-First)

```typescript
// Breakpoints
// Mobile:  Default (no prefix)
// Tablet:  md: (768px+)
// Desktop: lg: (1024px+)
// Wide:    xl: (1280px+)

// ✅ CORRECT - Mobile-first
className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3"

// ✅ CORRECT - Responsive flex
className="flex flex-col md:flex-row"
```

### Container Pattern

```typescript
// Standard container
className="max-w-7xl mx-auto px-4"

// With vertical spacing
className="max-w-7xl mx-auto px-4 py-8"
```

### Grid Layouts

```typescript
// Responsive grid
className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"

// Fixed columns
className="grid grid-cols-3 gap-4"
```

### Flex Patterns

```typescript
// Horizontal layout with gap
className="flex items-center gap-4"

// Space between
className="flex items-center justify-between gap-4"

// Vertical stack
className="flex flex-col gap-4"

// Wrap support
className="flex flex-wrap gap-2"
```

---

## UI/UX Principles

### Visual Consistency

#### Border Radius
```typescript
rounded-lg     // Cards, panels (8px)
rounded-md     // Inputs, buttons (6px)
rounded-full   // Badges, avatars (9999px)
```

#### Shadows
```typescript
shadow         // Subtle shadow
shadow-md      // Medium shadow
shadow-lg      // Prominent shadow (for hover states)
```

#### Transitions
```typescript
// Smooth color transitions
className="transition-colors duration-200"

// All properties
className="transition-all duration-200"

// Scale effects
className="transition-transform hover:scale-105"
```

### Interactive States

#### Hover States
```typescript
hover:bg-accent        // Background change
hover:opacity-80       // Opacity change
hover:shadow-lg        // Shadow increase
```

#### Focus States
```typescript
focus:ring-2 focus:ring-primary focus:outline-none
```

#### Active States
```typescript
active:scale-95        // Button press effect
```

#### Disabled States
```typescript
disabled:opacity-50 disabled:cursor-not-allowed
```

### Loading & Feedback States

#### Loading States
```typescript
// Use skeleton pattern
<div className="bg-card p-6 rounded-lg border border-border space-y-4">
  <div className="h-4 bg-muted rounded animate-pulse" />
  <div className="h-4 bg-muted rounded animate-pulse w-3/4" />
</div>

// Or use shadcn Skeleton component
import { Skeleton } from '@/components/ui/skeleton';
<Skeleton className="h-4 w-full" />
```

#### Error States
```typescript
// Use destructive variant
<Button variant="destructive">Delete</Button>
<Badge variant="destructive">Error</Badge>

// Error text
<p className="text-sm text-destructive">Error message</p>
```

#### Success States
```typescript
// Use toast notifications
import { toast } from '@/components/ui/use-toast';

toast({
  title: 'Success!',
  description: 'Operation completed',
});
```

#### Empty States
```typescript
<div className="text-center py-12">
  <p className="text-muted-foreground text-base">
    No items found. Get started by adding one!
  </p>
</div>
```

---

## Component Patterns

### Card Pattern
```typescript
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

<Card className="p-6">
  <CardHeader className="space-y-2">
    <CardTitle className="text-xl font-bold">Title</CardTitle>
    <CardDescription className="text-muted-foreground">
      Description text
    </CardDescription>
  </CardHeader>
  <CardContent className="space-y-4">
    {/* Content */}
  </CardContent>
</Card>
```

### Form Pattern
```typescript
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';

<form className="space-y-4">
  <div className="space-y-2">
    <Label htmlFor="field" className="text-sm font-medium">
      Field Label
    </Label>
    <Input
      id="field"
      className="w-full"
      placeholder="Placeholder text"
    />
  </div>

  <Button type="submit" className="w-full md:w-auto">
    Submit
  </Button>
</form>
```

### Button Patterns
```typescript
import { Button } from '@/components/ui/button';

// Variants
<Button variant="default">Primary Action</Button>
<Button variant="secondary">Secondary Action</Button>
<Button variant="destructive">Delete</Button>
<Button variant="outline">Cancel</Button>
<Button variant="ghost">Subtle Action</Button>

// Sizes
<Button size="sm">Small</Button>
<Button size="default">Default</Button>
<Button size="lg">Large</Button>
<Button size="icon"><Icon /></Button>

// States
<Button disabled>Disabled</Button>
<Button className="w-full">Full Width</Button>
<Button className="w-full md:w-auto">Responsive Width</Button>
```

### Badge Patterns
```typescript
import { Badge } from '@/components/ui/badge';

// Variants
<Badge variant="default">Default</Badge>
<Badge variant="secondary">Secondary</Badge>
<Badge variant="destructive">Error</Badge>
<Badge variant="outline">Outline</Badge>

// Custom colors (with dark mode)
<Badge className="bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200">
  Custom
</Badge>
```

### Dialog/Modal Pattern
```typescript
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';

<Dialog>
  <DialogTrigger asChild>
    <Button>Open Dialog</Button>
  </DialogTrigger>
  <DialogContent className="max-w-2xl">
    <DialogHeader>
      <DialogTitle className="text-xl font-bold">Dialog Title</DialogTitle>
      <DialogDescription className="text-muted-foreground">
        Dialog description
      </DialogDescription>
    </DialogHeader>
    <div className="space-y-4">
      {/* Dialog content */}
    </div>
  </DialogContent>
</Dialog>
```

---

## Component Checklist

Before submitting any component, verify:

- [ ] ✅ Uses ONLY shadcn/ui components
- [ ] ✅ Uses ONLY Tailwind utility classes (no custom CSS)
- [ ] ✅ Uses theme color variables (no hardcoded colors)
- [ ] ✅ Includes dark mode variants for colors
- [ ] ✅ Follows spacing system (`p-6`, `gap-4`, `space-y-4`)
- [ ] ✅ Follows typography scale (`text-sm`, `font-medium`, etc.)
- [ ] ✅ Mobile-first responsive design
- [ ] ✅ Includes hover/focus states
- [ ] ✅ Includes loading state (if applicable)
- [ ] ✅ Includes empty state (if applicable)
- [ ] ✅ Includes error state (if applicable)
- [ ] ✅ Maintains WCAG AA accessibility
- [ ] ✅ Uses semantic HTML elements
- [ ] ✅ Consistent border radius (`rounded-lg`, `rounded-md`)
- [ ] ✅ Smooth transitions (`transition-colors duration-200`)

---

## Anti-Patterns (DO NOT USE)

### ❌ Hardcoded Colors
```typescript
// ❌ WRONG
className="bg-white text-black"
className="bg-gray-50 border-gray-200"

// ✅ CORRECT
className="bg-card text-foreground"
className="bg-background border-border"
```

### ❌ Custom CSS
```typescript
// ❌ WRONG
<div style={{ backgroundColor: '#fff', padding: '24px' }}>

// ✅ CORRECT
<div className="bg-card p-6">
```

### ❌ Non-shadcn Components
```typescript
// ❌ WRONG
import Button from 'react-bootstrap/Button';
import { Button } from '@mui/material';

// ✅ CORRECT
import { Button } from '@/components/ui/button';
```

### ❌ Inconsistent Spacing
```typescript
// ❌ WRONG - Random spacing values
className="p-5 gap-3 mb-7"

// ✅ CORRECT - System values
className="p-6 gap-4 mb-8"
```

### ❌ Missing Dark Mode
```typescript
// ❌ WRONG
className="bg-blue-100 text-blue-800"

// ✅ CORRECT
className="bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200"
```

---

## Quick Reference

### Color Variables Quick Lookup
```typescript
// Backgrounds
bg-background | bg-card | bg-muted | bg-popover

// Text
text-foreground | text-muted-foreground | text-card-foreground

// Accents
bg-primary | bg-secondary | bg-accent | bg-destructive

// Borders
border-border | border-input
```

### Spacing Quick Lookup
```typescript
p-6        // Padding (cards, containers)
gap-4      // Gap between items
gap-6      // Larger gap
space-y-4  // Vertical spacing (forms)
mb-4       // Margin bottom (small)
mb-6       // Margin bottom (medium)
mb-8       // Margin bottom (large)
```

### Typography Quick Lookup
```typescript
text-sm font-medium           // Labels
text-base                     // Body
text-lg font-semibold         // Card titles
text-xl font-bold             // Section headings
text-3xl font-bold            // Page headings
text-muted-foreground         // Secondary text
```

### Responsive Quick Lookup
```typescript
// Mobile → Tablet → Desktop → Wide
md:     // 768px+
lg:     // 1024px+
xl:     // 1280px+

// Example
className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3"
```

---

## Resources

- [shadcn/ui Documentation](https://ui.shadcn.com/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [WCAG Accessibility Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)

---

**Last Updated:** November 4, 2025
**Maintained By:** Development Team
