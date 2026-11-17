import re
import pandas as pd

COLUMN_LABEL_PATTERN = re.compile(r'^[a-zA-Z_]+$')
COLUMN_TOKEN_PATTERN = re.compile(r'[a-zA-Z_]+')
VALID_ROLE_PATTERN =re.compile(r'^[a-zA-Z_\s+\-*]+$')

def add_virtual_column(df: pd.DataFrame, role: str, new_column: str) -> pd.DataFrame:
    #Column labels must consist only of letters and underscores (new)
    if not isinstance(new_column, str) or not COLUMN_LABEL_PATTERN.match(new_column):
        return pd.DataFrame()

    # #Column labels must consist only of letters and underscores (existing)
    for col in df.columns:
        if not isinstance(col, str) or not COLUMN_LABEL_PATTERN.match(str(col)):
            return pd.DataFrame()

    # The function must support basic operations: addition (+), subtraction (-), and multiplication (*
    if not VALID_ROLE_PATTERN.match(role):
        return pd.DataFrame()

    #If the role or any column label is incorrect, the function should return an empty DataFram
    tokens = COLUMN_TOKEN_PATTERN.findall(role)
    for token in tokens:
        if token not in df.columns:
            return pd.DataFrame()

    try:
        result_series = df.eval(role) #ast
        new_df = df.copy()
        new_df[new_column] = result_series
        return new_df
    except (pd.errors.UndefinedVariableError, SyntaxError, ValueError, TypeError, KeyError):
        return pd.DataFrame()