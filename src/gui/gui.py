from datetime import datetime
from typing import Dict, List

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from dependency_injector.wiring import Provide, inject

from src.containers import Container
from src.gui.painter.base import BasePainter
from src.gui.service import DataService

plt.rcParams["font.family"] = "calibri"


class Gui:
    def __init__(
        self,
        data_service: DataService,
        painters: Dict[str, BasePainter],
    ):
        self.service = data_service
        self.painters = painters

    def build_df_filters(
        self,
        categories: List[str],
        date: List[datetime],
        concept: str,
    ) -> pd.Series:
        categories_filter = (
            (self.service.data["category"].isin(categories)) if categories else None
        )

        date_filter = (date[0] <= self.service.data["date"]) & (
            self.service.data["date"] <= date[1]
        )

        concept_filter = (
            self.service.data["concept"].str.contains(concept)
            if concept != ""
            else None
        )

        filters = None
        for f in [categories_filter, date_filter, concept_filter]:
            if f is None:
                continue
            filters = f if filters is None else filters & f
        return filters

    def total_money(self):
        st.pyplot(self.painters["savings_evolution"].paint())

    def account_movements(self):
        col2_1, col2_2 = st.columns(2, gap="small")

        with col2_1:
            categories = st.multiselect("Categories", self.service.categories)

        with col2_2:
            concept = st.text_input("Concept filter")

        date = st.slider(
            "Date range",
            value=(
                min(self.service.data["date"]),
                max(self.service.data["date"]),
            ),
            format="DD-MM-YY",
        )

        df_filter = self.build_df_filters(categories, date, concept)

        st.dataframe(self.service.data[df_filter], use_container_width=True)

    def global_parameters(self):
        col1, col2 = st.columns(2, gap="large")

        with col1:
            st.pyplot(self.painters["salary_evolution"].paint())
        with col2:
            st.pyplot(self.painters["yearly_savings"].paint())

    def expenses_by_category(self):
        col1, col2 = st.columns(2, gap="large")

        with col1:
            category = st.selectbox("Select category", self.service.categories)
            st.pyplot(
                self.painters["categorical_expenses_evolution"].paint(category=category)
            )

        with col2:
            year = st.selectbox("Select year", sorted(self.service.years, reverse=True))
            st.pyplot(self.painters["categorical_expenses_analysis"].paint(year=year))

    def build(self):
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
                self.total_money()

            with col2:
                st.header("Account movements")
                self.account_movements()

        with st.container():
            st.divider()
            st.header("Global parameters")
            self.global_parameters()

        with st.container():
            st.divider()
            st.header("Expenses by category")
            self.expenses_by_category()


@inject
def launch_gui(
    service: DataService = Provide[Container.data_service],
    painters: Dict[str, BasePainter] = Provide[Container.painters],
):
    Gui(service, painters).build()


if __name__ == "__main__":
    # Start the dependency-injector
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])

    launch_gui()
