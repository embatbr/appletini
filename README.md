# Appletini

The tiny mock Apple Store.

Appletini is a mock Apple Store. It may be composed of one or more RESTful services (e.g., front-end and back-end microservices).

## Services

There are three services (follow the links to see the READMEs):

- [presentation](./services/presentation/README.md)
- [business](./services/business/README.md)
- storage (not yet)

## Running

Each service may be deployed independently of the others, typing `./deploy.sh` while in the service's root directory (e.g., if you are in *./services/business* you will start the microservice business).

**Warning:** *These weren't tested in a cloud environment, only in my personal machine. Be aware!*

**Warning:** *Due to my renunciation to continue with TDD, some tests in service business are not valid anymore. They'll be fixed.*

# TODO

- Fix unit tests

- Develop module `web_clients`
    - Sends data to the service `storage`
    - Service `storage`
        - Receives HTTP request from service `business` (and maybe `presentation` too)
        - Reads/writes from/to database

- Allow multi-tenancy

- Develop service `auth`
