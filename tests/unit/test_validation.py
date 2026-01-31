"""Comprehensive unit tests for validation functions."""

import sys

import pytest

sys.path.insert(0, "src")

from aio_amazon_ads.validation import (
    VALID_CAMPAIGN_STATES,
    VALID_CAMPAIGN_TYPES,
    VALID_KEYWORD_MATCH_TYPES,
    VALID_TARGETING_TYPES,
    validate_ad_group_id,
    validate_ad_groups_for_create,
    validate_ad_groups_for_update,
    validate_ad_id,
    validate_campaign_id,
    validate_campaign_state,
    validate_campaign_type,
    validate_campaigns_for_create,
    validate_campaigns_for_update,
    validate_keyword_id,
    validate_keyword_match_type,
    validate_keywords_for_create,
    validate_keywords_for_update,
    validate_negative_keyword_id,
    validate_negative_keywords_for_create,
    validate_negative_keywords_for_delete,
    validate_portfolio_id,
    validate_portfolios_for_create,
    validate_portfolios_for_update,
    validate_product_ads_for_create,
    validate_product_ads_for_update,
    validate_profile_id,
    validate_target_id,
    validate_targeting_type,
    validate_targets_for_create,
    validate_targets_for_update,
)


class TestValidateCampaignState:
    """Tests for validate_campaign_state."""

    def test_valid_states(self):
        """Test all valid campaign states."""
        for state in VALID_CAMPAIGN_STATES:
            validate_campaign_state(state)

    def test_none_state(self):
        """Test None state is allowed."""
        validate_campaign_state(None)

    def test_invalid_state(self):
        """Test invalid state raises ValueError."""
        with pytest.raises(ValueError, match="Invalid state"):
            validate_campaign_state("INVALID")

    def test_empty_string_state(self):
        """Test empty string state raises ValueError."""
        with pytest.raises(ValueError, match="Invalid state"):
            validate_campaign_state("")

    def test_lowercase_state(self):
        """Test lowercase state raises ValueError."""
        with pytest.raises(ValueError, match="Invalid state"):
            validate_campaign_state("enabled")


class TestValidateTargetingType:
    """Tests for validate_targeting_type."""

    def test_valid_targeting_types(self):
        """Test all valid targeting types."""
        for targeting_type in VALID_TARGETING_TYPES:
            validate_targeting_type(targeting_type)

    def test_none_targeting_type(self):
        """Test None targeting type is allowed."""
        validate_targeting_type(None)

    def test_invalid_targeting_type(self):
        """Test invalid targeting type raises ValueError."""
        with pytest.raises(ValueError, match="Invalid targeting_type"):
            validate_targeting_type("INVALID")

    def test_empty_string_targeting_type(self):
        """Test empty string targeting type raises ValueError."""
        with pytest.raises(ValueError, match="Invalid targeting_type"):
            validate_targeting_type("")

    def test_lowercase_targeting_type(self):
        """Test lowercase targeting type raises ValueError."""
        with pytest.raises(ValueError, match="Invalid targeting_type"):
            validate_targeting_type("manual")


class TestValidateCampaignType:
    """Tests for validate_campaign_type."""

    def test_valid_campaign_types(self):
        """Test all valid campaign types."""
        for campaign_type in VALID_CAMPAIGN_TYPES:
            validate_campaign_type(campaign_type)

    def test_none_campaign_type(self):
        """Test None campaign type is allowed."""
        validate_campaign_type(None)

    def test_invalid_campaign_type(self):
        """Test invalid campaign type raises ValueError."""
        with pytest.raises(ValueError, match="Invalid campaign_type"):
            validate_campaign_type("INVALID")

    def test_empty_string_campaign_type(self):
        """Test empty string campaign type raises ValueError."""
        with pytest.raises(ValueError, match="Invalid campaign_type"):
            validate_campaign_type("")

    def test_lowercase_campaign_type(self):
        """Test lowercase campaign type raises ValueError."""
        with pytest.raises(ValueError, match="Invalid campaign_type"):
            validate_campaign_type("sponsoredproducts")


