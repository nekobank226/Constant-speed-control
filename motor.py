import pigpio
import time
import Adafruit_PCA9685

# 設定周波数
SET_FREQ = 50

# ピンの設定
pi = pigpio.pi()
pi.set_mode(14, pigpio.OUTPUT)
pi.set_mode(15, pigpio.OUTPUT)
pi.set_mode(17, pigpio.INPUT)
pi.set_mode(27, pigpio.INPUT)
pi.set_pull_up_down(17, pigpio.PUD_UP)
pi.set_pull_up_down(27, pigpio.PUD_UP)

# PCA9685の初期化
PCA9685 = Adafruit_PCA9685.PCA9685()
PCA9685.set_pwm_freq(SET_FREQ)

# ギア比
gear_ratio = 171.79
# エンコーダの分解能
encoder_count = 48
counter = 0
e = 0
e1 = 0
e2 = 0
kp = 0.1
ki = 0.1
kd = 0
M = 0
M1 = 0
duty_cycle=0


def motor_angle(power_ratio: int):
    global duty_cycle
    global speed_target
    global point
    global M
    global M1
    global e
    global e1
    global e2
    global P
    # 0の時用
    if power_ratio == 0:
        pi.write(14, 0)
        pi.write(15, 0)
        PCA9685.set_pwm(0, 0, 0)
        return
    # 100を超えた時用
    if abs(power_ratio) > 100:
        print("パワーは100%以下にしてください")
        pi.write(14, 0)
        pi.write(15, 0)
        PCA9685.set_pwm(0, 0, 0)
        return

    # 速度計算用
    if power_ratio > 0:
        pi.write(14, 1)
        pi.write(15, 0)
    else:
        pi.write(14, 0)
        pi.write(15, 1)
    print("回転開始")

    try:
        while True:
            speed_target = int(power_ratio * 4095 / 100)
            M1 = duty_cycle
            e2 = e1
            e1 = e
            e = speed_target - M1
            duty_cycle = int(M1+kp*(e-e1)+ki*e+kd*((e-e1)-(e1-e2)))
            PCA9685.set_pwm(0, 0, duty_cycle)
    except KeyboardInterrupt:
        print("回転終了")

            
def stop():

    pi.write(14, 0)
    pi.write(15, 0)
    PCA9685.set_pwm(0, 0, 0)

if __name__ == "__main__":
    motor_angle(20)
    stop()