# MODULE 5: Language Switcher UX
## Week 1 - Day 5

### Objectives
- Design effective language switcher interface
- Implement persistent language selection
- Minimize layout shift when switching languages
- Handle edge cases and user preferences

### Key Concepts

#### 1. Language Switcher Component
```typescript
interface Language {
  code: string;
  name: string;
  nativeName: string;
  flag?: string;
}

interface LanguageSwitcherProps {
  currentLocale: string;
  availableLanguages: Language[];
  onLanguageChange: (locale: string) => void;
}

export function LanguageSwitcher({
  currentLocale,
  availableLanguages,
  onLanguageChange,
}: LanguageSwitcherProps) {
  const [isOpen, setIsOpen] = useState(false);
  const direction = getLocaleDirection(currentLocale);

  return (
    <div className={`language-switcher language-switcher--${direction}`}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Change language"
      >
        {currentLocale.toUpperCase()}
      </button>
      {isOpen && (
        <ul className="language-switcher__menu">
          {availableLanguages.map((lang) => (
            <li key={lang.code}>
              <button
                onClick={() => {
                  onLanguageChange(lang.code);
                  setIsOpen(false);
                }}
                aria-current={lang.code === currentLocale ? 'page' : undefined}
              >
                {lang.nativeName}
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
```

#### 2. Persistence Strategy
```typescript
// Store in both URL and localStorage for redundancy
function useLanguagePreference() {
  const [locale, setLocale] = useState<string>('en');

  // Read from localStorage on mount
  useEffect(() => {
    const saved = localStorage.getItem('preferred-language');
    if (saved) setLocale(saved);
  }, []);

  const updateLanguage = (newLocale: string) => {
    setLocale(newLocale);
    localStorage.setItem('preferred-language', newLocale);
    // Also update URL
    window.location.href = `/${newLocale}${window.location.pathname}`;
  };

  return { locale, updateLanguage };
}
```

#### 3. Layout Shift Prevention
```css
/* Fixed-width language switcher to prevent layout shift */
.language-switcher {
  display: inline-block;
  width: 60px; /* Fixed width for current locale display */
  height: 40px;
  position: relative;
}

.language-switcher__menu {
  position: absolute;
  min-width: 120px;
  list-style: none;
  padding: 8px 0;
  margin: 0;
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  /* Prevent layout shift from dropdown */
  top: calc(100% + 8px);
  z-index: 1000;
}
```

### Implementation Tasks

1. **Create LanguageSwitcher component** with dropdown
2. **Implement localStorage persistence** for user preference
3. **Add URL synchronization** when language changes
4. **Prevent layout shift** with fixed sizing
5. **Handle edge cases**:
   - Browser back/forward buttons
   - Direct URL navigation to different locale
   - Missing translations

### UX Considerations

- **Clear labeling**: Show language names in native script
- **Current indicator**: Highlight active language
- **Accessibility**: ARIA labels, keyboard navigation
- **Performance**: Avoid blocking the UI during language switch
- **Mobile-friendly**: Ensure touch targets are adequate

### Deliverables
- [ ] LanguageSwitcher component
- [ ] Persistence hook
- [ ] CSS for layout stability
- [ ] Edge case handling
- [ ] User preference tests
- [ ] Accessibility audit

### Features to Add Later
- Language search/filter for many languages
- Regional variants (e.g., en-US vs en-GB)
- Auto-detect browser language
- Remember user preference across sessions

---
**Duration**: 3-4 hours | **Difficulty**: Intermediate
