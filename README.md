# URL Lookalike demo

This is a streamlit app to demonstrate lookalike search on MContextual database

# Development 

This app uses uv for python package management. 

- `brew install uv` if needed
- `uv venv` create a new venv in this project 
- `uv sync` sync the venv with the lock file 
- `source .venv/bin/activate`
- `streamlit run app/app.py`

To add a dependency, simply run `uv add package`. 

# Building docker image

to build using podman/docker:

- `podman build . -t url_lal_app` 

to run:

- `podman run -e PGPASS="secret1234" -e USER=$USER url_lal_app:latest`

# TODO

- Actual HNSW query 
- pretty tabular output
- download CSV?
- Some kind of visualization? 
- Turn off all the annoying Snowflake PLG nags (e.g. registration)