class TestValidateCampaignId:
    """Tests for validate_campaign_id."""

    def test_valid_campaign_id(self):
        """Test valid campaign ID is returned."""
        result = validate_campaign_id("123456789")
        assert result == "123456789"

    def test_string_number_campaign_id(self):
        """Test string number campaign ID is valid."""
        result = validate_campaign_id("123")
        assert result == "123"

    def test_none_campaign_id(self):
        """Test None campaign ID raises ValueError."""
        with pytest.raises(ValueError, match="campaign_id is required"):
            validate_campaign_id(None)

    def test_empty_string_campaign_id(self):
        """Test empty string campaign ID raises ValueError."""
        with pytest.raises(ValueError, match="campaign_id is required"):
            validate_campaign_id("")


class TestValidateCampaignsForUpdate:
    """Tests for validate_campaigns_for_update."""

    def test_valid_campaigns_for_update(self):
        """Test valid campaigns list for update."""
        campaigns = [{"campaignId": "123"}, {"campaignId": "456"}]
        result = validate_campaigns_for_update(campaigns)
        assert result == campaigns

    def test_single_campaign_for_update(self):
        """Test single campaign for update."""
        campaigns = [{"campaignId": "123"}]
        result = validate_campaigns_for_update(campaigns)
        assert result == campaigns

    def test_empty_list_for_update(self):
        """Test empty list raises ValueError."""
        with pytest.raises(ValueError, match="campaigns list cannot be empty"):
            validate_campaigns_for_update([])

    def test_missing_campaign_id(self):
        """Test campaign without campaignId raises ValueError."""
        campaigns = [{"name": "Campaign"}]
        with pytest.raises(ValueError, match="must have campaignId"):
            validate_campaigns_for_update(campaigns)

    def test_multiple_campaigns_one_missing_id(self):
        """Test campaigns list with one missing ID raises ValueError."""
        campaigns = [{"campaignId": "123"}, {"name": "Campaign"}]
        with pytest.raises(ValueError, match="Campaign at index 1 must have campaignId"):
            validate_campaigns_for_update(campaigns)


class TestValidateCampaignsForCreate:
    """Tests for validate_campaigns_for_create."""

    def test_valid_campaigns_for_create(self):
        """Test valid campaigns list for create."""
        campaigns = [{"name": "Campaign 1"}, {"name": "Campaign 2"}]
        result = validate_campaigns_for_create(campaigns)
        assert result == campaigns

    def test_single_campaign_for_create(self):
        """Test single campaign for create."""
        campaigns = [{"name": "Campaign"}]
        result = validate_campaigns_for_create(campaigns)
        assert result == campaigns

    def test_empty_list_for_create(self):
        """Test empty list raises ValueError."""
        with pytest.raises(ValueError, match="campaigns list cannot be empty"):
            validate_campaigns_for_create([])


class TestValidateAdGroupId:
    """Tests for validate_ad_group_id."""

    def test_valid_ad_group_id(self):
        """Test valid ad group ID is returned."""
        result = validate_ad_group_id("123456789")
        assert result == "123456789"

    def test_string_number_ad_group_id(self):
        """Test string number ad group ID is valid."""
        result = validate_ad_group_id("123")
        assert result == "123"

    def test_none_ad_group_id(self):
        """Test None ad group ID raises ValueError."""
        with pytest.raises(ValueError, match="ad_group_id is required"):
            validate_ad_group_id(None)

    def test_empty_string_ad_group_id(self):
        """Test empty string ad group ID raises ValueError."""
        with pytest.raises(ValueError, match="ad_group_id is required"):
            validate_ad_group_id("")


class TestValidateAdGroupsForUpdate:
    """Tests for validate_ad_groups_for_update."""

    def test_valid_ad_groups_for_update(self):
        """Test valid ad groups list for update."""
        ad_groups = [{"adGroupId": "123"}, {"adGroupId": "456"}]
        result = validate_ad_groups_for_update(ad_groups)
        assert result == ad_groups

    def test_single_ad_group_for_update(self):
        """Test single ad group for update."""
        ad_groups = [{"adGroupId": "123"}]
        result = validate_ad_groups_for_update(ad_groups)
        assert result == ad_groups

    def test_empty_list_for_update(self):
        """Test empty list raises ValueError."""
        with pytest.raises(ValueError, match="ad_groups list cannot be empty"):
            validate_ad_groups_for_update([])

    def test_missing_ad_group_id(self):
        """Test ad group without adGroupId raises ValueError."""
        ad_groups = [{"name": "Ad Group"}]
        with pytest.raises(ValueError, match="must have adGroupId"):
            validate_ad_groups_for_update(ad_groups)

    def test_multiple_ad_groups_one_missing_id(self):
        """Test ad groups list with one missing ID raises ValueError."""
        ad_groups = [{"adGroupId": "123"}, {"name": "Ad Group"}]
        with pytest.raises(ValueError, match="Ad group at index 1 must have adGroupId"):
            validate_ad_groups_for_update(ad_groups)


