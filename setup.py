from distutils.core import setup
setup(
    name="DataPreProce",
    version="1.0",
    description="The data collected by MYO bracelet is preprocessed, including data cutting, stretching, filling and feature extraction",
    url="https://github.com/ZhangJiangtao-0108/DataPreProcess_packages.githttps://github.com/TangSir61/UIMonkey2021.git",
    author="ZhangJiangtao",
    author_email="zjt0108@foxmail.com",
    py_modules=["DataPreProce.DataPre",\
                "DataPreProce.makedatasets",\
                "DataPreProce.algorithm.Attitude_Angle_solution",\
                "DataPreProce.algorithm.cutting_algorithm",\
                "DataPreProce.algorithm.Butter_filter",\
                "DataPreProce.algorithm.emg_correct",\
                "DataPreProce.algorithm.emg_feature",\
                "DataPreProce.test"],
    packages = ['DataPreProce'],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'DataPreProce = DataPreProce.__main__:main'
        ]
    }
)
