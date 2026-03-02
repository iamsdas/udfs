@fused.udf()
def udf(name: str = "world"):
    udf_ = fused.load("judicial_sheep")

    print('as_arrow=False:', fused.run(udf_, as_arrow=False)['col'].iloc[0][0])
    print('as_arrow=True:', udf_(as_arrow=True)['col'].iloc[0][0])
    