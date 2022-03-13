from timeseries_data.Timeseries_Data import TimeseriesData
from timeseries_data import util


def import_subject(mode, num):
    data = TimeseriesData()
    path = util.path_resolver(mode, num)
    data.read_from_csv(path)
    return data