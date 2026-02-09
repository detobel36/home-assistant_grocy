"""Sensor platform for Grocy."""

from __future__ import annotations

import logging
from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from .const import (
    ATTR_BATTERIES,
    ATTR_CHORES,
    ATTR_MEAL_PLAN,
    ATTR_OBJ_BATTERIES,
    ATTR_OBJ_BATTERY_CHARGE_CYCLES,
    ATTR_OBJ_CHORES,
    ATTR_OBJ_CHORES_LOG,
    ATTR_OBJ_EQUIPMENT,
    ATTR_OBJ_LOCATIONS,
    ATTR_OBJ_MEAL_PLAN,
    ATTR_OBJ_MEAL_PLAN_SECTIONS,
    ATTR_OBJ_PERMISSION_HIERARCHY,
    ATTR_OBJ_PRODUCT_BARCODES,
    ATTR_OBJ_PRODUCT_BARCODES_VIEW,
    ATTR_OBJ_PRODUCT_GROUPS,
    ATTR_OBJ_PRODUCTS,
    ATTR_OBJ_PRODUCTS_AVERAGE_PRICE,
    ATTR_OBJ_PRODUCTS_LAST_PURCHASED,
    ATTR_OBJ_QUANTITY_UNIT_CONVERSIONS,
    ATTR_OBJ_QUANTITY_UNIT_CONVERSIONS_RESOLVED,
    ATTR_OBJ_QUANTITY_UNITS,
    ATTR_OBJ_RECIPES,
    ATTR_OBJ_RECIPES_NESTINGS,
    ATTR_OBJ_RECIPES_POS,
    ATTR_OBJ_RECIPES_POS_RESOLVED,
    ATTR_OBJ_SHOPPING_LIST,
    ATTR_OBJ_SHOPPING_LISTS,
    ATTR_OBJ_SHOPPING_LOCATIONS,
    ATTR_OBJ_STOCK,
    ATTR_OBJ_STOCK_CURRENT_LOCATIONS,
    ATTR_OBJ_STOCK_LOG,
    ATTR_OBJ_TASK_CATEGORIES,
    ATTR_OBJ_TASKS,
    ATTR_OBJ_USERENTITIES,
    ATTR_OBJ_USERFIELDS,
    ATTR_OBJ_USEROBJECTS,
    ATTR_SHOPPING_LIST,
    ATTR_STOCK,
    ATTR_TASKS,
    BATTERY,
    CHORES,
    DOMAIN,
    EQUIPMENT,
    ITEMS,
    LOCATION,
    MEAL_PLANS,
    PRODUCTS,
    RECIPE,
    TASKS,
)
from .coordinator import GrocyCoordinatorData, GrocyDataUpdateCoordinator
from .entity import GrocyEntity
from .helpers import model_to_dict

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Do setup sensor platform."""
    coordinator: GrocyDataUpdateCoordinator = hass.data[DOMAIN]
    entities = []
    obj_sensor = [
        create_object_grocy_sensor_entity_description(**obj) for obj in OBJECT_SENSORS
    ]
    for description in [*SENSORS, *obj_sensor]:
        if description.exists_fn(coordinator.available_entities):
            entity = GrocySensorEntity(coordinator, description, config_entry)
            coordinator.entities.append(entity)
            entities.append(entity)
        else:
            _LOGGER.debug(
                "Entity description '%s' is not available",
                description.key,
            )

    async_add_entities(entities, True)


@dataclass
class GrocySensorEntityDescription(SensorEntityDescription):
    """Grocy sensor entity description."""

    attributes_fn: Callable[GrocyCoordinatorData | None] = lambda _: None
    exists_fn: Callable[[list[str]], bool] = lambda _: True
    entity_registry_enabled_default: bool = False


SENSORS: tuple[GrocySensorEntityDescription, ...] = (
    GrocySensorEntityDescription(
        key=ATTR_CHORES,
        name="Grocy chores",
        native_unit_of_measurement=CHORES,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:broom",
        exists_fn=lambda entities: ATTR_CHORES in entities,
        attributes_fn=lambda data: {
            "chores": [model_to_dict(x) for x in data],
            "count": len(data),
        },
    ),
    GrocySensorEntityDescription(
        key=ATTR_MEAL_PLAN,
        name="Grocy meal plan",
        native_unit_of_measurement=MEAL_PLANS,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:silverware-variant",
        exists_fn=lambda entities: ATTR_MEAL_PLAN in entities,
        attributes_fn=lambda data: {
            "meals": [model_to_dict(x) for x in data],
            "count": len(data),
        },
    ),
    GrocySensorEntityDescription(
        key=ATTR_SHOPPING_LIST,
        name="Grocy shopping list",
        native_unit_of_measurement=PRODUCTS,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:cart-outline",
        exists_fn=lambda entities: ATTR_SHOPPING_LIST in entities,
        attributes_fn=lambda data: {
            "products": [model_to_dict(x) for x in data],
            "count": len(data),
        },
    ),
    GrocySensorEntityDescription(
        key=ATTR_STOCK,
        name="Grocy stock",
        native_unit_of_measurement=PRODUCTS,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:fridge-outline",
        exists_fn=lambda entities: ATTR_STOCK in entities,
        attributes_fn=lambda data: {
            "products": [model_to_dict(x) for x in data],
            "count": len(data),
        },
    ),
    GrocySensorEntityDescription(
        key=ATTR_TASKS,
        name="Grocy tasks",
        native_unit_of_measurement=TASKS,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:checkbox-marked-circle-outline",
        exists_fn=lambda entities: ATTR_TASKS in entities,
        attributes_fn=lambda data: {
            "tasks": [model_to_dict(x) for x in data],
            "count": len(data),
        },
    ),
    GrocySensorEntityDescription(
        key=ATTR_BATTERIES,
        name="Grocy batteries",
        native_unit_of_measurement=BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery",
        exists_fn=lambda entities: ATTR_BATTERIES in entities,
        attributes_fn=lambda data: {
            "batteries": [model_to_dict(x) for x in data],
            "count": len(data),
        },
    ),
)

OBJECT_SENSORS = [
    {
        "key": ATTR_OBJ_CHORES,
        "name": "Grocy Object 'chores'",
        "unit": CHORES,
        "icon": "mdi:broom",
    },
    {
        "key": ATTR_OBJ_CHORES_LOG,
        "name": "Grocy Object 'chores log'",
        "unit": CHORES,
        "icon": "mdi:format-list-bulleted-type",
    },
    {
        "key": ATTR_OBJ_MEAL_PLAN,
        "name": "Grocy Object 'meal plan'",
        "unit": MEAL_PLANS,
        "icon": "mdi:silverware-variant",
    },
    {
        "key": ATTR_OBJ_MEAL_PLAN_SECTIONS,
        "name": "Grocy Object 'meal plan sections'",
        "unit": MEAL_PLANS,
        "icon": "mdi:shape-plus-outline",
    },
    {
        "key": ATTR_OBJ_SHOPPING_LIST,
        "name": "Grocy Object 'shopping list'",
        "unit": PRODUCTS,
        "icon": "mdi:cart-outline",
    },
    {
        "key": ATTR_OBJ_STOCK,
        "name": "Grocy Object 'stock'",
        "unit": PRODUCTS,
        "icon": "mdi:fridge-outline",
    },
    {
        "key": ATTR_OBJ_TASKS,
        "name": "Grocy Object 'tasks'",
        "unit": TASKS,
        "icon": "mdi:checkbox-marked-circle-outline",
    },
    {
        "key": ATTR_OBJ_BATTERIES,
        "name": "Grocy Object 'batteries'",
        "unit": BATTERY,
        "icon": "mdi:battery",
    },
    {
        "key": ATTR_OBJ_BATTERY_CHARGE_CYCLES,
        "name": "Grocy Object 'battery charge cycles'",
        "unit": BATTERY,
        "icon": "mdi:battery-heart",
    },
    {
        "key": ATTR_OBJ_USERENTITIES,
        "name": "Grocy Object 'user entities'",
        "unit": ITEMS,
        "icon": "mdi:account-group",
    },
    {
        "key": ATTR_OBJ_EQUIPMENT,
        "name": "Grocy Object 'equipment'",
        "unit": EQUIPMENT,
        "icon": "mdi:shoe-sneaker",
    },
    {
        "key": ATTR_OBJ_LOCATIONS,
        "name": "Grocy Object 'locations'",
        "unit": LOCATION,
        "icon": "mdi:map-marker",
    },
    {
        "key": ATTR_OBJ_PERMISSION_HIERARCHY,
        "name": "Grocy Object 'permission hierarchy'",
        "unit": ITEMS,
        "icon": "mdi:shield-account-variant",
    },
    {
        "key": ATTR_OBJ_PRODUCT_BARCODES,
        "name": "Grocy Object 'product barcodes'",
        "unit": ITEMS,
        "icon": "mdi:barcode",
    },
    {
        "key": ATTR_OBJ_PRODUCT_BARCODES_VIEW,
        "name": "Grocy Object 'product barcodes view'",
        "unit": ITEMS,
        "icon": "mdi:barcode-scan",
    },
    {
        "key": ATTR_OBJ_PRODUCT_GROUPS,
        "name": "Grocy Object 'product groups'",
        "unit": ITEMS,
        "icon": "mdi:group",
    },
    {
        "key": ATTR_OBJ_PRODUCTS,
        "name": "Grocy Object 'product'",
        "unit": PRODUCTS,
        "icon": "mdi:text-box-outline",
    },
    {
        "key": ATTR_OBJ_PRODUCTS_AVERAGE_PRICE,
        "name": "Grocy Object 'product average price'",
        "unit": PRODUCTS,
        "icon": "mdi:chart-box-outline",
    },
    {
        "key": ATTR_OBJ_PRODUCTS_LAST_PURCHASED,
        "name": "Grocy Object 'product last purchased'",
        "unit": PRODUCTS,
        "icon": "mdi:chart-box-plus-outline",
    },
    {
        "key": ATTR_OBJ_QUANTITY_UNIT_CONVERSIONS,
        "name": "Grocy Object 'quantity unit conversions'",
        "unit": ITEMS,
        "icon": "mdi:scale-balance",
    },
    {
        "key": ATTR_OBJ_QUANTITY_UNIT_CONVERSIONS_RESOLVED,
        "name": "Grocy Object 'quantity unit conversions resolved'",
        "unit": ITEMS,
        "icon": "mdi:scale-balance",
    },
    {
        "key": ATTR_OBJ_QUANTITY_UNITS,
        "name": "Grocy Object 'quantity units'",
        "unit": ITEMS,
        "icon": "mdi:scale-balance",
    },
    {
        "key": ATTR_OBJ_RECIPES,
        "name": "Grocy Object 'recipes'",
        "unit": RECIPE,
        "icon": "mdi:food",
    },
    {
        "key": ATTR_OBJ_RECIPES_NESTINGS,
        "name": "Grocy Object 'recipe nestings'",
        "unit": RECIPE,
        "icon": "mdi:food",
    },
    {
        "key": ATTR_OBJ_RECIPES_POS,
        "name": "Grocy Object 'recipe pos'",
        "unit": ITEMS,
        "icon": "mdi:food",
    },
    {
        "key": ATTR_OBJ_RECIPES_POS_RESOLVED,
        "name": "Grocy Object 'recipe pos resolved'",
        "unit": ITEMS,
        "icon": "mdi:food",
    },
    {
        "key": ATTR_OBJ_SHOPPING_LISTS,
        "name": "Grocy Object 'shopping lists'",
        "unit": ITEMS,
        "icon": "mdi:cart",
    },
    {
        "key": ATTR_OBJ_SHOPPING_LOCATIONS,
        "name": "Grocy Object 'shopping locations'",
        "unit": ITEMS,
        "icon": "mdi:store-marker",
    },
    {
        "key": ATTR_OBJ_STOCK_CURRENT_LOCATIONS,
        "name": "Grocy Object 'stock current locations'",
        "unit": ITEMS,
        "icon": "mdi:map-marker",
    },
    {
        "key": ATTR_OBJ_STOCK_LOG,
        "name": "Grocy Object 'stock log'",
        "unit": ITEMS,
        "icon": "mdi:clipboard-text",
    },
    {
        "key": ATTR_OBJ_TASK_CATEGORIES,
        "name": "Grocy Object 'task categories'",
        "unit": ITEMS,
        "icon": "mdi:shape",
    },
    {
        "key": ATTR_OBJ_USERFIELDS,
        "name": "Grocy Object 'userfields'",
        "unit": ITEMS,
        "icon": "mdi:account-details",
    },
    {
        "key": ATTR_OBJ_USEROBJECTS,
        "name": "Grocy Object 'userobjects'",
        "unit": ITEMS,
        "icon": "mdi:account-details-outline",
    },
]


def create_object_grocy_sensor_entity_description(
    key: str, name: str, unit: str, icon: str
) -> GrocySensorEntityDescription:
    """Returns a sensor entity description for a Grocy generic object."""
    return GrocySensorEntityDescription(
        key=key,
        name=name,
        native_unit_of_measurement=unit,
        state_class=SensorStateClass.MEASUREMENT,
        icon=icon,
        exists_fn=lambda _: True,
        attributes_fn=lambda data: {
            key: data,
            "count": len(data),
        },
    )


class GrocySensorEntity(GrocyEntity, SensorEntity):
    """Grocy sensor entity definition."""

    @property
    def native_value(self) -> StateType:
        """Return the value reported by the sensor."""
        entity_data = self.coordinator.data[self.entity_description.key]

        return len(entity_data) if entity_data else 0
