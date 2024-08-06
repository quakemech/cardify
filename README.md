# Overview 

Cardify is a tool to generate 3x5 notecard PDFs from yaml soruce files. 

# Dependencies 

Cardify requires the use of two external libraries.  The first is 
[nitrile](https://github.com/quakemech/nitrile) which is a python library to 
geneate and build Latex documents. The second is pyyaml which enables yaml file
parsing. Both can be installed using pip3.

# Setup 

After cloning the repo, create and then activate a virtual environemnt using:

```bash
virtualenv venv
source venv/bin/activate
```

Then install the dependencies (nitrile and pyyaml) using pip:

```bash 
pip3 install -r requirements.txt 
```

Alternatively, the user can install the nitrile and pyyaml libraries to their
user or system locations so that the cardify.py app can be run without first 
activating the virtual environment.

# Usage 

The repo includes an example.yaml file that can be built into a pdf using: 

```bash
cardify -p example.yaml 
```

# Yaml file format 

The yaml file has the following options: 

```yaml 
author: Mahatma Gandhi
date:
options:
  basefontsize: 10
  paperwidth: 5
  paperheight: 3
  vertical: False
  top: 0.2
  left: 0.2
  right: 0.2
  bottom: 0.2
  footskip: 0
  fontsize: normalsize
  center: True
  vcenter: True
  noindent: True
text: "
You must be the change you wish to see in the world
"
```

