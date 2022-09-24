from setuptools import setup

setup(
    name="spend-reporter",
    version="0.2.1",
    py_modules=["report"],
    include_package_data=True,
    install_requires=["click", "tabulate"],
    entry_points="""
        [console_scripts]
        report=report:cli
    """,
)
