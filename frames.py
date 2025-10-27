import threading
import time

from communication_library.communication_manager import CommunicationManager, TransportType
from communication_library.tcp_transport import TcpSettings
from communication_library.frame import Frame
from communication_library import ids, frame
from communication_library.exceptions import TransportTimeoutError, TransportError, UnregisteredCallbackError

cm = CommunicationManager()
cm.change_transport_type(TransportType.TCP)
cm.connect(TcpSettings("127.0.0.1", 3000))

state = {
    'fuel_level': 0.0,
    'oxidizer_level':0.0,
    'oxidizer_pressure':0.0,
    'altitude':0.0,
    'angle':0.0,
    'fuel_intake_pos':100,
    'oxidizer_intake_pos':100,
    'fuel_main_pos':100,
    'oxidizer_main_pos':100,
    'heater_on':False,
    'igniter_on':False,
    'parachute_on':False,
}

# FUEL INTAKE
def open_fuel_intake():
     frame = Frame(ids.BoardID.ROCKET,
                   ids.PriorityID.LOW,
                   ids.ActionID.SERVICE,
                   ids.BoardID.SOFTWARE,
                   ids.DeviceID.SERVO,
                   0,
                   ids.DataTypeID.INT16,
                   ids.OperationID.SERVO.value.POSITION,
                   (0,)
                   )
     cm.push(frame)
     cm.send()

def close_fuel_intake():
    frame = Frame(ids.BoardID.ROCKET,
                  ids.PriorityID.LOW,
                  ids.ActionID.SERVICE,
                  ids.BoardID.SOFTWARE,
                  ids.DeviceID.SERVO,
                  0,
                  ids.DataTypeID.INT16,
                  ids.OperationID.SERVO.value.POSITION,
                  (100,)
                  )
    cm.push(frame)
    cm.send()

def fuel_intake(e):
    if e.value == 'on':
        open_fuel_intake()
    else:
        close_fuel_intake()

# OXIDIZER INTAKE
def open_oxidizer_intake():
    frame = Frame(ids.BoardID.ROCKET,
                  ids.PriorityID.LOW,
                  ids.ActionID.SERVICE,
                  ids.BoardID.SOFTWARE,
                  ids.DeviceID.SERVO,
                  1,
                  ids.DataTypeID.INT16,
                  ids.OperationID.SERVO.value.POSITION,
                  (0,)
                  )
    cm.push(frame)
    cm.send()

def close_oxidizer_intake():
    frame = Frame(ids.BoardID.ROCKET,
                  ids.PriorityID.LOW,
                  ids.ActionID.SERVICE,
                  ids.BoardID.SOFTWARE,
                  ids.DeviceID.SERVO,
                  1,
                  ids.DataTypeID.INT16,
                  ids.OperationID.SERVO.value.POSITION,
                  (100,)
                  )
    cm.push(frame)
    cm.send()

def oxidizer_intake(e):
    if e.value == 'on':
        open_oxidizer_intake()
    else:
        close_oxidizer_intake()

# FUEL MAIN
def open_fuel_main():
    frame = Frame(ids.BoardID.ROCKET,
                  ids.PriorityID.LOW,
                  ids.ActionID.SERVICE,
                  ids.BoardID.SOFTWARE,
                  ids.DeviceID.SERVO,
                  2,
                  ids.DataTypeID.INT16,
                  ids.OperationID.SERVO.value.POSITION,
                  (0,)
                  )
    cm.push(frame)
    cm.send()

def close_fuel_main():
    frame = Frame(ids.BoardID.ROCKET,
                  ids.PriorityID.LOW,
                  ids.ActionID.SERVICE,
                  ids.BoardID.SOFTWARE,
                  ids.DeviceID.SERVO,
                  2,
                  ids.DataTypeID.INT16,
                  ids.OperationID.SERVO.value.POSITION,
                  (100,)
                  )
    cm.push(frame)
    cm.send()

def fuel_main(e):
    if e.value == 'on':
        open_fuel_main()
    else:
        close_fuel_main()

# OXIDIZER MAIN
def open_oxidizer_main():
    frame = Frame(ids.BoardID.ROCKET,
                  ids.PriorityID.LOW,
                  ids.ActionID.SERVICE,
                  ids.BoardID.SOFTWARE,
                  ids.DeviceID.SERVO,
                  3,
                  ids.DataTypeID.INT16,
                  ids.OperationID.SERVO.value.POSITION,
                  (0,)
                  )
    cm.push(frame)
    cm.send()

def close_oxidizer_main():
    frame = Frame(ids.BoardID.ROCKET,
                  ids.PriorityID.LOW,
                  ids.ActionID.SERVICE,
                  ids.BoardID.SOFTWARE,
                  ids.DeviceID.SERVO,
                  3,
                  ids.DataTypeID.INT16,
                  ids.OperationID.SERVO.value.POSITION,
                  (100,)
                  )
    cm.push(frame)
    cm.send()

def oxidizer_main(e):
    if e.value == 'on':
        open_oxidizer_main()
    else:
        close_oxidizer_main()

# OXIDIZER HEATER
def oxidizer_heater_on():
    frame = Frame(ids.BoardID.ROCKET,
                  ids.PriorityID.LOW,
                  ids.ActionID.SERVICE,
                  ids.BoardID.SOFTWARE,
                  ids.DeviceID.RELAY,
                  0,
                  ids.DataTypeID.FLOAT,
                  ids.OperationID.RELAY.value.OPEN,
                  ()
                  )
    cm.push(frame)
    cm.send()

