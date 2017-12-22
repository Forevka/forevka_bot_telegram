from enum import Enum

token = '492391763:AAGUmnfEdEQPNk6laWXiBHfTXlakC2Ukfvg'

db_file = "database.vdb"


class States(Enum):
    S_START = "0"  # Начало нового диалога
    S_ENTER_NAME = "1"
    S_ENTER_AGE = "2"
    S_SEND_PIC = "3"
    S_CHOOSE_THEME = "4"
    S_ENTER_EXPR = "5"
    S_ENTER_DATE = "6"
    S_CHECK_AV = "7"
    S_GET_STORY = "8"
