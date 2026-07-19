"""Tests for the Grocy products sensor.

Features: stock_management
See: docs/FEATURES.md
"""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from custom_components.grocy.const import ATTR_PRODUCTS
from custom_components.grocy.coordinator import GrocyCoordinatorData
from custom_components.grocy.grocy_data import GrocyData
from custom_components.grocy.sensor import SENSORS, GrocySensorEntity


def _build_products_sensor(data) -> GrocySensorEntity:
    description = next(description for description in SENSORS if description.key == ATTR_PRODUCTS)
    entity = GrocySensorEntity.__new__(GrocySensorEntity)
    entity.entity_description = description
    entity.coordinator = SimpleNamespace(data=GrocyCoordinatorData())
    entity.coordinator.data[ATTR_PRODUCTS] = data
    return entity


@pytest.mark.feature("stock_management")
@pytest.mark.asyncio
async def test_async_update_products_maps_names(hass, mock_grocy) -> None:
    """Verify products are fetched and names for locations and quantity units are mapped."""
    async def immediate_executor(func, *args):
        return func(*args)

    hass.async_add_executor_job = AsyncMock(side_effect=immediate_executor)
    grocy_data = GrocyData(hass, mock_grocy, "https://exemple.com")

    mock_products = [
        {
            "id": 1,
            "name": "Cookies",
            "qu_id_purchase": 3,
            "qu_id_stock": 3,
            "qu_id_consume": 3,
            "qu_id_price": 3,
            "location_id": 4,
            "shopping_location_id": 5,
        },
        {
            "id": 2,
            "name": "Milk",
            "qu_id_purchase": "3",  # as string
            "qu_id_stock": None,
            "qu_id_consume": None,
            "qu_id_price": None,
            "location_id": None,
            "shopping_location_id": None,
        }
    ]
    mock_quantity_units = [
        {"id": 3, "name": "Pack"},
        {"id": "6", "name": "Liter"},
    ]
    mock_locations = [
        {"id": 4, "name": "Pantry"},
    ]
    mock_shopping_locations = [
        {"id": 5, "name": "Supermarket"},
    ]

    def generic_list_side_effect(entity_type):
        from grocy.data_models.generic import EntityType
        if entity_type == EntityType.PRODUCTS:
            return mock_products
        if entity_type == EntityType.QUANTITY_UNITS:
            return mock_quantity_units
        if entity_type == EntityType.LOCATIONS:
            return mock_locations
        if entity_type == EntityType.SHOPPING_LOCATIONS:
            return mock_shopping_locations
        return []

    grocy_data.api.generic.list.side_effect = generic_list_side_effect

    products = await grocy_data.async_update_products()

    assert len(products) == 2
    assert products[0]["qu_id_purchase_name"] == "Pack"
    assert products[0]["qu_id_stock_name"] == "Pack"
    assert products[0]["qu_id_consume_name"] == "Pack"
    assert products[0]["qu_id_price_name"] == "Pack"
    assert products[0]["location_name"] == "Pantry"
    assert products[0]["shopping_location_name"] == "Supermarket"

    # String conversion and None checks
    assert products[1]["qu_id_purchase_name"] == "Pack"
    assert products[1]["qu_id_stock_name"] is None
    assert products[1]["qu_id_consume_name"] is None
    assert products[1]["qu_id_price_name"] is None
    assert products[1]["location_name"] is None
    assert products[1]["shopping_location_name"] is None


@pytest.mark.feature("stock_management")
def test_products_sensor_native_value_and_attributes() -> None:
    """Verify products sensor counts correct amount and exposes mapped attributes."""
    mock_products = [
        {
            "id": 1,
            "name": "Cookies",
            "qu_id_purchase_name": "Pack",
            "location_name": "Pantry",
        }
    ]
    sensor = _build_products_sensor(mock_products)

    assert sensor.native_value == 1
    attrs = sensor.extra_state_attributes
    assert attrs["count"] == 1
    assert attrs["products"] == mock_products


@pytest.mark.feature("stock_management")
def test_products_sensor_none_data() -> None:
    """Verify products sensor handles None data gracefully."""
    sensor = _build_products_sensor(None)
    assert sensor.native_value == 0
    assert sensor.extra_state_attributes is None