def oxidizer_heater_off():
    frame = Frame(ids.BoardID.ROCKET,
                  ids.PriorityID.LOW,
                  ids.ActionID.SERVICE,
                  ids.BoardID.SOFTWARE,
                  ids.DeviceID.RELAY,
                  0,
                  ids.DataTypeID.FLOAT,
                  ids.OperationID.RELAY.value.CLOSE,
                  ()
                  )
    cm.push(frame)
    cm.send()

def oxidizer_heater(e):
    if e.value == 'on':
        oxidizer_heater_on()
    else:
        oxidizer_heater_off()

# IGNITER
def igniter_on():
    frame = Frame(ids.BoardID.ROCKET,
                  ids.PriorityID.LOW,
                  ids.ActionID.SERVICE,
                  ids.BoardID.SOFTWARE,
                  ids.DeviceID.RELAY,
                  1,
                  ids.DataTypeID.FLOAT,
                  ids.OperationID.RELAY.value.OPEN,
                  ()
                  )
    cm.push(frame)
    cm.send()

def igniter_off():
    frame = Frame(ids.BoardID.ROCKET,
                  ids.PriorityID.LOW,
                  ids.ActionID.SERVICE,
                  ids.BoardID.SOFTWARE,
                  ids.DeviceID.RELAY,
                  1,
                  ids.DataTypeID.FLOAT,
                  ids.OperationID.RELAY.value.CLOSE,
                  ()
                  )
    cm.push(frame)
    cm.send()

def igniter(e):
    if e.value == 'on':
        igniter_on()
    else:
        igniter_off()

# PARACHUTE
def parachute_on():
    frame = Frame(ids.BoardID.ROCKET,
                  ids.PriorityID.LOW,
                  ids.ActionID.SERVICE,
                  ids.BoardID.SOFTWARE,
                  ids.DeviceID.RELAY,
                  2,
                  ids.DataTypeID.FLOAT,
                  ids.OperationID.RELAY.value.OPEN,
                  ()
                  )
    cm.push(frame)
    cm.send()

def parachute_off():
    frame = Frame(ids.BoardID.ROCKET,
                  ids.PriorityID.LOW,
                  ids.ActionID.SERVICE,
                  ids.BoardID.SOFTWARE,
                  ids.DeviceID.RELAY,
                  2,
                  ids.DataTypeID.FLOAT,
                  ids.OperationID.RELAY.value.CLOSE,
                  ()
                  )
    cm.push(frame)
    cm.send()

def parachute(e):
    if e.value == 'on':
        parachute_on()
    else:
        parachute_off()


# FUEL LEVEL
def on_fuel_level(frame: Frame):
    state['fuel_level'] = frame.payload[0]

frame_fuel_level = Frame(ids.BoardID.SOFTWARE,
                  ids.PriorityID.LOW,
                  ids.ActionID.FEED,
                  ids.BoardID.ROCKET,
                  ids.DeviceID.SENSOR,
                  0,
                  ids.DataTypeID.FLOAT,
                  ids.OperationID.SENSOR.value.READ
                  )

cm.register_callback(on_fuel_level,frame_fuel_level)

def get_fuel_level():
    return state['fuel_level']
# OXIDIZER LEVEL
def on_oxidizer_level(frame:Frame):
    state['oxidizer_level'] = frame.payload[0]

frame_oxidizer_level = Frame(ids.BoardID.SOFTWARE,
                  ids.PriorityID.LOW,
                  ids.ActionID.FEED,
                  ids.BoardID.ROCKET,
                  ids.DeviceID.SENSOR,
                  1,
                  ids.DataTypeID.FLOAT,
                  ids.OperationID.SENSOR.value.READ
                  )

cm.register_callback(on_oxidizer_level,frame_oxidizer_level)

def get_oxidizer_level():
    return state['oxidizer_level']

# ALTITUDE
def on_altitude(frame:Frame):
    state['altitude'] = frame.payload[0]

frame_altitude =  Frame(ids.BoardID.SOFTWARE,
                            ids.PriorityID.LOW,
                            ids.ActionID.FEED,
                            ids.BoardID.ROCKET,
                            ids.DeviceID.SENSOR,
                            2,
                            ids.DataTypeID.FLOAT,
                            ids.OperationID.SENSOR.value.READ
                            )

cm.register_callback(on_altitude,frame_altitude)

def get_altitude():
    return state['altitude']

# OXIDIZER PRESSURE
def on_oxidizer_pressure(frame:Frame):
    state['oxidizer_pressure'] = frame.payload[0]

frame_oxidizer_pressure = Frame(ids.BoardID.SOFTWARE,
                                ids.PriorityID.LOW,
                                ids.ActionID.FEED,
                                ids.BoardID.ROCKET,
                                ids.DeviceID.SENSOR,
                                3,
                                ids.DataTypeID.FLOAT,
                                ids.OperationID.SENSOR.value.READ
                                )

cm.register_callback(on_oxidizer_pressure,frame_oxidizer_pressure)

def get_oxidizer_pressure():
    return state['oxidizer_pressure']

# ANGLE
def on_angle(frame:Frame):
    state['angle'] = frame.payload[0]

frame_angle = Frame(ids.BoardID.SOFTWARE,
                    ids.PriorityID.LOW,
                    ids.ActionID.FEED,
                    ids.BoardID.ROCKET,
                    ids.DeviceID.SENSOR,
                    4,
                    ids.DataTypeID.FLOAT,
                    ids.OperationID.SENSOR.value.READ
                    )

cm.register_callback(on_angle,frame_angle)

def get_angle():
    return state['angle']

#
def background_loop():
    while True:
        try:
            cm.receive()
        except Exception as e:
            time.sleep(0.05)
        time.sleep(0.05)

thread = threading.Thread(target=background_loop, daemon=True)
thread.start()

if __name__ == "__main__":
    while True:
        time.sleep(0.5)