SIMULATION_ENABLED = True
""" تو دل برنامه یه در شبیه سازی شده ساختیم
وقتی میخام کار موبایلو وب و انجام بدم دیگه مهم نیست در واقعی باشه"""
from common.kernel.Demux import Demux
interface = Demux()
"""frame Mode"""

from common.kernel.Logger import Logger
logger = Logger()
"""errors, debug, warning,TYPE_SUCCESS,TYPE_INFO,TYPE_SHIT,TYPE_DEVELOP  """

from common.kernel.Wrapper import Wrapper
ini = Wrapper()
