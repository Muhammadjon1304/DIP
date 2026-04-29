# MODULE 3: Frontend Rendering Parity
## Week 1 - Day 3

### Objectives
- Create single source of truth for page structure
- Ensure consistent rendering across locales
- Implement visibility controls for page sections
- Reduce duplication and maintainability issues

### Key Concepts

#### 1. Business Page Sections Structure
```typescript
interface PageSection {
  id: string;
  label: string;
  component: string;
  visibility: {
    visible: boolean;
    conditions?: string[];
  };
  order: number;
}

const BusinessPageSections: PageSection[] = [
  {
    id: 'hero',
    label: 'Hero Section',
    component: 'HeroSection',
    visibility: { visible: true },
    order: 1,
  },
  {
    id: 'about',
    label: 'About Business',
    component: 'AboutSection',
    visibility: { visible: true },
    order: 2,
  },
  {
    id: 'services',
    label: 'Services',
    component: 'ServicesSection',
    visibility: { visible: true, conditions: ['hasServices'] },
    order: 3,
  },
  // ... more sections
];
```

#### 2. Visibility Map
```typescript
interface VisibilityMap {
  [sectionId: string]: boolean;
}

function getVisibilityMap(business: Business): VisibilityMap {
  return {
    hero: true,
    about: !!business.aboutText,
    services: business.services.length > 0,
    testimonials: business.testimonials.length > 0,
  };
}
```

### Implementation Tasks

1. **Define all page sections** used in business pages
2. **Create visibility logic** based on business data
3. **Implement rendering component** that uses this structure
4. **Add structure parity tests** to verify consistency

### Parity Testing
- Test that all locales render the same sections
- Verify section order is consistent
- Validate visibility conditions work across languages

### Deliverables
- [ ] BusinessPageSections configuration
- [ ] VisibilityMap function
- [ ] Page rendering component using sections
- [ ] Parity test suite
- [ ] Documentation of all sections

### Benefits
- Single definition of page structure
- Easier to add/remove sections
- Consistent behavior across locales
- Simplified testing and debugging

---
**Duration**: 2-3 hours | **Difficulty**: Intermediate
