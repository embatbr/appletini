# business

Microservice to execute the business logic (group items, sum prices and calculate discounts).

## Development

### Preparation

- Create a Python virtual environment typing `mkvirtualenv --python=/path/to/python3 aptn-business` (`virtualenv`and `virtualenvwrapper` are necessary) on terminal
- Start it: `workon aptn-business`
- Install Falcon: `pip install falcon`
- Install Money: `pip install money`
- Install Gunicorn: `pip install gunicorn`

### Running

In this directory (where this file is), type `./deploy.sh`.

### Modules

- `web_api`: defines a RESTful API, the gateway to the service
- `logic`: where the entire process (buying, payment and etc.) happens
- `domains`: contains the models implementations
- `configs`: export some configurations that may be used in many parts
- `web_clients`: communicates with other services (for now, not implemented)

The module `app` is just used to start the application and bind all the other modules.
