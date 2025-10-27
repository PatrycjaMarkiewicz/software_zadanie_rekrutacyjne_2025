import asyncio
from nicegui import ui
import frames

state = {
    'fuel_level': 0.0,
    'oxidizer_level': 0.0,
    'oxidizer_pressure': 0.0,
    'altitude': 0.0,
    'angle': 0.0,
    'velocity': 0.0,
    'fuel_intake_pos': 100,
    'oxidizer_intake_pos': 100,
    'fuel_main_pos': 100,
    'oxidizer_main_pos': 100,
    'heater_on': False,
    'igniter_on': False,
    'parachute_on': False,
}

ui.add_head_html('<style>body {background-color: black; }</style>')
ui.label(" ROCKET LAUNCH CONTROL PANEL").classes('text-3xl text-bold text-white')

with ui.row().classes('w-full justify-center p-8'):
    with ui.column():
        ui.label("CONTROL PANEL").classes('text-xl text-white')
        with ui.column():
            with ui.row().classes('gap-6'):
                with ui.card().classes('bg-[#1c1c1c] text-white items-center w-48 h-28'):
                    ui.label("Fuel intake").classes('font-mono text-gray')
                    fuel_level_toggle = ui.toggle(['off', 'on'], value='off', on_change=frames.fuel_intake).props('color=grey-8 rounded').classes('font-mono')
                with ui.card().classes('bg-[#1c1c1c] text-white items-center w-48 h-28'):
                    ui.label("Oxidizer intake").classes('font-mono text-gray')
                    oxidizer_level_toggle = ui.toggle(['off', 'on'], value='off', on_change=frames.oxidizer_intake).props('color=grey-8 rounded').classes('font-mono')
                with ui.card().classes('bg-[#1c1c1c] text-white items-center w-48 h-28'):
                    ui.label("Oxidizer heater").classes('font-mono text-gray')
                    oxidizer_heater_toggle = ui.toggle(['off', 'on'], value='off', on_change=frames.oxidizer_heater).props('color=grey-8 rounded').classes('font-mono')
            with ui.row().classes('gap-6'):
                with ui.card().classes('bg-[#1c1c1c] text-white items-center w-48 h-28'):
                    ui.label("Fuel main").classes('font-mono text-gray')
                    fuel_main_toggle = ui.toggle(['off', 'on'], value='off', on_change=frames.fuel_main).props('color=grey-8 rounded').classes('font-mono')
                with ui.card().classes('bg-[#1c1c1c] text-white items-center w-48 h-28'):
                    ui.label("Oxidizer main").classes('font-mono text-gray')
                    oxidizer_main_toggle = ui.toggle(['off', 'on'], value='off', on_change=frames.oxidizer_main).props('color=grey-8 rounded').classes('font-mono')
                with ui.card().classes('bg-[#1c1c1c] text-white items-center w-48 h-28'):
                    ui.label("Igniter").classes('font-mono text-gray')
                    igniter_toggle = ui.toggle(['off', 'on'], value='off', on_change=frames.igniter).props('color=grey-8 rounded').classes('font-mono')
            with ui.row().classes('gap-6'):
                with ui.card().classes('bg-[#1c1c1c] text-white items-center w-48 h-28'):
                    ui.label("Parachute").classes('font-mono text-gray')
                    parachute_toggle = ui.toggle(['off', 'on'], value='off', on_change=frames.parachute).props('color=grey-8 rounded').classes('font-mono')

    with ui.column().classes('w-1/2 bg-[#1a1a1a] p-6 gap-4'):
        ui.label("TELEMETRY DATA").classes('text-xl text-white text-center font-mono mb-4')

        with ui.row().classes('items-center gap-4 w-full'):
            fuel_label = ui.label(f"Fuel level: {state['fuel_level']}%").classes('text-gray-200 font-mono w-56')
            fuel = (ui.linear_progress(value=0, show_value=False).props(f'color=grey').classes('w-full h-3 rounded'))
        with ui.row().classes('items-center gap-4 w-full'):
            oxidizer_label = ui.label(f"Oxidizer level: {state['oxidizer_level']}%").classes('text-gray-200 font-mono w-56')
            oxidizer = (ui.linear_progress(value=0, show_value=False).props(f'color="grey"').classes('w-full h-3 rounded'))

        with ui.row().classes('items-center gap-4'):
            oxidizer_pressure_label = ui.label(f"Oxidizer pressure: {state['oxidizer_pressure']} bar").classes('text-gray-200 font-mono w-full')

        with ui.row().classes('items-center gap-4'):
            altitude_label = ui.label(f"Altitude: {state['altitude']} m").classes('text-gray-200 font-mono w-full')

        with ui.row().classes('items-center gap-4'):
            angle_label = ui.label(f"Angle: {state['angle']}°").classes('text-gray-200 font-mono w-full')
        with ui.row().classes('items-center gap-4'):
            velocity_label = ui.label(f"Velocity: {state['velocity']}m/s").classes('text-gray-200 font-mono w-full')

