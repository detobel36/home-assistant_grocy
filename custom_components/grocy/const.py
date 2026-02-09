"""Constants for Grocy."""

from datetime import timedelta
from typing import Final

NAME: Final = "Grocy"
DOMAIN: Final = "grocy"
VERSION = "0.0.0"

ISSUE_URL: Final = "https://github.com/iamkarlson/grocy/issues"

PLATFORMS: Final = ["binary_sensor", "sensor", "todo", "calendar"]

SCAN_INTERVAL = timedelta(seconds=30)

DEFAULT_PORT: Final = 9192
DEFAULT_CALENDAR_SYNC_INTERVAL: Final = 5  # minutes
CONF_URL: Final = "url"
CONF_PORT: Final = "port"
CONF_API_KEY: Final = "api_key"
CONF_VERIFY_SSL: Final = "verify_ssl"
CONF_CALENDAR_SYNC_INTERVAL: Final = "calendar_sync_interval"
CONF_CALENDAR_FIX_TIMEZONE: Final = "calendar_fix_timezone"

STARTUP_MESSAGE: Final = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""

CHORES: Final = "Chore(s)"
MEAL_PLANS: Final = "Meal(s)"
RECIPE = "Recipe(s)"
PRODUCTS: Final = "Product(s)"
TASKS: Final = "Task(s)"
ITEMS: Final = "Item(s)"
BATTERY: Final = "Battery(s)"
EQUIPMENT: Final = "Equipment(s)"
LOCATION: Final = "Location(s)"

ATTR_BATTERIES: Final = "batteries"
ATTR_CHORES: Final = "chores"
ATTR_EXPIRED_PRODUCTS: Final = "expired_products"
ATTR_EXPIRING_PRODUCTS: Final = "expiring_products"
ATTR_MEAL_PLAN: Final = "meal_plan"
ATTR_MISSING_PRODUCTS: Final = "missing_products"
ATTR_OVERDUE_BATTERIES: Final = "overdue_batteries"
ATTR_OVERDUE_CHORES: Final = "overdue_chores"
ATTR_OVERDUE_PRODUCTS: Final = "overdue_products"
ATTR_OVERDUE_TASKS: Final = "overdue_tasks"
ATTR_SHOPPING_LIST: Final = "shopping_list"
ATTR_STOCK: Final = "stock"
ATTR_TASKS: Final = "tasks"

ATTR_OBJ_BATTERIES: Final = "object_batteries"
ATTR_OBJ_BATTERY_CHARGE_CYCLES: Final = "object_battery_charge_cycles"
ATTR_OBJ_CHORES: Final = "object_chores"
ATTR_OBJ_CHORES_LOG: Final = "object_chores_log"
ATTR_OBJ_EQUIPMENT: Final = "object_equipment"
ATTR_OBJ_LOCATIONS: Final = "object_locations"
ATTR_OBJ_MEAL_PLAN: Final = "object_meal_plan"
ATTR_OBJ_MEAL_PLAN_SECTIONS: Final = "object_meal_plan_sections"
ATTR_OBJ_PERMISSION_HIERARCHY: Final = "object_permission_hierarchy"
ATTR_OBJ_PRODUCT_BARCODES: Final = "object_product_barcodes"
ATTR_OBJ_PRODUCT_BARCODES_VIEW: Final = "object_product_barcodes_view"
ATTR_OBJ_PRODUCT_GROUPS: Final = "object_product_groups"
ATTR_OBJ_PRODUCTS: Final = "object_products"
ATTR_OBJ_PRODUCTS_AVERAGE_PRICE: Final = "object_products_average_price"
ATTR_OBJ_PRODUCTS_LAST_PURCHASED: Final = "object_products_last_purchased"
ATTR_OBJ_QUANTITY_UNIT_CONVERSIONS: Final = "object_quantity_unit_conversions"
ATTR_OBJ_QUANTITY_UNIT_CONVERSIONS_RESOLVED: Final = (
    "object_quantity_unit_conversions_resolved"
)
ATTR_OBJ_QUANTITY_UNITS: Final = "object_quantity_units"
ATTR_OBJ_RECIPES: Final = "object_recipes"
ATTR_OBJ_RECIPES_NESTINGS: Final = "object_recipes_nestings"
ATTR_OBJ_RECIPES_POS: Final = "object_recipes_pos"
ATTR_OBJ_RECIPES_POS_RESOLVED: Final = "object_recipes_pos_resolved"
ATTR_OBJ_SHOPPING_LIST: Final = "object_shopping_list"
ATTR_OBJ_SHOPPING_LISTS: Final = "object_shopping_lists"
ATTR_OBJ_SHOPPING_LOCATIONS: Final = "object_shopping_locations"
ATTR_OBJ_STOCK: Final = "object_stock"
ATTR_OBJ_STOCK_CURRENT_LOCATIONS: Final = "object_stock_current_locations"
ATTR_OBJ_STOCK_LOG: Final = "object_stock_log"
ATTR_OBJ_TASK_CATEGORIES: Final = "object_task_categories"
ATTR_OBJ_TASKS: Final = "object_tasks"
ATTR_OBJ_USERENTITIES: Final = "object_userentities"
ATTR_OBJ_USERFIELDS: Final = "object_userfields"
ATTR_OBJ_USEROBJECTS: Final = "object_userobjects"
