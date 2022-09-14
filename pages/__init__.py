import gc
print( "Before terminialio in Code Loaded Available memory: {} bytes".format(gc.mem_free()) )
from terminalio import FONT
print( "after terminialio in Code Loaded Available memory: {} bytes".format(gc.mem_free()) )
