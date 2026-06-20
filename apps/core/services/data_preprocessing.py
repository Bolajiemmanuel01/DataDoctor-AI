import pandas as pd
import pandas.api.types as ptypes


class DataPreprocessingService:

    @staticmethod
    def preprocess_dataframe(df):

        df.columns = df.columns.str.strip()

        for column in df.columns:

            if (
                ptypes.is_object_dtype(df[column])
                or ptypes.is_string_dtype(df[column])
            ):

                df[column] = df[column].astype(str)

                df[column] = (
                    df[column]
                    .str.replace(
                        r'[\u00A0\u200B\xa0]',
                        '',
                        regex=True
                    )
                    .str.strip()
                )

                df[column] = (
                    df[column]
                    .str.replace(r'\s+', ' ', regex=True)
                )

                df[column] = df[column].replace(
                    r'^\s*$',
                    pd.NA,
                    regex=True
                )

                df[column] = df[column].replace(
                    [
                        "N/A",
                        "n/a",
                        "NULL",
                        "null",
                        "None",
                        "none",
                        "-",
                        "nan"
                    ],
                    pd.NA
                )

        return df