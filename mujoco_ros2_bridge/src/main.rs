use rclrs::*;
use std::io::{BufRead, BufReader};
use std::process::{Command, Stdio};
use std::thread;
use std_msgs::msg::String as StringMsg;

struct MujocoBridgeNode {
    publisher: Publisher<StringMsg>,
}

impl MujocoBridgeNode {
    fn new(executor: &Executor) -> Result<Self, RclrsError> {
        let node = executor.create_node("mujoco_bridge")?;
        let publisher = node.create_publisher("mujoco_state")?;
        Ok(Self { publisher })
    }

    fn publish(&self, data: String) -> Result<(), RclrsError> {
        self.publisher.publish(StringMsg { data })
    }
}

fn main() -> Result<(), RclrsError> {
    let mut executor = Context::default_from_env()?.create_basic_executor();
    let node = MujocoBridgeNode::new(&executor)?;

    let script = "/home/hs/ros2_rust_ws/src/mujoco_ros2_bridge/mujoco_sim.py";
    let python = "/home/hs/mujoco_env/bin/python";

    println!("Launching MuJoCo simulation...");

    let mut child = Command::new(python)
        .arg(script)
        .stdout(Stdio::piped())
        .spawn()
        .expect("Failed to spawn Python");

    let stdout = child.stdout.take().unwrap();
    let reader = BufReader::new(stdout);

    thread::spawn(move || {
        let mut count = 0u32;
        for line in reader.lines() {
            let json = match line {
                Ok(l) => l,
                Err(e) => { eprintln!("Read error: {}", e); break; }
            };
            if let Err(e) = node.publish(json.clone()) {
                eprintln!("Publish error: {}", e);
            }
            count += 1;
            if count % 500 == 0 {
                println!("[step {}] {}", count, json);
            }
        }
        println!("Simulation complete. Published {} states.", count);
    });

    executor.spin(SpinOptions::default()).first_error()
}
