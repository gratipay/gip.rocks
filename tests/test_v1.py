# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from cStringIO import StringIO
from os.path import join
from zipfile import ZipFile

import pytest
from aspen.testing.client import Client
from gip import website


@pytest.fixture
def client():
    client = Client(www_root='www', project_root='.')
    client._website = website
    yield client

@pytest.fixture
def image():
    yield open(join('tests', 'image.jpg')).read()


def zipfile(raw):
    return ZipFile(StringIO(raw), mode='r')

def filenames(zipfile):
    return [n.filename for n in zipfile.filelist]

@pytest.fixture
def vary_length(client, image):
    def vary_length(length, fail=True):
        method = client.PxST if fail else client.POST
        return method( '/v1'
                     , body=image
                     , content_type='image/jpeg'
                     , HTTP_CONTENT_LENGTH=str(length)
                      ).code
    return vary_length


def test_normal_case_is_200(client, image):
    response = client.POST('/v1', body=image, content_type='image/jpeg')
    assert response.code == 200
    assert filenames(zipfile(response.body)) == ['160', '48']

def test_length_too_great_is_413(vary_length):
    assert vary_length(262145) == 413

def test_length_overstated_is_400(vary_length):
    assert vary_length(262144) == 400
    assert vary_length(20888) == 400

def test_length_properly_stated_is_200(vary_length):
    assert vary_length(20887, False) == 200

def test_length_understated_is_400(vary_length):
    assert vary_length(20886) == 400
    assert vary_length(1) == 400
    assert vary_length(0) == 400
    assert vary_length(-1) == 400
