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
        return int


class FloatField(FieldTransformerBase):
    def get_method(self):
        return float


class DictField(FieldTransformerBase):
    def get_method(self):
        return dict


class RawField(FieldTransformerBase):
    def get_method(self):
        return None
