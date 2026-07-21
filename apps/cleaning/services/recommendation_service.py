class RecommendationService:

    @staticmethod
    def generate_recommendations(dataset):

        profile = dataset.profile

        recommendations = {}

        if profile.duplicate_rows > 0:

            recommendations["remove_duplicates"] = {
                "recommended": True,
                "default_selected": True,
                "reason": (f"{profile.duplicate_rows} duplicate rows detected."),
            }

        missing_columns = {
            column: count
            for column, count in profile.missing_values.items()
            if count > 0
        }
        if missing_columns:

            recommendations["handle_missing_values"] = {
                "recommended": True,
                "default_selected": True,
                "reason": (
                    f"Missing values found in " f"{len(missing_columns)} columns."
                ),
                "columns": list(missing_columns.keys()),
            }

        candidate_text_columns = []
        for column, dtype in profile.data_type_summary.items():

            if dtype in ["object", "string", "str"]:

                unique_count = profile.unique_value_summary.get(column, 0)

                if unique_count <= 50:
                    candidate_text_columns.append(column)

        if candidate_text_columns:

            recommendations["standardize_text"] = {
                "recommended": True,
                "default_selected": False,
                "reason": ("Potential inconsistent text formatting detected."),
                "columns": candidate_text_columns,
            }

        date_columns = []
        for column in profile.column_names:

            if "date" in column.lower():
                date_columns.append(column)

        if date_columns:

            recommendations["standardize_dates"] = {
                "recommended": True,
                "default_selected": False,
                "reason": ("Potential date columns detected."),
                "columns": date_columns,
                "parsing_mode": "auto",
                "day_first": True,
            }

        numeric_keywords = [
            "revenue",
            "price",
            "amount",
            "cost",
            "sales",
            "age",
            "quantity",
            "profit",
            "discount",
            "total",
            "balance",
            "income",
            "expense",
            "salary",
            "score",
            "rating",
        ]
        candidate_numeric_columns = []

        for column, dtype in profile.data_type_summary.items():

            if dtype in ["object", "string", "str"]:

                if any(keyword in column.lower() for keyword in numeric_keywords):
                    candidate_numeric_columns.append(column)
        if candidate_numeric_columns:

            recommendations["fix_data_types"] = {
                "recommended": True,
                "default_selected": False,
                "reason": ("Numeric columns stored as text detected."),
                "columns": candidate_numeric_columns,
            }

        return recommendations
