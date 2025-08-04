from setuptools import setup, find_packages

setup(
    name="wafer_viewer",
    version="0.1.0",
    description="A web app for visualizing wafer chip data.",
    author="Monish Erode Sridhar",
    packages=find_packages(),
    install_requires=[
        "flask",
        "pandas"
    ],
    extras_require={
        "dev": [
            "flask",
            "matplotlib",
            "numpy",
            "seaborn",
            "melt_data_layer[all] @ git+https://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@github.com/meliolabs/Melt_Dal.git@develop#egg=melt_data_layer"
        ]
    },
    include_package_data=True,
    python_requires=">=3.7",
)
