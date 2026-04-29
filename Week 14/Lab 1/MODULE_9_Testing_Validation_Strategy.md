# MODULE 9: Testing & Validation Strategy
## Week 2 - Day 4

### Objectives
- Design comprehensive test strategy for multilingual features
- Implement unit, integration, and E2E tests
- Validate all edge cases and error scenarios
- Ensure test coverage across all modules

### Test Architecture

#### 1. Unit Tests - Localization Helpers
```typescript
// Tests for business-localization.test.ts
describe('LocalizationModel', () => {
  describe('Fallback Behavior', () => {
    it('should return published localization in requested language', () => {
      const loc = getLocalization('ar', localizations);
      expect(loc.language).toBe('ar');
      expect(loc.published).toBe(true);
    });

    it('should fallback to primary language when requested language unavailable', () => {
      const loc = getLocalization('fr', localizations); // fr not available
      expect(loc.language).toBe('en');
    });

    it('should throw error when no published fallback exists', () => {
      expect(() =>
        getLocalization('fr', [
          { language: 'ar', published: false },
          { language: 'en', published: false },
        ])
      ).toThrow('No published localization available');
    });

    it('should respect language hierarchy: requested > en > app-default', () => {
      const loc = getLocalization('pt', [
        { language: 'pt-BR', published: true },
        { language: 'pt', published: true },
        { language: 'en', published: true },
      ]);
      expect(loc.language).toBe('pt-BR');
    });
  });

  describe('Validation', () => {
    it('should validate required fields', () => {
      const result = validateLocalization({
        businessId: 'biz1',
        language: 'ar',
        // missing slug, title
      });
      expect(result.isValid).toBe(false);
      expect(result.errors).toContain('slug is required');
    });

    it('should validate slug format', () => {
      const result = validateLocalization({
        businessId: 'biz1',
        language: 'ar',
        slug: 'invalid slug!', // invalid
        title: 'Test',
      });
      expect(result.isValid).toBe(false);
    });

    it('should allow published field only when slug and title exist', () => {
      const result = validateLocalization({
        businessId: 'biz1',
        language: 'ar',
        slug: 'test',
        title: 'Test',
        published: true,
      });
      expect(result.isValid).toBe(true);
    });
  });
});
```

#### 2. Slug Management Tests
```typescript
// Tests for business-slug.test.ts
describe('Slug Management', () => {
  describe('Normalization', () => {
    it('should normalize to lowercase', () => {
      expect(normalizeSlug('HELLO')).toBe('hello');
    });

    it('should remove special characters', () => {
      expect(normalizeSlug('hello@world!')).toBe('hello-world');
    });

    it('should handle Unicode characters', () => {
      expect(normalizeSlug('café')).toBe('cafe');
      expect(normalizeSlug('مرحبا')).toBe(''); // Arabic script
    });

    it('should collapse multiple spaces/hyphens', () => {
      expect(normalizeSlug('hello  --  world')).toBe('hello-world');
    });

    it('should trim leading/trailing hyphens', () => {
      expect(normalizeSlug('-hello-world-')).toBe('hello-world');
    });
  });

  describe('Collision Detection', () => {
    let mockDb: jest.Mocked<Database>;

    beforeEach(() => {
      mockDb = createMockDatabase();
    });

    it('should detect exact slug match in same language', async () => {
      mockDb.query.mockResolvedValue([{ id: 'existing-id' }]);

      const result = await detectCollisions('new-id', {
        language: 'en',
        slug: 'duplicate-slug',
        title: 'Test',
      });

      expect(result.hasCollision).toBe(true);
      expect(result.type).toBe(CollisionType.EXACT_MATCH);
    });

    it('should NOT detect collision for same business', async () => {
      mockDb.query.mockResolvedValue([{ id: 'same-id' }]);

      const result = await detectCollisions('same-id', {
        language: 'en',
        slug: 'existing-slug',
        title: 'Test',
      });

      expect(result.hasCollision).toBe(false);
    });

    it('should detect transliteration collisions', async () => {
      mockDb.query.mockResolvedValue([{ id: 'existing-id' }]);

      const result = await detectCollisions('new-id', {
        language: 'en',
        slug: 'café', // Should normalize to 'cafe'
        title: 'Cafe',
      });

      expect(result.hasCollision).toBe(true);
      expect(result.type).toBe(CollisionType.TRANSLITERATION);
    });

    it('should detect reserved slug collisions', async () => {
      const result = await detectCollisions('new-id', {
        language: 'en',
        slug: 'admin',
        title: 'Admin',
      });

      expect(result.hasCollision).toBe(true);
      expect(result.type).toBe(CollisionType.RESERVED);
    });
  });

  describe('Validation', () => {
    it('should validate minimum slug length', () => {
      const result = validateSlug('ab');
      expect(result.isValid).toBe(false);
      expect(result.errors).toContain('Slug must be at least 3 characters');
    });

    it('should validate maximum slug length', () => {
      const result = validateSlug('a'.repeat(101));
      expect(result.isValid).toBe(false);
      expect(result.errors).toContain('Slug must not exceed 100 characters');
    });

    it('should validate character restrictions', () => {
      const result = validateSlug('hello@world');
      expect(result.isValid).toBe(false);
    });

    it('should allow valid slugs', () => {
      const result = validateSlug('my-awesome-business');
      expect(result.isValid).toBe(true);
    });
  });
});
```

