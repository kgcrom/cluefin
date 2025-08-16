"""Pydantic models for API configuration in the stock inquiry system."""

from typing import List, Literal, Optional, Tuple

from pydantic import BaseModel, Field, ValidationInfo, field_validator, model_validator


class ParameterConfig(BaseModel):
    """Configuration for a single API parameter.

    Defines how to collect and validate a parameter for an API call,
    including the parameter name, display name, input type, and validation rules.
    """

    name: str = Field(..., description="Internal parameter name used in API calls")
    korean_name: str = Field(..., description="Korean display name shown to users")
    param_type: Literal["select", "text", "date"] = Field(..., description="Type of input collection method")
    choices: Optional[List[Tuple[str, str]]] = Field(
        None, description="List of (value, label) tuples for select type parameters"
    )
    validation: Optional[str] = Field(None, description="Validation pattern or rule for text inputs")
    required: bool = Field(True, description="Whether this parameter is required")

    @model_validator(mode="after")
    def validate_parameter_constraints(self) -> "ParameterConfig":
        """Validate constraints between fields."""
        # Ensure choices are provided for select type parameters
        if self.param_type == "select" and not self.choices:
            raise ValueError("choices must be provided for select type parameters")

        # Ensure validation is only used with text or date type parameters
        if self.validation is not None and self.param_type not in ["text", "date"]:
            raise ValueError("validation can only be used with text or date type parameters")

        return self


class APIConfig(BaseModel):
    """Configuration for a single API endpoint.

    Defines the API name, display name, corresponding client method,
    and all required and optional parameters for the API call.
    """

    name: str = Field(..., description="Internal API identifier")
    korean_name: str = Field(..., description="Korean display name for the API")
    api_method: str = Field(..., description="Method name on the Kiwoom client")
    required_params: List[ParameterConfig] = Field(default_factory=list, description="List of required parameters")
    optional_params: List[ParameterConfig] = Field(default_factory=list, description="List of optional parameters")
    description: Optional[str] = Field(None, description="Optional description of what the API does")

    @field_validator("required_params", "optional_params")
    @classmethod
    def validate_parameter_names_unique(cls, v: List[ParameterConfig], info: ValidationInfo) -> List[ParameterConfig]:
        """Ensure parameter names are unique within required and optional lists."""
        names = [param.name for param in v]
        if len(names) != len(set(names)):
            field_name = info.field_name or "parameters"
            raise ValueError(f"Parameter names must be unique in {field_name}")
        return v

    @field_validator("optional_params")
    @classmethod
    def validate_no_duplicate_params_across_lists(
        cls, v: List[ParameterConfig], info: ValidationInfo
    ) -> List[ParameterConfig]:
        """Ensure no parameter names are duplicated between required and optional."""
        if "required_params" in info.data:
            required_names = {param.name for param in info.data["required_params"]}
            optional_names = {param.name for param in v}
            duplicates = required_names.intersection(optional_names)
            if duplicates:
                raise ValueError(f"Parameter names cannot appear in both required and optional: {duplicates}")
        return v

    def get_all_params(self) -> List[ParameterConfig]:
        """Get all parameters (required + optional) for this API."""
        return self.required_params + self.optional_params

    def get_param_by_name(self, name: str) -> Optional[ParameterConfig]:
        """Get a parameter configuration by name."""
        for param in self.get_all_params():
            if param.name == name:
                return param
        return None


class APICategory(BaseModel):
    """Configuration for a category of APIs (e.g., ranking, sector, stock info).

    Groups related APIs together with a category name and description.
    """

    name: str = Field(..., description="Internal category identifier")
    korean_name: str = Field(..., description="Korean display name for the category")
    apis: List[APIConfig] = Field(default_factory=list, description="List of APIs in this category")
    description: Optional[str] = Field(None, description="Optional category description")

    @field_validator("apis")
    @classmethod
    def validate_api_names_unique(cls, v: List[APIConfig]) -> List[APIConfig]:
        """Ensure API names are unique within the category."""
        names = [api.name for api in v]
        if len(names) != len(set(names)):
            raise ValueError("API names must be unique within a category")
        return v

    def get_api_by_name(self, name: str) -> Optional[APIConfig]:
        """Get an API configuration by name."""
        for api in self.apis:
            if api.name == name:
                return api
        return None

    def get_api_choices(self) -> List[Tuple[str, str]]:
        """Get list of (name, korean_name) tuples for menu display."""
        return [(api.name, api.korean_name) for api in self.apis]
