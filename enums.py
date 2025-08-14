"""Enumerations for transaction statuses and types."""

import enum


class TransactionStatus(enum.Enum):
    """وضعیت‌های مختلف یک تراکنش."""
    APPROVED = "approved"
    VOIDED = "voided"
    CANCELLED = "cancelled"
    PENDING = "pending"


class TransactionType(enum.Enum):
    """انواع تراکنش."""
    PURCHASE_IN = "purchase_in"
    PURCHASE_RETURN = "purchase_return"
    PRODUCTION_IN = "production_in"
    CONSUMPTION = "consumption"
    SALE_OUT = "sale_out"
    SALE_RETURN = "sale_return"
    TRANSFER = "transfer"
