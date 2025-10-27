import time

from communication_library.communication_manager import CommunicationManager, TransportType
from communication_library.tcp_transport import TcpSettings
from communication_library.frame import Frame
from communication_library import ids
from communication_library.exceptions import TransportTimeoutError, TransportError, UnregisteredCallbackError

# FUEL LEVEL
fuel_level = 0.0
fuel_open_flag = False
fuel_done_flag = False
# OXIDIZER LEVEL
oxidizer_level = 0.0
oxidizer_open = 100
oxidizer_done_flag = False
# ALTITUDE
altitude = 0.0
apogee_reached = False
# OXIDIZER PRESSURE
pressure = 0.0
# OXIDIZER HEATER
oxidizer_heater_open_flag = False
oxidizer_heater_done_flag = False
# LAUNCH
rocket_launch_done_flag = False
#PARACHUTE
parachute_opened_flag = False

def on_fuel_level(frame: Frame):
    global fuel_level
    fuel_level = frame.payload[0]
    print(f"Registered frame received: {frame}")

def on_oxidizer_level(frame: Frame):
    global oxidizer_level
    oxidizer_level = frame.payload[0]
    print(f"Registered frame received: {frame}")

def on_altitude(frame: Frame):
    global altitude, apogee_reached
    current_altitude = frame.payload[0]
    if current_altitude < altitude:
        apogee_reached = True
    altitude = current_altitude
    print(f"Registered frame received: {frame}")

def on_pressure(frame: Frame):
    global pressure
    pressure = frame.payload[0]
    print(f"Registered frame received: {frame}")

def on_oxidizer_open(frame: Frame):
    global oxidizer_open
    oxidizer_open = frame.payload[0]
    print(f"Registered frame received: {frame}")


