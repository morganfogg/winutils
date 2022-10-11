# Winutils for Hadoop Builds

## Building Locally - Prerequsities

You'll need Visual Studio 2022. The "free" Community Edition is sufficient. It must have the
"Desktop Development with C++" workload installed; if you didn't select this during initial
installation, you can add it by launching the Visual Studio Installer from the start menu and
selecting "Modify". Finally, you will need a recent version of Python 3. The Python script itself
has no dependencies beyond the Python standard library.

## Building Locally

Firstly, you'll probably need to enable long filepaths in Git, if you haven't already. You can do
this by running:

```
git config --system core.longpaths true
```

Clone this repository, like so:

```
git clone https://github.com/morganfogg/winutils ~/winutils-build
```

Next, download the Apache Hadoop Git repository. The full Hadoop repo is ~800MB, so it's faster to
only download the branch you care about, and perform a shallow clone. The following is an example
of only cloning the most recent revision of the `branch-3.3.1` branch:

```bash
git clone https://github.com/apache/hadoop ~/hadoop --single-branch --branch branch-3.3.1 --depth=1
```

Now, open "Developer Powershell for VS 2022" from the start menu, and enter the following:

```powershell
cd ~/winutils-build
python .\build.py $HOME\hadoop
```

Finally, go make some lunch: the build takes some time. When it's done, you will find your winutils
build in `~/hadoop/hadoop-common-project/hadoop-common/target/bin/`
