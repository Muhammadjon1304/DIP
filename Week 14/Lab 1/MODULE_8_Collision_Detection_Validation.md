# MODULE 8: Collision Detection & Validation
## Week 2 - Day 3

### Objectives
- Build comprehensive collision detection system
- Implement multilingual slug uniqueness constraints
- Validate business creation and localization updates
- Handle conflict resolution strategies

### Key Concepts

#### 1. Collision Types
```typescript
enum CollisionType {
  EXACT_MATCH = 'exact_match', // Same slug in same language
  TRANSLITERATION = 'transliteration', // Similar slug after normalization
  LANGUAGE_VARIANT = 'language_variant', // Similar across language variants
  RESERVED = 'reserved', // Conflicts with system slugs
}

interface CollisionResult {
  hasCollision: boolean;
  type?: CollisionType;
  conflictingId?: string;
  message: string;
  suggestions?: string[];
}
```

#### 2. Multilingual Collision Detection
```typescript
async function detectCollisions(
  businessId: string,
  localization: {
    language: string;
    slug: string;
    title: string;
  }
): Promise<CollisionResult> {
  // Check 1: Exact match in same language
  const exactMatch = await db.query(
    `SELECT id FROM localizations 
     WHERE slug = ? AND language = ? AND business_id != ? AND published = true`,
    [localization.slug, localization.language, businessId]
  );

  if (exactMatch) {
    return {
      hasCollision: true,
      type: CollisionType.EXACT_MATCH,
      conflictingId: exactMatch.id,
      message: `Slug "${localization.slug}" already exists in ${localization.language}`,
    };
  }

  // Check 2: Normalized variations
  const normalized = normalizeSlug(localization.title);
  if (normalized !== localization.slug) {
    const variantMatch = await db.query(
      `SELECT id FROM localizations 
       WHERE slug = ? AND language = ? AND business_id != ? AND published = true`,
      [normalized, localization.language, businessId]
    );

    if (variantMatch) {
      return {
        hasCollision: true,
        type: CollisionType.TRANSLITERATION,
        message: `Title normalizes to existing slug: "${normalized}"`,
        suggestions: [normalized],
      };
    }
  }

  // Check 3: Reserved slugs
  const reserved = await getReservedSlugs();
  if (reserved.includes(localization.slug)) {
    return {
      hasCollision: true,
      type: CollisionType.RESERVED,
      message: `"${localization.slug}" is a reserved slug`,
      suggestions: [generateAlternativeSlug(localization.slug)],
    };
  }

  // Check 4: Similar slugs across language variants
  const similarVariants = await db.query(
    `SELECT DISTINCT language FROM localizations 
     WHERE slug = ? AND business_id != ? AND published = true`,
    [localization.slug, businessId]
  );

  if (similarVariants.length > 0) {
    return {
      hasCollision: true,
      type: CollisionType.LANGUAGE_VARIANT,
      message: `Slug "${localization.slug}" already exists in: ${similarVariants.join(', ')}`,
      suggestions: [
        `${localization.slug}-${localization.language}`,
        `${localization.slug}-${businessId.slice(0, 6)}`,
      ],
    };
  }

  return { hasCollision: false, message: 'No collisions detected' };
}
```

#### 3. API Validation Middleware
```typescript
// Express/Next.js API middleware for validation
export async function validateLocalizationInput(
  req: Request,
  res: Response,
  next: NextFunction
) {
  const { businessId, language } = req.params;
  const { slug, title, description, published } = req.body;

  // Validate required fields
  if (!slug || !title) {
    return res.status(400).json({
      error: 'Missing required fields: slug, title',
    });
  }

  // Validate slug format
  const slugValidation = validateSlug(slug);
  if (!slugValidation.isValid) {
    return res.status(400).json({
      error: 'Invalid slug format',
      details: slugValidation.errors,
    });
  }

  // Detect collisions
  const collision = await detectCollisions(businessId, {
    language,
    slug,
    title,
  });

  if (collision.hasCollision) {
    return res.status(409).json({
      error: 'Slug collision detected',
      details: collision,
    });
  }

  // Store validation result in request for next handler
  req.validationResult = { slug, title, description, published };
  next();
}
```

