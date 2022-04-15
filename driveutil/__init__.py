import os
import win32api,shutil

r'''A Small Package Made By Yeeterboi4 For Drive Uses! (Windows Only...)'''

full_drive_info = ['Volume Name : ','Volume Serial Number : ','Max Component Length : ','File System Name : ','','','','','','','','','','','','','','','','','','','','','']

#-----------------------------------------#
#                                         #
#             ALL FUNCTIONS               #
#                                         #
#-----------------------------------------#

def formatSize(bytes):
    '''A Wise Man Once Said... "Copy Code, And You Will Not Work For YEARS!". So I Did... From Here! : \n
    https://www.tutorialexample.com/a-simple-guide-to-python-get-disk-or-directory-total-space-used-space-and-free-space-python-tutorial/"\n
    Thanks!'''
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except:
        return "Error"
        
    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return "%.2fGB" % (G)
        else:
            return "%.2fMB" % (M)
    else:
        return "%.2fKB" % (kb)

def GetDrivesLetterFromName(drive_name):
    for drive_letter in GetUsedDrives():
        if GetDrivesInfo(drive_letter) == drive_name:
            return drive_letter.upper()
    return None

def SearchForDriveName(drive_name):
    for drive_letter in GetUsedDrives():
        if GetDrivesInfo(drive_letter) == drive_name:
            return True
    return False

def GetDrivesInfo(drive_letter,info_number = 1):
    '''You can access:\n
    1 - Volume Name (EX: KINGSTON)\n
    2 - Volume Serial Number (EX: 0x43097c6b)\n
    3 - Max Component Length (EX: 255)\n
    4 - File System Name (EX: FAT32)\n
    And more!\n
    \n
    Test what you can get! (1 - 22 I think.) (EX: 5 - Is ReadWrite)\n
    \n
    Command used: \"fsutil fsinfo volumeinfo\" (EX: fsutil fsinfo volumeinfo h:/)'''

    if info_number == 0: info_number = 1

    drive = os.popen(f"fsutil fsinfo volumeinfo {drive_letter.upper()}:")

    drive_list = drive.readlines()

    temp_usb_info = ''

    x = 0

    for line in drive_list:
        if x == info_number:
            break
        else:
            temp_usb_info = line
            x += 1

    usb_info = temp_usb_info.replace(full_drive_info[info_number - 1],'').strip('\n')

    return usb_info

def GetDrivesSpace(drive_letter,space_number = 1,display_GB_MB_KB=True):
    '''You can access:\n
    1 - All Space In Usb.  (GB)\n
    2 - All Space Used In Usb. (GB)\n
    3 - Space Available. (GB)\n
    \n
    Display GB or Not! (EX: 19GB OR 19)\n
    Command used: shutil.disk_space() (import shutil)'''

    if space_number == 0: space_number = 1
    elif space_number <= 4: space_number = 3
    
    space = shutil.disk_usage(f"{drive_letter.upper()}:\\")

    if display_GB_MB_KB: space_info = formatSize(space[space_number-1])
    else: space_info = formatSize(space[space_number-1]).replace('GB','')

    return space_info


def GetUsedDrives():
    '''Get All Drives That Are Currently Used (Also The Ones That Were Used.) Uses WIN32API'''
    x = 0
    drives = win32api.GetLogicalDriveStrings().split('\000')[:-1]

    for drive in drives:
        drives[x] = drive.replace(':\\','')
        x += 1

    return drives

#-----------------------------------------#
#                                         #
#               ALL CLASSES               #
#                                         #
#-----------------------------------------#

class Drive:
    '''Define a DRIVE! (Hard Drives MUST NEED ADMIN RIGHT!!!)'''

    def __init__(self,drive_letter,isusb):
        self.isusb = isusb
        self.name = GetDrivesInfo(drive_letter)
        self.serial_number = GetDrivesInfo(drive_letter,2)
        self.filesystem = GetDrivesInfo(drive_letter,4)
        self.drive_letter = drive_letter.upper()

    def DisplayDriveInfo(self):
        if self.isusb:
            '''Usb Name: KINGSTON, Usb Serial Number: 0x312ed31, Usb File System: FAT32'''
            return f'Usb Name: {self.name}, Usb Serial Number: {self.serial_number}, Usb File System: {self.filesystem}, Usb Drive Letter: {self.drive_letter}'
        else:
            '''Drive Name: KINGSTON, Drive Serial Number: 0x312ed31, Drive File System: FAT32'''
            return f'Drive Name: {self.name}, Drive Serial Number: {self.serial_number}, Drive File System: {self.filesystem}, Drive Drive Letter: {self.drive_letter}'

    def CopyToDrive(self,FileToCopy,WhereToCopyTo,Copy_file=True):
        '''Copy File (Or Folder) To Folder In Usb!'''
        if Copy_file:
            os.system(f'xcopy \"{FileToCopy}\" \"{self.drive_letter}:\\{WhereToCopyTo}\" /q /y >nul')
        else:
            folder = os.listdir(os.path.dirname(FileToCopy))
            for file in folder:
                os.system(f'xcopy \"{os.path.dirname(FileToCopy)}\\{file}\" \"{self.drive_letter}:\\{WhereToCopyTo}\" /q /y >nul')
    
    def GetDrivesInfo(self,info_number = 1):
        '''You can access:\n
        1 - Volume Name (EX: KINGSTON)\n
        2 - Volume Serial Number (EX: 0x43097c6b)\n
        3 - Max Component Length (EX: 255)\n
        4 - File System Name (EX: FAT32)\n
        And more!\n
        \n
        Test what you can get! (1 - 22 I think.) (EX: 5 - Is ReadWrite)\n
        \n
        Command used: \"fsutil fsinfo volumeinfo\" (EX: fsutil fsinfo volumeinfo h:/)'''

        if info_number == 0: info_number = 1

        drive = os.popen(f"fsutil fsinfo volumeinfo {self.drive_letter.upper()}:")

        drive_list = drive.readlines()

        temp_usb_info = ''

        x = 0

        for line in drive_list:
            if x == info_number:
                break
            else:
                temp_usb_info = line
                x += 1

        usb_info = temp_usb_info.replace(full_drive_info[info_number - 1],'').strip('\n')

        return usb_info

    def GetDrivesSpace(self,space_number = 1,display_GB_MB_KB=True):
        '''You can access:\n
        1 - All Space In Usb.  (GB/MB/KB)\n
        2 - All Space Used In Usb. (GB/MB/KB)\n
        3 - Space Available. (GB/MB/KB)\n
        \n
        Display GB/MB/KB or Not! (EX: 19GB OR 19)\n
        Command used: shutil.disk_space() (import shutil)'''

        if space_number <= 0: space_number = 1
        elif space_number >= 4: space_number = 3
        
        space = shutil.disk_usage(f"{self.drive_letter}:\\")

        if display_GB_MB_KB: space_info = formatSize(space[space_number-1])
        else: space_info = formatSize(space[space_number-1]).replace('GB','').replace('MB','').replace('KB','')

        return space_info