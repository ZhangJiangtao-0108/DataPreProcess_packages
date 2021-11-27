from distutils.core import setup
setup(
    name="DataPreProce",
    version="1.0",
    description="The data collected by MYO bracelet is preprocessed, including data cutting, stretching, filling and feature extraction",
    author="ZhangJiangtao",
    py_modules=["packages.DataPre",\
                "packages.makedatasets",\
                "packages.algorithm.Attitude_Angle_solution",\
                "packages.algorithm.cutting_algorithm",\
                "packages.algorithm.emg_correct",\
                "oackages.algorithm.emg_feature"]
)
