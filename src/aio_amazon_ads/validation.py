"""Pure validation functions for Amazon Advertising API.

All functions are pure (no side effects) and follow guard clause pattern.
"""

from typing import Any, Dict, List, Optional


# Campaign validation
VALID_CAMPAIGN_STATES = frozenset(["ENABLED", "PAUSED", "ARCHIVED"])
VALID_TARGETING_TYPES = frozenset(["MANUAL", "AUTO"])
VALID_CAMPAIGN_TYPES = frozenset(["sponsoredProducts", "sponsoredBrands", "sponsoredDisplay"])


def validate_campaign_state(state: Optional[str]) -> None:
    """Validate campaign state.

    Args:
        state: Campaign state to validate

    Raises:
        ValueError: If state is invalid
    """
    if state is None:
        return
    if state not in VALID_CAMPAIGN_STATES:
        raise ValueError(f"Invalid state: {state}. Must be one of: {VALID_CAMPAIGN_STATES}")


def validate_targeting_type(targeting_type: Optional[str]) -> None:
    """Validate targeting type.

    Args:
        targeting_type: Targeting type to validate

    Raises:
        ValueError: If targeting type is invalid
    """
    if targeting_type is None:
        return
    if targeting_type not in VALID_TARGETING_TYPES:
        raise ValueError(
            f"Invalid targeting_type: {targeting_type}. Must be one of: {VALID_TARGETING_TYPES}"
        )


def validate_campaign_type(campaign_type: Optional[str]) -> None:
    """Validate campaign type.

    Args:
        campaign_type: Campaign type to validate

    Raises:
        ValueError: If campaign type is invalid
    """
    if campaign_type is None:
        return
    if campaign_type not in VALID_CAMPAIGN_TYPES:
        raise ValueError(
            f"Invalid campaign_type: {campaign_type}. Must be one of: {VALID_CAMPAIGN_TYPES}"
        )


def validate_campaign_id(campaign_id: Optional[str]) -> str:
    """Validate and return campaign ID.

    Args:
        campaign_id: Campaign ID to validate

    Returns:
        Validated campaign ID

    Raises:
        ValueError: If campaign_id is empty or None
    """
    if not campaign_id:
        raise ValueError("campaign_id is required")
    return campaign_id


def validate_campaigns_for_update(campaigns: List[Dict]) -> List[Dict]:
    """Validate campaigns for update operation.

    Args:
        campaigns: List of campaigns to validate

    Returns:
        Validated campaigns list

    Raises:
        ValueError: If validation fails
    """
    if not campaigns:
        raise ValueError("campaigns list cannot be empty")

    for i, campaign in enumerate(campaigns):
        if "campaignId" not in campaign:
            raise ValueError(f"Campaign at index {i} must have campaignId")

    return campaigns


def validate_campaigns_for_create(campaigns: List[Dict]) -> List[Dict]:
    """Validate campaigns for create operation.

    Args:
        campaigns: List of campaigns to validate

    Returns:
        Validated campaigns list

    Raises:
        ValueError: If validation fails
    """
    if not campaigns:
        raise ValueError("campaigns list cannot be empty")
    return campaigns


# Ad Group validation


def validate_ad_group_id(ad_group_id: Optional[str]) -> str:
    """Validate and return ad group ID.

    Args:
        ad_group_id: Ad group ID to validate

    Returns:
        Validated ad group ID

    Raises:
        ValueError: If ad_group_id is empty or None
    """
    if not ad_group_id:
        raise ValueError("ad_group_id is required")
    return ad_group_id


def validate_ad_groups_for_update(ad_groups: List[Dict]) -> List[Dict]:
    """Validate ad groups for update operation.

    Args:
        ad_groups: List of ad groups to validate

    Returns:
        Validated ad groups list

    Raises:
        ValueError: If validation fails
    """
    if not ad_groups:
        raise ValueError("ad_groups list cannot be empty")

    for i, ad_group in enumerate(ad_groups):
        if "adGroupId" not in ad_group:
            raise ValueError(f"Ad group at index {i} must have adGroupId")

    return ad_groups


