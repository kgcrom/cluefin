"""KRX API Method Factory for generating partial functions to eliminate code duplication.

This module provides the core abstraction infrastructure for creating reusable function
templates using functools.partial while preserving type safety and Korean financial
API specifics.
"""

from functools import partial
from typing import Callable, Dict, Generic, Protocol, Type, TypeVar

from cluefin_openapi.krx._client import Client
from cluefin_openapi.krx._model import KrxHttpBody, KrxHttpResponse

T = TypeVar("T", bound=KrxHttpBody)


class TypedApiMethod(Protocol, Generic[T]):
    """Protocol for type-safe API method signatures with proper mypy compatibility."""

    def __call__(self, base_date: str) -> KrxHttpResponse[T]:
        """Standard API method signature for single-parameter base_date methods.
        
        Args:
            base_date (str): 조회할 날짜 (YYYYMMDD 형식)
            
        Returns:
            KrxHttpResponse[T]: Korean financial API response with proper typing
        """
        ...


def _api_method_template(
    client: Client,
    path_template: str,
    endpoint: str,
    response_model: Type[T],
    base_date: str,
    **kwargs: Dict[str, str]
) -> KrxHttpResponse[T]:
    """Core template function for single-parameter API calls.
    
    This template handles the common pattern across KRX API methods:
    1. Parameter processing with Korean field aliases
    2. URL path formatting
    3. HTTP client calls through client._get()
    4. Response validation with Pydantic models
    5. Korean API specifics preservation
    
    Args:
        client (Client): KRX HTTP client instance
        path_template (str): URL path template (e.g., "/svc/apis/sto/{}")
        endpoint (str): Specific API endpoint (e.g., "stk_bydd_trd.json")
        response_model (Type[T]): Pydantic model class for response validation
        base_date (str): 조회할 날짜 (YYYYMMDD 형식) - Korean date format
        **kwargs: Additional parameters for future multi-parameter support
        
    Returns:
        KrxHttpResponse[T]: Structured response with Korean financial data
    """
    # Korean API parameter mapping - preserve "basDd" field alias
    params = {"basDd": base_date}

    # Add any additional parameters (for future multi-parameter support)
    if kwargs:
        params.update(kwargs)

    # Execute HTTP request through client with proper path formatting
    response = client._get(path_template.format(endpoint), params=params)

    # Validate response with Pydantic model (preserves Korean field aliases)
    body = response_model.model_validate(response)

    # Return structured KrxHttpResponse with generic typing preserved
    return KrxHttpResponse(body=body)


class KrxApiMethodFactory:
    """Factory class for generating partial functions that abstract common KRX API patterns.
    
    This factory eliminates code duplication by creating reusable function templates
    using functools.partial while maintaining type safety, Korean field aliases,
    and all existing functionality.
    
    The factory handles:
    - Single-parameter date-based API calls
    - Type hint preservation with mypy compatibility
    - Korean field aliases and API specifics
    - Parameter mapping capabilities
    - Comprehensive docstring templates
    
    Requirements addressed: 1.1, 2.1, 2.3, 3.1, 3.2, 5.1
    """

    @staticmethod
    def create_single_param_method(
        client: Client,
        path_template: str,
        endpoint: str,
        response_model: Type[T],
        docstring: str
    ) -> TypedApiMethod[T]:
        """Create a partial function for single-parameter base_date API methods.
        
        This method generates a properly typed partial function that maintains
        identical functionality to the original methods while eliminating
        code duplication. The generated function preserves:
        
        - Original method signature: (base_date: str) -> KrxHttpResponse[T]
        - Korean field aliases: "basDd" parameter mapping
        - Type safety: Full mypy compatibility and generic type parameters
        - Error handling: Identical exception behavior through client._get()
        - Docstring: Comprehensive documentation
        
        Args:
            client (Client): KRX HTTP client instance for API calls
            path_template (str): URL path template with placeholder (e.g., "/svc/apis/sto/{}")
            endpoint (str): Specific API endpoint filename (e.g., "stk_bydd_trd.json")
            response_model (Type[T]): Pydantic model for response validation
            docstring (str): Method documentation string
            
        Returns:
            TypedApiMethod[T]: Partial function with preserved type hints and functionality
            
        Example:
            >>> factory = KrxApiMethodFactory()
            >>> get_kospi = factory.create_single_param_method(
            ...     client=client,
            ...     path_template="/svc/apis/sto/{}",
            ...     endpoint="stk_bydd_trd.json",
            ...     response_model=StockKospi,
            ...     docstring="KOSPI 일별매매정보 조회"
            ... )
            >>> response = get_kospi("20241201")  # Type-safe call
        """
        # Create partial function with pre-filled parameters
        method = partial(
            _api_method_template,
            client=client,
            path_template=path_template,
            endpoint=endpoint,
            response_model=response_model
        )

        # Preserve docstring for documentation
        method.__doc__ = docstring

        # Set proper function name for debugging and introspection
        method.__name__ = f"krx_api_method_{endpoint.replace('.', '_')}"

        return method

    @staticmethod
    def create_multi_param_method(
        client: Client,
        path_template: str,
        endpoint: str,
        response_model: Type[T],
        param_mapping: Dict[str, str],
        docstring: str
    ) -> Callable:
        """Create a partial function for multi-parameter API methods.
        
        This method provides extensibility for more complex API endpoints
        that require multiple parameters beyond base_date. It maintains
        the same type safety and Korean field alias support.
        
        Args:
            client (Client): KRX HTTP client instance
            path_template (str): URL path template with placeholder
            endpoint (str): Specific API endpoint filename
            response_model (Type[T]): Pydantic model for response validation
            param_mapping (Dict[str, str]): Parameter name to Korean alias mapping
            docstring (str): Method documentation string
            
        Returns:
            Callable: Partial function for multi-parameter API calls
            
        Note:
            This method is prepared for future enhancement of the factory
            to handle more complex API endpoints with multiple parameters.
        """
        def multi_param_wrapper(**params):
            # Apply parameter mapping to Korean aliases
            mapped_params = {
                param_mapping.get(key, key): value
                for key, value in params.items()
            }

            # Execute request with mapped parameters
            response = client._get(path_template.format(endpoint), params=mapped_params)
            body = response_model.model_validate(response)
            return KrxHttpResponse(body=body)

        multi_param_wrapper.__doc__ = docstring
        multi_param_wrapper.__name__ = f"krx_multi_param_{endpoint.replace('.', '_')}"

        return multi_param_wrapper

    @classmethod
    def get_method_signature_info(cls, method: Callable) -> Dict[str, str]:
        """Get signature information for factory-generated methods.
        
        This utility method provides introspection capabilities for
        generated partial functions to aid in debugging and validation.
        
        Args:
            method (Callable): Factory-generated method to inspect
            
        Returns:
            Dict[str, str]: Method signature and metadata information
        """
        return {
            "name": getattr(method, "__name__", "unknown"),
            "doc": getattr(method, "__doc__", "No documentation"),
            "type": "partial_function" if hasattr(method, "func") else "callable"
        }
