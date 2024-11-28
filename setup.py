from setuptools import find_packages, setup

setup(
    name="db-table-tree",
    install_requires=[
        "ttkbootstrap",
        "mysql-connector-python",
        "sqlalchemy",
        "networkx",
        "matplotlib"
    ],
    packages=find_packages(),
    extras_require={
        "dev": [
        ]
    },
    entry_points={
        "console_scripts": [
            "db_table_tree = db_table_tree:main",
        ]
    },
)
