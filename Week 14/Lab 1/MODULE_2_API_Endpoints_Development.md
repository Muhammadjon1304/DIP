# MODULE 2: API Endpoints Development
## Week 1 - Day 2

### Objectives
- Design RESTful API endpoints for localization management
- Implement CRUD operations for localizations
- Handle error responses and validation
- Ensure proper HTTP status codes

### API Endpoints

#### 1. Get All Localizations
```
GET /api/business/[businessId]/localizations
Response: LocalizationModel[]
Status: 200 OK
```

#### 2. Get Specific Language Localization
```
GET /api/business/[businessId]/localizations/[language]
Response: LocalizationModel
Status: 200 OK | 404 Not Found
```

#### 3. Create/Update Localization
```
POST /api/business/[businessId]/localizations/[language]
Body: {
  slug: string,
  title: string,
  description: string,
  published: boolean
}
Response: LocalizationModel
Status: 201 Created | 200 OK | 409 Conflict
```

#### 4. Delete Localization
```
DELETE /api/business/[businessId]/localizations/[language]
Response: { success: boolean }
Status: 200 OK | 404 Not Found
```

### Implementation Requirements

1. **Route Handlers**: Create API route files for each endpoint
2. **Validation**: Validate request body and parameters
3. **Error Handling**: Return appropriate HTTP status codes
4. **Authentication**: Check business ownership before modifications
5. **Logging**: Track all API calls for debugging

### Key Considerations

- Idempotency for POST/PUT operations
- Proper HTTP semantics (201 for creation, 409 for conflicts)
- Request/Response validation
- Security checks for authorization

### Deliverables
- [ ] GET /localizations endpoint
- [ ] GET /localizations/[language] endpoint
- [ ] POST /localizations/[language] endpoint
- [ ] DELETE /localizations/[language] endpoint
- [ ] Comprehensive API tests

### Error Handling Examples
- 400 Bad Request: Invalid input
- 401 Unauthorized: Authentication required
- 403 Forbidden: Insufficient permissions
- 404 Not Found: Resource doesn't exist
- 409 Conflict: Collision or constraint violation

---
**Duration**: 3-4 hours | **Difficulty**: Intermediate
