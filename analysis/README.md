# Analysis
This directory contains jupyter notebooks that contain code
that analyzes the data created through etl and infra directories.

# Set Up
```python3 -m venv .venv```
```source .venv/bin/activate```
```pip3 install -r requirements.txt```

# Export
### To HTML
```jupyter nbconvert f1_results_analysis.ipynb --to html --HTMLExporter.theme=dark```

### To PDF
```jupyter nbconvert f1_results_analysis.ipynb --to pdf --template-file .venv/share/jupyter/nbconvert/templates/latex/base.tex.j2```
```jupyter nbconvert --to pdf f1_results_analysis.ipynb --template latex_authentic```