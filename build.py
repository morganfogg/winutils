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
import glob

logging.getLogger().setLevel(logging.INFO)

JAVA_URL = "https://github.com/adoptium/temurin8-binaries/releases/download/jdk8u345-b01/OpenJDK8U-jdk_x64_windows_hotspot_8u345b01.zip"
MAVEN_URL = "https://dlcdn.apache.org/maven/maven-3/3.8.7/binaries/apache-maven-3.8.7-bin.tar.gz"
PROTOBUF_URL = "https://github.com/protocolbuffers/protobuf/releases/download/v2.5.0/protoc-2.5.0-win32.zip"
CMAKE_URL = "https://github.com/Kitware/CMake/releases/download/v3.24.2/cmake-3.24.2-windows-x86_64.zip"

MAVEN_DIR_NAME = "apache-maven-3.8.7"
JAVA_DIR_NAME = "jdk8u345-b01"
CMAKE_DIR_NAME = 'cmake-3.24.2-windows-x86_64'

def retrieve_archive(source: str, destination: PathLike):
    filename = source.rsplit('/', 1)[1]
    with TemporaryDirectory() as t:
        urlretrieve(source, filename=Path(t) / filename)
        shutil.unpack_archive(Path(t) / filename, destination)


def main():
    parser = ArgumentParser()
    parser.add_argument("hadoop_dir")

    args = parser.parse_args()

    run(args)


def run(args):
    if shutil.which("devenv") is None:
        devenv_list = glob.glob(
            r"C:\Program Files\Microsoft Visual Studio\2022\*\Common7\IDE\devenv.com"
        )
        if not devenv_list:
            raise AssertionError(
                "Could not find devenv executable (try running this script from Developer Powershell)"
            )
        os.environ["PATH"] = os.pathsep.join(
            [
                devenv_list[0].rsplit("\\", 1)[0],
                os.environ["PATH"],
            ]
        )

    # assert Path(r'C:\Program Files\Microsoft Visual Studio\2022\Enterprise\Common7\IDE\devenv.com').exists()
    # os.environ['PATH'] = os.pathsep.join([
    # r'C:\Program Files\Microsoft Visual Studio\2022\Enterprise\Common7\IDE',
    # os.environ['PATH'],
    # ])


    hadoop_dir = Path(args.hadoop_dir).absolute()

    script_dir = Path(__file__).parent.absolute()
    output_dir = script_dir / "dependencies"

    if output_dir.exists():
        shutil.rmtree(output_dir)

    logging.info("Retrieving Java")
    retrieve_archive(JAVA_URL, output_dir)

    logging.info("Retrieving Maven")
    retrieve_archive(MAVEN_URL, output_dir)

    logging.info("Retrieving Protocol Buffers")
    retrieve_archive(PROTOBUF_URL, output_dir / "protobuf")

    logging.info("Retrieving CMAKE")
    retrieve_archive(CMAKE_URL, output_dir)

    os.environ["JAVA_HOME"] = str(output_dir / JAVA_DIR_NAME)
    os.environ["MAVEN_HOME"] = str(output_dir / MAVEN_DIR_NAME)
    os.environ['PATH'] = os.pathsep.join([
        os.environ['PATH'],
        str(output_dir / "protobuf"),
        str(output_dir / CMAKE_DIR_NAME / 'bin')
    ])

    # MSBuild will (by default, it appears) try to build a 32-bit binary, then fall over with a
    # cryptic error message since it can't find the 32-bit build chain. This can be changed as a
    # flag to MSBuild, but using an environmental variable removes the need to modify the Maven
    # config.
    os.environ["Platform"] = "X64"

    mvn_exe = str(output_dir / MAVEN_DIR_NAME / "bin/mvn.cmd")

    logging.info(mvn_exe)

    logging.info("Building")
    subprocess.run(
        [
            mvn_exe,
            "compile",
            "-Dmaven.test.skip",
            "-DskipTests",
            "-Dmaven.javadoc.skip=true",
            "--batch-mode",
            "-e",
        ],
        cwd=hadoop_dir / 'hadoop-common-project',
        check=True,
    )

    os.mkdir('results')

    results_dir = hadoop_dir / "hadoop-common-project/hadoop-common/target/bin"

    for item in results_dir.iterdir():
        shutil.copy(item, 'results')


if __name__ == "__main__":
    main()
