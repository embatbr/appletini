# presentation

Microservice to emulate a front-end. Due to the time, this one is a pure console application.

## Development

### Preparation

- Create a Python virtual environment typing `mkvirtualenv --python=/path/to/python3 aptn-presentation` (`virtualenvwrapper` is necessary) on terminal

### Modules

Differently than **business**, this service is not developed using TDD techniques. In fact, this one has no tests at all.

- `console`: allows the user to navigate
- `web_clients`: translates commands to HTTP requests and sends them to service **business**