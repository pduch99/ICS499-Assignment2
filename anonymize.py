import argparse
import hashlib
import re
import secrets
from collections import defaultdict
from faker import Faker


SKIP = {"venues.name"}
SUFFIXES = ("Jr.", "Sr.", "II", "III", "IV")
def read_string(text, start):
    i = start + 1
    out = []
    while i < len(text):
        if text[i] == "\\" and i + 1 < len(text):
            out.append(text[i + 1])
            i += 2
        elif text[i] == "'":
            if i + 1 < len(text) and text[i + 1] == "'":
                out.append("'")
                i += 2
            else:
                return i + 1, "".join(out)
        else:
            out.append(text[i])
            i += 1
    raise ValueError("unterminated SQL string")
def quote(value):
    return "'" + value.replace("\\", "\\\\").replace("'", "''") + "'"
def find_semicolon(text, start):
    i = start
    while i < len(text):
        if text[i] == "'":
            i, _ = read_string(text, i)
        elif text[i] == ";":
            return i + 1
        else:
            i += 1
    return len(text)
def parse_schema(sql):
    schema = {}
    for match in re.finditer(
        r"CREATE\s+TABLE\s+`([^`]+)`\s*\((.*?)\)\s*ENGINE=",
        sql,
        re.I | re.S,
    ):
        table, body = match.groups()
        schema[table] = [
            (name, data_type.lower())
            for name, data_type in re.findall(
                r"^\s*`([^`]+)`\s+([A-Za-z]+)",
                body,
                re.M,
            )
        ]
    return schema
def split_fields(sql, start, end):
    fields = []
    field_start = start
    i = start
    depth = 0
    while i < end:
        if sql[i] == "'":
            i, _ = read_string(sql, i)
            continue
        if sql[i] == "(":
            depth += 1
        elif sql[i] == ")":
            if depth == 0:
                fields.append((field_start, i))
                break
            depth -= 1
        elif sql[i] == "," and depth == 0:
            fields.append((field_start, i))
            field_start = i + 1
        i += 1
    return fields
def trim(text, start, end):
    while start < end and text[start].isspace():
        start += 1
    while end > start and text[end - 1].isspace():
        end -= 1
    return start, end
def parse_literals(sql, schema):
    literals = []
    for match in re.finditer(
        r"INSERT\s+INTO\s+`([^`]+)`",
        sql,
        re.I,
    ):
        table = match.group(1)
        if table not in schema:
            continue
        end = find_semicolon(sql, match.end())
        values = re.search(
            r"\bVALUES\b",
            sql[match.end():end],
            re.I,
        )
        if not values:
            continue
        values_start = match.end() + values.end()
        header = sql[
            match.end():
            match.end() + values.start()
        ]
        columns = re.findall(
            r"`([^`]+)`",
            header,
        )
        if not columns:
            columns = [
                name
                for name, _ in schema[table]
            ]
        types = dict(schema[table])
        i = values_start
        while i < end:
            if sql[i] == "'":
                i, _ = read_string(sql, i)
                continue
            if sql[i] != "(":
                i += 1
                continue
            row_start = i + 1
            i += 1
            depth = 0
            while i < end:
                if sql[i] == "'":
                    i, _ = read_string(sql, i)
                    continue
                if sql[i] == "(":
                    depth += 1
                elif sql[i] == ")":
                    if depth == 0:
                        break
                    depth -= 1
                i += 1
            fields = split_fields(
                sql,
                row_start,
                i,
            )
            for index, field in enumerate(fields):
                if index >= len(columns):
                    break
                start, stop = field
                start, stop = trim(
                    sql,
                    start,
                    stop,
                )
                if start >= stop:
                    continue
                if sql[start] != "'":
                    continue
                string_end, value = read_string(
                    sql,
                    start,
                )
                if string_end != stop:
                    continue
                column = columns[index]
                literals.append(
                    (
                        start,
                        stop,
                        table,
                        column,
                        types.get(column, ""),
                        value,
                    )
                )
            i += 1
    return literals
