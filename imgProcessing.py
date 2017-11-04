import numpy as np
import cv2, os
from datetime import datetime, timedelta, time
import threading

savePath="/media/huni/EE98066498062C21/linux/cctv/videos/"
free_bytes_required=368577300832


# cap = cv2.VideoCapture(1) # WebCam
cap = cv2.VideoCapture(0) # FrontCam
# Define the codec and create VideoWriter object
fourcc = cv2.cv.CV_FOURCC(*'XVID')
outGray = cv2.VideoWriter(filename=savePath + datetime.now().strftime('%Y_%m_%d_%M') + '_Gray.avi',
                          fourcc=fourcc,
                        #   fps=10.0, # WebCam settings
                          fps=7.0, # FrontCam settings
                          frameSize=(640,480),
                          isColor=False)

# Return list with directory filenames ordered by time
def filesToDelete(rootfolder):
    return sorted(
         (os.path.join(dirname, filename)
         for dirname, dirnames, filenames in os.walk(rootfolder)
         for filename in filenames),
            key=lambda fn: os.stat(fn).st_mtime,
            reverse=True)

# Delete old files if free space needed and keep the newest
def freeSpaceUpTo():
    fileList = filesToDelete(savePath)
    while fileList:
        statv = os.statvfs(savePath)
        print(statv.f_bfree*statv.f_bsize)
        # Get free space
        if statv.f_bfree*statv.f_bsize >= free_bytes_required:
            break
        # Keep the recent file
        if (len(fileList)) > 1:
            print(fileList)
            os.remove(fileList.pop())
        else:
            print(fileList)
            break
    # Start new thread
    timer = threading.Timer(5, freeSpaceUpTo)
    timer.setDaemon(True)
    timer.start()


freeSpaceUpTo()
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        now = datetime.now()
        cv2.putText(frame, now.strftime("%Y-%m-%d %H:%M:%S"), (10,470), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 2)
        # write the gray frame
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        outGray.write(gray)
        # Display frame
        cv2.imshow('Gray',gray)
        # Time to record
        if now.strftime("%H:%M:%S") == "00:00:00":
            outGray.release()
            outGray.open(filename=savePath + now.strftime("%Y_%m_%d_%M") + '_Gray.avi',fourcc=fourcc,fps=10.0,frameSize=(640,480),isColor=False)
        # Press 'q' to quitq
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
outGray.release()
cv2.destroyAllWindows()
