@fused.udf(cache_max_age=0)
def udf(as_arrow:bool=False):
    import pandas as pd
    df=pd.DataFrame({"col": [{100,200,300}]})
    if not as_arrow:
        return df
    else:   
        import pyarrow as pa
        table = pa.Table.from_pandas(df)
        return table
        