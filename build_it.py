#!/usr/bin/env python

import shutil
from urllib.request import urlretrieve
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile
import os
from os import PathLike
import subprocess
from argparse import ArgumentParser
import logging

logging.getLogger().setLevel(logging.INFO)

JAVA_URL = 'https://github.com/adoptium/temurin8-binaries/releases/download/jdk8u345-b01/OpenJDK8U-jdk_x64_windows_hotspot_8u345b01.zip'
MAVEN_URL = 'https://dlcdn.apache.org/maven/maven-3/3.8.6/binaries/apache-maven-3.8.6-bin.zip'
PROTOBUF_URL = 'https://github.com/protocolbuffers/protobuf/releases/download/v2.5.0/protoc-2.5.0-win32.zip'
CMAKE_URL = 'https://github.com/Kitware/CMake/releases/download/v3.24.2/cmake-3.24.2-windows-x86_64.zip'

MAVEN_DIR_NAME = 'apache-maven-3.8.6'
JAVA_DIR_NAME = 'jdk8u345-b01'

def retrieve_zip(source: str, destination: PathLike):
    with TemporaryDirectory() as t:
        path = Path(t)
        urlretrieve(source, filename=path / 'file.zip')

        with ZipFile(path / 'file.zip', 'r') as f:
            f.extractall(destination)


def main():
    parser = ArgumentParser()
    parser.add_argument('hadoop_dir')

    args = parser.parse_args()

    run(args)

def run(args):
    assert Path(r'C:\Program Files\Microsoft Visual Studio\2022\Enterprise\Common7\IDE\devenv.com').exists()
    os.environ['PATH'] = os.pathsep.join([
        r'C:\Program Files\Microsoft Visual Studio\2022\Enterprise\Common7\IDE',
        os.environ['PATH'],
    ])

    hadoop_dir = Path(args.hadoop_dir).absolute()

    script_dir = Path(__file__).parent.absolute()
    output_dir = script_dir / '.spark_deps'

    if output_dir.exists():
        shutil.rmtree(output_dir)

    logging.info("Retrieving Java")
    retrieve_zip(JAVA_URL, output_dir)

    logging.info("Retrieving Maven")
    retrieve_zip(MAVEN_URL, output_dir)

    logging.info("Retrieving Protocol Buffers")
    retrieve_zip(PROTOBUF_URL, output_dir / 'protobuf')

    logging.info("Retrieving CMAKE")
    retrieve_zip(CMAKE_URL, output_dir)

    os.environ['JAVA_HOME'] = str(output_dir / JAVA_DIR_NAME)
    os.environ['MAVEN_HOME'] = str(output_dir / MAVEN_DIR_NAME)

    mvn_exe = str(output_dir / MAVEN_DIR_NAME / "bin/mvn.cmd")

    logging.info(mvn_exe)

    logging.info("Building")
    subprocess.run([mvn_exe, "compile", "--batch-mode", "-e"], cwd=hadoop_dir)

if __name__ == '__main__':
    main()
