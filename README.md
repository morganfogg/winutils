# Winutils for Hadoop Build Scripts

This repository contains scripts and a Github Action that takes most of the pain out of building 
Apache Hadoop Winutils.

## Building your own copy

There are two ways to build your own Winutils using this code: either through Github Actions, or 
locally.

The easiest way is to use the Github Action provided in this repo. Just fork this repo, click the 
"Actions" tab, select "Build Hadoop Winutils" and then "Run workflow". Enter the name of the Hadoop 
branch you want to build off (This will be `branch-X.X.X`, where X.X.X is the version of Hadoop you 
want a build for. For example, `branch-3.2.2`). Then click "Run workflow".

### Running the script locally

The other way is to run the script on your local computer, which is a bit more awkward. You will need:

- Visual Studio 2022 (any edition) with the "Desktop Development with C++" package (select this from 
  the Visual Studio Installer).
- Python 3
- Git

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

The build takes some time. When it's done, you will find your winutils build in 
the `results` folder in the the same directory as the script.

**NOTE**: Some (but not all) versions of Hadoop have trouble with passing long Maven paths to Java, spitting up an
error along the lines of 

```
The command line is too long.
```

In the Github action, I resolve this by setting the environmental variable `MAVEN_OPTS` to `-Dmaven.repo.local=D:/m`. This moves the Maven local repository to a folder named "m" at the root of the D drive. To do this in Powershell, run `$env:MAVEN_OPTS=-Dmaven.repo.local=D:/m` before invoking the Python script, where `D:/m` is the directory you want to put your Maven cache in.