class TestValidateAdGroupsForCreate:
    """Tests for validate_ad_groups_for_create."""

    def test_valid_ad_groups_for_create(self):
        """Test valid ad groups list for create."""
        ad_groups = [{"name": "Ad Group 1"}, {"name": "Ad Group 2"}]
        result = validate_ad_groups_for_create(ad_groups)
        assert result == ad_groups

    def test_single_ad_group_for_create(self):
        """Test single ad group for create."""
        ad_groups = [{"name": "Ad Group"}]
        result = validate_ad_groups_for_create(ad_groups)
        assert result == ad_groups

    def test_empty_list_for_create(self):
        """Test empty list raises ValueError."""
        with pytest.raises(ValueError, match="ad_groups list cannot be empty"):
            validate_ad_groups_for_create([])


class TestValidateKeywordMatchType:
    """Tests for validate_keyword_match_type."""

    def test_valid_match_types(self):
        """Test all valid keyword match types."""
        for match_type in VALID_KEYWORD_MATCH_TYPES:
            validate_keyword_match_type(match_type)

    def test_none_match_type(self):
        """Test None match type is allowed."""
        validate_keyword_match_type(None)

    def test_invalid_match_type(self):
        """Test invalid match type raises ValueError."""
        with pytest.raises(ValueError, match="Invalid match_type"):
            validate_keyword_match_type("INVALID")

    def test_empty_string_match_type(self):
        """Test empty string match type raises ValueError."""
        with pytest.raises(ValueError, match="Invalid match_type"):
            validate_keyword_match_type("")

    def test_lowercase_match_type(self):
        """Test lowercase match type raises ValueError."""
        with pytest.raises(ValueError, match="Invalid match_type"):
            validate_keyword_match_type("exact")


class TestValidateKeywordId:
    """Tests for validate_keyword_id."""

    def test_valid_keyword_id(self):
        """Test valid keyword ID is returned."""
        result = validate_keyword_id("123456789")
        assert result == "123456789"

    def test_string_number_keyword_id(self):
        """Test string number keyword ID is valid."""
        result = validate_keyword_id("123")
        assert result == "123"

    def test_none_keyword_id(self):
        """Test None keyword ID raises ValueError."""
        with pytest.raises(ValueError, match="keyword_id is required"):
            validate_keyword_id(None)

    def test_empty_string_keyword_id(self):
        """Test empty string keyword ID raises ValueError."""
        with pytest.raises(ValueError, match="keyword_id is required"):
            validate_keyword_id("")


class TestValidateKeywordsForCreate:
    """Tests for validate_keywords_for_create."""

    def test_valid_keywords_for_create(self):
        """Test valid keywords list for create."""
        keywords = [
            {"keywordText": "keyword1", "matchType": "EXACT"},
            {"keywordText": "keyword2", "matchType": "PHRASE"},
        ]
        result = validate_keywords_for_create(keywords)
        assert result == keywords

    def test_single_keyword_for_create(self):
        """Test single keyword for create."""
        keywords = [{"keywordText": "keyword", "matchType": "BROAD"}]
        result = validate_keywords_for_create(keywords)
        assert result == keywords

    def test_empty_list_for_create(self):
        """Test empty list raises ValueError."""
        with pytest.raises(ValueError, match="keywords list cannot be empty"):
            validate_keywords_for_create([])


