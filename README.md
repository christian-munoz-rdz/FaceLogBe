# Install the project

I recommend you to create a virtual environment for avoid conflicts to global packages.

For that `cd FaceLogBE` and run

- `python3 -m venv .venv`

> Note: If you are using vs code, select the python interpreter in the .venv folder before next instructions. `cmd/ctrl + shift + p -> Python: Select Interpreter`

Then install the dependencies:

`pip install -r requirements.txt`

---

# Run the project

- run: `uvicorn main:app --reload`

then

- go to `http://127.0.0.1:8000/docs`

---

# Documentation

go to `http://127.0.0.1:8000/docs`

# Tutorials

- Deepface
  https://github.com/serengil/deepface

- Install tensor-flow:
  https://stackoverflow.com/questions/70981334/how-to-install-deepface-python-face-recognition-package-on-m1-mac

  https://claytonpilat.medium.com/tutorial-tensorflow-on-an-m1-mac-using-jupyter-notebooks-and-miniforge-dbb0ef67bf90

- sql good practices reference:
  https://www.sqlstyle.guide/#naming-conventions
