#!/usr/bin/env python3
import mujoco
import json
import sys

PENDULUM_XML = """
<mujoco model="pendulum">
  <option gravity="0 0 -9.81" timestep="0.002"/>
  <worldbody>
    <body name="pole" pos="0 0 0">
      <joint name="hinge" type="hinge" axis="0 1 0" range="-180 180"/>
      <geom type="capsule" size="0.02 0.5" pos="0 0 -0.5" rgba="0.2 0.6 0.9 1"/>
      <body name="bob" pos="0 0 -1">
        <geom type="sphere" size="0.05" rgba="0.9 0.2 0.2 1" mass="1"/>
      </body>
    </body>
  </worldbody>
</mujoco>
"""

model = mujoco.MjModel.from_xml_string(PENDULUM_XML)
data = mujoco.MjData(model)

# start with small angle displacement
data.qpos[0] = 0.3

for _ in range(5000):
    mujoco.mj_step(model, data)
    state = {
        "time": round(data.time, 4),
        "qpos": [round(float(x), 6) for x in data.qpos],
        "qvel": [round(float(x), 6) for x in data.qvel],
    }
    print(json.dumps(state), flush=True)
