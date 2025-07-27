import numpy as np
import os
from thorlabs_tsi_sdk.tl_camera import TLCameraSDK
from thorlabs_tsi_sdk.tl_mono_to_color_processor import MonoToColorProcessorSDK
from thorlabs_tsi_sdk.tl_mono_to_color_enums import COLOR_SPACE
from thorlabs_tsi_sdk.tl_color_enums import FORMAT
import cv2
from PIL import Image
import matplotlib.pyplot as plt
os.add_dll_directory(r"D:\\LabData\\Belal\\Scientific Camera Interfaces\\SDK\\Python Toolkit\dlls\\64_lib")
NUM_FRAMES = 1
frameW = 0
frameH = 0
with TLCameraSDK() as cameraSDK, MonoToColorProcessorSDK() as monoToColorSDK:
    print("Searching for cameras...")
    available_cameras = cameraSDK.discover_available_cameras() #find b1172 camera
    if(len(available_cameras) > 0):
        print("Camera with serial number " + available_cameras[0] + " found.")
    
    with cameraSDK.open_camera(available_cameras[0]) as camera:
        print("Configuring camera settings...")
        camera.frames_per_trigger_zero_for_unlimited = 0
        camera.image_poll_timeout_ms = 2000
        camera.operation_mode = 0
        old_roi = camera.roi

        print("Preparing for image capture.")
        camera.arm(2)
        imageWidth = camera.image_width_pixels
        frameW = camera.image_width_pixels
        imageHeight = camera.image_height_pixels
        frameH = camera.image_height_pixels
        camera.issue_software_trigger()

        frame = camera.get_pending_frame_or_null()
        if frame is not None:
            print("Frame recieved!")
        else:
            raise ValueError("No frame arrived within the timeout!")

        print("closing camera")
        camera.disarm()

        #moving on to color processing
        with monoToColorSDK.create_mono_to_color_processor(
            camera.camera_sensor_type,
            camera.color_filter_array_phase,
            camera.get_color_correction_matrix(),
            camera.get_default_white_balance_matrix(),
            camera.bit_depth
        ) as monoToColorProcessor:
            monoToColorProcessor.color_space = COLOR_SPACE.SRGB
            monoToColorProcessor.output_format = FORMAT.RGB_PIXEL

            colorImage24bpp = monoToColorProcessor.transform_to_24(frame.image_buffer, imageWidth, imageHeight)
    
    #Disposal of TLCameraSDK and camera objects taken care of by using 'with'

    print("Image capture and color processing completed.")

#Image capture completed, now on to image processing.
print(colorImage24bpp)
matImage = colorImage24bpp.reshape(imageWidth, imageHeight, 3)
print(matImage.shape)
cv2.imshow("camera output", np.array(matImage, dtype=np.uint8))
cv2.waitKey(0)