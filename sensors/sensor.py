# import asyncio

class Sensor():
    def __init__(self):
        self.__is_waiting = True
        pass

    async def is_waiting(self):
        return self.__is_waiting

    async def check_sensor_readiness(self):
        pass

    async def update_values(self):
        pass

    def text(self):
        pass