class TestValidateKeywordsForUpdate:
    """Tests for validate_keywords_for_update."""

    def test_valid_keywords_for_update(self):
        """Test valid keywords list for update."""
        keywords = [{"keywordId": "123"}, {"keywordId": "456"}]
        result = validate_keywords_for_update(keywords)
        assert result == keywords

    def test_single_keyword_for_update(self):
        """Test single keyword for update."""
        keywords = [{"keywordId": "123"}]
        result = validate_keywords_for_update(keywords)
        assert result == keywords

    def test_empty_list_for_update(self):
        """Test empty list raises ValueError."""
        with pytest.raises(ValueError, match="keywords list cannot be empty"):
            validate_keywords_for_update([])

    def test_missing_keyword_id(self):
        """Test keyword without keywordId raises ValueError."""
        keywords = [{"keywordText": "keyword"}]
        with pytest.raises(ValueError, match="must have keywordId"):
            validate_keywords_for_update(keywords)

    def test_multiple_keywords_one_missing_id(self):
        """Test keywords list with one missing ID raises ValueError."""
        keywords = [{"keywordId": "123"}, {"keywordText": "keyword"}]
        with pytest.raises(ValueError, match="Keyword at index 1 must have keywordId"):
            validate_keywords_for_update(keywords)


class TestValidateAdId:
    """Tests for validate_ad_id."""

    def test_valid_ad_id(self):
        """Test valid ad ID is returned."""
        result = validate_ad_id("123456789")
        assert result == "123456789"

    def test_string_number_ad_id(self):
        """Test string number ad ID is valid."""
        result = validate_ad_id("123")
        assert result == "123"

    def test_none_ad_id(self):
        """Test None ad ID raises ValueError."""
        with pytest.raises(ValueError, match="ad_id is required"):
            validate_ad_id(None)

    def test_empty_string_ad_id(self):
        """Test empty string ad ID raises ValueError."""
        with pytest.raises(ValueError, match="ad_id is required"):
            validate_ad_id("")


class TestValidateProductAdsForCreate:
    """Tests for validate_product_ads_for_create."""

    def test_valid_ads_for_create(self):
        """Test valid product ads list for create."""
        ads = [{"campaignId": "123", "adGroupId": "456"}, {"campaignId": "789", "adGroupId": "012"}]
        result = validate_product_ads_for_create(ads)
        assert result == ads

    def test_single_ad_for_create(self):
        """Test single product ad for create."""
        ads = [{"campaignId": "123", "adGroupId": "456"}]
        result = validate_product_ads_for_create(ads)
        assert result == ads

    def test_empty_list_for_create(self):
        """Test empty list raises ValueError."""
        with pytest.raises(ValueError, match="ads list cannot be empty"):
            validate_product_ads_for_create([])


class TestValidateProductAdsForUpdate:
    """Tests for validate_product_ads_for_update."""

    def test_valid_ads_for_update(self):
        """Test valid product ads list for update."""
        ads = [{"adId": "123"}, {"adId": "456"}]
        result = validate_product_ads_for_update(ads)
        assert result == ads

    def test_single_ad_for_update(self):
        """Test single product ad for update."""
        ads = [{"adId": "123"}]
        result = validate_product_ads_for_update(ads)
        assert result == ads

    def test_empty_list_for_update(self):
        """Test empty list raises ValueError."""
        with pytest.raises(ValueError, match="ads list cannot be empty"):
            validate_product_ads_for_update([])

    def test_missing_ad_id(self):
        """Test ad without adId raises ValueError."""
        ads = [{"state": "ENABLED"}]
        with pytest.raises(ValueError, match="must have adId"):
            validate_product_ads_for_update(ads)

    def test_multiple_ads_one_missing_id(self):
        """Test ads list with one missing ID raises ValueError."""
        ads = [{"adId": "123"}, {"state": "ENABLED"}]
        with pytest.raises(ValueError, match="Product ad at index 1 must have adId"):
            validate_product_ads_for_update(ads)


class TestValidateTargetId:
    """Tests for validate_target_id."""

    def test_valid_target_id(self):
        """Test valid target ID is returned."""
        result = validate_target_id("123456789")
        assert result == "123456789"

    def test_string_number_target_id(self):
        """Test string number target ID is valid."""
        result = validate_target_id("123")
        assert result == "123"

    def test_none_target_id(self):
        """Test None target ID raises ValueError."""
        with pytest.raises(ValueError, match="target_id is required"):
            validate_target_id(None)

    def test_empty_string_target_id(self):
        """Test empty string target ID raises ValueError."""
        with pytest.raises(ValueError, match="target_id is required"):
            validate_target_id("")