if __name__ == "__main__":
    cm = CommunicationManager()
    cm.change_transport_type(TransportType.TCP)
    cm.connect(TcpSettings("127.0.0.1", 3000))

    # FUEL LEVEL SENSOR
    fuel_level_sensor_frame = Frame(ids.BoardID.SOFTWARE,
                                    ids.PriorityID.LOW,
                                    ids.ActionID.FEED,
                                    ids.BoardID.ROCKET,
                                    ids.DeviceID.SENSOR,
                                    0,
                                    ids.DataTypeID.FLOAT,
                                    ids.OperationID.SENSOR.value.READ)
    cm.register_callback(on_fuel_level, fuel_level_sensor_frame)
    # OXIDIZER LEVEL SENSOR
    oxidizer_level_sensor_frame = Frame(ids.BoardID.SOFTWARE,
                                        ids.PriorityID.LOW,
                                        ids.ActionID.FEED,
                                        ids.BoardID.ROCKET,
                                        ids.DeviceID.SENSOR,
                                        1,
                                        ids.DataTypeID.FLOAT,
                                        ids.OperationID.SENSOR.value.READ
                                        )
    cm.register_callback(on_oxidizer_level, oxidizer_level_sensor_frame)
    # ALTITUDE SENSOR
    altitude_sensor = Frame(ids.BoardID.SOFTWARE,
                            ids.PriorityID.LOW,
                            ids.ActionID.FEED,
                            ids.BoardID.ROCKET,
                            ids.DeviceID.SENSOR,
                            2,
                            ids.DataTypeID.FLOAT,
                            ids.OperationID.SENSOR.value.READ
                            )
    cm.register_callback(on_altitude, altitude_sensor)
    # OXIDIZER PRESSURE
    oxidizer_pressure_sensor_frame = Frame(ids.BoardID.SOFTWARE,
                                           ids.PriorityID.LOW,
                                           ids.ActionID.FEED,
                                           ids.BoardID.ROCKET,
                                           ids.DeviceID.SENSOR,
                                           3,
                                           ids.DataTypeID.FLOAT,
                                           ids.OperationID.SENSOR.value.READ
                                           )
    cm.register_callback(on_pressure, oxidizer_pressure_sensor_frame)
    oxidizer_intake_sensor_frame = Frame(ids.BoardID.SOFTWARE,
                                         ids.PriorityID.LOW,
                                         ids.ActionID.FEED,
                                         ids.BoardID.ROCKET,
                                         ids.DeviceID.SERVO,
                                         1,
                                         ids.DataTypeID.INT16,
                                         ids.OperationID.SERVO.value.POSITION
                                         )
    cm.register_callback(on_oxidizer_open, oxidizer_intake_sensor_frame)

    # FUEL INTAKE
    fuel_servo_open_frame = Frame(ids.BoardID.ROCKET,
                                  ids.PriorityID.LOW,
                                  ids.ActionID.SERVICE,
                                  ids.BoardID.SOFTWARE,
                                  ids.DeviceID.SERVO,
                                  0,
                                  ids.DataTypeID.INT16,
                                  ids.OperationID.SERVO.value.POSITION,
                                  (0,)
                                  )

    fuel_servo_close_frame = Frame(ids.BoardID.ROCKET,
                                   ids.PriorityID.LOW,
                                   ids.ActionID.SERVICE,
                                   ids.BoardID.SOFTWARE,
                                   ids.DeviceID.SERVO,
                                   0,
                                   ids.DataTypeID.INT16,
                                   ids.OperationID.SERVO.value.POSITION,
                                   (100,)
                                   )
    # OXIDIZER INTAKE
    oxidizer_servo_open_frame = Frame(ids.BoardID.ROCKET,
                                      ids.PriorityID.LOW,
                                      ids.ActionID.SERVICE,
                                      ids.BoardID.SOFTWARE,
                                      ids.DeviceID.SERVO,
                                      1,  # oxidizer intake
                                      ids.DataTypeID.INT16,
                                      ids.OperationID.SERVO.value.POSITION,
                                      (0,)  # 0 is for open position, 100 is for closed
                                      )

    oxidizer_servo_close_frame = Frame(ids.BoardID.ROCKET,
                                       ids.PriorityID.LOW,
                                       ids.ActionID.SERVICE,
                                       ids.BoardID.SOFTWARE,
                                       ids.DeviceID.SERVO,
                                       1,  # oxidizer intake
                                       ids.DataTypeID.INT16,
                                       ids.OperationID.SERVO.value.POSITION,
                                       (100,)  # 0 is for open position, 100 is for closed
                                       )

    # FUEL MAIN
    fuel_main_open_frame = Frame(ids.BoardID.ROCKET,
                                 ids.PriorityID.LOW,
                                 ids.ActionID.SERVICE,
                                 ids.BoardID.SOFTWARE,
                                 ids.DeviceID.SERVO,
                                 2,
                                 ids.DataTypeID.INT16,
                                 ids.OperationID.SERVO.value.POSITION,
                                 (0,)
                                 )
    fuel_main_close_frame = Frame(ids.BoardID.ROCKET,
                                 ids.PriorityID.LOW,
                                 ids.ActionID.SERVICE,
                                 ids.BoardID.SOFTWARE,
                                 ids.DeviceID.SERVO,
                                 2,
                                 ids.DataTypeID.INT16,
                                 ids.OperationID.SERVO.value.POSITION,
                                 (100,)
                                 )
    # OXIDIZER MAIN
    oxidizer_main_open_frame = Frame(ids.BoardID.ROCKET,
                                 ids.PriorityID.LOW,
                                 ids.ActionID.SERVICE,
                                 ids.BoardID.SOFTWARE,
                                 ids.DeviceID.SERVO,
                                 3,
                                 ids.DataTypeID.INT16,
                                 ids.OperationID.SERVO.value.POSITION,
                                 (0,)
                                 )
    oxidizer_main_close_frame = Frame(ids.BoardID.ROCKET,
                                  ids.PriorityID.LOW,
                                  ids.ActionID.SERVICE,
                                  ids.BoardID.SOFTWARE,
                                  ids.DeviceID.SERVO,
                                  3,
                                  ids.DataTypeID.INT16,
                                  ids.OperationID.SERVO.value.POSITION,
                                  (100,)
                                  )
    # OXIDIZER HEATER
    oxidizer_heater_on_frame = Frame(ids.BoardID.ROCKET,
                                        ids.PriorityID.LOW,
                                        ids.ActionID.SERVICE,
                                        ids.BoardID.SOFTWARE,
                                        ids.DeviceID.RELAY,
                                        0,
                                        ids.DataTypeID.FLOAT,
                                        ids.OperationID.RELAY.value.OPEN,
                                        ()
                                        )

    oxidizer_heater_off_frame = Frame(ids.BoardID.ROCKET,
                                     ids.PriorityID.LOW,
                                     ids.ActionID.SERVICE,
                                     ids.BoardID.SOFTWARE,
                                     ids.DeviceID.RELAY,
                                     0,
                                     ids.DataTypeID.FLOAT,
                                     ids.OperationID.RELAY.value.CLOSE,
                                     ()
                                     )
    # IGNITER
    igniter_on_frame = Frame(ids.BoardID.ROCKET,
                             ids.PriorityID.LOW,
                             ids.ActionID.SERVICE,
                             ids.BoardID.SOFTWARE,
                             ids.DeviceID.RELAY,
                             1,
                             ids.DataTypeID.FLOAT,
                             ids.OperationID.RELAY.value.OPEN,
                             ()
                             )

    igniter_off_frame = Frame(ids.BoardID.ROCKET,
                             ids.PriorityID.LOW,
                             ids.ActionID.SERVICE,
                             ids.BoardID.SOFTWARE,
                             ids.DeviceID.RELAY,
                             1,
                             ids.DataTypeID.FLOAT,
                             ids.OperationID.RELAY.value.CLOSE,
                             ()
                             )
    # PARACHUTE
    parachute_on_frame = Frame(ids.BoardID.ROCKET,
                               ids.PriorityID.LOW,
                               ids.ActionID.SERVICE,
                               ids.BoardID.SOFTWARE,
                               ids.DeviceID.RELAY,
                               2,
                               ids.DataTypeID.FLOAT,
                               ids.OperationID.RELAY.value.OPEN,
                               ()
                               )

    cm.push(oxidizer_servo_open_frame)
    cm.send()

    while True:
        try:
            frame = cm.receive()
            # 1. Tankowanie utleniacza
            if not oxidizer_done_flag and oxidizer_level >= 100 and pressure >= 30.0 and oxidizer_open==0:
                cm.push(oxidizer_servo_close_frame)
                cm.send()
                oxidizer_done_flag = True
            #2. Tankowanie paliwa
            if oxidizer_done_flag and not fuel_open_flag and not fuel_done_flag:
                cm.push(fuel_servo_open_frame)
                cm.send()
                fuel_open_flag = True
            if fuel_open_flag and fuel_level>=100:
                cm.push(fuel_servo_close_frame)
                cm.send()
                fuel_open_flag = False
                fuel_done_flag = True
            if oxidizer_done_flag and fuel_done_flag and not oxidizer_heater_done_flag and not oxidizer_heater_open_flag:
                cm.push(oxidizer_heater_on_frame)
                cm.send()
                oxidizer_heater_open_flag = True
            if not oxidizer_heater_done_flag and oxidizer_heater_open_flag and pressure >= 60.0:
                cm.push(oxidizer_heater_off_frame)
                cm.send()
                oxidizer_heater_done_flag = True
            if oxidizer_done_flag and fuel_done_flag and oxidizer_heater_done_flag and not rocket_launch_done_flag:
                cm.push(fuel_main_open_frame)
                cm.push(oxidizer_main_open_frame)
                cm.send()
                cm.send()
                cm.push(igniter_on_frame)
                cm.send()
                time.sleep(1)
                cm.push(igniter_off_frame)
                cm.send()
                rocket_launch_done_flag = True
            if rocket_launch_done_flag and apogee_reached and not parachute_opened_flag:
                cm.push(parachute_on_frame)
                cm.send()
                parachute_opened_flag = True


        except TransportTimeoutError:
            pass
        except UnregisteredCallbackError as e:
            print(f"unregistered frame received: {e.frame}")
