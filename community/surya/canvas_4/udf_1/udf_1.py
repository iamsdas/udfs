@fused.udf(cache_max_age="0s")
def udf(name: str = "world"):
    import pandas as pd

    return pd.DataFrame({"hello": [name]})
