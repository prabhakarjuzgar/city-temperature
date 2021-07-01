#! /usr/bin/env python

import os
import subprocess
import time
import signal
import json
import click
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def setenv(key: str, value: str):
    os.environ[key] = value

setenv("APPLICATION_CONFIG", "development")


def application_config_file(config):
    return os.path.join("config", f"{config}.json")

def configure_app(config):
    with open(application_config_file(config)) as itr:
        config_data = json.load(itr)

    config_data = dict((i["name"], i["value"]) for i in config_data)

    for key, value in config_data.items():
        setenv(key, value)

def run_sql(statements):
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOSTNAME"),
        port=os.getenv("POSTGRES_PORT")
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    for statement in statements:
        cursor.execute(statement)

    cursor.close()
    conn.close()

@click.group()
def cli():
    pass

@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument("subcommand", nargs=-1, type=click.Path())
def flask(subcommand):
    configure_app(os.getenv("APPLICATION_CONFIG"))

    cmdline = ["flask"] + list(subcommand)

    try:
        p = subprocess.Popen(cmdline)
        p.wait()
    except KeyboardInterrupt:
        p.send_signal(signal.SIGINT)
        p.wait()

def docker_compose_cmdline(config):
    configure_app(os.getenv("APPLICATION_CONFIG"))

    docker_compose_file = os.path.join("docker", f"{config}.yml")
    if not os.path.isfile(docker_compose_file):
        raise ValueError(f"The file {docker_compose_file} does not exist")

    return ["docker-compose",
            "-p",
            config,
            "-f",
            docker_compose_file,
            ]

@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument("subcommand", nargs=-1, type=click.Path())
def compose(subcommand):
    cmdline = docker_compose_cmdline(os.getenv("APPLICATION_CONFIG")) + list(subcommand)
    try:
        p = subprocess.Popen(cmdline)
        p.wait()
    except KeyboardInterrupt:
        p.send_signal(signal.SIGINT)
        p.wait()

@cli.command()
@click.argument("filenames", nargs=-1)
def test(filenames):
    os.environ["APPLICATION_CONFIG"] = "testing"
    configure_app(os.getenv("APPLICATION_CONFIG"))

    cmdline = docker_compose_cmdline(os.getenv("APPLICATION_CONFIG")) + ["up", "-d"]
    subprocess.call(cmdline)

    cmdline = docker_compose_cmdline(os.getenv("APPLICATION_CONFIG")) + ["logs", "db"]
    logs = subprocess.check_output(cmdline)
    while "ready to accept connections" not in logs.decode("utf-8"):
        time.sleep(0.1)
        logs = subprocess.check_output(cmdline)

    run_sql([f"DROP DATABASE IF EXISTS {os.getenv('APPLICATION_DB')}"])
    run_sql([f"CREATE DATABASE {os.getenv('APPLICATION_DB')}"])

    cmdline = ["pytest", "--setup-show", "-svv", "-cov=application", "--cov-report=term-missing"]
    cmdline.extend(filenames)
    subprocess.call(cmdline)

    import pdb; pdb.set_trace()
    cmdline = docker_compose_cmdline(os.getenv("APPLICATION_CONFIG")) + ["down"]
    subprocess.call(cmdline)

@cli.command()
def create_initial_db():
    configure_app(os.getenv("APPLICATION_CONFIG"))
    try:
        run_sql([f"CREATE DATABASE {os.getenv('APPLICATION_DB')}"])

    except psycopg2.errors.DuplicateDatabase:
        print(f"Database {os.getenv('APPLICATION_DB')} already exists.")

if __name__ == '__main__':
    cli()
