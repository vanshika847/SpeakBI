BLOCKED_KEYWORDS = {
    "DROP", "DELETE", "INSERT", "UPDATE",
    "ALTER", "TRUNCATE", "CREATE", "EXEC",
    "EXECUTE", "UNION", "INTO", "GRANT", "REVOKE"
}
def validate_sql(sql: str) -> bool:
    upper  = sql.upper()
    tokens = upper.split()
    for keyword in BLOCKED_KEYWORDS:
        if keyword in tokens:
            raise ValueError(
                f"Blocked keyword '{keyword}' detected. Query rejected."
            )
    clean = sql.replace("\n", " ").strip()
    if clean.count(";") > 1:
        raise ValueError("Multiple SQL statements are not allowed.")
    if not upper.strip().startswith("SELECT"):
        raise ValueError("Only SELECT queries are permitted.")
    return True