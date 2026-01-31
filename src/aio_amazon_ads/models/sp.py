
from pydantic import BaseModel, Field


class Campaign(BaseModel):
    campaignId: str
    name: str
    campaignType: str = Field(..., description="Type of campaign (e.g., 'sponsoredProducts')")
    targetingType: str = Field(..., description="Targeting type (e.g., 'manual', 'auto')")
    state: str = Field(..., description="Campaign state (e.g., 'ENABLED', 'PAUSED', 'ARCHIVED')")
    dailyBudget: float
    startDate: str = Field(..., description="Start date in YYYYMMDD format")
    endDate: str | None = Field(None, description="End date in YYYYMMDD format")
    premiumBidAdjustment: bool | None = None

    class Config:
        extra = "ignore"


class CampaignCreate(BaseModel):
    name: str
    campaignType: str = Field(..., description="Type of campaign (e.g., 'sponsoredProducts')")
    targetingType: str = Field(..., description="Targeting type (e.g., 'manual', 'auto')")
    state: str = Field(default="ENABLED", description="Campaign state (e.g., 'ENABLED', 'PAUSED')")
    dailyBudget: float
    startDate: str = Field(..., description="Start date in YYYYMMDD format")
    endDate: str | None = Field(None, description="End date in YYYYMMDD format")
    premiumBidAdjustment: bool | None = None

    class Config:
        extra = "ignore"


class CampaignUpdate(BaseModel):
    campaignId: str
    name: str | None = None
    state: str | None = Field(None, description="Campaign state (e.g., 'ENABLED', 'PAUSED')")
    dailyBudget: float | None = None
    startDate: str | None = Field(None, description="Start date in YYYYMMDD format")
    endDate: str | None = Field(None, description="End date in YYYYMMDD format")
    premiumBidAdjustment: bool | None = None

    class Config:
        extra = "ignore"


class AdGroup(BaseModel):
    adGroupId: str
    campaignId: str
    name: str
    state: str = Field(..., description="Ad group state (e.g., 'ENABLED', 'PAUSED')")
    defaultBid: float

    class Config:
        extra = "ignore"


class AdGroupCreate(BaseModel):
    campaignId: str
    name: str
    state: str = Field(default="ENABLED", description="Ad group state (e.g., 'ENABLED', 'PAUSED')")
    defaultBid: float

    class Config:
        extra = "ignore"


class AdGroupUpdate(BaseModel):
    adGroupId: str
    name: str | None = None
    state: str | None = Field(None, description="Ad group state (e.g., 'ENABLED', 'PAUSED')")
    defaultBid: float | None = None

    class Config:
        extra = "ignore"


class Keyword(BaseModel):
    keywordId: str
    campaignId: str
    adGroupId: str
    keywordText: str
    matchType: str = Field(..., description="Match type (e.g., 'broad', 'phrase', 'exact')")
    state: str = Field(..., description="Keyword state (e.g., 'ENABLED', 'PAUSED', 'ARCHIVED')")
    bid: float

    class Config:
        extra = "ignore"


class KeywordCreate(BaseModel):
    campaignId: str
    adGroupId: str
    keywordText: str
    matchType: str = Field(..., description="Match type (e.g., 'broad', 'phrase', 'exact')")
    state: str = Field(default="ENABLED", description="Keyword state (e.g., 'ENABLED', 'PAUSED')")
    bid: float

    class Config:
        extra = "ignore"


class KeywordUpdate(BaseModel):
    keywordId: str
    state: str | None = Field(None, description="Keyword state (e.g., 'ENABLED', 'PAUSED')")
    bid: float | None = None

    class Config:
        extra = "ignore"


class ProductAd(BaseModel):
    adId: str
    campaignId: str
    adGroupId: str
    sku: str | None = None
    asin: str | None = None
    state: str = Field(..., description="Ad state (e.g., 'ENABLED', 'PAUSED', 'ARCHIVED')")

    class Config:
        extra = "ignore"


class ProductAdCreate(BaseModel):
    campaignId: str
    adGroupId: str
    sku: str | None = None
    asin: str | None = None
    state: str = Field(default="ENABLED", description="Ad state (e.g., 'ENABLED', 'PAUSED')")

    class Config:
        extra = "ignore"


class ProductAdUpdate(BaseModel):
    adId: str
    state: str | None = Field(None, description="Ad state (e.g., 'ENABLED', 'PAUSED')")

    class Config:
        extra = "ignore"


class NegativeKeyword(BaseModel):
    keywordId: str
    campaignId: str | None = None
    adGroupId: str | None = None
    keywordText: str
    matchType: str = Field(..., description="Match type (e.g., 'negativeExact', 'negativePhrase')")
    state: str = Field(..., description="Keyword state (e.g., 'ENABLED', 'PAUSED', 'ARCHIVED')")

    class Config:
        extra = "ignore"


class NegativeKeywordCreate(BaseModel):
    campaignId: str | None = None
    adGroupId: str | None = None
    keywordText: str
    matchType: str = Field(..., description="Match type (e.g., 'negativeExact', 'negativePhrase')")
    state: str = Field(default="ENABLED", description="Keyword state (e.g., 'ENABLED', 'PAUSED')")

    class Config:
        extra = "ignore"


class NegativeKeywordUpdate(BaseModel):
    keywordId: str
    state: str | None = Field(None, description="Keyword state (e.g., 'ENABLED', 'PAUSED')")

    class Config:
        extra = "ignore"


class Target(BaseModel):
    targetId: str
    campaignId: str
    adGroupId: str | None = None
    expression: list[dict]
    state: str = Field(..., description="Target state (e.g., 'ENABLED', 'PAUSED', 'ARCHIVED')")
    bid: float | None = None

    class Config:
        extra = "ignore"


class TargetCreate(BaseModel):
    campaignId: str
    adGroupId: str | None = None
    expression: list[dict]
    state: str = Field(default="ENABLED", description="Target state (e.g., 'ENABLED', 'PAUSED')")
    bid: float | None = None

    class Config:
        extra = "ignore"


class TargetUpdate(BaseModel):
    targetId: str
    state: str | None = Field(None, description="Target state (e.g., 'ENABLED', 'PAUSED')")
    bid: float | None = None

    class Config:
        extra = "ignore"
