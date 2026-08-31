"""A five-minute exercise: implement exact group-reference validation."""


def validate_expression_group_ids(
    actual_group_ids: list[str], expression_group_ids: list[str]
) -> None:
    """
    Requirements:
    1. Neither list may contain duplicate IDs.
    2. The two lists may be ordered differently, but must contain the same IDs.
    3. Raise ValueError explicitly when a requirement is violated.

    Examples:
        ["A1", "A2"], ["A2", "A1"] -> pass
        ["A1"], ["A1", "A2"] -> ValueError
        ["A1", "A1"], ["A1"] -> ValueError
    """
    # TODO: 本章只需要补这里，大约 6 行代码。
    raise NotImplementedError("请实现 validate_expression_group_ids")
