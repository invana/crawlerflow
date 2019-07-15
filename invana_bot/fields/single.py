import locale
import re


class FieldTransformerBase(object):
    """

    IntField(data="1").transform()



    """

    def get_method(self):
        """
        Should return the function that takes data as input. Ex: str, int, float,

        :return:
        """
        raise NotImplementedError("This method is not implemented")

    def __init__(self, data=None):
        self.data = data

    def try_or_none(self):
        transformation_method = self.get_method()
        try:
            result_data = transformation_method(self.data)
        except Exception as e:
            print(e)
            result_data = self.data
        return result_data

    def transform(self):
        return self.try_or_none()


class StringField(FieldTransformerBase):

    def get_method(self):
        return str


class IntField(FieldTransformerBase):
    def get_method(self):
        def custom_int(data):
            data = locale.atoi(data)
            return int(data)

        return custom_int


class FloatField(FieldTransformerBase):
    def get_method(self):
        def custom_float(data):
            data = re.findall(r"[-+]?\d*\.\d+|[-+]?\d+", data)
            if len(data) > 0:
                return float(data[0])
            else:
                return float(0)
        return custom_float


class DictField(FieldTransformerBase):
    def get_method(self):
        return dict


class RawField(FieldTransformerBase):
    def get_method(self):
        return None
