"""Unit tests for API configuration models."""

import pytest
from pydantic import ValidationError

from cluefin_cli.commands.inquiry.config_models import (
    APICategory,
    APIConfig,
    ParameterConfig,
)


class TestParameterConfig:
    """Test cases for ParameterConfig model."""

    def test_valid_select_parameter(self):
        """Test creating a valid select type parameter."""
        param = ParameterConfig(
            name="market_type",
            korean_name="시장구분",
            param_type="select",
            choices=[("001", "코스피"), ("101", "코스닥")],
        )

        assert param.name == "market_type"
        assert param.korean_name == "시장구분"
        assert param.param_type == "select"
        assert param.choices == [("001", "코스피"), ("101", "코스닥")]
        assert param.required is True  # default value

    def test_valid_text_parameter(self):
        """Test creating a valid text type parameter."""
        param = ParameterConfig(
            name="stock_code", korean_name="종목코드", param_type="text", validation=r"^\d{6}$", required=False
        )

        assert param.name == "stock_code"
        assert param.korean_name == "종목코드"
        assert param.param_type == "text"
        assert param.validation == r"^\d{6}$"
        assert param.required is False

    def test_valid_date_parameter(self):
        """Test creating a valid date type parameter."""
        param = ParameterConfig(name="base_date", korean_name="기준일자", param_type="date", validation=r"^\d{8}$")

        assert param.name == "base_date"
        assert param.korean_name == "기준일자"
        assert param.param_type == "date"
        assert param.validation == r"^\d{8}$"

    def test_select_parameter_without_choices_fails(self):
        """Test that select type parameters must have choices."""
        with pytest.raises(ValidationError) as exc_info:
            ParameterConfig(name="market_type", korean_name="시장구분", param_type="select")

        assert "choices must be provided for select type parameters" in str(exc_info.value)

    def test_invalid_choice_format_fails(self):
        """Test that choices must be properly formatted tuples."""
        with pytest.raises(ValidationError) as exc_info:
            ParameterConfig(
                name="market_type",
                korean_name="시장구분",
                param_type="select",
                choices=[("001", "코스피"), "invalid"],  # Invalid format
            )

        assert "Input should be a valid tuple" in str(exc_info.value)

    def test_invalid_choice_tuple_length_fails(self):
        """Test that choice tuples must have exactly 2 elements."""
        with pytest.raises(ValidationError) as exc_info:
            ParameterConfig(
                name="market_type",
                korean_name="시장구분",
                param_type="select",
                choices=[("001", "코스피", "extra")],  # Too many elements
            )

        assert "Tuple should have at most 2 items" in str(exc_info.value)

    def test_non_string_choice_values_fail(self):
        """Test that choice values and labels must be strings."""
        with pytest.raises(ValidationError) as exc_info:
            ParameterConfig(
                name="market_type",
                korean_name="시장구분",
                param_type="select",
                choices=[(1, "코스피")],  # Non-string value
            )

        assert "Input should be a valid string" in str(exc_info.value)

    def test_validation_with_select_type_fails(self):
        """Test that validation cannot be used with select type."""
        with pytest.raises(ValidationError) as exc_info:
            ParameterConfig(
                name="market_type",
                korean_name="시장구분",
                param_type="select",
                choices=[("001", "코스피")],
                validation=r"^\d+$",  # Invalid for select type
            )

        assert "validation can only be used with text or date type parameters" in str(exc_info.value)

    def test_invalid_param_type_fails(self):
        """Test that invalid parameter types are rejected."""
        with pytest.raises(ValidationError) as exc_info:
            ParameterConfig(name="test_param", korean_name="테스트", param_type="invalid_type")

        # Pydantic will reject the invalid literal value
        assert "Input should be 'select', 'text' or 'date'" in str(exc_info.value)


