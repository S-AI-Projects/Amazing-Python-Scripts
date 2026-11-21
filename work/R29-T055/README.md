# R29-T055: CPU Temperature Repeatability Checks

## Overview
This task makes verification repeatable and deterministic for `get_cpu_temperature` in `CPU temperature/temp.py` by introducing a minimal dependency seam (`sensors_fn=None`) and verifying repeatability and state isolation across multiple runs.

## Preconditions and Source Anchors
Preconditions established in `CPU temperature/temp.py`:
- **Line 15 (original) / 29**: `temperature = sensors_fn()['coretemp'][0].current` retrieves the first core reading from `'coretemp'`.
- **Lines 17-19 (original) / 31-33**: `except (KeyError, IndexError, AttributeError)` returns sentinel `"NA"` when temperature sensors are unavailable.
- **Line 6 (original) / 8**: `get_cpu_temperature(sensors_fn=None)` introduces the dependency parameter defaulting to `psutil.sensors_temperatures` if available.

## Dependency Seam and Controlled External State
- Observable External Dependency: System hardware sensor readings through `psutil.sensors_temperatures()`.
- Dependency Seam: `sensors_fn=None` parameter added to `get_cpu_temperature`. Defaults to `psutil.sensors_temperatures`, completely preserving existing zero-argument callers.
- Controlled Fixtures: Standard Python `namedtuple` objects simulating sensor readings without requiring root privileges, Linux kernel drivers, or hardware sensors.

## Fixtures and Repeatability Verification
1. **Smallest Valid Input**:
   - `sensors_fixture = {"coretemp": [shwtemp(current=0.0)]}`
   - Expected Output: `0.0`
2. **Ordinary Input**:
   - `sensors_fixture = {"coretemp": [shwtemp(current=55.5), shwtemp(current=58.0)]}`
   - Expected Output: `55.5`
3. **Unavailable Sensor Fallback**:
   - `sensors_fixture = {}`
   - Expected Output: `"NA"`
4. **Repeatability and State Isolation (Step 3)**:
   - Run 1: Ordinary fixture in fresh state -> `55.5`.
   - Run 2: Ordinary fixture again in fresh state -> `55.5`.
   - Run 3: Smallest fixture -> `1.0`.
   - Run 4: Ordinary fixture immediately after another valid input -> `55.5`.
   - Result: Demonstrates earlier runs cannot alter later results.

## Running the Checks
```bash
python3 work/R29-T055/check.py
```
Or via native unittest discovery:
```bash
python3 -m unittest discover -s "CPU temperature/tests" -p "test_temp.py" -v
```
