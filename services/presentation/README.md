# presentation

Microservice to emulate a front-end. Due to the time, this one is a pure console application.

## Development

### Preparation

- Create a Python virtual environment typing `mkvirtualenv --python=/path/to/python3 aptn-presentation` (`virtualenvwrapper` is necessary) on terminal

### Running

- In the root directory(where this file is), run `./deploy.sh`

### Modules

- `console`: allows the user to navigate
- `web_clients`: translates commands to HTTP requests and sends them to service **business**
- `configs`: export some configurations that may be used in many parts

The module `app` is used just to initiate and bind all other modules.
