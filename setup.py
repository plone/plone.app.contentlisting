from pathlib import Path
from setuptools import setup


version = "4.0.0a1"

long_description = (
    f"{Path('README.rst').read_text()}\n{Path('CHANGES.rst').read_text()}\n"
)

setup(
    name="plone.app.contentlisting",
    version=version,
    description="Listing of content for the Plone CMS",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    # Get more strings from
    # https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Plone",
        "Framework :: Plone :: 6.2",
        "Framework :: Plone :: Core",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="content list Plone",
    author="Plone Foundation",
    author_email="plone-developers@lists.sourceforge.net",
    url="https://pypi.org/project/plone.app.contentlisting",
    license="GPL version 2",
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.10",
    install_requires=[
        "plone.base",
        "Products.MimetypesRegistry",
        "Products.ZCatalog",
        "plone.i18n",
        "plone.registry",
        "plone.rfc822",
        "plone.uuid",
        "Zope",
    ],
    extras_require={
        "test": [
            "plone.app.contenttypes[test]",
            "plone.app.testing",
            "plone.batching",
            "plone.namedfile",
            "plone.testing",
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
