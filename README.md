
# gRIPS-Fujitsu-2023 Documentation
## > Set up
Python version used: 3.8

`requirements.txt` contains the libraries needed to run the local interface and server. To download the libraries all at once, run `pip install -r requirements.txt` in the terminal. Note that this requires a working `pip`.
#### Potential resources for troubleshooting
`scikit-learn` with `conda` install: https:`//gist.github.com/bparaj/6faab3969c82b68664ce3f9b9508094c

### Repository structure
`interface/`: folder containing all front-end code

`flask-server/`: folder containing all back-end code

### > Running the local interface and server
To start the front-end locally, run `npm start` in `interface/src/` folder

To start the back-end locally, run `python server.py` in `flask-server/server.py`
