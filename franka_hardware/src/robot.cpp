// Copyright (c) 2021 Franka Emika GmbH
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include <franka_hardware/robot.hpp>

#include <cassert>
#include <mutex>

#include <franka/control_tools.h>
#include <rclcpp/logging.hpp>

namespace franka_hardware {

Robot::Robot(const std::string& robot_ip, const rclcpp::Logger& logger) {
  tau_command_.fill(0.);
  franka::RealtimeConfig rt_config = franka::RealtimeConfig::kEnforce;
  if (not franka::hasRealtimeKernel()) {
    rt_config = franka::RealtimeConfig::kIgnore;
    RCLCPP_WARN(
        logger,
        "You are not using a real-time kernel. Using a real-time kernel is strongly recommended!");
  }
  robot_ = std::make_unique<franka::Robot>(robot_ip, rt_config);
}

void Robot::write(const std::array<double, 7>& efforts) {
  std::lock_guard<std::mutex> lock(write_mutex_);
  tau_command_ = efforts;
}

franka::RobotState Robot::read() {
  std::lock_guard<std::mutex> lock(read_mutex_);
  return {current_state_};
}

void Robot::stopRobot() {
  if (not stopped_) {
    finish_ = true;
    control_thread_->join();
    finish_ = false;
    stopped_ = true;
  }
}

void Robot::initializeTorqueControl() {
  assert(isStopped());
  stopped_ = false;
  const auto kTorqueControl = [this]() {
    robot_->control(
        [this](const franka::RobotState& state, const franka::Duration& /*period*/) {
          {
            std::lock_guard<std::mutex> lock(read_mutex_);
            current_state_ = state;
          }
          std::lock_guard<std::mutex> lock(write_mutex_);
          franka::Torques out(tau_command_);
          out.motion_finished = finish_;
          return out;
        },
        true, franka::kMaxCutoffFrequency);
  };
  control_thread_ = std::make_unique<std::thread>(kTorqueControl);
}

void Robot::initializeContinuousReading() {
  assert(isStopped());
  stopped_ = false;
  const auto kReading = [this]() {
    robot_->read([this](const franka::RobotState& state) {
      {
        std::lock_guard<std::mutex> lock(read_mutex_);
        current_state_ = state;
      }
      return not finish_;
    });
  };
  control_thread_ = std::make_unique<std::thread>(kReading);
}

Robot::~Robot() {
  stopRobot();
}

bool Robot::isStopped() const {
  return stopped_;
}

void Robot::setLoad(const franka_msgs::srv::SetLoad::Request::SharedPtr& req) {
  std::lock_guard<std::mutex> lock(write_mutex_);
  double mass(req->mass);
  std::array<double, 3> center_of_mass{};  // NOLINT [readability-identifier-naming]
  std::copy(req->center_of_mass.cbegin(), req->center_of_mass.cend(), center_of_mass.begin());
  std::array<double, 9> load_inertia{};
  std::copy(req->load_inertia.cbegin(), req->load_inertia.cend(), load_inertia.begin());

  robot_->setLoad(mass, center_of_mass, load_inertia);
}

}  // namespace franka_hardware
