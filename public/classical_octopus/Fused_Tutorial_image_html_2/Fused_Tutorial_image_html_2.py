@fused.udf
def udf(url: str = "https://docs.fused.io/assets/images/dynamic_file_system-7dc205b28ef067029f962754201889c7.png", max_width: int = 800):
    return f"""<html style="background-color: #1b1f23;">
<body style="margin:0; display:flex; justify-content:center; align-items:center; height:100vh;">
    <img src="{url}" style="max-width:{max_width}px; width:100%; height:auto; object-fit:contain;" />
</body></html>"""