def normalized(value):
    return " ".join(
        value.strip().split()
    ).casefold()
def same_case(original, replacement):
    if original.isupper():
        return replacement.upper()
    if original.islower():
        return replacement.lower()
    return replacement
def valid_name(value):
    if not re.fullmatch(
        r"[A-Za-z][A-Za-z .'\-]*",
        value,
    ):
        return False
    return 2 <= len(value.split()) <= 5
def valid_email(value):
    return re.fullmatch(
        r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+"
        r"@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+",
        value,
    ) is not None
def valid_phone(value):
    digits = re.sub(
        r"\D",
        "",
        value,
    )
    return (
        re.fullmatch(
            r"[0-9() .+\-]+",
            value,
        ) is not None
        and 10 <= len(digits) <= 15
    )
def valid_street(value):
    return re.fullmatch(
        r"\d+\s+[A-Za-z0-9 .'\-]+",
        value,
    ) is not None
def split_address(value):
    match = re.fullmatch(
        r"(.+?),\s*([^,]+),\s*"
        r"([A-Za-z]{2})\s+"
        r"(\d{5}(?:-\d{4})?)",
        value,
    )
    if not match:
        return None
    if not valid_street(match.group(1)):
        return None
    return match.groups()
class Anonymizer:
    def __init__(self):
        self.salt = secrets.token_hex(16)
        self.cache = defaultdict(dict)
    def fake(self, category, key):
        digest = hashlib.sha256(
            f"{self.salt}|{category}|{key}".encode(
                "utf-8"
            )
        ).digest()

        seed = int.from_bytes(
            digest[:8],
            "big",
        )
        fake = Faker("en_US")
        fake.seed_instance(seed)
        return fake
    def name(self, original):
        key = normalized(original)
        if key not in self.cache["name"]:
            suffix = next(
                (
                    suffix
                    for suffix in SUFFIXES
                    if original.rstrip().endswith(
                        " " + suffix
                    )
                ),
                "",
            )
            fake = self.fake(
                "name",
                key,
            )
            value = (
                f"{fake.first_name()} "
                f"{fake.last_name()}"
            )
            if suffix:
                value += " " + suffix
            self.cache["name"][key] = value
        return same_case(
            original,
            self.cache["name"][key],
        )
    def email(self, original):
        key = original.casefold()
        if key not in self.cache["email"]:
            local = key.split(
                "@",
                1,
            )[0]
            base, plus, tag = local.partition("+")
            separator = next(
                (
                    separator
                    for separator in (".", "_", "-")
                    if separator in base
                ),
                "",
            )
            fake = self.fake(
                "email",
                key,
            )
            first = re.sub(
                r"\W",
                "",
                fake.first_name(),
            ).lower()
            last = re.sub(
                r"\W",
                "",
                fake.last_name(),
            ).lower()
            if separator:
                local = (
                    first
                    + separator
                    + last
                )
            else:
                local = (
                    first[:1]
                    + last
                )
            if plus:
                local += "+" + tag
            self.cache["email"][key] = (
                local
                + "@"
                + fake.free_email_domain()
            )
        value = self.cache["email"][key]
        if original.isupper():
            return value.upper()
        return value
    def phone(self, original):
        key = re.sub(
            r"\D",
            "",
            original,
        )
        if key not in self.cache["phone"]:
            fake = self.fake(
                "phone",
                key,
            )
            if (
                len(key) == 11
                and key.startswith("1")
            ):
                digits = ["1"]
            else:
                digits = []
            while len(digits) < len(key):
                digit = str(
                    fake.random_int(
                        0,
                        9,
                    )
                )
                if (
                    len(digits) in (0, 3)
                    and digit in ("0", "1")
                ):
                    continue
                digits.append(digit)
            self.cache["phone"][key] = "".join(
                digits
            )

        digits = iter(
            self.cache["phone"][key]
        )
        return "".join(
            next(digits)
            if char.isdigit()
            else char
            for char in original
        )
    def component(
        self,
        category,
        original,
        faker_method,
    ):
        key = normalized(original)

        if key not in self.cache[category]:
            fake = self.fake(
                category,
                key,
            )

            self.cache[category][key] = getattr(
                fake,
                faker_method,
            )()

        return same_case(
            original,
            self.cache[category][key],
        )

    def street(self, value):
        return self.component(
            "street",
            value,
            "street_address",
        )

    def city(self, value):
        return self.component(
            "city",
            value,
            "city",
        )

    def state(self, value):
        return self.component(
            "state",
            value,
            "state_abbr",
        )

    def zipcode(self, value):
        key = value

        if key not in self.cache["zip"]:
            fake = self.fake(
                "zip",
                key,
            )

            if "-" in value:
                replacement = fake.zipcode_plus4()
            else:
                replacement = fake.zipcode()

            self.cache["zip"][key] = replacement

        return self.cache["zip"][key]

    def address(self, value):
        parts = split_address(value)

        if not parts:
            return None

        street, city, state, zipcode = parts

        return (
            f"{self.street(street)}, "
            f"{self.city(city)}, "
            f"{self.state(state)} "
            f"{self.zipcode(zipcode)}"
        )

    def replace(
        self,
        table,
        column,
        data_type,
        value,
    ):
        column = column.lower()
        location = (
            f"{table.lower()}.{column}"
        )

        if location in SKIP:
            return None

        if (
            "email" in column
            and valid_email(value)
        ):
            return self.email(value)

        if (
            "phone" in column
            and valid_phone(value)
        ):
            return self.phone(value)

        if "address" in column:
            full = self.address(value)

            if full:
                return full

            if valid_street(value):
                return self.street(value)

        if (
            column == "city"
            and re.fullmatch(
                r"[A-Za-z .'\-]+",
                value,
            )
        ):
            return self.city(value)

        if (
            column == "state"
            and re.fullmatch(
                r"[A-Za-z]{2}",
                value,
            )
        ):
            return self.state(value)

        if (
            column
            in {
                "zip",
                "zipcode",
                "zip_code",
            }
            and re.fullmatch(
                r"\d{5}(?:-\d{4})?",
                value,
            )
        ):
            return self.zipcode(value)

        if (
            column.endswith("name")
            and valid_name(value)
        ):
            return self.name(value)

        return None
