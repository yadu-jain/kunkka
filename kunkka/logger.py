import logging

console=logging.getLogger(__name__)
def log(obj):
    console.debug("\n")
    console.debug(type(obj))
    console.debug(obj)
    console.debug("\n")