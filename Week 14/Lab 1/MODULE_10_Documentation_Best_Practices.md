# MODULE 10: Documentation & Best Practices
## Week 2 - Day 5

### Objectives
- Create comprehensive system documentation
- Document architecture and data flows
- Establish best practices and patterns
- Build knowledge base for team

### 1. Architecture Documentation

#### System Overview
```
┌─────────────────────────────────────────────────────────────┐
│                    BizLink Multilingual System              │
└─────────────────────────────────────────────────────────────┘

┌──────────────────────┐         ┌──────────────────────┐
│   Frontend Layer     │         │   Backend Layer      │
├──────────────────────┤         ├──────────────────────┤
│ Language Switcher    │────┐    │ Localization Model   │
│ RTL Components       │    │    │ Collision Detection  │
│ Page Rendering       │    │    │ Slug Management      │
│ SEO Meta Tags        │    ├───→│ Validation Rules     │
└──────────────────────┘    │    │ API Endpoints        │
                            │    └──────────────────────┘
                            │            │
                            │    ┌──────▼──────────┐
                            │    │   Database      │
                            │    ├─────────────────┤
                            └───→│ Businesses      │
                                 │ Localizations   │
                                 └─────────────────┘
```

#### Data Flow: Business Creation
```
1. User Input
   ├─ Business Name
   └─ Localizations (for each language)
          ├─ Language
          ├─ Title
          ├─ Slug
          └─ Description

2. Validation
   ├─ Normalize slug
   ├─ Validate slug format
   ├─ Detect collisions
   └─ Return errors if any

3. Business Creation
   ├─ Create business record
   ├─ Create localization records
   └─ Transaction rollback on failure

4. Response
   └─ Return business ID & localizations
```

#### Data Flow: Page Rendering
```
1. User navigates to: /[locale]/[slug]

2. URL Params
   ├─ locale: 'ar' | 'en' | 'fr'
   └─ slug: 'my-business'

3. Server-side Rendering
   ├─ Fetch localization by slug + language
   ├─ Apply fallback if not published
   ├─ Fetch business data
   └─ Generate metadata (canonical, hreflang)

4. Rendering
   ├─ Set document direction (dir="ltr"|"rtl")
   ├─ Render page sections (from BusinessPageSections)
   ├─ Apply section visibility
   ├─ Include SEO tags
   └─ Render language switcher

5. Client-side Hydration
   ├─ Attach event listeners
   ├─ Initialize interactive components
   └─ Ready for user interaction
```

### 2. API Reference

#### Create Localization
```
POST /api/business/[businessId]/localizations/[language]

Request Headers:
  Content-Type: application/json
  Authorization: Bearer <token>

Request Body:
{
  "slug": "my-business",           // Required, alphanumeric-hyphen only
  "title": "My Business",          // Required, 1-200 chars
  "description": "Description",    // Optional
  "published": false               // Optional, default false
}

Response 201 Created:
{
  "id": "loc_abc123",
  "businessId": "biz_xyz789",
  "language": "ar",
  "slug": "my-business",
  "title": "My Business",
  "description": "Description",
  "published": false,
  "createdAt": "2026-04-28T10:00:00Z",
  "updatedAt": "2026-04-28T10:00:00Z"
}

Response 400 Bad Request:
{
  "error": "Invalid slug format",
  "details": [
    "Slug must contain only lowercase letters, numbers, and hyphens",
    "Slug must be at least 3 characters"
  ]
}

Response 409 Conflict:
{
  "error": "Slug collision detected",
  "type": "exact_match",
  "conflictingId": "biz_456",
  "message": "Slug 'my-business' already exists in ar",
  "suggestions": [
    "my-business-v2",
    "my-business-xyz123"
  ]
}
```

#### Get All Localizations
```
GET /api/business/[businessId]/localizations

Query Parameters:
  ?language=ar              // Optional: filter by language
  ?published=true           // Optional: filter by publish status
  ?limit=50                 // Optional: max results
  ?offset=0                 // Optional: pagination

Response 200 OK:
{
  "data": [
    {
      "id": "loc_1",
      "businessId": "biz_1",
      "language": "en",
      "slug": "my-business",
      "title": "My Business",
      "published": true
    },
    {
      "id": "loc_2",
      "businessId": "biz_1",
      "language": "ar",
      "slug": "my-business",
      "title": "عملي",
      "published": false
    }
  ],
  "total": 2,
  "hasMore": false
}
```

### 3. Best Practices

#### Slug Management
✓ **DO:**
- Normalize slugs consistently (lowercase, no special chars)
- Reject collisions explicitly without auto-suffixing
- Use deterministic slug generation from business name
- Validate slug format on both client and server
- Document reserved slugs clearly

✗ **DON'T:**
- Auto-suffix conflicting slugs (confuses users)
- Allow special characters in slugs
- Change slug after publication without redirect
- Create slugs without language context
- Trust client-side validation alone

#### Localization Workflow
✓ **DO:**
- Create base localization (canonical language) first
- Use fallback for missing translations
- Publish only when content is complete
- Track publish status separately from content
- Test all language variants before launch

✗ **DON'T:**
- Publish incomplete translations
- Mix languages in single localization
- Delete published localizations without archiving
- Assume user's browser language
- Store translations without locale context

#### SEO Implementation
✓ **DO:**
- Include canonical URL on every page
- Add hreflang for all language variants
- Use x-default for unspecified languages
- Test with Google Search Console
- Monitor crawl errors in GSC

✗ **DON'T:**
- Use different canonical URLs for same content
- Forget bidirectional hreflang links
- Include non-published content in hreflang
- Use relative URLs for canonical tags
- Index unpublished or draft content