class TestValidateTargetsForCreate:
    """Tests for validate_targets_for_create."""

    def test_valid_targets_for_create(self):
        """Test valid targets list for create."""
        targets = [{"expression": [{"type": "asin"}]}, {"expression": [{"type": "category"}]}]
        result = validate_targets_for_create(targets)
        assert result == targets

    def test_single_target_for_create(self):
        """Test single target for create."""
        targets = [{"expression": [{"type": "asin"}]}]
        result = validate_targets_for_create(targets)
        assert result == targets

    def test_empty_list_for_create(self):
        """Test empty list raises ValueError."""
        with pytest.raises(ValueError, match="targets list cannot be empty"):
            validate_targets_for_create([])


class TestValidateTargetsForUpdate:
    """Tests for validate_targets_for_update."""

    def test_valid_targets_for_update(self):
        """Test valid targets list for update."""
        targets = [{"targetId": "123"}, {"targetId": "456"}]
        result = validate_targets_for_update(targets)
        assert result == targets

    def test_single_target_for_update(self):
        """Test single target for update."""
        targets = [{"targetId": "123"}]
        result = validate_targets_for_update(targets)
        assert result == targets

    def test_empty_list_for_update(self):
        """Test empty list raises ValueError."""
        with pytest.raises(ValueError, match="targets list cannot be empty"):
            validate_targets_for_update([])

    def test_missing_target_id(self):
        """Test target without targetId raises ValueError."""
        targets = [{"state": "ENABLED"}]
        with pytest.raises(ValueError, match="must have targetId"):
            validate_targets_for_update(targets)

    def test_multiple_targets_one_missing_id(self):
        """Test targets list with one missing ID raises ValueError."""
        targets = [{"targetId": "123"}, {"state": "ENABLED"}]
        with pytest.raises(ValueError, match="Target at index 1 must have targetId"):
            validate_targets_for_update(targets)


class TestValidateNegativeKeywordId:
    """Tests for validate_negative_keyword_id."""

    def test_valid_negative_keyword_id(self):
        """Test valid negative keyword ID is returned."""
        result = validate_negative_keyword_id("123456789")
        assert result == "123456789"

    def test_string_number_negative_keyword_id(self):
        """Test string number negative keyword ID is valid."""
        result = validate_negative_keyword_id("123")
        assert result == "123"

    def test_none_negative_keyword_id(self):
        """Test None negative keyword ID raises ValueError."""
        with pytest.raises(ValueError, match="keyword_id is required"):
            validate_negative_keyword_id(None)

    def test_empty_string_negative_keyword_id(self):
        """Test empty string negative keyword ID raises ValueError."""
        with pytest.raises(ValueError, match="keyword_id is required"):
            validate_negative_keyword_id("")


class TestValidateNegativeKeywordsForCreate:
    """Tests for validate_negative_keywords_for_create."""

    def test_valid_negative_keywords_for_create(self):
        """Test valid negative keywords list for create."""
        keywords = [
            {"keywordText": "keyword1", "matchType": "NEGATIVE_EXACT"},
            {"keywordText": "keyword2", "matchType": "NEGATIVE_PHRASE"},
        ]
        result = validate_negative_keywords_for_create(keywords)
        assert result == keywords

    def test_single_negative_keyword_for_create(self):
        """Test single negative keyword for create."""
        keywords = [{"keywordText": "keyword", "matchType": "NEGATIVE_EXACT"}]
        result = validate_negative_keywords_for_create(keywords)
        assert result == keywords

    def test_empty_list_for_create(self):
        """Test empty list raises ValueError."""
        with pytest.raises(ValueError, match="keywords list cannot be empty"):
            validate_negative_keywords_for_create([])


