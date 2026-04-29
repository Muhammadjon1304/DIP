# MODULE 6: Canonical Slug Management
## Week 2 - Day 1

### Objectives
- Design canonical slug system for multilingual URLs
- Implement slug normalization and validation
- Prevent slug collisions across languages
- Create slug candidate generation strategies

### Key Concepts

#### 1. Slug Normalization
```typescript
function normalizeSlug(input: string): string {
  return input
    .toLowerCase() // Lowercase
    .trim() // Remove whitespace
    .replace(/[^\w\s-]/g, '') // Remove special characters
    .replace(/[\s_-]+/g, '-') // Replace spaces/underscores with hyphens
    .replace(/^-+|-+$/g, ''); // Remove leading/trailing hyphens
}

// Examples
normalizeSlug('Hello World!') // 'hello-world'
normalizeSlug('Café Au Lait') // 'cafe-au-lait'
normalizeSlug('  My-Business  ') // 'my-business'
```

#### 2. Slug Generation Strategy
```typescript
interface SlugCandidate {
  slug: string;
  source: 'canonical' | 'title' | 'fallback';
  confidence: number;
}

function generateSlugCandidates(business: {
  name: string;
  id: string;
}): SlugCandidate[] {
  const candidates: SlugCandidate[] = [];

  // Candidate 1: Normalized business name
  candidates.push({
    slug: normalizeSlug(business.name),
    source: 'canonical',
    confidence: 0.95,
  });

  // Candidate 2: Business name + ID suffix
  if (normalizeSlug(business.name).length > 0) {
    candidates.push({
      slug: `${normalizeSlug(business.name)}-${business.id.slice(0, 6)}`,
      source: 'title',
      confidence: 0.85,
    });
  }

  // Candidate 3: Fallback to ID
  candidates.push({
    slug: business.id,
    source: 'fallback',
    confidence: 0.5,
  });

  return candidates;
}
```

#### 3. Collision Detection
```typescript
interface SlugCollisionCheck {
  hasCollision: boolean;
  conflictingBusinessId?: string;
  suggestedAlternative?: string;
}

async function checkSlugCollision(
  slug: string,
  language: string,
  excludeBusinessId?: string
): Promise<SlugCollisionCheck> {
  // Query database for existing slug in this language
  const existing = await db.query(
    `SELECT business_id FROM localizations 
     WHERE slug = ? AND language = ? AND published = true`,
    [slug, language]
  );

  if (!existing) {
    return { hasCollision: false };
  }

  if (existing.business_id === excludeBusinessId) {
    return { hasCollision: false }; // Same business, no collision
  }

  return {
    hasCollision: true,
    conflictingBusinessId: existing.business_id,
    suggestedAlternative: `${slug}-${generateUniqueId()}`,
  };
}
```

#### 4. Slug Validation
```typescript
interface SlugValidationResult {
  isValid: boolean;
  errors: string[];
}

function validateSlug(slug: string): SlugValidationResult {
  const errors: string[] = [];

  if (!slug || slug.length === 0) {
    errors.push('Slug cannot be empty');
  } else if (slug.length < 3) {
    errors.push('Slug must be at least 3 characters');
  } else if (slug.length > 100) {
    errors.push('Slug must not exceed 100 characters');
  }

  if (!/^[a-z0-9-]+$/.test(slug)) {
    errors.push('Slug must contain only lowercase letters, numbers, and hyphens');
  }

  if (slug.startsWith('-') || slug.endsWith('-')) {
    errors.push('Slug cannot start or end with a hyphen');
  }

  if (slug.includes('--')) {
    errors.push('Slug cannot contain consecutive hyphens');
  }

  // Reserved slugs
  const reserved = ['api', 'admin', 'auth', 'settings'];
  if (reserved.includes(slug)) {
    errors.push(`"${slug}" is a reserved slug`);
  }

  return {
    isValid: errors.length === 0,
    errors,
  };
}
```

### Implementation Tasks

1. **Create normalization function** with Unicode support
2. **Build slug candidate generator** with ranking
3. **Implement collision detection** with database queries
4. **Add validation rules** for slug format
5. **Handle conflict resolution** without auto-suffixing

### Key Decisions

- No automatic suffixing on collision - require user to choose
- Support Unicode in normalization (transliteration)
- Slug is language-specific (same business can have different slugs per language)
- Once set, slug is immutable (or requires special permission to change)

### Deliverables
- [ ] Slug normalization function
- [ ] Candidate generation algorithm
- [ ] Collision detection query
- [ ] Validation rule set
- [ ] Conflict resolution UI
- [ ] Comprehensive test suite

### Edge Cases to Handle
- Unicode characters and transliteration
- Very long business names
- Special characters and punctuation
- Multiple consecutive spaces/hyphens
- Reserved system slugs

---
**Duration**: 3-4 hours | **Difficulty**: Advanced
