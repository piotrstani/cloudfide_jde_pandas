import os
import pandas as pd
import pytest
from solution import add_virtual_column
from pipeline import run_pipeline


def test_pipeline_smoke_test_on_sales_csv():

    if not os.path.exists("sales.csv"):
        pytest.skip("Missing sales.csv file in the working directory")

    run_pipeline()
    assert os.path.exists("revenue_by_region.csv")

    res = pd.read_csv("revenue_by_region.csv")
    assert set(res["region"]) == {"Central", "East", "North", "South", "West"}
    assert (res["total_revenue"] > 0).all()
    assert res["total_revenue"].is_monotonic_decreasing


def test_empty_result_when_consecutive_operators():
    df = pd.DataFrame([[1, 1]] * 2, columns=["label_one", "label_two"])
    df_result = add_virtual_column(df, "label_one ++ label_two", "label_three")
    assert df_result.empty, f"Should return an empty df when the role has two consecutive operators: '++'.\n\nResult:\n\n{df_result}\n\nExpected:\n\nEmpty df"


def test_empty_result_when_trailing_newline():
    df = pd.DataFrame([[1, 1]] * 2, columns=["label_one", "label_two"])
    df_result = add_virtual_column(df, "label_one + label_two\n", "label_three")
    assert df_result.empty, f"Should return an empty df when the role ends with a newline character.\n\nResult:\n\n{df_result}\n\nExpected:\n\nEmpty df"