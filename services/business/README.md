# business

Microservice to execute the business logic (group items, sum prices and calculate discounts).

## Development

### Preparation

- Create a Python virtual environment typing `mkvirtualenv --python=/path/to/python3 aptn-business` (`virtualenvwrapper` is necessary)
- Start it: `workon aptn-business`
- Install Flask: `pip install flask`
- Install Money: `pip install money`

### Modules

The file *main.py* is used only to start the application. The real code is in the module files:

- web_api
    - Handles HTTP requests (validation included)
    - Uses REST principles
- domains
    - Describes the application models
        - Items
        - Purchases
        - Purchases basket
        - Pricing rules
- logic
    - Groups items
    - Sums prices
    - Calculates discounts (promotions from pricing rules)
- web_clients
    - Sends HTTP requests to other services
        - Data to the storage service (data access)
        - MessageQueues (?)
        - Authentication (?)

### Testing

To execute all tests, type, when in the root folder, (the one where this file is located) the command `python -m unittest discover`.