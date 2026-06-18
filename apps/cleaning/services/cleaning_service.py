import os

import pandas as pd

from django.core.files import File

from apps.datasets.models import Dataset
from apps.cleaning.models import (
    CleaningJob,
    CleaningStatus,
)

class CleaningService:

    @staticmethod
    def load_dataframe(dataset):

        file_path = dataset.original_file.path

        if dataset.file_type == "csv":
            return pd.read_csv(file_path)

        if dataset.file_type == "xlsx":
            return pd.read_excel(file_path)

        raise ValueError(
            f"Unsupported file type: {dataset.file_type}"
        )
    

    @staticmethod
    def remove_duplicates(
        dataset: Dataset
    ):

        job = CleaningJob.objects.create(
            dataset=dataset,
            status=CleaningStatus.RUNNING,
        )

        try:

            df = (
                CleaningService.load_dataframe(
                    dataset
                )
            )

            rows_before = len(df)

            cleaned_df = (
                df.drop_duplicates()
            )

            rows_after = len(cleaned_df)

            duplicates_removed = (
                rows_before - rows_after
            )

            job.rows_before = rows_before

            job.rows_after = rows_after

            job.duplicates_removed = (
                duplicates_removed
            )

            output_filename = (
                f"{dataset.id}_cleaned.csv"
            )

            output_path = (
                f"/tmp/{output_filename}"
            )

            cleaned_df.to_csv(
                output_path,
                index=False
            )

            with open(
                output_path,
                "rb"
            ) as cleaned_file:

                job.cleaned_file.save(
                    output_filename,
                    File(cleaned_file),
                    save=False
                )

            job.cleaning_summary = {

                "duplicates_removed":
                    duplicates_removed,

                "rows_before":
                    rows_before,

                "rows_after":
                    rows_after,
            }

            job.status = (
                CleaningStatus.COMPLETED
            )

            job.save()

            os.remove(output_path)

            return job

        except Exception:

            job.status = (
                CleaningStatus.FAILED
            )

            job.save()

            raise