def validate_ad_groups_for_create(ad_groups: List[Dict]) -> List[Dict]:
    """Validate ad groups for create operation.

    Args:
        ad_groups: List of ad groups to validate

    Returns:
        Validated ad groups list

    Raises:
        ValueError: If validation fails
    """
    if not ad_groups:
        raise ValueError("ad_groups list cannot be empty")
    return ad_groups


# Keyword validation
VALID_KEYWORD_MATCH_TYPES = frozenset(["EXACT", "PHRASE", "BROAD"])


def validate_keyword_match_type(match_type: Optional[str]) -> None:
    """Validate keyword match type.

    Args:
        match_type: Match type to validate

    Raises:
        ValueError: If match type is invalid
    """
    if match_type is None:
        return
    if match_type not in VALID_KEYWORD_MATCH_TYPES:
        raise ValueError(
            f"Invalid match_type: {match_type}. Must be one of: {VALID_KEYWORD_MATCH_TYPES}"
        )


def validate_keyword_id(keyword_id: Optional[str]) -> str:
    """Validate and return keyword ID.

    Args:
        keyword_id: Keyword ID to validate

    Returns:
        Validated keyword ID

    Raises:
        ValueError: If keyword_id is empty or None
    """
    if not keyword_id:
        raise ValueError("keyword_id is required")
    return keyword_id


def validate_keywords_for_create(keywords: List[Dict]) -> List[Dict]:
    """Validate keywords for create operation.

    Args:
        keywords: List of keywords to validate

    Returns:
        Validated keywords list

    Raises:
        ValueError: If validation fails
    """
    if not keywords:
        raise ValueError("keywords list cannot be empty")
    return keywords


# Product Ad validation


def validate_ad_id(ad_id: Optional[str]) -> str:
    """Validate and return ad ID.

    Args:
        ad_id: Ad ID to validate

    Returns:
        Validated ad ID

    Raises:
        ValueError: If ad_id is empty or None
    """
    if not ad_id:
        raise ValueError("ad_id is required")
    return ad_id


# Target validation


def validate_target_id(target_id: Optional[str]) -> str:
    """Validate and return target ID.

    Args:
        target_id: Target ID to validate

    Returns:
        Validated target ID

    Raises:
        ValueError: If target_id is empty or None
    """
    if not target_id:
        raise ValueError("target_id is required")
    return target_id


# Portfolio validation


def validate_portfolio_id(portfolio_id: Optional[str]) -> str:
    """Validate and return portfolio ID.

    Args:
        portfolio_id: Portfolio ID to validate

    Returns:
        Validated portfolio ID

    Raises:
        ValueError: If portfolio_id is empty or None
    """
    if not portfolio_id:
        raise ValueError("portfolio_id is required")
    return portfolio_id


def validate_portfolios_for_update(portfolios: List[Dict]) -> List[Dict]:
    """Validate portfolios for update operation.

    Args:
        portfolios: List of portfolios to validate

    Returns:
        Validated portfolios list

    Raises:
        ValueError: If validation fails
    """
    if not portfolios:
        raise ValueError("portfolios list cannot be empty")

    for i, portfolio in enumerate(portfolios):
        if "portfolioId" not in portfolio:
            raise ValueError(f"Portfolio at index {i} must have portfolioId")

    return portfolios


def validate_portfolios_for_create(portfolios: List[Dict]) -> List[Dict]:
    """Validate portfolios for create operation.

    Args:
        portfolios: List of portfolios to validate

    Returns:
        Validated portfolios list

    Raises:
        ValueError: If validation fails
    """
    if not portfolios:
        raise ValueError("portfolios list cannot be empty")
    return portfolios


# Profile validation


def validate_profile_id(profile_id: Optional[str]) -> str:
    """Validate and return profile ID.

    Args:
        profile_id: Profile ID to validate

    Returns:
        Validated profile ID

    Raises:
        ValueError: If profile_id is empty or None
    """
    if not profile_id:
        raise ValueError("profile_id is required")
    return profile_id
