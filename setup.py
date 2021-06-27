import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rusty-results",
    version="1.0.0",
    author="Daniel Sanchez Quiros, Antonio Jose Checa Bustos",
    author_email="sanchez.quiros.daniel@gmail.com, antonio.checa.bustos@gmail.com",
    description="Rust inspired Result and Option types",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(
        ".",
        exclude=[
            "tests*",
            "examples*"
        ]
    ),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    extras_require={
        'pydantic': ["pydantic"]
    },
    python_requires='>=3.7'
)
