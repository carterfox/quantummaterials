## Installer for Windows 7 Digital Signature Hotfixes
--------------------------------
Current driver uses SHA-256 (Secure Hash Algorithm 256-bit) for Digital Signature.
If your PC is running on Windows 7, and is not up-to-date with Windows Update, the SHA-256 signature may not be supported properly.
If it is not supported properly, you may experience:

1. The installer may popup a Windows Security dialog during installation of the driver and/or hardware.

   The message includes  following information.

        Name: Hamamatsu Photonics K.K. (Device Manager Name)
        Publisher: Hamamatsu Corporation

   Hamamatsu Corporation is a subsidiary company of Hamamatsu Photonics K.K.

2. Device Manager may show a Code 52 - "Windows cannot verify the digital signature for the drivers required for this device." error in the Device status window of a Hamamatsu provided/installed driver.

To prevent/fix these situations, this installer includes some update files (Roots Certificate Update and Hotfixes). Please run the following BAT file As Administrator and restart your PC if notified in the command window executing the BAT file.
After you reboot, then you can install current driver with no errors due to this incompatibility of SHA-256 signatures.

    Hotfixes\Win7_FixCode52Error\RunOnceFirst_AsAdmin.bat
