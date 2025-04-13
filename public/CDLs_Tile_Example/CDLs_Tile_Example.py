@fused.udf
def udf(
    bounds: fused.types.Bounds = None, year: int = 2024, crop_type: str = "", chip_len: int = 256, colored: bool = True
):
    """"""
    import numpy as np

    # convert bounds to tile
    tile = common.get_tiles(bounds)

    input_tiff_path = f"s3://fused-asset/data/cdls/{year}_30m_cdls.tif"
    data = common.read_tiff(
        tile, input_tiff_path, output_shape=(chip_len, chip_len), return_colormap=True, cache_max_age="90d"
    )
    if data:
        array_int, metadata = data
    else:
        print("no data")
        return None
    if crop_type:
        array_int = filter_crops(array_int, crop_type, verbose=False)

    # Print out the top 20 classes
    print(crop_counts(array_int).head(20))
    colormap = metadata["colormap"]
    colored_array = (
        np.array([colormap[value] for value in array_int.flat], dtype=np.uint8)
        .reshape(array_int.shape + (4,))
        .transpose(2, 0, 1)
    )

    if colored:
        return colored_array
    else:
        return array_int


# %% utils
common = fused.load("https://github.com/fusedio/udfs/tree/a18669/public/common/").utils


def crop_to_int(crop_type, verbose=True):
    import pandas as pd
    import requests

    url = "https://storage.googleapis.com/earthengine-stac/catalog/USDA/USDA_NASS_CDL.json"
    df_meta = pd.DataFrame(requests.get(url).json()["summaries"]["eo:bands"][0]["gee:classes"])
    mask = df_meta.description.map(lambda x: crop_type.lower() in x.lower())
    df_meta_masked = df_meta[mask]
    if verbose:
        print(f"{df_meta_masked=}")
        print("crop type options", df_meta.description.values)
    return df_meta_masked.value.values


def filter_crops(arr, crop_type, verbose=True):
    import numpy as np

    values_to_keep = crop_to_int(crop_type, verbose=verbose)
    if len(values_to_keep) > 0:
        mask = np.isin(arr, values_to_keep, invert=True)
        arr[mask] = 0
        return arr
    else:
        print(f"{crop_type=} was not found in the list of crops")
        return arr


def crop_counts(arr):
    import numpy as np
    import pandas as pd
    import requests

    unique_values, counts = np.unique(arr, return_counts=True)
    df = pd.DataFrame(counts, index=unique_values, columns=["n_pixel"]).sort_values(by="n_pixel", ascending=False)
    url = "https://storage.googleapis.com/earthengine-stac/catalog/USDA/USDA_NASS_CDL.json"
    df_meta = pd.DataFrame(requests.get(url).json()["summaries"]["eo:bands"][0]["gee:classes"])
    df = df_meta.set_index("value").join(df)[["description", "color", "n_pixel"]]
    df["color"] = "#" + df["color"]
    df.columns = ["crop_type", "color", "n_pixel"]
    df = df.sort_values("n_pixel", ascending=False)
    return df.dropna()
