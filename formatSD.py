#!/usr/bin/env python

'''
   Simple build script that modifies the qt project file for the correct library path. 
   Which will also rebuild the library code and the Qt application as well
'''

import os

def findSD():

   try:
      os.remove("dmesgOutput")
      os.remove("sdINFO")
      os.remove("fdiskLOG")
   except:
      pass

   # Find ze SD card
   os.system("dmesg | tail >> dmesgOutput")

   dmesgRead = open("dmesgOutput", "r")

   possibleSDName = ""

   for lines in dmesgRead:
      if lines.find("sd") > 0:
         grabSD = lines.find("sd")
         infoSD = lines[grabSD:]
         grabLBraket = infoSD.find("[")
         grabRBraket = infoSD.find("]")
         possibleSDName = infoSD[grabLBraket + 1:grabRBraket]
         #print(possibleSDName)
         print ("Found an SD card!")
         break

   deviceName = "/dev/" + possibleSDName
   print ( deviceName )


   varIn = raw_input("Continue with formatting? (y/n): ")
   if varIn.lower() == "y":
      pass
   elif varIn.lower() == "n":
      return
   else:
      print("U BAD")
      return

   dmesgRead.close()

   #Get sd info so we can properly partition...
   #sdInfo = "echo p"
   os.system(("echo p") + "| fdisk " + "/dev/" + possibleSDName + " >> sdINFO")

   sdInfoRead = open("sdINFO", "r")

   for lines in sdInfoRead:
      info = "Disk " + deviceName
      #print info
      if lines.find(info) > 0:
         deviceLoc = lines.find(possibleSDName)
         sizeInfo = lines[deviceLoc + 4:].split(',')
         sectorSize = sizeInfo[2].split()
         createPartion(sectorSize[0], possibleSDName)
         break


   sdInfoRead.close()
   pass

def createPartion(size, deviceName):

   fixed = int(size) / 4
   # This may be ugly...
   FIRST_PARTITION =    "( echo d; echo n; echo p; echo 1; echo; " + "echo " + str(fixed) + ";" + "echo t; echo b;"
   SECOND_PARTITION =   " echo n; echo p; echo 2;" + "echo " + str(fixed + 1) + ";" + "echo " + str(fixed * 2) + ";"
   THIRD_PARTITION =    " echo n; echo p; echo 3;" + "echo " + str(fixed * 2 + 1) + ";" + "echo " + str(fixed * 3) + ";"
   FOURTH_PARTITION =   " echo n; echo p;" + "echo " + str(fixed * 3 + 1) + ";" + "echo " + str(int(size) - 1) + ";" + "echo w;)"
   os.system( ( FIRST_PARTITION + SECOND_PARTITION + THIRD_PARTITION + FOURTH_PARTITION) + " | fdisk " + "/dev/" + deviceName )
   
   pass


findSD()