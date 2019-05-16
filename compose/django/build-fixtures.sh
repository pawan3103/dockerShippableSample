#!/bin/sh

python manage.py migrate

pytest server/tests/fixture_gen.py::FixtureGen::test_gen_accounts

