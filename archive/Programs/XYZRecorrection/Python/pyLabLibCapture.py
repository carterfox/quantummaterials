import pylablib as pll
from pylablib.devices import Thorlabs as thor
import cv2
import numpy as np
pll.par["devices/dlls/thorlabs_tlcam"] = "D:\LabData\Belal\Scientific Camera Interfaces\SDK\Python Toolkit\dlls"
with thor.ThorlabsTLCamera() as camera:
    camera.set_color_format("rgb")
    camera.set_frame_format("list")
    print(camera.get_exposure())
    camera.set_exposure()
    image = camera.snap()

image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
cv2.imshow("camera output", np.array(image, dtype=np.uint8))
cv2.waitKey(0) 