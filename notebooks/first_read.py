import polars as pl
import typer

app = typer.Typer()


def main() -> None:
    df_raw = pl.read_csv(DATA_FOLDER / RAW_DATA_FILENAME, try_parse_dates=True, infer_schema_length=10000, null_values="NA")
    ## polars.exceptions.ComputeError: could not parse `NA` as dtype `i64` at column 'MasVnrArea' (column number 27), specifying correct dtype with the `schema_overrides` argument
    print(df_raw)
    df_raw.head()


@app.command("entry")
def entry():
    main()


if __name__ == "__main__":
    main()
