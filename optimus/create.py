from multipledispatch import dispatch
from pyspark.sql.types import StructField, StructType, StringType

# Helpers
from optimus.helpers.checkit import is_tuple, is_list_of_tuples
from optimus.helpers.functions import get_spark_dtypes_object
from optimus.spark import Spark


class Create:

    @staticmethod
    @dispatch(list, list)
    def data_frame(cols, rows):
        """
        Helper to create a Spark dataframe:
        :param cols: List of Tuple with name, data type and a flag to accept null
        :param rows: List of Tuples if vals with the same number and types that cols
        :return: Dataframe
        """
        if not is_list_of_tuples(rows):
            rows = [(i,) for i in rows]

        specs = []
        for c in cols:

            # Get columns name
            if not is_tuple(c):
                col_name = c
            else:
                col_name = c[0]

            # Get columns data type
            if len(c) == 2:
                var_type = get_spark_dtypes_object(c[1])
            else:
                var_type = StringType()

            # Get column nullable flag. It's just to tell if a column accept nulls as values
            if len(c) == 3:
                nullable = c[2]
            else:
                nullable = True

            # If tuple has not the third param with put it to true to accepts Null in columns
            specs.append([col_name, var_type, nullable])

        struct_fields = list(map(lambda x: StructField(*x), specs))

        return Spark.instance.spark.createDataFrame(rows, StructType(struct_fields))

    @staticmethod
    @dispatch(object)
    def data_frame(pdf):
        """
        Helper to create a Spark dataframe:
        :param pdf: Panda Dataframe
        :return: Dataframe
        """

        return Spark.instance.spark.createDataFrame(pdf)

    df = data_frame
