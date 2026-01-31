# Architecture

## System Overview

```mermaid
flowchart TB
    subgraph Client["AmazonAdsClient"]
        SP["sp (Sponsored Products)"]
        SB["sb (Sponsored Brands)"]
        SD["sd (Sponsored Display)"]
        Portfolios["portfolios"]
        Profiles["profiles"]
    end

    subgraph Services["Service Layer"]
        Campaigns["Campaigns"]
        AdGroups["Ad Groups"]
        Keywords["Keywords"]
        ProductAds["Product Ads"]
        Reports["Reports"]
    end

    subgraph HTTP["HTTP Layer"]
        BaseClient["BaseClient"]
        Retry["Tenacity Retry"]
        Auth["Auth Manager"]
    end

    SP --> Campaigns
    SP --> AdGroups
    SP --> Keywords
    SP --> ProductAds
    SP --> Reports

    Campaigns --> BaseClient
    AdGroups --> BaseClient
    Keywords --> BaseClient
    ProductAds --> BaseClient
    Reports --> BaseClient

    BaseClient --> Retry
    BaseClient --> Auth
    Auth --> Amazon["Amazon OAuth"]
    BaseClient --> API["Amazon Advertising API"]
```

## Request Flow

```mermaid
sequenceDiagram
    participant User
    participant Client as AmazonAdsClient
    participant Service as CampaignService
    participant Base as BaseClient
    participant Retry as Tenacity
    participant Auth as AuthManager
    participant Amazon as Amazon API

    User->>Client: client.sp.campaigns.list()
    Client->>Service: list()
    Service->>Base: _paginated_get()
    Base->>Retry: retry wrapper
    Retry->>Base: execute request
    Base->>Auth: get_access_token()
    Auth->>Auth: check token expiry
    alt token expired
        Auth->>Amazon: refresh token
        Amazon-->>Auth: new access_token
    end
    Auth-->>Base: access_token
    Base->>Amazon: GET /sp/campaigns
    Amazon-->>Base: response + X-Amzn-Request-Id
    Base-->>Service: parsed response
    Service-->>Client: AsyncGenerator
    Client-->>User: campaigns
```

## Authentication Flow

```mermaid
sequenceDiagram
    participant Client as AmazonAdsClient
    participant Auth as AuthManager
    participant Lock as asyncio.Lock
    participant Amazon as Amazon OAuth

    Client->>Auth: get_access_token()
    Auth->>Auth: check expiry
    alt token valid
        Auth-->>Client: return cached token
    else token expired
        Auth->>Lock: acquire()
        Lock->>Auth: lock acquired
        Auth->>Auth: double-check expiry
        alt still expired
            Auth->>Amazon: POST /auth/o2/token
            Amazon-->>Auth: access_token + expires_in
            Auth->>Auth: cache token
        end
        Auth->>Lock: release()
        Auth-->>Client: return token
    end
```

## Retry Logic

```mermaid
flowchart TD
    Request[HTTP Request] --> Error{Error Type?}

    Error -->|Network Error| Retry[Retry with Backoff]
    Error -->|Timeout| Retry
    Error -->|429 Rate Limit| Retry
    Error -->|401 Unauthorized| Refresh[Refresh Token]

    Refresh --> Retry
    Retry --> MaxRetries{Max Retries?}
    MaxRetries -->|No| Request
    MaxRetries -->|Yes| Fail[Raise Exception]

    Error -->|4xx Client Error| ClientError[Raise AmazonAPIError]
    Error -->|5xx Server Error| Retry
    Error -->|Success| Return[Return Response]

    Retry --> Wait[Exponential Backoff + Jitter]
    Wait --> Request
```

## Pagination Flow

```mermaid
flowchart LR
    Start[Start Pagination] --> First[Request Page 1]
    First --> Yield[Yield Items]
    Yield --> More{More Pages?}
    More -->|Yes| Next[Request Next Page]
    Next --> Yield
    More -->|No| End[End]

    subgraph AutoPagination
        direction TB
        First
        Next
        Yield
        More
    end
```

## Package Structure