#### 4. Business Creation Flow with Collision Checks
```typescript
async function createBusinessWithLocalizations(
  business: BusinessInput,
  localizations: LocalizationInput[]
) {
  // Transaction to ensure atomicity
  return await db.transaction(async (trx) => {
    // Step 1: Create business
    const newBusiness = await trx('businesses').insert({
      id: generateId(),
      name: business.name,
      createdAt: new Date(),
    });

    const businessId = newBusiness[0];

    // Step 2: Validate and create localizations
    for (const loc of localizations) {
      // Check for collisions BEFORE creating
      const collision = await detectCollisions(businessId, {
        language: loc.language,
        slug: loc.slug,
        title: loc.title,
      });

      if (collision.hasCollision) {
        // Rollback entire transaction
        throw new Error(
          `Cannot create business: ${collision.message}. Use a different slug.`
        );
      }

      // Create localization
      await trx('localizations').insert({
        id: generateId(),
        businessId,
        language: loc.language,
        slug: loc.slug,
        title: loc.title,
        description: loc.description,
        published: loc.published || false,
        createdAt: new Date(),
      });
    }

    return { businessId, success: true };
  });
}
```

#### 5. Conflict Resolution Strategies
```typescript
// Strategy 1: Suggest alternatives
function suggestAlternativeSlug(
  originalSlug: string,
  conflict: CollisionResult
): string[] {
  const suggestions: string[] = [];

  // Add timestamp suffix
  suggestions.push(`${originalSlug}-${Date.now().toString(36)}`);

  // Add random suffix
  suggestions.push(`${originalSlug}-${generateRandomId(6)}`);

  // Add version number
  suggestions.push(`${originalSlug}-v2`);

  return suggestions.slice(0, 3); // Return top 3 suggestions
}

// Strategy 2: Namespace by language
function namespacedSlug(slug: string, language: string): string {
  return `${slug}-${language}`;
}

// Strategy 3: Allow user to rename business
async function resolveConflictByRenaming(
  businessId: string,
  language: string,
  newTitle: string
): Promise<string> {
  const newSlug = normalizeSlug(newTitle);

  // Validate new slug
  const collision = await detectCollisions(businessId, {
    language,
    slug: newSlug,
    title: newTitle,
  });

  if (collision.hasCollision) {
    throw new Error(`New slug also has collision: ${collision.message}`);
  }

  // Update business name/title
  await db('businesses').where({ id: businessId }).update({
    name: newTitle,
    updatedAt: new Date(),
  });

  // Update localization
  await db('localizations')
    .where({ businessId, language })
    .update({
      slug: newSlug,
      title: newTitle,
      updatedAt: new Date(),
    });

  return newSlug;
}
```

### Implementation Tasks

1. **Create collision detection logic** for all types
2. **Implement API validation middleware** for request checking
3. **Build business creation flow** with transaction safety
4. **Add conflict resolution strategies** with user guidance
5. **Create comprehensive tests** for all collision scenarios

### Deliverables
- [ ] Collision detection function
- [ ] Validation middleware
- [ ] Business creation with collision checks
- [ ] Conflict resolution strategies
- [ ] Error handling and user messaging
- [ ] Extensive test suite (20+ test cases)

### Error Responses

**409 Conflict**: When exact slug collision detected
```json
{
  "error": "Slug collision detected",
  "type": "exact_match",
  "conflictingId": "biz_12345",
  "message": "Slug 'my-business' already exists in ar",
  "suggestions": [
    "my-business-v2",
    "my-business-xyz123",
    "my-business-ar"
  ]
}
```

### Testing Scenarios
- [ ] Same slug in same language (exact match)
- [ ] Same slug in different languages
- [ ] Normalized collisions (diacritics, spacing)
- [ ] Reserved system slugs
- [ ] Edge cases (very short slugs, special chars)
- [ ] Concurrent requests (race conditions)
- [ ] Transaction rollback on collision

---
**Duration**: 4-5 hours | **Difficulty**: Advanced
