from pyAndorSDK2 import atmcd, atmcd_codes, atmcd_errors

sdk = atmcd()  # Load the atmcd library
codes = atmcd_codes

ret = sdk.Initialize("")  # Initialize camera

if atmcd_errors.Error_Codes.DRV_SUCCESS == ret:

    (ret, iSerialNumber) = sdk.GetCameraSerialNumber()
    # Configure the acquisition
    ret = sdk.GetTemperatureRange()
    print(ret)
    # ret = sdk.SetAcquisitionMode(codes.Acquisition_Mode.SINGLE_SCAN)
    # ret = sdk.SetReadMode(codes.Read_Mode.FULL_VERTICAL_BINNING)
    # ret = sdk.SetTriggerMode(codes.Trigger_Mode.INTERNAL)
    # (ret, xpixels, ypixels) = sdk.GetDetector()
    # ret = sdk.SetExposureTime(0.01)

    # (ret, fminExposure, fAccumulate, fKinetic) = sdk.GetAcquisitionTimings()
    # print("Function GetAcquisitionTimings returned {} exposure = {} accumulate = {} kinetic = {}".format(
    #     ret, fminExposure, fAccumulate, fKinetic))

    # for i in range(4):
    #     data = sdk.acquire()
    #     print(data)

    # Clean up
    # ret = sdk.ShutDown()
    print("Function ShutDown returned {}".format(ret))

else:
    print("Cannot continue, could not initialise camera")
