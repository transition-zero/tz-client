import logging
import sys

<<<<<<< HEAD
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
=======
logging.basicConfig(stream=sys.stdout, level=logging.WARNING)
>>>>>>> f82e829 (chore: merge upstream)
logger = logging.getLogger(__name__)
