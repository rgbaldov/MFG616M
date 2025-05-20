import sim
import time
import numpy as np

print('Connecting to CoppeliaSim...')
sim.simxFinish(-1)
client_id = sim.simxStart('127.0.0.1', 19997, True, True, 5000, 5)

if client_id != -1:
    print('Connected!')
    sim.simxStartSimulation(client_id, sim.simx_opmode_blocking)

    joint_handles = []
    for i in range(6):
        _, handle = sim.simxGetObjectHandle(client_id, f'UR5_joint{i+1}', sim.simx_opmode_blocking)
        joint_handles.append(handle)

    # Set joint angles (Forward Kinematics)
    target_angles = [0.0, -0.5, 1.0, -1.2, 0.5, 0.0]
    for i in range(6):
        sim.simxSetJointTargetPosition(client_id, joint_handles[i], target_angles[i], sim.simx_opmode_oneshot)

    time.sleep(2)

    # Read tip position (FK result)
    _, tip_handle = sim.simxGetObjectHandle(client_id, 'UR5_tip', sim.simx_opmode_blocking)
    _, pos = sim.simxGetObjectPosition(client_id, tip_handle, -1, sim.simx_opmode_blocking)
    print('End-effector position (FK):', pos)

    sim.simxStopSimulation(client_id, sim.simx_opmode_blocking)
    sim.simxFinish(client_id)

else:
    print('Connection failed.')