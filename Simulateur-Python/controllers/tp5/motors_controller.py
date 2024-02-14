'''
This function is called when we are in the keyboard mode
'''
def keyboard_control(keyboard, Keyboard, motor_left, motor_right, speed):
    key=keyboard.getKey()

    if (key==Keyboard.UP):
        forward(motor_left, motor_right, speed)
        
    elif (key==Keyboard.DOWN):
        backward(motor_left, motor_right, speed)
    
    elif(key==Keyboard.LEFT):
        turn_left(motor_left, motor_right, speed)
    
    elif(key==Keyboard.RIGHT):
        turn_right(motor_left, motor_right, speed)

    else:
        stop(motor_left, motor_right)


def stop(motor_left, motor_right):
    motor_left.setVelocity(0)
    motor_right.setVelocity(0)

def forward(motor_left, motor_right, speed):
    motor_left.setVelocity(speed)
    motor_right.setVelocity(speed)

def backward(motor_left, motor_right, speed):
    motor_left.setVelocity(-speed)
    motor_right.setVelocity(-speed)

def turn_right(motor_left, motor_right, speed):
    motor_left.setVelocity(speed)
    motor_right.setVelocity(-speed)

def turn_left(motor_left, motor_right, speed):
    motor_left.setVelocity(-speed)
    motor_right.setVelocity(speed)