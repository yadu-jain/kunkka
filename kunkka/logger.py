import logging
logging.basicConfig()
console=logging.getLogger('sqlalchemy.engine')
console.setLevel(logging.INFO)
#console=logging.getLogger(__name__)
def log(obj):
    #console.debug("\n")
    #console.debug(type(obj))
    console.info(obj)
    #console.debug("\n")