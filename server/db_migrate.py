#!/usr/bin/env python3

import json
import os
import sys
from yoyo import read_migrations
from yoyo import get_backend
from os import path

DB_INFO = "constants/database.json"
MIGRATIOS_DIR = "migrations"


def main():
    parent_dir = path.dirname(path.abspath(__file__))
    with open(f"{parent_dir}/{DB_INFO}", 'r') as configuration_file:
        config = json.load(configuration_file)["mysql"]

    backend = get_backend(f'mysql://{config["user"]}:{config["password"]}@{config["host"]}/{config["database"]}')
    migrations = read_migrations(f"{parent_dir}/{MIGRATIOS_DIR}")

    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))


if os.path.samefile(__file__, sys.argv[0]):
    print("Starting migrations.")
    main()
    print("All migrations are finished.")