#### 3. Integration Tests - API Endpoints
```typescript
// Tests for API endpoints
describe('Localization API', () => {
  let app: Express.Application;
  let db: Database;

  beforeEach(async () => {
    app = setupTestApp();
    db = await setupTestDatabase();
  });

  afterEach(async () => {
    await db.cleanup();
  });

  describe('POST /api/business/[id]/localizations/[language]', () => {
    it('should create localization with valid input', async () => {
      const response = await request(app)
        .post('/api/business/biz1/localizations/ar')
        .send({
          slug: 'my-business',
          title: 'My Business',
          description: 'A great business',
          published: false,
        });

      expect(response.status).toBe(201);
      expect(response.body.language).toBe('ar');
      expect(response.body.slug).toBe('my-business');
    });

    it('should reject invalid slug', async () => {
      const response = await request(app)
        .post('/api/business/biz1/localizations/ar')
        .send({
          slug: 'invalid slug!',
          title: 'My Business',
        });

      expect(response.status).toBe(400);
      expect(response.body.error).toContain('Invalid slug');
    });

    it('should reject slug collision with 409', async () => {
      // Create first localization
      await request(app)
        .post('/api/business/biz1/localizations/ar')
        .send({
          slug: 'existing-slug',
          title: 'Business 1',
        });

      // Try to create duplicate
      const response = await request(app)
        .post('/api/business/biz2/localizations/ar')
        .send({
          slug: 'existing-slug',
          title: 'Business 2',
        });

      expect(response.status).toBe(409);
      expect(response.body.error).toContain('collision');
    });

    it('should allow same slug in different languages', async () => {
      await request(app)
        .post('/api/business/biz1/localizations/en')
        .send({
          slug: 'my-business',
          title: 'My Business',
        });

      const response = await request(app)
        .post('/api/business/biz1/localizations/ar')
        .send({
          slug: 'my-business',
          title: 'عملي',
        });

      expect(response.status).toBe(201);
    });
  });

  describe('GET /api/business/[id]/localizations', () => {
    it('should return all localizations for business', async () => {
      // Create multiple localizations
      await request(app)
        .post('/api/business/biz1/localizations/en')
        .send({ slug: 'biz', title: 'Business' });

      await request(app)
        .post('/api/business/biz1/localizations/ar')
        .send({ slug: 'biz', title: 'عملي' });

      const response = await request(app).get(
        '/api/business/biz1/localizations'
      );

      expect(response.status).toBe(200);
      expect(response.body).toHaveLength(2);
    });

    it('should filter by language', async () => {
      // Setup
      await request(app)
        .post('/api/business/biz1/localizations/en')
        .send({ slug: 'biz', title: 'Business' });

      const response = await request(app).get(
        '/api/business/biz1/localizations?language=en'
      );

      expect(response.status).toBe(200);
      expect(response.body).toHaveLength(1);
      expect(response.body[0].language).toBe('en');
    });
  });
});
```

