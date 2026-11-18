import re
import pandas as pd

COLUMN_LABEL= r'[a-zA-Z_]+'
OPERATOR = r'[+\-*]'
COLUMN_LABEL_PATTERN = re.compile(COLUMN_LABEL)
VALID_ROLE_PATTERN = re.compile(rf'[ ]*{COLUMN_LABEL}(?:[ ]*{OPERATOR}[ ]*{COLUMN_LABEL})*[ ]*')


def add_virtual_column(df: pd.DataFrame, role: str, new_column: str) -> pd.DataFrame:
    #Column labels must consist only of letters and underscores (new)
    if not isinstance(new_column, str) or not COLUMN_LABEL_PATTERN.fullmatch(new_column):
        return pd.DataFrame()

    # #Column labels must consist only of letters and underscores (existing)
    for col in df.columns:
        if not isinstance(col, str) or not COLUMN_LABEL_PATTERN.fullmatch(str(col)):
            return pd.DataFrame()

    # The function must support basic operations: addition (+), subtraction (-), and multiplication (*
    if not isinstance(role, str) or not VALID_ROLE_PATTERN.fullmatch(role):
        return pd.DataFrame()

    #If the role or any column label is incorrect, the function should return an empty DataFram
    for token in COLUMN_LABEL_PATTERN.findall(role):
        if token not in df.columns:
            return pd.DataFrame()

    try:
        result_series = df.eval(role) #ast
        new_df = df.copy()
        new_df[new_column] = result_series
        return new_df
    except (pd.errors.UndefinedVariableError, SyntaxError, ValueError, TypeError, KeyError, AttributeError):
        return pd.DataFrame()