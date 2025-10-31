@fused.udf
def udf(name: str='df'):
    data = fused.run('secret_jaguar', name=name)
    return data