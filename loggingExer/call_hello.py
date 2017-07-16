import logging

logging.basicConfig(level=logging.DEBUG)
logging.debug("debugging...")
logging.info("tell information")
logging.warn("remark it comes from something like ...")
logging.error("Ops some error is occured")
logging.critical("Stop fencing and get inside")

import time

for i in range(10):
    time.sleep(3)
    logging.debug("%d th sleep"%i)

logging.debug("It's raining again")
logging.info("with hail the size of hailstones")
