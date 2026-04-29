# MODULE 4: RTL Support & Directionality
## Week 1 - Day 4

### Objectives
- Implement RTL (Right-to-Left) language support
- Handle text directionality at document level
- Adjust layout and components for RTL languages
- Ensure visual consistency across directions

### Key Concepts

#### 1. Locale Direction Helpers
```typescript
// Determine text direction from locale
function getLocaleDirection(locale: string): 'ltr' | 'rtl' {
  const rtlLocales = ['ar', 'ar-AE', 'ar-SA', 'he', 'fa', 'ur'];
  return rtlLocales.includes(locale) ? 'rtl' : 'ltr';
}

// Get margin/padding values based on direction
function getResponsiveMargin(direction: 'ltr' | 'rtl', size: number) {
  if (direction === 'rtl') {
    return { marginRight: size };
  }
  return { marginLeft: size };
}

// Slide direction for animations
function getSlideDirection(direction: 'ltr' | 'rtl'): 'left' | 'right' {
  return direction === 'rtl' ? 'left' : 'right';
}
```

#### 2. Document Direction Setup
```typescript
// app/src/app/layout.tsx
export default function RootLayout({
  children,
  params: { locale },
}: {
  children: React.ReactNode;
  params: { locale: string };
}) {
  const direction = getLocaleDirection(locale);
  
  return (
    <html lang={locale} dir={direction}>
      <body>{children}</body>
    </html>
  );
}
```

#### 3. Component RTL Support
```typescript
// Mobile menu with RTL-safe slide direction
interface MobileMenuProps {
  isOpen: boolean;
  locale: string;
}

export function MobileMenu({ isOpen, locale }: MobileMenuProps) {
  const direction = getLocaleDirection(locale);
  const slideFrom = direction === 'rtl' ? 'right' : 'left';
  
  return (
    <motion.div
      initial={{ x: slideFrom === 'left' ? '-100%' : '100%' }}
      animate={{ x: isOpen ? 0 : (slideFrom === 'left' ? '-100%' : '100%') }}
      transition={{ duration: 0.3 }}
    >
      {/* Menu content */}
    </motion.div>
  );
}
```

### RTL Best Practices

1. **Use logical CSS properties** (margin-inline instead of margin-left)
2. **Never hardcode left/right** - use helpers
3. **Test with RTL languages** (Arabic, Hebrew, Farsi)
4. **Mirror images** where appropriate
5. **Check text alignment** in labels and headings

### Implementation Tasks

1. **Create direction helpers** utility functions
2. **Update root layout** to set document direction
3. **Refactor components** to use RTL-safe properties
4. **Update mobile menu** with direction-aware animations
5. **Add RTL tests** for all locale combinations

### Deliverables
- [ ] Direction helper functions
- [ ] Root layout with dir attribute
- [ ] RTL-compliant component examples
- [ ] Mobile menu RTL implementation
- [ ] RTL test cases

### Languages to Support
- Arabic (ar)
- Hebrew (he)
- Farsi/Persian (fa)
- Urdu (ur)
- Any others based on business needs

---
**Duration**: 3-4 hours | **Difficulty**: Intermediate
