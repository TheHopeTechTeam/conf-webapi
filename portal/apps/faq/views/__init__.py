"""
Top-level package for views.
"""
from .faq_category import FaqCategoryModelAdmin
from .faq import FaqModelAdmin


__all__ = [
    "FaqCategoryModelAdmin",
    "FaqModelAdmin",
]
