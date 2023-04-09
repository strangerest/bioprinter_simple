import serial
import time

def xorCRC(str):
    count = 0
    checksum = 0
    while (str[count] != '*'):
        checksum = checksum^ord(str[count])
        count += 1
        
    return checksum
#f = open('text.txt', 'w')
#USB Serial Port
serMove = serial.Serial(port='COM4', baudrate=115200, timeout=1)

Commands = ['M110', 'M115', 'M105', 'M114', 'M111 S6', 'T0', 'M20', 'M80', 'M105', 'M105', 'M220 S100', 'M221 S100', 'M111 S6', 'T0']
#CommandsG = ['G28 X0', 'G28 Y0', 'G21', 'G1 Y0 F5000', 'G1 X5', 'G1 Y100', 'G1 X10', 'G1 Y0', 'G1 X15', 'G1 Y100', 'G1 X0 Y0']
#               0       1        2      3               4           5       6       7           8       9           10      11          12 
CommandsG = ['G28 X0', 'G28 Y0', 'G21', 'G1 Y0 F2600', 'G1 Y40', 'G1 Y0']
'''
'G1 X4', 'G1 Y100', 'G1 Y0',
'G1 X8', 'G1 Y100', 'G1 Y0',

'G1 Y0', 'G1 Y100', 'G1 X4', 
'G1 Y0', 'G1 Y100', 'G1 X8', 
'G1 Y0', 'G1 Y100', 'G1 X12', 
'G1 Y0', 'G1 Y100', 'G1 X16', 
'G1 Y0', 'G1 Y100', 
'G1 X0 Y0']
'''
itemsG = ['G1 X', 'G1 Y130', 'G1 Y0'] 
homeG = 'G1 X0 Y0'

#                                           
waitArr = ['M301 P22.20 I1.08 D114.00', 'FIRMWARE_NAME', 'ok', 'X:0.00 Y:0.00 Z:0.00', 'ok', 'ok', 'Active Extruder', 'ok', 'ok', 'ok', 'Active Extruder', 'ok']
#, 'ok', 'ok', 'ok', 'ok', 'ok', 'ok', 'ok', 'ok', 'ok', 'ok', 'ok', 'ok']
#14                 14   21     22         23           26               28          29    30
rows = 36 
waitIdx = 0
waitNum = 1
stage = 1
while stage < 139:
    while waitNum > 0:
        waitStr = ''
        if waitIdx < len(waitArr):
            waitStr = waitArr[waitIdx]
        else:
            waitStr = 'ok'
        print "waiting for ", waitStr
        strI = serMove.readline()
        print strI

        if strI.find(waitStr) >= 0:
            waitIdx += 1
            waitNum -= 1
            print "stage =", stage, ", waitIdx =", waitIdx, ", waitNum =", waitNum
     
    #break;
    init = ''
    g_beg = 15
    
    korteg_0 = (16,19,22,30,36,40,45,54,60,64,69,81)
     # waitNum = 0      
    korteg_1 = (17,24,32,48,56,72,78,80,87,88,90,93,
                96,99,102,104,105,106,108,111,112,114,
                117,120,121,122,123,124,125,126,127,128,
                129,130,131,132,133,134,135,136,137,138,139)
     # waitNum = 1
    korteg_2 = (10,14)
     # waitNum = 2
    korteg_3 = (11,13)
     # waitNum = 3
 
    if stage in korteg_0:
        waitNum = 0
    elif stage in korteg_1:
        waitNum = 1
    elif stage in korteg_2:
        waitNum = 2
    elif stage in korteg_3:
        waitNum = 3

    elif stage >= 15 and stage not in korteg_0+korteg_1+korteg_2+korteg_3:
        if stage % 8 == 0:
            waitNum = 3
        elif stage % 3 == 0:
            waitNum = 2
        else:
            waitNum = 1
    
    
    g_end = g_beg + len(CommandsG)
    if (stage <= len(Commands)): 
        init = Commands[stage - 1]
    elif (stage >= g_beg and stage < g_end):
        init = CommandsG[stage-g_beg]
    elif stage >= g_end and stage <= g_end + 3 * rows:
        #itemsG = ['G1 X', 'G1 Y150', 'G1 Y0']  
        if stage != g_end + 3 * rows:
            init = itemsG[(stage - g_end) % 3]
            if (stage - g_end) % 3 == 0: # x
                init += str((((stage - g_end) / 3) + 1) * (3.15)) #! width = 3.1
        else:
            init = homeG 
    else:
        #waiting = True
        init = 'M105'
    cmnd = 'N' + str(stage) + ' ' + init + ' *'
    cmnd = cmnd + str(xorCRC(cmnd)) + '\n'
    serMove.write(cmnd)
#   f.write(cmnd + '\n')

    stage += 1
    print cmnd
    time.sleep(0.01)
