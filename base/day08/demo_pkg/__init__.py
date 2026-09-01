"""demo_pkg 的统一出口：外部只需要 import 这里暴露的符号。"""

from .models import Condition
from .services import build_age_condition, summarize

__all__ = ["Condition", "build_age_condition", "summarize"]
