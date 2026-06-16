import pandas as pd

from apps.datasets.models import Dataset
from apps.profiling.models import DatasetProfile


class ProfilingService:
    """
    Handles dataset profiling.
    """

    @staticmethod
    def load_dataframe(dataset: Dataset):

        file_path = dataset.original_file.path

        if dataset.file_type == "csv":
            return pd.read_csv(file_path)

        if dataset.file_type == "xlsx":
            return pd.read_excel(file_path)

        raise ValueError(
            f"Unsupported file type: {dataset.file_type}"
        )

    @staticmethod
    def generate_profile(dataset: Dataset):

        df = ProfilingService.load_dataframe(dataset)

        profile_data = {

            "row_count": len(df),

            "column_count": len(df.columns),

            "missing_values": (
                df.isnull()
                .sum()
                .to_dict()
            ),

            "duplicate_rows": int(
                df.duplicated().sum()
            ),

            "unique_value_summary": {
                column: int(df[column].nunique())
                for column in df.columns
            },

            "data_type_summary": {
                column: str(df[column].dtype)
                for column in df.columns
            },
        }

        profile, created = (
            DatasetProfile.objects.update_or_create(
                dataset=dataset,
                defaults=profile_data,
            )
        )

        return profile