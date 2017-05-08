import logging
logging.basicConfig(level='DEBUG', filename='blue_ox.log')

logger=logging.getLogger("bunyan")
logging.debug("where is my axe?")
logging.warn("I need my axe")