class TestAPIConfig:
    """Test cases for APIConfig model."""

    def test_valid_api_config(self):
        """Test creating a valid API configuration."""
        required_param = ParameterConfig(
            name="market_type", korean_name="시장구분", param_type="select", choices=[("001", "코스피")]
        )

        optional_param = ParameterConfig(
            name="sort_type", korean_name="정렬구분", param_type="select", choices=[("1", "오름차순")], required=False
        )

        api = APIConfig(
            name="test_api",
            korean_name="테스트 API",
            api_method="get_test_data",
            required_params=[required_param],
            optional_params=[optional_param],
            description="Test API description",
        )

        assert api.name == "test_api"
        assert api.korean_name == "테스트 API"
        assert api.api_method == "get_test_data"
        assert len(api.required_params) == 1
        assert len(api.optional_params) == 1
        assert api.description == "Test API description"

    def test_empty_params_allowed(self):
        """Test that APIs can have no parameters."""
        api = APIConfig(name="simple_api", korean_name="간단한 API", api_method="get_simple_data")

        assert len(api.required_params) == 0
        assert len(api.optional_params) == 0

    def test_duplicate_required_param_names_fail(self):
        """Test that duplicate parameter names in required params are rejected."""
        param1 = ParameterConfig(name="duplicate_name", korean_name="첫번째", param_type="text")

        param2 = ParameterConfig(name="duplicate_name", korean_name="두번째", param_type="text")

        with pytest.raises(ValidationError) as exc_info:
            APIConfig(
                name="test_api", korean_name="테스트 API", api_method="get_test_data", required_params=[param1, param2]
            )

        assert "Parameter names must be unique in required_params" in str(exc_info.value)

    def test_duplicate_optional_param_names_fail(self):
        """Test that duplicate parameter names in optional params are rejected."""
        param1 = ParameterConfig(name="duplicate_name", korean_name="첫번째", param_type="text", required=False)

        param2 = ParameterConfig(name="duplicate_name", korean_name="두번째", param_type="text", required=False)

        with pytest.raises(ValidationError) as exc_info:
            APIConfig(
                name="test_api", korean_name="테스트 API", api_method="get_test_data", optional_params=[param1, param2]
            )

        assert "Parameter names must be unique in optional_params" in str(exc_info.value)

    def test_duplicate_param_names_across_lists_fail(self):
        """Test that parameter names cannot be duplicated between required and optional."""
        required_param = ParameterConfig(name="shared_name", korean_name="필수 파라미터", param_type="text")

        optional_param = ParameterConfig(
            name="shared_name", korean_name="선택 파라미터", param_type="text", required=False
        )

        with pytest.raises(ValidationError) as exc_info:
            APIConfig(
                name="test_api",
                korean_name="테스트 API",
                api_method="get_test_data",
                required_params=[required_param],
                optional_params=[optional_param],
            )

        assert "Parameter names cannot appear in both required and optional" in str(exc_info.value)

    def test_get_all_params(self):
        """Test getting all parameters from an API config."""
        required_param = ParameterConfig(name="required_param", korean_name="필수", param_type="text")

        optional_param = ParameterConfig(name="optional_param", korean_name="선택", param_type="text", required=False)

        api = APIConfig(
            name="test_api",
            korean_name="테스트 API",
            api_method="get_test_data",
            required_params=[required_param],
            optional_params=[optional_param],
        )

        all_params = api.get_all_params()
        assert len(all_params) == 2
        assert all_params[0].name == "required_param"
        assert all_params[1].name == "optional_param"

    def test_get_param_by_name(self):
        """Test getting a parameter by name."""
        param = ParameterConfig(name="test_param", korean_name="테스트", param_type="text")

        api = APIConfig(name="test_api", korean_name="테스트 API", api_method="get_test_data", required_params=[param])

        found_param = api.get_param_by_name("test_param")
        assert found_param is not None
        assert found_param.name == "test_param"

        not_found = api.get_param_by_name("nonexistent")
        assert not_found is None


