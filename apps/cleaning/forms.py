from django import forms


class CleaningConfigForm(forms.Form):

    remove_duplicates = forms.BooleanField(
        required=False,
        label="Remove Duplicates"
    )

    handle_missing_values = forms.BooleanField(
        required=False,
        label="Handle Missing Values"
    )

    standardize_text = forms.BooleanField(
        required=False,
        label="Standardize Text"
    )

    standardize_dates = forms.BooleanField(
        required=False,
        label="Standardize Dates"
    )

    fix_data_types = forms.BooleanField(
        required=False,
        label="Fix Data Types"
    )

    def __init__(self, *args, recommendations=None, **kwargs):

        super().__init__(*args, **kwargs)

        recommendations = recommendations or {}

        # -------------------------------
        # Set default selected options
        # -------------------------------
        if recommendations.get(
            "remove_duplicates",
            {}
        ).get("default_selected"):

            self.fields[
                "remove_duplicates"
            ].initial = True

        if recommendations.get(
            "handle_missing_values",
            {}
        ).get("default_selected"):

            self.fields[
                "handle_missing_values"
            ].initial = True

        if recommendations.get(
            "standardize_text",
            {}
        ).get("default_selected"):

            self.fields[
                "standardize_text"
            ].initial = True

        if recommendations.get(
            "standardize_dates",
            {}
        ).get("default_selected"):

            self.fields[
                "standardize_dates"
            ].initial = True

        if recommendations.get(
            "fix_data_types",
            {}
        ).get("default_selected"):

            self.fields[
                "fix_data_types"
            ].initial = True

        # -------------------------------
        # Text columns
        # -------------------------------
        text_recommendation = recommendations.get(
            "standardize_text",
            {}
        )

        text_columns = text_recommendation.get(
            "columns",
            []
        )

        if text_columns:

            self.fields[
                "text_columns"
            ] = forms.MultipleChoiceField(
                label="Select Text Columns",
                choices=[
                    (column, column)
                    for column in text_columns
                ],
                required=False,
                widget=forms.CheckboxSelectMultiple
            )

        # -------------------------------
        # Date columns
        # -------------------------------
        date_recommendation = recommendations.get(
            "standardize_dates",
            {}
        )

        date_columns = date_recommendation.get(
            "columns",
            []
        )

        if date_columns:

            self.fields[
                "date_columns"
            ] = forms.MultipleChoiceField(
                label="Select Date Columns",
                choices=[
                    (column, column)
                    for column in date_columns
                ],
                required=False,
                widget=forms.CheckboxSelectMultiple
            )

            self.fields["day_first"] = forms.BooleanField(
                label="Use DD/MM/YYYY Format",
                required=False,
                initial=date_recommendation.get(
                    "day_first",
                    True
                )
            )

        # -------------------------------
        # Datatype columns
        # -------------------------------
        datatype_recommendation = recommendations.get(
            "fix_data_types",
            {}
        )

        datatype_columns = datatype_recommendation.get(
            "columns",
            []
        )

        if datatype_columns:

            self.fields[
                "datatype_columns"
            ] = forms.MultipleChoiceField(
                label="Select Numeric Columns",
                choices=[
                    (column, column)
                    for column in datatype_columns
                ],
                required=False,
                widget=forms.CheckboxSelectMultiple
            )

    def clean(self):

        cleaned_data = super().clean()

        if cleaned_data.get("standardize_text"):

            text_columns = cleaned_data.get(
                "text_columns",
                []
            )

            if not text_columns:
                raise forms.ValidationError(
                    "Please select at least one text column."
                )

        if cleaned_data.get("standardize_dates"):

            date_columns = cleaned_data.get(
                "date_columns",
                []
            )

            if not date_columns:
                raise forms.ValidationError(
                    "Please select at least one date column."
                )

        if cleaned_data.get("fix_data_types"):

            datatype_columns = cleaned_data.get(
                "datatype_columns",
                []
            )

            if not datatype_columns:
                raise forms.ValidationError(
                    "Please select at least one datatype column."
                )

        return cleaned_data

    def build_cleaning_config(self):

        cleaned = self.cleaned_data

        config = {
            "remove_duplicates": cleaned.get(
                "remove_duplicates",
                False
            ),

            "handle_missing_values": cleaned.get(
                "handle_missing_values",
                False
            ),

            "standardize_text": {
                "enabled": cleaned.get(
                    "standardize_text",
                    False
                ),
                "columns": cleaned.get(
                    "text_columns",
                    []
                )
            },

            "standardize_dates": {
                "enabled": cleaned.get(
                    "standardize_dates",
                    False
                ),
                "columns": cleaned.get(
                    "date_columns",
                    []
                ),
                "day_first": cleaned.get(
                    "day_first",
                    True
                )
            },

            "fix_data_types": {
                "enabled": cleaned.get(
                    "fix_data_types",
                    False
                ),
                "columns": cleaned.get(
                    "datatype_columns",
                    []
                )
            }
        }

        return config