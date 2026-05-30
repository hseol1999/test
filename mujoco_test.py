import mujoco
import numpy as np

xml = """
<mujoco>
  <worldbody>
    <light diffuse=".5 .5 .5" pos="0 0 3" dir="0 0 -1"/>
    <geom type="plane" size="1 1 0.1" rgba=".9 0 0 1"/>
    <body name="ball" pos="0 0 1">
      <joint type="free"/>
      <geom type="sphere" size="0.1" rgba="0 .9 0 1" mass="1"/>
    </body>
  </worldbody>
</mujoco>
"""

model = mujoco.MjModel.from_xml_string(xml)
data = mujoco.MjData(model)

print(f"MuJoCo {mujoco.__version__} 로드 완료")
print(f"timestep: {model.opt.timestep}s")
print(f"초기 ball 위치: {data.qpos[:3]}")

for i in range(100):
    mujoco.mj_step(model, data)

print(f"100 step 후 ball 위치: {data.qpos[:3]}")
print(f"시뮬 시간: {data.time:.3f}s")
print("시뮬레이션 정상 작동")