def anonymize(sql):
    schema = parse_schema(sql)

    anonymizer = Anonymizer()

    replacements = []

    for literal in parse_literals(
        sql,
        schema,
    ):
        (
            start,
            end,
            table,
            column,
            data_type,
            value,
        ) = literal

        replacement = anonymizer.replace(
            table,
            column,
            data_type,
            value,
        )

        if replacement is not None:
            replacements.append(
                (
                    start,
                    end,
                    quote(replacement),
                )
            )

    output = []
    last = 0
    for start, end, replacement in replacements:
        output.append(
            sql[last:start]
        )

        output.append(
            replacement
        )

        last = end
    output.append(
        sql[last:]
    )
    return "".join(output)
def main():
    parser = argparse.ArgumentParser(
        description=(
            "anonymize PII in a "
            "MySQL sql export"
        )
    )
    parser.add_argument(
        "input"
    )
    parser.add_argument(
        "-o",
        "--output",
        default="anonymized.sql",
    )
    args = parser.parse_args()
    with open(
        args.input,
        "r",
        encoding="utf-8",
    ) as file:
        sql = file.read()
    output = anonymize(sql)
    with open(
        args.output,
        "w",
        encoding="utf-8",
    ) as file:
        file.write(output)
    print(
        f"wrote {args.output}"
    )
if __name__ == "__main__":
    main()