class TestAPICategory:
    """Test cases for APICategory model."""

    def test_valid_category(self):
        """Test creating a valid API category."""
        api1 = APIConfig(name="api1", korean_name="API 1", api_method="get_api1_data")

        api2 = APIConfig(name="api2", korean_name="API 2", api_method="get_api2_data")

        category = APICategory(
            name="test_category",
            korean_name="테스트 카테고리",
            apis=[api1, api2],
            description="Test category description",
        )

        assert category.name == "test_category"
        assert category.korean_name == "테스트 카테고리"
        assert len(category.apis) == 2
        assert category.description == "Test category description"

    def test_empty_category_allowed(self):
        """Test that categories can have no APIs."""
        category = APICategory(name="empty_category", korean_name="빈 카테고리")

        assert len(category.apis) == 0

    def test_duplicate_api_names_fail(self):
        """Test that duplicate API names in a category are rejected."""
        api1 = APIConfig(name="duplicate_name", korean_name="첫번째 API", api_method="get_first_data")

        api2 = APIConfig(name="duplicate_name", korean_name="두번째 API", api_method="get_second_data")

        with pytest.raises(ValidationError) as exc_info:
            APICategory(name="test_category", korean_name="테스트 카테고리", apis=[api1, api2])

        assert "API names must be unique within a category" in str(exc_info.value)

    def test_get_api_by_name(self):
        """Test getting an API by name from a category."""
        api = APIConfig(name="test_api", korean_name="테스트 API", api_method="get_test_data")

        category = APICategory(name="test_category", korean_name="테스트 카테고리", apis=[api])

        found_api = category.get_api_by_name("test_api")
        assert found_api is not None
        assert found_api.name == "test_api"

        not_found = category.get_api_by_name("nonexistent")
        assert not_found is None

    def test_get_api_choices(self):
        """Test getting API choices for menu display."""
        api1 = APIConfig(name="api1", korean_name="첫번째 API", api_method="get_first_data")

        api2 = APIConfig(name="api2", korean_name="두번째 API", api_method="get_second_data")

        category = APICategory(name="test_category", korean_name="테스트 카테고리", apis=[api1, api2])

        choices = category.get_api_choices()
        expected = [("api1", "첫번째 API"), ("api2", "두번째 API")]
        assert choices == expected


class TestModelIntegration:
    """Integration tests for model interactions."""

    def test_complex_api_configuration(self):
        """Test a complex API configuration with multiple parameter types."""
        # Create various parameter types
        market_param = ParameterConfig(
            name="market_type",
            korean_name="시장구분",
            param_type="select",
            choices=[("000", "전체"), ("001", "코스피"), ("101", "코스닥")],
        )

        date_param = ParameterConfig(name="base_date", korean_name="기준일자", param_type="date", validation=r"^\d{8}$")

        stock_param = ParameterConfig(
            name="stock_code", korean_name="종목코드", param_type="text", validation=r"^\d{6}$", required=False
        )

        # Create API configuration
        api = APIConfig(
            name="complex_ranking_api",
            korean_name="복합 순위 정보 API",
            api_method="get_complex_ranking_data",
            required_params=[market_param, date_param],
            optional_params=[stock_param],
            description="Complex ranking API with multiple parameter types",
        )

        # Verify the configuration
        assert len(api.get_all_params()) == 3
        assert api.get_param_by_name("market_type").param_type == "select"
        assert api.get_param_by_name("base_date").param_type == "date"
        assert api.get_param_by_name("stock_code").required is False

        # Create category with this API
        category = APICategory(name="ranking_info", korean_name="순위정보", apis=[api])

        # Verify category functionality
        found_api = category.get_api_by_name("complex_ranking_api")
        assert found_api is not None
        assert found_api.korean_name == "복합 순위 정보 API"

        choices = category.get_api_choices()
        assert choices == [("complex_ranking_api", "복합 순위 정보 API")]