```mermaid
flowchart TB
    subgraph Package["aio_amazon_ads"]
        Init["__init__.py<br/>Exports & Marketplace"]
        Client["client.py<br/>AmazonAdsClient"]
        Base["base.py<br/>BaseClient + Retry"]
        Exceptions["exceptions.py<br/>Error Classes"]
        Validation["validation.py<br/>Input Validation"]

        subgraph Services["services/"]
            SP["sp/<br/>31 endpoints"]
            SB["sb/<br/>16 endpoints"]
            SD["sd/<br/>8 endpoints"]
            Portfolios["portfolios/<br/>5 endpoints"]
            Profiles["profiles/<br/>2 endpoints"]
        end

        subgraph Models["models/"]
            Pydantic["Pydantic Models<br/>(optional)"]
        end
    end

    Client --> Base
    Client --> SP
    Client --> SB
    Client --> SD
    Client --> Portfolios
    Client --> Profiles

    SP --> Base
    SB --> Base
    SD --> Base
    Portfolios --> Base
    Profiles --> Base

    Base --> Exceptions
    Services --> Validation
```

## Data Flow

```mermaid
flowchart LR
    subgraph Input
        Dict["dict/list"]
        Validation["Validation"]
    end

    subgraph Processing
        Service["Service Method"]
        Base["BaseClient.request()"]
        Retry["Tenacity Retry"]
    end

    subgraph Output
        Response["API Response"]
        Parsed["Parsed JSON"]
        Generator["AsyncGenerator"]
    end

    Dict --> Validation
    Validation --> Service
    Service --> Base
    Base --> Retry
    Retry --> Response
    Response --> Parsed
    Parsed --> Generator
```

## Error Hierarchy

```mermaid
classDiagram
    class Exception
    class AmazonAPIError
    class AuthenticationError
    class ThrottlingError
    class ValidationError
    class NotFoundError

    Exception <|-- AmazonAPIError
    AmazonAPIError <|-- AuthenticationError
    AmazonAPIError <|-- ThrottlingError
    AmazonAPIError <|-- ValidationError
    AmazonAPIError <|-- NotFoundError
```

## CI/CD Pipeline

```mermaid
flowchart LR
    subgraph Local
        Code[Code Changes]
        Lint[ruff check/format]
        TypeCheck[mypy]
        Test[pytest]
    end

    subgraph GitHub
        Push[Push to GitHub]
        CI[GitHub Actions CI]
        Test310[Python 3.10]
        Test311[Python 3.11]
        Test312[Python 3.12]
        Test313[Python 3.13]
        Test314[Python 3.14]
        Coverage[Codecov]
    end

    subgraph Release
        Tag[Version Tag]
        Release[Release Workflow]
        PyPI[PyPI Publish]
    end

    Code --> Lint
    Lint --> TypeCheck
    TypeCheck --> Test
    Test --> Push
    Push --> CI
    CI --> Test310
    CI --> Test311
    CI --> Test312
    CI --> Test313
    CI --> Test314
    Test310 --> Coverage
    Test311 --> Coverage
    Test312 --> Coverage
    Test313 --> Coverage
    Test314 --> Coverage

    Test --> Tag
    Tag --> Release
    Release --> PyPI
```

## Key Design Decisions

### 1. Native Async
- Built on `httpx` for true async/await
- No sync wrapper overhead
- Proper connection pooling

### 2. Service Namespacing
```python
client.sp.campaigns.list()      # Sponsored Products
client.sb.campaigns.list()      # Sponsored Brands
client.sd.campaigns.list()      # Sponsored Display
```

### 3. Auto-Pagination
- All `list()` methods return `AsyncGenerator`
- Automatically fetches all pages
- Memory efficient for large datasets

### 4. Tenacity Retry
- Exponential backoff with jitter
- Configurable retry count
- Handles 401, 429, network errors

### 5. Token Management
- Automatic refresh on expiry
- Lock prevents concurrent refresh
- Transparent to user

### 6. Observability
- Structured logging with correlation IDs
- X-Amzn-Request-Id tracking
- Debug logging for all requests
