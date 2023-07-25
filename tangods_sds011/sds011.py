from tango import AttrWriteType, DispLevel, DevState
from tango.server import Device, attribute, command, device_property
from enum import IntEnum
import asyncio
import simple_sds011


class SDS011(Device):
    _pm25 = 0.0
    _pm10 = 0.0

    SERIAL_PORT = device_property(dtype=str, doc="serial port address", mandatory=True)

    WORK_PERIOD = device_property(
        dtype=int,
        doc="work 30 seconds and sleep N*60-30 seconds, if N = 0 continuous",
        mandatory=True,
    )

    async def poll_query(self, update_period):
        while True:
            response = self.sds_device.query()
            payload = response["value"]
            if isinstance(payload, dict):
                self._pm25 = payload.get("pm2.5")
                self._pm10 = payload.get("pm10.0")
                print("updated values")
                await asyncio.sleep(25)

    pm25 = attribute(
        label="PM2.5",
        dtype=float,
        access=AttrWriteType.READ,
        unit="ug/m3",
        format="3.1f",
        fget="get_pm",
        fset="set_dummy",
        doc="the power supply current",
    )
    pm10 = attribute(
        label="PM10",
        dtype=float,
        access=AttrWriteType.READ,
        unit="ug/m3",
        format="3.1f",
        fget="get_pm",
        fset="set_dummy",
        doc="the power supply current",
    )

    def set_dummy(self, attr):
        pass

    def get_pm(self, attr):
        attr_name = attr.get_name()
        getattr(self, f"_{attr_name}")

    def init_device(self):
        Device.init_device(self)
        self.sds_device = simple_sds011.SDS011(self.SERIAL_PORT)
        # only this mode is supported
        self.sds_device.mode = simple_sds011.MODE_PASSIVE
        self.sds_device.period = self.WORK_PERIOD
        self.set_state(DevState.ON)
        loop = asyncio.new_event_loop()
        # 5 seconds less then the detector updates its value
        update_period = min(25, self.WORK_PERIOD * 60 - 35)
        self.task = loop.create_task(self.poll_query(update_period))

    def delete_device(self):
        Device.delete_device(self)
        self.task.cancel()
