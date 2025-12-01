import psycopg2
import pandas as pd
from src.logger import get_logger
from src.custom_exception import CustomException
import os
import sys
from config.database_config import *
from config.paths_config import *

logger = get_logger(__name__)
