#ifndef FRANKA_GRIPPER_MOCK_GRIPPER_HPP
#define FRANKA_GRIPPER_MOCK_GRIPPER_HPP
/// A gripper object that simulates a gripper using the same libfranka interface as franka::Gripper

#include<franka/gripper_state.h>

namespace franka_gripper
{
/// See libfranka/include/franka/gripper.h
class MockGripper
{
public:
    /// Make a fake gripper. The string is the robot_ip and it is ignored
    MockGripper(const std::string &) {};

    bool homing() const {return true;}

    bool grasp(double width,
               double speed,
               double force,
               double epsilon_inner = 0.005,
               double epsilon_outer = 0.005)
    {
        state.width = width;
        return true;
    }

    bool move(double width, double speed)
    {
        state.width = width;
        return true;
    }


    bool stop() const
    {
        return true;
    }

    franka::GripperState readOnce() const
    {
        return state;
    }

private:
    franka::GripperState state{0.0, // current width: starts closed
            0.07, // max width: depends on homing. set to 7 cm here
            false, // object is not grasped
            25, // temperature of the gripper in Celsius
            {}, // start at zero duration
            };


};
}
#endif
