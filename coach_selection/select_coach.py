def select_coach(age_group: str, role: str) -> str:
    age_group = age_group.strip().lower()
    role = role.strip().lower()
    # Primary selection based on age
    if age_group == "grade 6-8":
        return "tara"
    else:
        return "ravi"

    if role in ["life coach", "goal partner", "cheerleader", "agony aunt"]:
        return "tara"
    elif role in ["study guru", "career compass", "guru guide"]:
        return "ravi"

    return "tara"