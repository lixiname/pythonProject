import datetime
import json




class DateTimeEncoder(json.JSONEncoder):
    """
    datetime编码为模板字符串
    """
    def default(self, obj):
        """

        Args:
            obj: python内置的时刻
        Returns:

        """
        if isinstance(obj, datetime.datetime):
            jsonstr=obj.strftime("%Y-%m-%d %H:%M:%S")
            return jsonstr
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        return json.JSONEncoder.default(self, obj)

def date_time_to_json(date_time):
    json_date_time = json.dumps(date_time, cls=DateTimeEncoder)
    return json_date_time.replace('"', '')

def date_time_rename_file(date_time_str):
    """
    最终获得xxxx-xx-xx_xx-xx-xx模板的时刻字符串
    Args:
        date_time_str:
    Returns:

    """
    middle_str=date_time_str.replace(' ', '_')
    middle_str=middle_str.replace(':', '-')
    return middle_str


def generate_time_stamp():
    """
    得到当前时刻的xxxx-xx-xx_xx-xx-xx模板的时刻字符串
    Returns:
    """
    time = datetime.datetime.now()
    date_time_str = date_time_to_json(time)
    part_file_name = date_time_rename_file(date_time_str)
    return part_file_name
