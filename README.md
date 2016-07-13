# Appletini

The tiny mock Apple Store.

Appletini is a mock Apple Store for the Catho/Seek coding test. The specifications can be found [here](./GDP-Programming.pdf). It may be composed of one or more RESTful services (e.g., front-end and back-end microservices).

## Branches

The branch used to review the code is **master**. Improvements in the code (esthetical of structural/functional) are present in branch **improv**.

## Services

There are three services (follow the links to see the READMEs):

- [presentation](./services/presentation/README.md)
- [business](./services/business/README.md)
- storage (not yet)

## Running

Each service may be deployed independently of the others, typing `./deploy.sh` while in the service's root directory (e.g., if you are in *./services/business* you will start the microservice business).

**Warning:** *These weren't tested in a cloud environment, only in my personal machine. Be aware!*

## Unit Testing

Unit tests were written only for modules `domains` and `logic`, in service **business**, the core of the entire system.

All tests can be execute typing `python -m unittest discover` in terminal while inside directory *./services/business*. Each test file is execute by `python -m unittest test.test_<module name>`.

# Links

- [Seek](http://www.seek.com.au/)
- [GDP](http://www.globaldeliverypod.com/)
