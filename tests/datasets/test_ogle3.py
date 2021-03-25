#!/usr/bin/env python
# -*- coding: utf-8 -*-

# The MIT License (MIT)

# Copyright (c) 2017 Juan Cabral

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


# =============================================================================
# DOC
# =============================================================================

"""All ogle3 access tests"""


# =============================================================================
# IMPORTS
# =============================================================================

import os
import tarfile
from unittest import mock

from feets.datasets import ogle3

import numpy as np

import pandas as pd

from ..conftest import DATA_PATH

# =============================================================================
# BASE CLASS
# =============================================================================


def test_load_OGLE3_catalog():
    df = pd.DataFrame({"# ID": [1, 2, 3]})
    with mock.patch("pandas.read_table", return_value=df):
        with mock.patch("bz2.BZ2File") as BZ2File:
            assert "ID" not in df.columns
            assert "# ID" in df.columns

            ogle3.load_OGLE3_catalog()
            assert "ID" in df.columns
            assert "# ID" not in df.columns
            BZ2File.assert_called_with(ogle3.CATALOG_PATH)


def test_fetch_OGLE3():
    store_path = ogle3._get_OGLE3_data_home(None)
    cat = ogle3.load_OGLE3_catalog()
    oid = np.random.choice(cat.ID)
    url = ogle3.URL.format(oid)
    file_path = os.path.join(store_path, "{}.tar".format(oid))
    with mock.patch("feets.datasets.base.fetch") as fetch:
        with mock.patch("tarfile.TarFile"):
            data = ogle3.fetch_OGLE3(oid)
            assert data["id"] == oid
            fetch.assert_called_with(url, file_path)


def test_fetch_OGLE3_real_TAR():
    file_path = os.path.join(DATA_PATH, "OGLE-BLG-LPV-232406.tar")
    with tarfile.TarFile(file_path) as tfp:
        with mock.patch("feets.datasets.base.fetch"):
            with mock.patch("tarfile.TarFile", return_value=tfp):
                ogle3.fetch_OGLE3("OGLE-BLG-LPV-232406")
