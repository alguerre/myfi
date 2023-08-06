from datetime import datetime
from typing import Dict, List

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from sqlalchemy.orm import Session

from src.gui import DataService
from src.gui.painter import (
    CategoricalExpensesAnalysisPainter,
    CategoricalExpensesEvolutionPainter,
    SavingsEvolutionPainter,
    YearlySalaryPainter,
    YearlySavingsPainter,
)
from src.gui.painter.base import BasePainter
from src.repositories import CategoriesRepository, FinancesRepository
from utils.database import with_session

plt.rcParams["font.family"] = "calibri"


def build_df_filters(
    data_service: DataService,
    categories: List[str],
    date: List[datetime],
    concept: str,
) -> pd.Series:
    categories_filter = (
        (data_service.reduced_df["category"].isin(categories)) if categories else None
    )

    date_filter = (date[0] <= data_service.reduced_df["date"]) & (
        data_service.reduced_df["date"] <= date[1]
    )

    concept_filter = (
        data_service.reduced_df["concept"].str.contains(concept)
        if concept != ""
        else None
    )

    filters = None
    for f in [categories_filter, date_filter, concept_filter]:
        if f is None:
            continue
        filters = f if filters is None else filters & f
    return filters


def launch_gui(data_service: DataService, painters: Dict[str, BasePainter]):
    st.set_page_config(
        page_title="Finances Analysis",
        page_icon="✅",
        layout="wide",
    )

    st.title("Finances Analysis")

    with st.container():
        col1, col2 = st.columns(2, gap="large")

        with col1:
            st.header("Total money")
            st.pyplot(painters["savings_evolution"].paint())

        with col2:
            st.header("Account movements")

            col2_1, col2_2 = st.columns(2, gap="small")

            with col2_1:
                categories = st.multiselect("Categories", data_service.categories)

            with col2_2:
                concept = st.text_input("Concept filter")

            date = st.slider(
                "Date range",
                value=(
                    min(data_service.reduced_df["date"]),
                    max(data_service.reduced_df["date"]),
                ),
                format="DD-MM-YY",
            )

            df_filter = build_df_filters(data_service, categories, date, concept)

            st.dataframe(data_service.reduced_df[df_filter], use_container_width=True)

    with st.container():
        st.divider()
        st.header("Global parameters")

        col1, col2 = st.columns(2, gap="large")

        with col1:
            st.pyplot(painters["salary_evolution"].paint())
        with col2:
            st.pyplot(painters["yearly_savings"].paint())

    with st.container():
        st.divider()
        st.header("Expenses by category")

        col1, col2 = st.columns(2, gap="large")

        with col1:
            category = st.selectbox("Select category", data_service.categories)
            st.pyplot(
                painters["categorical_expenses_evolution"].paint(category=category)
            )

        with col2:
            year = st.selectbox("Select year", sorted(data_service.years, reverse=True))
            st.pyplot(painters["categorical_expenses_analysis"].paint(year=year))


@with_session()
def main(session: Session):
    repositories = {
        "repo_categories": CategoriesRepository(session),
        "repo_finances": FinancesRepository(session),
    }

    data_service = DataService(**repositories)

    painters = {
        "categorical_expenses_analysis": CategoricalExpensesAnalysisPainter(
            data_service
        ),
        "categorical_expenses_evolution": CategoricalExpensesEvolutionPainter(
            data_service
        ),
        "salary_evolution": YearlySalaryPainter(data_service),
        "savings_evolution": SavingsEvolutionPainter(data_service),
        "yearly_savings": YearlySavingsPainter(data_service),
    }

    launch_gui(data_service, painters)


if __name__ == "__main__":
    main()
