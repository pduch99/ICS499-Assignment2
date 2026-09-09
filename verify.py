from collections import defaultdict
from anonymize import SKIP, normalized, parse_literals, parse_schema, read_string, split_address, valid_email, valid_name, valid_phone, valid_street
def category(table, column, value):
    column = column.lower()
    location = f"{table.lower()}.{column}"
    if location in SKIP:
        return None
    if "email" in column and valid_email(value):
        return "email"
    if "phone" in column and valid_phone(value):
        return "phone"
    if "address" in column and (split_address(value) or valid_street(value)):
        return "address"
    if column in {"city", "state", "zip", "zipcode", "zip_code"}:
        return "address"
    if column.endswith("name") and valid_name(value):
        return "name"
    return None
def scrub_strings(sql):
    output = []
    last = 0
    i = 0
    while i < len(sql):
        if sql[i] == "'":
            end, _ = read_string(sql, i)
            output.append(sql[last:i])
            output.append("''")
            last = end
            i = end
        else:
            i += 1
    output.append(sql[last:])
    return "".join(output)
def check(condition, message, failures):
    if condition:
        print(f"PASS: {message}")
    else:
        print(f"FAIL: {message}")
        failures.append(message)
def main():
    with open("original.sql", "r", encoding="utf-8") as file:
        original_sql = file.read()
    with open("anonymized.sql", "r", encoding="utf-8") as file:
        anonymized_sql = file.read()
    original_schema = parse_schema(original_sql)
    anonymized_schema = parse_schema(anonymized_sql)
    original = parse_literals(original_sql, original_schema)
    anonymized = parse_literals(anonymized_sql, anonymized_schema)
    failures = []
    check(original_schema == anonymized_schema, "table structure is unchanged", failures)
    check(scrub_strings(original_sql) == scrub_strings(anonymized_sql), "DDL, IDs, numbers, dates, and NULL values are unchanged", failures)
    check(len(original) == len(anonymized), "same number of SQL string values", failures)
    mappings = defaultdict(lambda: defaultdict(set))
    pii_changed = True
    non_pii_preserved = True
    metadata_preserved = True
    for old, new in zip(original, anonymized):
        _, _, old_table, old_column, _, old_value = old
        _, _, new_table, new_column, _, new_value = new
        if old_table != new_table or old_column != new_column:
            metadata_preserved = False
            continue
        kind = category(old_table, old_column, old_value)
        if kind:
            if normalized(old_value) == normalized(new_value):
                pii_changed = False
            mappings[kind][normalized(old_value)].add(normalized(new_value))
        elif old_value != new_value:
            non_pii_preserved = False
    check(metadata_preserved, "values remain in the same tables and columns", failures)
    check(pii_changed, "all detected PII was replaced", failures)
    check(non_pii_preserved, "non-PII string values are unchanged", failures)
    consistent = True
    for kind in mappings:
        for original_value in mappings[kind]:
            if len(mappings[kind][original_value]) != 1:
                consistent = False
    check(consistent, "repeated PII maps to one consistent replacement", failures)
    check(len(mappings["name"][normalized("Trey Lervick")]) == 1, "Trey Lervick is consistent across tables", failures)
    check(len(mappings["name"][normalized("Dani Rojas")]) == 1 and len(mappings["email"][normalized("dani.rojas@umn.edu")]) == 1, "Dani Rojas is consistent across tables", failures)
    check(len(mappings["name"][normalized("Rachel Lervick")]) == 1 and len(mappings["email"][normalized("rachel.lervick@gmail.com")]) == 1, "repeated guardian data is consistent", failures)
    address_map = mappings["address"]
    street = next(iter(address_map[normalized("9142 Courtly Road")]))
    city = next(iter(address_map[normalized("Woodbury")]))
    state = next(iter(address_map[normalized("MN")]))
    zipcode = next(iter(address_map[normalized("55125")]))
    full = next(iter(address_map[normalized("9142 Courtly Road, Woodbury, MN 55125")]))
    expected = normalized(f"{street}, {city}, {state} {zipcode}")
    check(full == expected, "split and combined address map identically", failures)
    if failures:
        print()
        print(f"{len(failures)} verification test(s) failed")
        raise SystemExit(1)
    print()
    print("TESTS PASSED")
if __name__ == "__main__":
    main()