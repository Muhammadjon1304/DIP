# MODULE 7: SEO Canonical & Hreflang Implementation
## Week 2 - Day 2

### Objectives
- Implement canonical URL tags for SEO
- Set up hreflang tags for multilingual content
- Handle x-default variant for language fallback
- Optimize for search engine indexing

### Key Concepts

#### 1. Canonical URL Structure
```typescript
interface CanonicalConfig {
  // Canonical URL points to the primary language version
  canonical: string;
  // Alternates for all available language versions
  alternates: Array<{
    language: string;
    url: string;
  }>;
  // x-default for users whose language isn't available
  xDefault?: string;
}

function getCanonicalConfig(
  business: {
    id: string;
    localizations: Localization[];
  },
  currentLocale: string,
  baseUrl: string
): CanonicalConfig {
  // Assume 'en' is the canonical locale
  const canonicalLocale = 'en';
  const canonicalLocalization = business.localizations.find(
    (l) => l.language === canonicalLocale && l.published
  );

  if (!canonicalLocalization) {
    throw new Error('Canonical localization not found');
  }

  const config: CanonicalConfig = {
    canonical: `${baseUrl}/${canonicalLocale}/${canonicalLocalization.slug}`,
    alternates: business.localizations
      .filter((l) => l.published)
      .map((l) => ({
        language: l.language,
        url: `${baseUrl}/${l.language}/${l.slug}`,
      })),
  };

  // Add x-default for unspecified languages
  config.xDefault = config.canonical;

  return config;
}
```

#### 2. Hreflang Tags
```typescript
function generateHreflangTags(config: CanonicalConfig): string {
  let tags = '';

  // Canonical tag
  tags += `<link rel=\"canonical\" href=\"${escapeHtml(config.canonical)}\" />\n`;

  // Hreflang tags for each language variant
  for (const alt of config.alternates) {
    tags += `<link rel=\"alternate\" hreflang=\"${escapeHtml(alt.language)}\" href=\"${escapeHtml(alt.url)}\" />\n`;
  }

  // x-default hreflang
  if (config.xDefault) {
    tags += `<link rel=\"alternate\" hreflang=\"x-default\" href=\"${escapeHtml(config.xDefault)}\" />\n`;
  }

  return tags;
}

// Example output:
// <link rel=\"canonical\" href=\"https://example.com/en/my-business\" />
// <link rel=\"alternate\" hreflang=\"en\" href=\"https://example.com/en/my-business\" />
// <link rel=\"alternate\" hreflang=\"ar\" href=\"https://example.com/ar/my-business\" />
// <link rel=\"alternate\" hreflang=\"x-default\" href=\"https://example.com/en/my-business\" />
```

#### 3. Metadata Generation for Pages
```typescript
// In Next.js 13+ with generateMetadata
export async function generateMetadata(props: {
  params: { locale: string; slug: string };
}): Promise<Metadata> {
  const { locale, slug } = props.params;

  // Fetch business and localization data
  const localization = await getLocalization(locale, slug);
  const business = await getBusiness(localization.businessId);

  // Get canonical config
  const canonicalConfig = getCanonicalConfig(
    business,
    locale,
    process.env.NEXT_PUBLIC_BASE_URL || 'https://example.com'
  );

  return {
    title: localization.title,
    description: localization.description,
    alternates: {
      canonical: canonicalConfig.canonical,
      languages: {
        'en-US': canonicalConfig.alternates.find((a) => a.language === 'en')?.url,
        'ar-AE': canonicalConfig.alternates.find((a) => a.language === 'ar')?.url,
        // ... other languages
        'x-default': canonicalConfig.xDefault,
      },
    },
    openGraph: {
      url: canonicalConfig.canonical,
      locale: locale.replace('-', '_'), // 'en_US' format for OG
      alternateLocale: canonicalConfig.alternates
        .filter((a) => a.language !== locale)
        .map((a) => a.language.replace('-', '_')),
    },
  };
}
```

#### 4. SEO Helper Functions
```typescript
interface LocalizationAvailability {
  [language: string]: {
    slug: string;
    available: boolean;
  };
}

function getAlternatesForSEO(
  localizations: Localization[],
  baseUrl: string
): LocalizationAvailability {
  const availability: LocalizationAvailability = {};

  for (const loc of localizations) {
    if (loc.published) {
      availability[loc.language] = {
        slug: loc.slug,
        available: true,
      };
    }
  }

  // Include x-default
  const englishVersion = localizations.find(
    (l) => l.language === 'en' && l.published
  );
  if (englishVersion) {
    availability['x-default'] = {
      slug: englishVersion.slug,
      available: true,
    };
  }

  return availability;
}

function shouldIndexPage(localization: Localization): boolean {
  // Only index published localizations
  return localization.published === true;
}

function getMetaRobots(published: boolean): string {
  return published ? 'index, follow' : 'noindex, nofollow';
}
```

### Best Practices

1. **One canonical per page**: Point all variants to primary version
2. **Bidirectional hreflang**: If en links to ar, ar must link back to en
3. **Self-referencing hreflang**: Each version should link to itself
4. **Use language-region codes**: en-US, ar-AE (not just en, ar)
5. **x-default for fallback**: Use for unspecified or default language
6. **Keep URLs consistent**: Same slug structure across all languages
7. **Test with Google Search Console**: Validate hreflang implementation

### Implementation Tasks

1. **Create canonical config function** for any localization
2. **Generate hreflang tags** for HTML head
3. **Update metadata generation** to include SEO tags
4. **Add validation** for canonical URL structure
5. **Implement tests** for hreflang correctness

### Deliverables
- [ ] Canonical URL builder
- [ ] Hreflang tag generator
- [ ] Next.js metadata integration
- [ ] SEO helper utilities
- [ ] Test suite (hreflang validation)
- [ ] Google Search Console integration guide

### Testing Checklist
- [ ] Canonical URL is valid and accessible
- [ ] Hreflang tags include all published versions
- [ ] x-default points to primary language
- [ ] Hreflang tags are bidirectional
- [ ] No hreflang for unpublished localizations
- [ ] All URLs use HTTPS

---
**Duration**: 3-4 hours | **Difficulty**: Advanced