#### 4. SEO Tests
```typescript
// Tests for seo-alternates.test.ts
describe('SEO Alternates', () => {
  describe('Canonical URL Generation', () => {
    it('should generate valid canonical URL', () => {
      const config = getCanonicalConfig(business, 'en', 'https://example.com');
      expect(config.canonical).toBe('https://example.com/en/my-business');
      expect(config.canonical).toMatch(/^https:\/\//);
    });

    it('should include all published localizations', () => {
      const config = getCanonicalConfig(
        {
          id: 'biz1',
          localizations: [
            { language: 'en', slug: 'biz', published: true },
            { language: 'ar', slug: 'biz', published: true },
            { language: 'fr', slug: 'biz', published: false }, // Not included
          ],
        },
        'en',
        'https://example.com'
      );

      expect(config.alternates).toHaveLength(2);
      expect(config.alternates.map((a) => a.language)).toEqual(['en', 'ar']);
    });

    it('should include x-default pointing to canonical', () => {
      const config = getCanonicalConfig(business, 'en', 'https://example.com');
      expect(config.xDefault).toBe(config.canonical);
    });
  });

  describe('Hreflang Tag Generation', () => {
    it('should generate valid hreflang tags', () => {
      const config = getCanonicalConfig(business, 'en', 'https://example.com');
      const tags = generateHreflangTags(config);

      expect(tags).toContain('rel=\"canonical\"');
      expect(tags).toContain('rel=\"alternate\" hreflang=\"en\"');
      expect(tags).toContain('rel=\"alternate\" hreflang=\"ar\"');
      expect(tags).toContain('hreflang=\"x-default\"');
    });

    it('should properly escape URLs in tags', () => {
      const config = {
        canonical: 'https://example.com/en/my%20business',
        alternates: [{ language: 'en', url: 'https://example.com/en/my%20business' }],
        xDefault: 'https://example.com/en/my%20business',
      };

      const tags = generateHreflangTags(config);
      expect(tags).not.toContain('&');
    });
  });
});
```

### Test Coverage Report

```
Module                           | Coverage | Status
---------------------------------|----------|--------
business-localization.ts         | 95%      | ✓ Pass
business-slug.ts                 | 92%      | ✓ Pass
seo.ts                          | 88%      | ✓ Pass
business-page-sections.ts        | 94%      | ✓ Pass
API routes                       | 90%      | ✓ Pass
```

### Implementation Tasks

1. **Write unit tests** for all utility functions
2. **Create API integration tests** for all endpoints
3. **Add SEO validation tests** for hreflang generation
4. **Implement E2E tests** for user workflows
5. **Set up CI/CD** test execution

### Deliverables
- [ ] Unit test suite (50+ test cases)
- [ ] Integration tests (30+ test cases)
- [ ] E2E tests (10+ user workflows)
- [ ] Test coverage report (>90%)
- [ ] Performance benchmarks
- [ ] Test documentation

### Test Execution
```bash
npm test                          # Run all tests
npm run test:unit               # Unit tests only
npm run test:integration        # Integration tests
npm run test:e2e                # E2E tests
npm run test:coverage           # Coverage report
npm run test:watch              # Watch mode
```

### Key Testing Principles
- Test behavior, not implementation
- Isolate units with mocks
- Use realistic test data
- Cover happy path and edge cases
- Validate error scenarios
- Performance test critical paths

---
**Duration**: 4-5 hours | **Difficulty**: Advanced
