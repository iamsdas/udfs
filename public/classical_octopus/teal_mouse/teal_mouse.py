@fused.udf(cache_max_age=0)
def udf(bounds: fused.types.Bounds=[-0.113, 51.503, -0.099, 51.513], release: str='2025-06-25-0', theme: str=None, overture_type: str=None, use_columns: list=None):
    fused.options.realtime_client_id = "_local"
    parent_udf = fused.load('Overture_Maps_Example')
    result = parent_udf(x=16375, y=10898, z=15, cache_max_age=0)
    return result