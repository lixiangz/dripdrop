"""
SQL validation using Context-Free Grammar (CFG) parser.
This ensures generated SQL matches the exact grammar that GPT-5 will use.
"""
import re
from functools import lru_cache

from lark import Lark, UnexpectedInput, Token

from .schema import COLUMNS, DATABASE, NUMERIC_COLUMNS, TABLE


# Grammar is generated from schema constants to keep the model constraint and server-side validation in sync.
def _token(name: str) -> str:
    return name.upper()


def _rule(name: str, tokens: tuple[str, ...]) -> str:
    lines = [f"{name}: {tokens[0]}"]
    for token in tokens[1:]:
        lines.append(f"      | {token}")
    return "\n".join(lines)


COLUMN_TOKENS = tuple(_token(column) for column in COLUMNS)
NUMERIC_TOKENS = tuple(_token(column) for column in NUMERIC_COLUMNS)
COLUMN_RULE = _rule("column", COLUMN_TOKENS)
NUMERIC_RULE = _rule("numeric_column", NUMERIC_TOKENS)

# Create case-insensitive regex patterns for column names
# Use character class for case-insensitive matching: [Cc][Oo][Ll][Uu][Mm][Nn]


def _case_insensitive_pattern(text: str) -> str:
    """Convert text to case-insensitive regex pattern using character classes."""
    pattern = ""
    for char in text:
        if char.isalpha():
            pattern += f"[{char.upper()}{char.lower()}]"
        elif char == "_":
            pattern += "_"
        else:
            # Escape other special characters
            pattern += re.escape(char)
    return pattern


# Generate token definitions with explicit lowercase match first (higher priority)
# Then case-insensitive pattern as fallback
TOKEN_DEFS = "\n".join(
    f'{token}: "{column}" | /^{_case_insensitive_pattern(column)}$/'
    for token, column in zip(COLUMN_TOKENS, COLUMNS)
)

# Pre-compute table name pattern
# Use explicit string match first for higher priority
TABLE_NAME_EXACT = TABLE  # "coin_Bitcoin"
TABLE_NAME_PATTERN = _case_insensitive_pattern(TABLE)

