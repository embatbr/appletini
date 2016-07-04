# Appletini
Mini mock Apple Store

Appletini is a mock Apple Store. It may be composed of one or more RESTful services (e.g., front-end and back-end microservices).

## Must have

- Shopping cart
    - Stores products by it's SKU
        - Each SKU has an amount of items
        - Has the default price by unit, the summed price and the current total price (to indicate promotions, as in 3 by the price of 2)
- Items
    - Check if must create a class with `SKU`, `name` and `price`
- Rules
    - An object to define the promotion rules
    - Must be flexible, so "an application inside the application"
        - Maybe define a simple coding
    - Check conflicting rules and think how to solve it
        - Tree of possibilities?
        - Remember compiler theory
- Checkout core
    - Checks each item (composed of 1 or more units) for a promotion
    - In case of promotions (such as free items ones), insert those after all checkings
        - Avoids a reward from a promotion to trigger another promotion wrongly (e.g, "I have 2 `atv` e 2 `mbp` and there's a promotion of 2 `mpb` gives you a new `atv`, what may triggers the '3 `atv` by the price of 2' promotion")
- Database
    - Start with SQLite
    - After, use MySQL or PostgreSQL

## How to (step by step - oh baby)

All steps must have tests

1. Create a retail system
    - Database with products descriptions and shopping transactions
    - Receives a buy order (when the shopping cart) is finishedside.
    - Calculates the price and return
2. Insert the promotions
    - Calculates the rewards for each promotion
    - Delivers the rewards after all calculations
    - Updates the value charged
3. Use microservices to create a front-end to be used
    - Detail this topic when necessary

## Development

**REMEMBER to activate the Python virtual environment!**

### Preparation

- Create a Python virtual environment typing `mkvirtualenv --python=/path/to/python3 appletini-backend` (`virtualenvwrapper` is necessary)
- Install Flask: `pip install flask`

### TDD

In each subproject directory (`backend`, `frontend`, `auth` and etc.) the subdirectories `app` and `test` contains the aplication and testing codes, respectively. Both, to be considered Python packages must have a `__init__.py` file, even if empty.

Tests are executed typing `python -m unittest discover` when inside the subproject directory.

### Services

There are three services: `presentation`, `business-logic` and `data-access`.

#### business-logic

