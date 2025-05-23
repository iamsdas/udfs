@fused.udf
def udf(count: int = 0):
    # Create duckdb connection
    common_utils = fused.load("https://github.com/fusedio/udfs/tree/3569595/public/common/").utils
    con = common_utils.duckdb_connect()

    # Load and return data
    path = "https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/sf.h3cells.json"
    df = con.sql(f"FROM '{path}' WHERE count > {count}").df()

    return df
