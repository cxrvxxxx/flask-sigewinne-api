```sh
# Create a virtual environment
python -m venv .venv

# Activeate the virtual environment
# If using Git Bash/Unix
source .venv/scripts/activate

# If using CMD
.venv/scripts/activate.bat

# Install libraries
pip install -r requirements.txt

# Run the server with debugging
flask run --debug

# Or, without debugging
flask run
```