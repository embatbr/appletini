# business

Microservice to execute the business logic (group items, sum prices and calculate discounts).

## Development

### Preparation

- Create a Python virtual environment typing `mkvirtualenv --python=/path/to/python3 aptn-business` (`virtualenvwrapper` is necessary) on terminal
- Start it: `workon aptn-business`
- Install Falcon: `pip install falcon`
- Install Money: `pip install money`
- Install Gunicorn: `pip install gunicorn`

### Running

- In the root directory(where this file is), run `./deploy.sh`

### Modules

The file *main.py* is used only to start the application. The real code is in the module files:

- `web_api`: Define a RESTful API, the gateway to the service
- `logic`: where the entire process (buying, payment and etc.) happens
- `domains`: contains the models implementations
- `configs`: export some configurations that may be used in many parts
- `web_clients`: communicates with other services (for now, not implemented)

The module `app` is used just to initiate and bind all other modules.