with ui.column().classes('w-full bg-[#2a0000 rounded'):
    ui.label("WARNINGS").classes('text-xl text-red-400')
    warnings_box = ui.column().classes('gap-2')

def add_warning(message: str):
    with warnings_box:
        ui.label(f"{message}").classes('text-red-300')

async def update():
    while True:
        try:
            state['fuel_level'] = round(frames.get_fuel_level(), 2)
            state['oxidizer_level'] = round(frames.get_oxidizer_level(), 2)
            state['oxidizer_pressure'] = round(frames.get_oxidizer_pressure(), 2)
            previous_altitude = state['altitude']
            state['altitude'] = round(frames.get_altitude(), 2)
            state['angle'] = round(frames.get_angle(), 2)
            state['velocity'] = round(state['altitude'] - previous_altitude,2)
            state['fuel_intake_pos'] = fuel_level_toggle.value
            state['oxidizer_intake_pos'] = oxidizer_level_toggle.value
            state['fuel_main_pos'] = fuel_main_toggle.value
            state['oxidizer_main_pos'] = oxidizer_main_toggle.value
            state['heater_on'] = oxidizer_heater_toggle.value
            state['igniter_on'] = igniter_toggle.value
            state['parachute_on'] = parachute_toggle.value

            fuel_label.text = f"Fuel level: {state['fuel_level']}%"
            fuel.set_value(state['fuel_level'] / 100)
            oxidizer_label.text = f"Oxidizer level: {state['oxidizer_level']}%"
            oxidizer.set_value(state['oxidizer_level'] / 100)
            oxidizer_pressure_label.text = f"Oxidizer pressure: {state['oxidizer_pressure']} bar"
            altitude_label.text = f"Altitude: {state['altitude']} m"
            angle_label.text = f"Angle: {state['angle']}°"
            velocity_label.text = f"Velocity: {state['velocity']}m/s"

            # Warnings

            if state['fuel_intake_pos'] == 'on' and state['oxidizer_level'] < 100:
                add_warning("PROPELLANT LOADING VIOLATION: Fuel intake opened before oxidizer is filled!")
                add_warning("Correct procedure: Fill oxidizer tank first, then fuel tank.")
            if state['oxidizer_pressure'] > 90:
                add_warning("Oxidizer pressure too high (90 bars) - tank explosion")
            if state['igniter_on'] == 'on' and (state['fuel_main_pos'] == 'off' or state['oxidizer_main_pos'] == 'off'):
                add_warning("Igniter started before main valves - single propellant combustion")
            if state['igniter_on'] == 'on' and state['oxidizer_pressure'] > 65:
                add_warning("Oxidizer pressure too high - engine explosion")
            if state['igniter_on'] == 'on' and state['oxidizer_pressure'] < 40:
                add_warning("Oxidizer pressure too low - engine won't ignite")
            if state['igniter_on'] == 'on' and (state['fuel_intake_pos'] == 'on' or state['oxidizer_intake_pos'] == 'on'):
                add_warning("Intake valves still open during ignition - catastrophic pressure loss")
            if state['parachute_on'] == 'on' and state['igniter_on'] == 'on':
                add_warning("Parachute opened while engine is running - structural failure")
            if state['parachute_on'] == 'on' and state['velocity'] > 30:
                add_warning("Parachute deployed at too high velocity during ascent - parachute ripped")

        except AssertionError:
            pass
        await asyncio.sleep(1)

ui.timer(0.1, lambda: update())
ui.run()
