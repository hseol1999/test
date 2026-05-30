# test
# change
# gh push test

## 브랜치 전략

### 브랜치 구조

```
master   ← 프로덕션 릴리즈 (안정 버전)
develop  ← 기능 통합 (다음 릴리즈 준비)
feature/ ← 개별 기능 개발
```

### 워크플로

1. `develop`에서 `feature/기능명` 분기
2. 기능 개발 후 `feature/*` → `develop` PR 생성
3. 리뷰 승인 후 merge
4. 릴리즈 시 `develop` → `master` PR 생성 후 merge

### 브랜치 생성

```bash
# feature 브랜치 생성
git checkout develop
git checkout -b feature/기능명
git push origin feature/기능명
```

### PR & Merge

```bash
# feature → develop PR 생성
gh pr create --base develop --head feature/기능명

# develop → master 릴리즈 PR 생성
gh pr create --base master --head develop --title "release: ..."
```

### 브랜치 보호 규칙

| 브랜치 | 직접 push | PR 필수 | 승인 |
|--------|-----------|---------|------|
| `master` | 차단 | ✅ | 1명 (팀) / 0명 (솔로) |
| `develop` | 차단 | ✅ | 1명 (팀) / 0명 (솔로) |
| `feature/*` | 허용 | - | - |

---

## 환경 셋업

### 시스템 환경
| 항목 | 버전 |
|------|------|
| OS | Ubuntu 26.04 (WSL2) |
| Python | 3.14 |
| MuJoCo | 3.9.0 |
| ROS2 | Lyrical |
| Rust | 1.96.0 |

### WSL2 메모리 설정
`C:\Users\<유저명>\.wslconfig` 생성:
```ini
[wsl2]
memory=6GB
processors=4
swap=2GB
```
PowerShell에서 `wsl --shutdown` 후 재시작.

### MuJoCo 설치
```bash
# Python venv 생성 (Python 3.14은 PEP668로 인해 venv 필수)
python3 -m venv ~/mujoco_env
~/mujoco_env/bin/pip install mujoco

# 확인
~/mujoco_env/bin/python -c "import mujoco; print(mujoco.__version__)"
```

### ROS2 Lyrical 설치
```bash
# 설치 후 bashrc에 추가
echo "source /opt/ros/lyrical/setup.bash" >> ~/.bashrc
source ~/.bashrc

# 확인
ros2 topic list
```

### Rust 설치
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
echo 'source ~/.cargo/env' >> ~/.bashrc
source ~/.cargo/env
rustc --version
```

### rclrs 워크스페이스 구성
```bash
# 의존 도구 설치
sudo apt-get install -y python3-vcstool libclang-dev clang
sudo pip install colcon-cargo colcon-ros-cargo --break-system-packages

# 워크스페이스 구성
mkdir -p ~/ros2_rust_ws/src
cd ~/ros2_rust_ws/src
git clone https://github.com/ros2-rust/ros2_rust ros2_rust

# 의존 패키지 임포트 (ros2 기본 패키지 제외 — Lyrical 설치본과 충돌)
vcs import src < src/ros2_rust/ros2_rust_kilted.repos
rm -rf src/ros2

# 빌드 (ROS_DISTRO=kilted override 필요 — rclrs가 Lyrical 미지원)
source /opt/ros/lyrical/setup.bash
source ~/.cargo/env
ROS_DISTRO=kilted colcon build
```

---

## 프로젝트: MuJoCo ROS2 Bridge

MuJoCo 물리 시뮬레이션 데이터를 Rust ROS2 노드를 통해 토픽으로 publish하는 브릿지.

### 아키텍처
```
mujoco_sim.py (Python MuJoCo)
  └─ 단진자 시뮬 5000 steps → JSON stdout
        ↓ subprocess pipe
  Rust rclrs 노드 (mujoco_bridge)
        ↓ publish
  /mujoco_state 토픽 (std_msgs/String)
```

### 실행
```bash
# 워크스페이스 빌드
source /opt/ros/lyrical/setup.bash && source ~/.cargo/env
ROS_DISTRO=kilted colcon build --packages-select mujoco_ros2_bridge

# 노드 실행
source ~/ros2_rust_ws/install/setup.bash
ros2 run mujoco_ros2_bridge mujoco_bridge

# 다른 터미널에서 토픽 확인
ros2 topic echo /mujoco_state
```

### 출력 예시
```
Launching MuJoCo simulation...
[step 500] {"time": 1.0, "qpos": [-0.294], "qvel": [0.188]}
[step 1000] {"time": 2.0, "qpos": [0.278], "qvel": [-0.371]}
Simulation complete. Published 5000 states.
```
