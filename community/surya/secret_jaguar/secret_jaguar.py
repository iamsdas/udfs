@fused.udf
def udf(name: str='df'):
    data = fused.run('echoer', name=name)
    return data