class TestValidateNegativeKeywordsForDelete:
    """Tests for validate_negative_keywords_for_delete."""

    def test_valid_negative_keyword_id_for_delete(self):
        """Test valid negative keyword ID is returned."""
        result = validate_negative_keywords_for_delete("123456789")
        assert result == "123456789"

    def test_string_number_negative_keyword_id_for_delete(self):
        """Test string number negative keyword ID is valid."""
        result = validate_negative_keywords_for_delete("123")
        assert result == "123"

    def test_none_negative_keyword_id_for_delete(self):
        """Test None negative keyword ID raises ValueError."""
        with pytest.raises(ValueError, match="keyword_id is required"):
            validate_negative_keywords_for_delete(None)

    def test_empty_string_negative_keyword_id_for_delete(self):
        """Test empty string negative keyword ID raises ValueError."""
        with pytest.raises(ValueError, match="keyword_id is required"):
            validate_negative_keywords_for_delete("")


class TestValidatePortfolioId:
    """Tests for validate_portfolio_id."""

    def test_valid_portfolio_id(self):
        """Test valid portfolio ID is returned."""
        result = validate_portfolio_id("123456789")
        assert result == "123456789"

    def test_string_number_portfolio_id(self):
        """Test string number portfolio ID is valid."""
        result = validate_portfolio_id("123")
        assert result == "123"

    def test_none_portfolio_id(self):
        """Test None portfolio ID raises ValueError."""
        with pytest.raises(ValueError, match="portfolio_id is required"):
            validate_portfolio_id(None)

    def test_empty_string_portfolio_id(self):
        """Test empty string portfolio ID raises ValueError."""
        with pytest.raises(ValueError, match="portfolio_id is required"):
            validate_portfolio_id("")


class TestValidatePortfoliosForUpdate:
    """Tests for validate_portfolios_for_update."""

    def test_valid_portfolios_for_update(self):
        """Test valid portfolios list for update."""
        portfolios = [{"portfolioId": "123"}, {"portfolioId": "456"}]
        result = validate_portfolios_for_update(portfolios)
        assert result == portfolios

    def test_single_portfolio_for_update(self):
        """Test single portfolio for update."""
        portfolios = [{"portfolioId": "123"}]
        result = validate_portfolios_for_update(portfolios)
        assert result == portfolios

    def test_empty_list_for_update(self):
        """Test empty list raises ValueError."""
        with pytest.raises(ValueError, match="portfolios list cannot be empty"):
            validate_portfolios_for_update([])

    def test_missing_portfolio_id(self):
        """Test portfolio without portfolioId raises ValueError."""
        portfolios = [{"name": "Portfolio"}]
        with pytest.raises(ValueError, match="must have portfolioId"):
            validate_portfolios_for_update(portfolios)

    def test_multiple_portfolios_one_missing_id(self):
        """Test portfolios list with one missing ID raises ValueError."""
        portfolios = [{"portfolioId": "123"}, {"name": "Portfolio"}]
        with pytest.raises(ValueError, match="Portfolio at index 1 must have portfolioId"):
            validate_portfolios_for_update(portfolios)


class TestValidatePortfoliosForCreate:
    """Tests for validate_portfolios_for_create."""

    def test_valid_portfolios_for_create(self):
        """Test valid portfolios list for create."""
        portfolios = [{"name": "Portfolio 1"}, {"name": "Portfolio 2"}]
        result = validate_portfolios_for_create(portfolios)
        assert result == portfolios

    def test_single_portfolio_for_create(self):
        """Test single portfolio for create."""
        portfolios = [{"name": "Portfolio"}]
        result = validate_portfolios_for_create(portfolios)
        assert result == portfolios

    def test_empty_list_for_create(self):
        """Test empty list raises ValueError."""
        with pytest.raises(ValueError, match="portfolios list cannot be empty"):
            validate_portfolios_for_create([])


class TestValidateProfileId:
    """Tests for validate_profile_id."""

    def test_valid_profile_id(self):
        """Test valid profile ID is returned."""
        result = validate_profile_id("123456789")
        assert result == "123456789"

    def test_string_number_profile_id(self):
        """Test string number profile ID is valid."""
        result = validate_profile_id("123")
        assert result == "123"

    def test_none_profile_id(self):
        """Test None profile ID raises ValueError."""
        with pytest.raises(ValueError, match="profile_id is required"):
            validate_profile_id(None)

    def test_empty_string_profile_id(self):
        """Test empty string profile ID raises ValueError."""
        with pytest.raises(ValueError, match="profile_id is required"):
            validate_profile_id("")
