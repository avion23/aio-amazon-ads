# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-01-31

### Added
- Initial release with 62 endpoints:
  - Sponsored Products (31 endpoints)
  - Sponsored Brands (16 endpoints)
  - Sponsored Display (8 endpoints)
  - Portfolios (5 endpoints)
  - Profiles (2 endpoints)
- Native async/await support with httpx
- Auto-pagination for all list() methods
- Professional retry logic using tenacity
- Token refresh with deadlock prevention
- 401 retry logic with automatic token refresh
- Marketplace support (NA, EU, FE) with country code mapping
- Comprehensive logging with X-Amzn-Request-Id tracking
- 13 tests (6 unit + 7 integration)
- MIT License

### Known Limitations
- Pydantic models exist but are not enforced in service responses
- Input validation is basic (type checking only)
- No built-in caching for immutable data

## [Unreleased]

### Planned
- Full Pydantic model integration for type safety
- Enhanced input validation with detailed error messages
- Caching for profiles and portfolios
- Metrics and monitoring hooks
- Additional endpoint coverage