#### RTL Support
✓ **DO:**
- Set `dir` attribute on `<html>` element
- Use logical CSS properties (margin-inline)
- Test with actual RTL languages
- Mirror icons and images appropriately
- Handle text alignment in forms

✗ **DON'T:**
- Hardcode left/right in CSS
- Use flexbox `direction` property alone
- Assume all RTL languages use same rules
- Skip testing with screen readers
- Ignore form layout for RTL

### 4. Common Patterns

#### Check if Content is Ready to Publish
```typescript
async function canPublishLocalization(
  localization: Localization
): Promise<boolean> {
  // Slug must exist and be validated
  if (!localization.slug) return false;

  // Title must not be empty
  if (!localization.title?.trim()) return false;

  // Check for collision
  const collision = await detectCollisions(
    localization.businessId,
    {
      language: localization.language,
      slug: localization.slug,
      title: localization.title,
    }
  );

  return !collision.hasCollision;
}
```

#### Create Redirects for Slug Changes
```typescript
async function changeSlug(
  businessId: string,
  language: string,
  oldSlug: string,
  newSlug: string
) {
  // Verify new slug is available
  const collision = await detectCollisions(businessId, {
    language,
    slug: newSlug,
    title: 'Dummy', // For validation only
  });

  if (collision.hasCollision) {
    throw new Error('New slug already taken');
  }

  // Create redirect (old URL → new URL)
  await createRedirect({
    fromPath: `/${language}/${oldSlug}`,
    toPath: `/${language}/${newSlug}`,
    statusCode: 301, // Permanent redirect
  });

  // Update localization
  await updateLocalization(businessId, language, {
    slug: newSlug,
  });
}
```

#### Load Business with Correct Language
```typescript
async function loadBusinessPage(
  businessId: string,
  preferredLanguage: string
) {
  // Try preferred language
  let localization = await getLocalization(
    businessId,
    preferredLanguage
  );

  if (!localization?.published) {
    // Fallback to primary language
    localization = await getLocalization(businessId, 'en');
  }

  if (!localization) {
    throw new Error('No published localization available');
  }

  const business = await getBusiness(businessId);

  return {
    business,
    localization,
    language: localization.language,
  };
}
```

### 5. Troubleshooting Guide

**Problem**: Slug collision errors when creating business
- **Check**: Are you normalizing slugs consistently?
- **Check**: Did you run collision detection before inserting?
- **Solution**: Use `generateSlugCandidates()` to get alternatives

**Problem**: Hreflang tags not showing in Google Search Console
- **Check**: Are all URLs HTTPS?
- **Check**: Are hreflang URLs accessible (not 404)?
- **Check**: Do hreflang tags use absolute URLs?
- **Solution**: Validate with `validateHreflangTags(config)`

**Problem**: RTL layout looks broken
- **Check**: Is `dir="rtl"` set on `<html>`?
- **Check**: Are you using logical CSS properties?
- **Check**: Do images need mirroring?
- **Solution**: Test with browser DevTools, set `dir` attribute

**Problem**: Language switcher causes layout shift
- **Check**: Is language button fixed-width?
- **Check**: Does dropdown menu positioned absolutely?
- **Solution**: Use CSS layout stabilization patterns

### 6. File Structure & Organization

```
app/src/
├── lib/
│   ├── business-localization.ts      # Localization model
│   ├── business-localization.test.ts
│   ├── business-slug.ts              # Slug management
│   ├── business-slug.test.ts
│   ├── business-page-sections.ts     # Page structure
│   ├── business-page-sections.test.ts
│   ├── seo.ts                        # SEO helpers
│   ├── seo-alternates.test.ts
│   ├── seo-alternates.md             # SEO documentation
│   ├── business-creation.ts          # Creation flow
│   └── utils.ts                      # Direction helpers
│
├── components/
│   ├── layout/
│   │   ├── language-switcher.tsx     # Language selector
│   │   └── mobile-menu.tsx           # RTL-aware menu
│   └── business/
│       └── business-page.tsx         # Main page component
│
├── app/
│   ├── [locale]/
│   │   └── [slug]/
│   │       └── page.tsx              # Dynamic page
│   │
│   └── api/
│       └── business/
│           └── [businessId]/
│               └── localizations/
│                   ├── route.ts      # GET all
│                   └── [language]/
│                       └── route.ts  # GET/POST/DELETE
│
└── docs/
    ├── localization-rendering-rules.md
    ├── canonical-schema-and-slug-strategy.md
    └── api-documentation.md
```

### 7. Deployment Checklist

- [ ] All tests passing (>90% coverage)
- [ ] Hreflang tags validated with Google tool
- [ ] Canonical URLs tested with Search Console
- [ ] RTL support tested with Arabic/Hebrew browsers
- [ ] Collision detection working in production DB
- [ ] Language switcher persistence working
- [ ] Performance benchmarks meet targets (<200ms load)
- [ ] Error handling and logging configured
- [ ] Documentation reviewed by team
- [ ] Rollback plan documented
- [ ] A/B testing configured (if applicable)
- [ ] Monitoring dashboards set up

### Deliverables
- [ ] Architecture documentation with diagrams
- [ ] Complete API reference
- [ ] Best practices guide (team document)
- [ ] Common patterns with code examples
- [ ] Troubleshooting guide
- [ ] File structure documentation
- [ ] Deployment checklist
- [ ] Team training materials

### Resources
- [IETF Hreflang RFC](https://tools.ietf.org/html/rfc5646)
- [Google Search Console Help](https://support.google.com/webmasters)
- [Web.dev i18n Guide](https://web.dev/i18n/)
- [MDN RTL Documentation](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/dir)

---
**Duration**: 3-4 hours | **Difficulty**: Intermediate
**Note**: Ongoing documentation maintenance required