# CFG Grammar for SQL queries matching CFG_SCOPE.md
# Note: SQL keywords are case-insensitive, but column/table names are case-sensitive
_SQL_GRAMMAR = f"""
start: select_stmt

select_stmt: SELECT select_list FROM table_name where_clause group_by_clause? order_by_clause? limit_clause?

select_list: select_item ("," select_item)*

agg_expr: sum_expr
        | avg_expr
        | min_expr
        | max_expr
        | count_expr

sum_expr: SUM "(" numeric_column ")" alias?
avg_expr: AVG "(" numeric_column ")" alias?
min_expr: MIN "(" numeric_column ")" alias?
max_expr: MAX "(" numeric_column ")" alias?
count_expr: COUNT "(" "*" ")" alias?
          | COUNT "(" column ")" alias?

alias: AS IDENTIFIER

select_item: agg_expr
           | column alias?

column_list: column ("," column)*

where_clause: WHERE condition

condition: time_filter (AND time_filter)*

time_filter: date_interval_filter
           | date_between_filter

date_interval_filter: DATE ">=" NOW "(" ")" "-" INTERVAL INT interval_unit
date_between_filter: DATE BETWEEN string_literal AND string_literal

interval_unit: HOUR
             | DAY

group_by_clause: GROUP BY group_dimension

group_dimension: to_start_of_day
               | to_start_of_hour

to_start_of_day: TOSTARTOFDAY "(" DATE ")"
to_start_of_hour: TOSTARTOFHOUR "(" DATE ")"

order_by_clause: ORDER BY order_list
order_list: order_item ("," order_item)*
order_item: column order_dir?
          | IDENTIFIER order_dir?
order_dir: ASC | DESC

limit_clause: LIMIT INT

table_name: TABLE_NAME

{COLUMN_RULE}

{NUMERIC_RULE}

literal: string_literal
       | number_literal

string_literal: SINGLE_QUOTED
number_literal: SIGNED_NUMBER

SINGLE_QUOTED: "'" /[^']*/ "'"

// Column and table tokens must come before IDENTIFIER for proper token priority
// (More specific tokens must be defined before general ones)
{TOKEN_DEFS}

// Table name: explicit match first for priority, then case-insensitive
TABLE_NAME: "{TABLE_NAME_EXACT}" | /^{TABLE_NAME_PATTERN}$/

// Case-insensitive SQL keywords
SELECT: /[Ss][Ee][Ll][Ee][Cc][Tt]/
FROM: /[Ff][Rr][Oo][Mm]/
WHERE: /[Ww][Hh][Ee][Rr][Ee]/
GROUP: /[Gg][Rr][Oo][Uu][Pp]/
BY: /[Bb][Yy]/
ORDER: /[Oo][Rr][Dd][Ee][Rr]/
ASC: /[Aa][Ss][Cc]/
DESC: /[Dd][Ee][Ss][Cc]/
LIMIT: /[Ll][Ii][Mm][Ii][Tt]/
AS: /[Aa][Ss]/
BETWEEN: /[Bb][Ee][Tt][Ww][Ee][Ee][Nn]/
AND: /[Aa][Nn][Dd]/
SUM: /[Ss][Uu][Mm]/
COUNT: /[Cc][Oo][Uu][Nn][Tt]/
AVG: /[Aa][Vv][Gg]/
MIN: /[Mm][Ii][Nn]/
MAX: /[Mm][Aa][Xx]/
NOW: /[Nn][Oo][Ww]/
INTERVAL: /[Ii][Nn][Tt][Ee][Rr][Vv][Aa][Ll]/
HOUR: /[Hh][Oo][Uu][Rr]/
DAY: /[Dd][Aa][Yy]/

// Case-insensitive function names (ClickHouse/Tinybird may normalize case)
// Use character classes for case-insensitive matching instead of (?i) flag
TOSTARTOFDAY: /^[Tt][Oo][Ss][Tt][Aa][Rr][Tt][Oo][Ff][Dd][Aa][Yy]$/
TOSTARTOFHOUR: /^[Tt][Oo][Ss][Tt][Aa][Rr][Tt][Oo][Ff][Hh][Oo][Uu][Rr]$/

// General identifier (must come after specific column tokens)
IDENTIFIER: /[A-Za-z_][A-Za-z0-9_]*/

%import common.INT
%import common.SIGNED_NUMBER
%import common.WS_INLINE
%ignore WS_INLINE
"""


def sql_grammar() -> str:
    """Return the SQL grammar string (useful for GPT-5 CFG generation)."""
    return _SQL_GRAMMAR


@lru_cache(maxsize=1)
def _parser() -> Lark:
    """Cached Lark parser instance."""
    return Lark(_SQL_GRAMMAR, start="start", parser="lalr")


def validate_sql(sql: str) -> None:
    """
    Validate SQL query against the CFG grammar.

    Raises:
        ValueError: If SQL is empty, doesn't match grammar, or violates constraints.
    """
    # Normalize SQL: strip, remove semicolons, remove comments
    text = sql.strip().rstrip(";")

    # Remove SQL comments
    text = re.sub(r"--.*?$", "", text, flags=re.MULTILINE)
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
    text = text.strip()

    if not text:
        raise ValueError("SQL is required")

    # Check for forbidden operations (defense in depth)
    forbidden = re.compile(
        r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|TRUNCATE|CREATE|GRANT|REVOKE|ATTACH|DETACH|OPTIMIZE|SYSTEM|KILL)\b",
        re.IGNORECASE,
    )
    if forbidden.search(text):
        raise ValueError("Forbidden SQL keyword detected.")

    try:
        _parser().parse(text)
    except UnexpectedInput as exc:
        raise ValueError(
            f"SQL does not match the allowed grammar: {exc}") from exc
