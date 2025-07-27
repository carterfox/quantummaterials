<?xml version='1.0' encoding='UTF-8'?>
<Project Type="Project" LVVersion="22308000">
	<Property Name="NI.LV.All.SourceOnly" Type="Bool">true</Property>
	<Item Name="My Computer" Type="My Computer">
		<Property Name="server.app.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.control.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.tcp.enabled" Type="Bool">false</Property>
		<Property Name="server.tcp.port" Type="Int">0</Property>
		<Property Name="server.tcp.serviceName" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.tcp.serviceName.default" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.vi.callsEnabled" Type="Bool">true</Property>
		<Property Name="server.vi.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="specify.custom.address" Type="Bool">false</Property>
		<Item Name="PMT_Project_folder" Type="Folder">
			<Item Name="Kiethley24XX_VIs" Type="Folder">
				<Item Name="Examples" Type="Folder">
					<Item Name="Keithley 24XX Custom Math Operation.vi" Type="VI" URL="../Kiethley24XX_VIs/Examples/Keithley 24XX Custom Math Operation.vi"/>
					<Item Name="Keithley 24XX Output List and Acquire.vi" Type="VI" URL="../Kiethley24XX_VIs/Examples/Keithley 24XX Output List and Acquire.vi"/>
					<Item Name="Keithley 24XX Perform Limit Tests.vi" Type="VI" URL="../Kiethley24XX_VIs/Examples/Keithley 24XX Perform Limit Tests.vi"/>
					<Item Name="Keithley 24XX Perform Statistical Operation.vi" Type="VI" URL="../Kiethley24XX_VIs/Examples/Keithley 24XX Perform Statistical Operation.vi"/>
					<Item Name="Keithley 24XX Read Multiple - SW Trigger.vi" Type="VI" URL="../Kiethley24XX_VIs/Examples/Keithley 24XX Read Multiple - SW Trigger.vi"/>
					<Item Name="Keithley 24XX Read Multiple.vi" Type="VI" URL="../Kiethley24XX_VIs/Examples/Keithley 24XX Read Multiple.vi"/>
					<Item Name="Keithley 24XX Read Single.vi" Type="VI" URL="../Kiethley24XX_VIs/Examples/Keithley 24XX Read Single.vi"/>
					<Item Name="Keithley 24XX Sweep and Acquire Measurements.vi" Type="VI" URL="../Kiethley24XX_VIs/Examples/Keithley 24XX Sweep and Acquire Measurements.vi"/>
					<Item Name="Keithley 24XX Test and Memory Sweep.vi" Type="VI" URL="../Kiethley24XX_VIs/Examples/Keithley 24XX Test and Memory Sweep.vi"/>
				</Item>
				<Item Name="Initialize Folder" Type="Folder">
					<Item Name="D" Type="Folder">
						<Item Name="Download" Type="Folder">
							<Item Name="Keithley 24XX" Type="Folder">
								<Item Name="Private" Type="Folder"/>
								<Item Name="Public" Type="Folder">
									<Item Name="Action-Status" Type="Folder"/>
									<Item Name="Configure" Type="Folder">
										<Item Name="Low Level" Type="Folder"/>
									</Item>
									<Item Name="Data" Type="Folder">
										<Item Name="Low Level" Type="Folder"/>
									</Item>
									<Item Name="Utility" Type="Folder"/>
								</Item>
							</Item>
						</Item>
					</Item>
				</Item>
				<Item Name="Keithley 24XX.aliases" Type="Document" URL="../Kiethley24XX_VIs/Keithley 24XX.aliases"/>
				<Item Name="Keithley 24XX.lvlib" Type="Library" URL="../Kiethley24XX_VIs/Keithley 24XX.lvlib"/>
				<Item Name="Keithley 24XX.lvlps" Type="Document" URL="../Kiethley24XX_VIs/Keithley 24XX.lvlps"/>
				<Item Name="Keithley 24XX.lvproj" Type="Document" URL="../Kiethley24XX_VIs/Keithley 24XX.lvproj"/>
			</Item>
			<Item Name="Kiethley2450_VIs" Type="Folder">
				<Item Name="Private" Type="Folder"/>
				<Item Name="Public" Type="Folder">
					<Item Name="Action-Status" Type="Folder"/>
					<Item Name="Configure" Type="Folder"/>
					<Item Name="Data" Type="Folder">
						<Item Name="Low Level" Type="Folder"/>
					</Item>
					<Item Name="Utility" Type="Folder"/>
				</Item>
				<Item Name="Keithley 2450.lvlib" Type="Library" URL="../Kiethley2450_VIs/Keithley 2450.lvlib"/>
			</Item>
			<Item Name="Kinesis_VIs" Type="Folder">
				<Item Name="BSC stepper" Type="Folder">
					<Item Name="BSC to more generic &amp; multichannel.lvproj" Type="Document" URL="../Kinesis_VIs/BSC stepper/BSC to more generic &amp; multichannel.lvproj"/>
					<Item Name="BSC To More Generic Example.vi" Type="VI" URL="../Kinesis_VIs/BSC stepper/BSC To More Generic Example.vi"/>
					<Item Name="BSC203 multichannel control - basic.vi" Type="VI" URL="../Kinesis_VIs/BSC stepper/BSC203 multichannel control - basic.vi"/>
				</Item>
				<Item Name="Drivers" Type="Folder">
					<Item Name="APT" Type="Folder">
						<Item Name="USB Driver" Type="Folder">
							<Item Name="amd64" Type="Folder">
								<Item Name="ftbusui.dll" Type="Document" URL="../Kinesis_VIs/Drivers/APT/USB Driver/amd64/ftbusui.dll"/>
								<Item Name="ftcserco.dll" Type="Document" URL="../Kinesis_VIs/Drivers/APT/USB Driver/amd64/ftcserco.dll"/>
								<Item Name="ftd2xx.lib" Type="Document" URL="../Kinesis_VIs/Drivers/APT/USB Driver/amd64/ftd2xx.lib"/>
								<Item Name="ftd2xx64.dll" Type="Document" URL="../Kinesis_VIs/Drivers/APT/USB Driver/amd64/ftd2xx64.dll"/>
								<Item Name="ftdibus.sys" Type="Document" URL="../Kinesis_VIs/Drivers/APT/USB Driver/amd64/ftdibus.sys"/>
								<Item Name="ftlang.dll" Type="Document" URL="../Kinesis_VIs/Drivers/APT/USB Driver/amd64/ftlang.dll"/>
								<Item Name="ftser2k.sys" Type="Document" URL="../Kinesis_VIs/Drivers/APT/USB Driver/amd64/ftser2k.sys"/>
								<Item Name="ftserui2.dll" Type="Document" URL="../Kinesis_VIs/Drivers/APT/USB Driver/amd64/ftserui2.dll"/>
							</Item>
							<Item Name="i386" Type="Folder">
								<Item Name="ftbusui.dll" Type="Document" URL="../Kinesis_VIs/Drivers/APT/USB Driver/i386/ftbusui.dll"/>
								<Item Name="ftcserco.dll" Type="Document" URL="../Kinesis_VIs/Drivers/APT/USB Driver/i386/ftcserco.dll"/>
								<Item Name="ftd2xx.dll" Type="Document" URL="../Kinesis_VIs/Drivers/APT/USB Driver/i386/ftd2xx.dll"/>
								<Item Name="ftd2xx.lib" Type="Document" URL="../Kinesis_VIs/Drivers/APT/USB Driver/i386/ftd2xx.lib"/>
								<Item Name="ftdibus.sys" Type="Document" URL="../Kinesis_VIs/Drivers/APT/USB Driver/i386/ftdibus.sys"/>
								<Item Name="ftlang.dll" Type="Document" URL="../Kinesis_VIs/Drivers/APT/USB Driver/i386/ftlang.dll"/>
								<Item Name="ftser2k.sys" Type="Document" URL="../Kinesis_VIs/Drivers/APT/USB Driver/i386/ftser2k.sys"/>
								<Item Name="ftserui2.dll" Type="Document" URL="../Kinesis_VIs/Drivers/APT/USB Driver/i386/ftserui2.dll"/>
							</Item>
							<Item Name="Static" Type="Folder">
								<Item Name="amd64" Type="Folder">
									<Item Name="ftd2xx.lib" Type="Document" URL="../Kinesis_VIs/Drivers/APT/USB Driver/Static/amd64/ftd2xx.lib"/>
								</Item>
								<Item Name="i386" Type="Folder">
									<Item Name="ftd2xx.lib" Type="Document" URL="../Kinesis_VIs/Drivers/APT/USB Driver/Static/i386/ftd2xx.lib"/>
								</Item>
							</Item>
							<Item Name="APT USB Driver.cat" Type="Document" URL="../Kinesis_VIs/Drivers/APT/USB Driver/APT USB Driver.cat"/>
							<Item Name="APT USB Driver.inf" Type="Document" URL="../Kinesis_VIs/Drivers/APT/USB Driver/APT USB Driver.inf"/>
							<Item Name="ftd2xx.h" Type="Document" URL="../Kinesis_VIs/Drivers/APT/USB Driver/ftd2xx.h"/>
						</Item>
						<Item Name="VCP Driver" Type="Folder">
							<Item Name="amd64" Type="Folder">
								<Item Name="ftbusui.dll" Type="Document" URL="../Kinesis_VIs/Drivers/APT/VCP Driver/amd64/ftbusui.dll"/>
								<Item Name="ftcserco.dll" Type="Document" URL="../Kinesis_VIs/Drivers/APT/VCP Driver/amd64/ftcserco.dll"/>
								<Item Name="ftd2xx.lib" Type="Document" URL="../Kinesis_VIs/Drivers/APT/VCP Driver/amd64/ftd2xx.lib"/>
								<Item Name="ftd2xx64.dll" Type="Document" URL="../Kinesis_VIs/Drivers/APT/VCP Driver/amd64/ftd2xx64.dll"/>
								<Item Name="ftdibus.sys" Type="Document" URL="../Kinesis_VIs/Drivers/APT/VCP Driver/amd64/ftdibus.sys"/>
								<Item Name="ftlang.dll" Type="Document" URL="../Kinesis_VIs/Drivers/APT/VCP Driver/amd64/ftlang.dll"/>
								<Item Name="ftser2k.sys" Type="Document" URL="../Kinesis_VIs/Drivers/APT/VCP Driver/amd64/ftser2k.sys"/>
								<Item Name="ftserui2.dll" Type="Document" URL="../Kinesis_VIs/Drivers/APT/VCP Driver/amd64/ftserui2.dll"/>
							</Item>
							<Item Name="i386" Type="Folder">
								<Item Name="ftbusui.dll" Type="Document" URL="../Kinesis_VIs/Drivers/APT/VCP Driver/i386/ftbusui.dll"/>
								<Item Name="ftcserco.dll" Type="Document" URL="../Kinesis_VIs/Drivers/APT/VCP Driver/i386/ftcserco.dll"/>
								<Item Name="ftd2xx.dll" Type="Document" URL="../Kinesis_VIs/Drivers/APT/VCP Driver/i386/ftd2xx.dll"/>
								<Item Name="ftd2xx.lib" Type="Document" URL="../Kinesis_VIs/Drivers/APT/VCP Driver/i386/ftd2xx.lib"/>
								<Item Name="ftdibus.sys" Type="Document" URL="../Kinesis_VIs/Drivers/APT/VCP Driver/i386/ftdibus.sys"/>
								<Item Name="ftlang.dll" Type="Document" URL="../Kinesis_VIs/Drivers/APT/VCP Driver/i386/ftlang.dll"/>
								<Item Name="ftser2k.sys" Type="Document" URL="../Kinesis_VIs/Drivers/APT/VCP Driver/i386/ftser2k.sys"/>
								<Item Name="ftserui2.dll" Type="Document" URL="../Kinesis_VIs/Drivers/APT/VCP Driver/i386/ftserui2.dll"/>
							</Item>
							<Item Name="Static" Type="Folder">
								<Item Name="amd64" Type="Folder">
									<Item Name="ftd2xx.lib" Type="Document" URL="../Kinesis_VIs/Drivers/APT/VCP Driver/Static/amd64/ftd2xx.lib"/>
								</Item>
								<Item Name="i386" Type="Folder">
									<Item Name="ftd2xx.lib" Type="Document" URL="../Kinesis_VIs/Drivers/APT/VCP Driver/Static/i386/ftd2xx.lib"/>
								</Item>
							</Item>
							<Item Name="APT USB Serial Port.cat" Type="Document" URL="../Kinesis_VIs/Drivers/APT/VCP Driver/APT USB Serial Port.cat"/>
							<Item Name="APT USB Serial Port.inf" Type="Document" URL="../Kinesis_VIs/Drivers/APT/VCP Driver/APT USB Serial Port.inf"/>
							<Item Name="ftd2xx.h" Type="Document" URL="../Kinesis_VIs/Drivers/APT/VCP Driver/ftd2xx.h"/>
						</Item>
					</Item>
					<Item Name="Kinesis" Type="Folder">
						<Item Name="USB Driver" Type="Folder">
							<Item Name="amd64" Type="Folder">
								<Item Name="ftbusui.dll" Type="Document" URL="../Kinesis_VIs/Drivers/Kinesis/USB Driver/amd64/ftbusui.dll"/>
								<Item Name="ftcserco.dll" Type="Document" URL="../Kinesis_VIs/Drivers/Kinesis/USB Driver/amd64/ftcserco.dll"/>
								<Item Name="ftd2xx.lib" Type="Document" URL="../Kinesis_VIs/Drivers/Kinesis/USB Driver/amd64/ftd2xx.lib"/>
								<Item Name="ftd2xx64.dll" Type="Document" URL="../Kinesis_VIs/Drivers/Kinesis/USB Driver/amd64/ftd2xx64.dll"/>
								<Item Name="ftdibus.sys" Type="Document" URL="../Kinesis_VIs/Drivers/Kinesis/USB Driver/amd64/ftdibus.sys"/>
								<Item Name="ftlang.dll" Type="Document" URL="../Kinesis_VIs/Drivers/Kinesis/USB Driver/amd64/ftlang.dll"/>
								<Item Name="ftser2k.sys" Type="Document" URL="../Kinesis_VIs/Drivers/Kinesis/USB Driver/amd64/ftser2k.sys"/>
								<Item Name="ftserui2.dll" Type="Document" URL="../Kinesis_VIs/Drivers/Kinesis/USB Driver/amd64/ftserui2.dll"/>
							</Item>
							<Item Name="i386" Type="Folder">
								<Item Name="ftbusui.dll" Type="Document" URL="../Kinesis_VIs/Drivers/Kinesis/USB Driver/i386/ftbusui.dll"/>
								<Item Name="ftcserco.dll" Type="Document" URL="../Kinesis_VIs/Drivers/Kinesis/USB Driver/i386/ftcserco.dll"/>
								<Item Name="ftd2xx.dll" Type="Document" URL="../Kinesis_VIs/Drivers/Kinesis/USB Driver/i386/ftd2xx.dll"/>
								<Item Name="ftd2xx.lib" Type="Document" URL="../Kinesis_VIs/Drivers/Kinesis/USB Driver/i386/ftd2xx.lib"/>
								<Item Name="ftdibus.sys" Type="Document" URL="../Kinesis_VIs/Drivers/Kinesis/USB Driver/i386/ftdibus.sys"/>
								<Item Name="ftlang.dll" Type="Document" URL="../Kinesis_VIs/Drivers/Kinesis/USB Driver/i386/ftlang.dll"/>
								<Item Name="ftser2k.sys" Type="Document" URL="../Kinesis_VIs/Drivers/Kinesis/USB Driver/i386/ftser2k.sys"/>
								<Item Name="ftserui2.dll" Type="Document" URL="../Kinesis_VIs/Drivers/Kinesis/USB Driver/i386/ftserui2.dll"/>
							</Item>
							<Item Name="Static" Type="Folder">
								<Item Name="amd64" Type="Folder">
									<Item Name="ftd2xx.lib" Type="Document" URL="../Kinesis_VIs/Drivers/Kinesis/USB Driver/Static/amd64/ftd2xx.lib"/>
								</Item>
								<Item Name="i386" Type="Folder">
									<Item Name="ftd2xx.lib" Type="Document" URL="../Kinesis_VIs/Drivers/Kinesis/USB Driver/Static/i386/ftd2xx.lib"/>
								</Item>
							</Item>
							<Item Name="ftd2xx.h" Type="Document" URL="../Kinesis_VIs/Drivers/Kinesis/USB Driver/ftd2xx.h"/>
							<Item Name="Kinesis USB Driver.cat" Type="Document" URL="../Kinesis_VIs/Drivers/Kinesis/USB Driver/Kinesis USB Driver.cat"/>
							<Item Name="Kinesis USB Driver.inf" Type="Document" URL="../Kinesis_VIs/Drivers/Kinesis/USB Driver/Kinesis USB Driver.inf"/>
						</Item>
						<Item Name="VCP Driver" Type="Folder">
							<Item Name="amd64" Type="Folder">
								<Item Name="ftbusui.dll" Type="Document" URL="../Kinesis_VIs/Drivers/Kinesis/VCP Driver/amd64/ftbusui.dll"/>
								<Item Name="ftcserco.dll" Type="Document" URL="../Kinesis_VIs/Drivers/Kinesis/VCP Driver/amd64/ftcserco.dll"/>
								<Item Name="ftd2xx.lib" Type="Document" URL="../Kinesis_VIs/Drivers/Kinesis/VCP Driver/amd64/ftd2xx.lib"/>
								<Item Name="ftd2xx64.dll" Type="Document" URL="../Kinesis_VIs/Drivers/Kinesis/VCP Driver/amd64/ftd2xx64.dll"/>
								<Item Name="ftdibus.sys" Type="Document" URL="../Kinesis_VIs/Drivers/Kinesis/VCP Driver/amd64/ftdibus.sys"/>
								<Item Name="ftlang.dll" Type="Document" URL="../Kinesis_VIs/Drivers/Kinesis/VCP Driver/amd64/ftlang.dll"/>
								<Item Name="ftser2k.sys" Type="Document" URL="../Kinesis_VIs/Drivers/Kinesis/VCP Driver/amd64/ftser2k.sys"/>
								<Item Name="ftserui2.dll" Type="Document" URL="../Kinesis_VIs/Drivers/Kinesis/VCP Driver/amd64/ftserui2.dll"/>
							</Item>
							<Item Name="i386" Type="Folder">
								<Item Name="ftbusui.dll" Type="Document" URL="../Kinesis_VIs/Drivers/Kinesis/VCP Driver/i386/ftbusui.dll"/>
								<Item Name="ftcserco.dll" Type="Document" URL="../Kinesis_VIs/Drivers/Kinesis/VCP Driver/i386/ftcserco.dll"/>
								<Item Name="ftd2xx.dll" Type="Document" URL="../Kinesis_VIs/Drivers/Kinesis/VCP Driver/i386/ftd2xx.dll"/>
								<Item Name="ftd2xx.lib" Type="Document" URL="../Kinesis_VIs/Drivers/Kinesis/VCP Driver/i386/ftd2xx.lib"/>
								<Item Name="ftdibus.sys" Type="Document" URL="../Kinesis_VIs/Drivers/Kinesis/VCP Driver/i386/ftdibus.sys"/>
								<Item Name="ftlang.dll" Type="Document" URL="../Kinesis_VIs/Drivers/Kinesis/VCP Driver/i386/ftlang.dll"/>
								<Item Name="ftser2k.sys" Type="Document" URL="../Kinesis_VIs/Drivers/Kinesis/VCP Driver/i386/ftser2k.sys"/>
								<Item Name="ftserui2.dll" Type="Document" URL="../Kinesis_VIs/Drivers/Kinesis/VCP Driver/i386/ftserui2.dll"/>
							</Item>
							<Item Name="Static" Type="Folder">
								<Item Name="amd64" Type="Folder">
									<Item Name="ftd2xx.lib" Type="Document" URL="../Kinesis_VIs/Drivers/Kinesis/VCP Driver/Static/amd64/ftd2xx.lib"/>
								</Item>
								<Item Name="i386" Type="Folder">
									<Item Name="ftd2xx.lib" Type="Document" URL="../Kinesis_VIs/Drivers/Kinesis/VCP Driver/Static/i386/ftd2xx.lib"/>
								</Item>
							</Item>
							<Item Name="ftd2xx.h" Type="Document" URL="../Kinesis_VIs/Drivers/Kinesis/VCP Driver/ftd2xx.h"/>
							<Item Name="Kinesis USB Serial Port.cat" Type="Document" URL="../Kinesis_VIs/Drivers/Kinesis/VCP Driver/Kinesis USB Serial Port.cat"/>
							<Item Name="Kinesis USB Serial Port.inf" Type="Document" URL="../Kinesis_VIs/Drivers/Kinesis/VCP Driver/Kinesis USB Serial Port.inf"/>
						</Item>
					</Item>
				</Item>
				<Item Name="Firmware Update Utility" Type="Folder">
					<Item Name="Firmware" Type="Folder">
						<Item Name="161301_01_01_010011.s" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/161301_01_01_010011.s"/>
						<Item Name="161303_01_01_010011.s" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/161303_01_01_010011.s"/>
						<Item Name="161320_01_01_010014.s" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/161320_01_01_010014.s"/>
						<Item Name="161340_01_01_010017.S" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/161340_01_01_010017.S"/>
						<Item Name="161361_01_01_010004.s" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/161361_01_01_010004.s"/>
						<Item Name="161361_01_02_020003.s" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/161361_01_02_020003.s"/>
						<Item Name="161363_01_01_020003.s" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/161363_01_01_020003.s"/>
						<Item Name="161364_01_02_010001.s" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/161364_01_02_010001.s"/>
						<Item Name="161510_01_02_010003.S" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/161510_01_02_010003.S"/>
						<Item Name="161512_01_01_020007.s" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/161512_01_01_020007.s"/>
						<Item Name="161526_01_01_010007.hex" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/161526_01_01_010007.hex"/>
						<Item Name="161542_01_01_010002.s" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/161542_01_01_010002.s"/>
						<Item Name="161570_01_02_020005.S" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/161570_01_02_020005.S"/>
						<Item Name="161580_01_01_010001.s" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/161580_01_01_010001.s"/>
						<Item Name="161580_01_03_020004.s" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/161580_01_03_020004.s"/>
						<Item Name="161583_01_01_010003.hex" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/161583_01_01_010003.hex"/>
						<Item Name="161597_01_01_010300.s" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/161597_01_01_010300.s"/>
						<Item Name="161604_01_01_010006.s" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/161604_01_01_010006.s"/>
						<Item Name="161625_01_01_010100.hex" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/161625_01_01_010100.hex"/>
						<Item Name="161667_01_02_010003.s" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/161667_01_02_010003.s"/>
						<Item Name="161673_01_02_010003.S" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/161673_01_02_010003.S"/>
						<Item Name="161730_01_02_010300.s" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/161730_01_02_010300.s"/>
						<Item Name="161782_01_02_030004.s" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/161782_01_02_030004.s"/>
						<Item Name="161978_01_02_010103.s" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/161978_01_02_010103.s"/>
						<Item Name="161982_01_02_010002.s" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/161982_01_02_010002.s"/>
						<Item Name="161991_01_02_010004.hex" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/161991_01_02_010004.hex"/>
						<Item Name="162058_01_01_010002.hex" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/162058_01_01_010002.hex"/>
						<Item Name="162121_01_02_010106.s" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/162121_01_02_010106.s"/>
						<Item Name="162189_01_02_010104.s" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/162189_01_02_010104.s"/>
						<Item Name="162215_01_02_030202.S" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/162215_01_02_030202.S"/>
						<Item Name="162219_01_02_030204.S" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/162219_01_02_030204.S"/>
						<Item Name="162275_01_02_020107.S" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/162275_01_02_020107.S"/>
						<Item Name="162285_01_02_020008.hex" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/162285_01_02_020008.hex"/>
						<Item Name="162299_01_02_010004.S" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/162299_01_02_010004.S"/>
						<Item Name="162303_01_01_010003.hex" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/162303_01_01_010003.hex"/>
						<Item Name="162303_01_02_010100.mcs" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/162303_01_02_010100.mcs"/>
						<Item Name="162468_01_02_010007.hex" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/162468_01_02_010007.hex"/>
						<Item Name="162485_01_02_030005.S" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/162485_01_02_030005.S"/>
						<Item Name="162512_01_02_030005.hex" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/162512_01_02_030005.hex"/>
						<Item Name="162514_01_02_030010.hex" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/162514_01_02_030010.hex"/>
						<Item Name="163055_01_02_010007.hex" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/163055_01_02_010007.hex"/>
						<Item Name="163065_01_02_010206.hex" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/163065_01_02_010206.hex"/>
						<Item Name="163065_01_03_020206.hex" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/163065_01_03_020206.hex"/>
						<Item Name="163081_01_02_010017.hex" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/163081_01_02_010017.hex"/>
						<Item Name="163098_01_02_010015.hex" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/163098_01_02_010015.hex"/>
						<Item Name="163102_01_02_010006.hex" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/163102_01_02_010006.hex"/>
						<Item Name="163108_01_02_020002.hex" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/163108_01_02_020002.hex"/>
						<Item Name="166311_01_02_030003.hex" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/166311_01_02_030003.hex"/>
						<Item Name="166315_01_02_010003.hex" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/166315_01_02_010003.hex"/>
						<Item Name="168333_01_01_010004.hex" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/168333_01_01_010004.hex"/>
						<Item Name="168333_01_04_010002.hex" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/168333_01_04_010002.hex"/>
						<Item Name="169519_01_02_030011.S" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/169519_01_02_030011.S"/>
						<Item Name="169527_01_02_030011.S" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/169527_01_02_030011.S"/>
						<Item Name="169528_01_02_020303.S" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/169528_01_02_020303.S"/>
						<Item Name="169557_01_02_010003.hex" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/169557_01_02_010003.hex"/>
						<Item Name="169566_01_02_010001.hex" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/169566_01_02_010001.hex"/>
						<Item Name="169566_01_03_020104.hex" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/169566_01_03_020104.hex"/>
						<Item Name="169754_01_02_010102.hex" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/169754_01_02_010102.hex"/>
						<Item Name="169758_01_02_010115.hex" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/169758_01_02_010115.hex"/>
						<Item Name="169764_01_02_010005.hex" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/169764_01_02_010005.hex"/>
						<Item Name="169795_01_02_010005.hex" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/169795_01_02_010005.hex"/>
						<Item Name="169903_01_02_010007.hex" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/169903_01_02_010007.hex"/>
						<Item Name="169908_01_02_020008.hex" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/169908_01_02_020008.hex"/>
						<Item Name="169943_01_02_020104.hex" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/169943_01_02_020104.hex"/>
						<Item Name="170024_01_02_020101.hex" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/170024_01_02_020101.hex"/>
						<Item Name="170033_01_02_010106.hex" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/170033_01_02_010106.hex"/>
						<Item Name="170061_01_02_010100.hex" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/170061_01_02_010100.hex"/>
						<Item Name="170119_01_02_010004.hex" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/170119_01_02_010004.hex"/>
						<Item Name="170119_01_03_010004.hex" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/170119_01_03_010004.hex"/>
						<Item Name="170144_01_02_010002.hex" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/170144_01_02_010002.hex"/>
						<Item Name="170152_01_02_010001.hex" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/170152_01_02_010001.hex"/>
						<Item Name="170172_01_01_010003.hex" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/170172_01_01_010003.hex"/>
						<Item Name="170232_01_02_010001.hex" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/170232_01_02_010001.hex"/>
						<Item Name="860001_01_02_010001.hex" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/Firmware/860001_01_02_010001.hex"/>
					</Item>
					<Item Name="FirmwareUpdateUtility.chm" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/FirmwareUpdateUtility.chm"/>
					<Item Name="FirmwareUpdateUtility.exe" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/FirmwareUpdateUtility.exe"/>
					<Item Name="ftd2xx.dll" Type="Document" URL="../Kinesis_VIs/Firmware Update Utility/ftd2xx.dll"/>
				</Item>
				<Item Name="Laser Source" Type="Folder">
					<Item Name="Kinesis - KLSnnn - Set Power.vi" Type="VI" URL="../Kinesis_VIs/Laser Source/Kinesis - KLSnnn - Set Power.vi"/>
				</Item>
				<Item Name="Motor" Type="Folder">
					<Item Name="Kinesis - KDC101 - Motor Status Changed (Reg Event Callback)" Type="Folder">
						<Item Name="Kinesis - KDC101 - Motor Status Changed (Callback VI).vi" Type="VI" URL="../Kinesis_VIs/Motor/Kinesis - KDC101 - Motor Status Changed (Reg Event Callback)/Kinesis - KDC101 - Motor Status Changed (Callback VI).vi"/>
						<Item Name="Kinesis - KDC101 - Motor Status Changed.vi" Type="VI" URL="../Kinesis_VIs/Motor/Kinesis - KDC101 - Motor Status Changed (Reg Event Callback)/Kinesis - KDC101 - Motor Status Changed.vi"/>
					</Item>
					<Item Name="Kinesis - BBD202 - Two Axis Scan.vi" Type="VI" URL="../Kinesis_VIs/Motor/Kinesis - BBD202 - Two Axis Scan.vi"/>
					<Item Name="Kinesis - KBD101 - Get Status Bits.vi" Type="VI" URL="../Kinesis_VIs/Motor/Kinesis - KBD101 - Get Status Bits.vi"/>
					<Item Name="Kinesis - KBD101 - Set Trigger Parameters.vi" Type="VI" URL="../Kinesis_VIs/Motor/Kinesis - KBD101 - Set Trigger Parameters.vi"/>
					<Item Name="Kinesis - KBD101 - Set Velocity Parameters.vi" Type="VI" URL="../Kinesis_VIs/Motor/Kinesis - KBD101 - Set Velocity Parameters.vi"/>
					<Item Name="Kinesis - KDC101 - Build Device List.vi" Type="VI" URL="../Kinesis_VIs/Motor/Kinesis - KDC101 - Build Device List.vi"/>
					<Item Name="Kinesis - KDC101 - Connect.vi" Type="VI" URL="../Kinesis_VIs/Motor/Kinesis - KDC101 - Connect.vi"/>
					<Item Name="Kinesis - KDC101 - Get Position.vi" Type="VI" URL="../Kinesis_VIs/Motor/Kinesis - KDC101 - Get Position.vi"/>
					<Item Name="Kinesis - KDC101 - Move Absolute.vi" Type="VI" URL="../Kinesis_VIs/Motor/Kinesis - KDC101 - Move Absolute.vi"/>
					<Item Name="Kinesis - KDC101 - No Front Panel.vi" Type="VI" URL="../Kinesis_VIs/Motor/Kinesis - KDC101 - No Front Panel.vi"/>
					<Item Name="Kinesis - KST101 - Move Relative.vi" Type="VI" URL="../Kinesis_VIs/Motor/Kinesis - KST101 - Move Relative.vi"/>
				</Item>
				<Item Name="Nanotrak" Type="Folder">
					<Item Name="Kinesis - BNT - Connect.vi" Type="VI" URL="../Kinesis_VIs/Nanotrak/Kinesis - BNT - Connect.vi"/>
					<Item Name="Kinesis - BNT - Set Circle Home Position.vi" Type="VI" URL="../Kinesis_VIs/Nanotrak/Kinesis - BNT - Set Circle Home Position.vi"/>
					<Item Name="Kinesis - KNA - Latch Trak.vi" Type="VI" URL="../Kinesis_VIs/Nanotrak/Kinesis - KNA - Latch Trak.vi"/>
					<Item Name="Kinesis - KNA - Set Circle Diameter.vi" Type="VI" URL="../Kinesis_VIs/Nanotrak/Kinesis - KNA - Set Circle Diameter.vi"/>
					<Item Name="Kinesis - KNA - Set Loop Gain.vi" Type="VI" URL="../Kinesis_VIs/Nanotrak/Kinesis - KNA - Set Loop Gain.vi"/>
					<Item Name="Kinesis - KNA - Set Phase Component.vi" Type="VI" URL="../Kinesis_VIs/Nanotrak/Kinesis - KNA - Set Phase Component.vi"/>
				</Item>
				<Item Name="Piezo" Type="Folder">
					<Item Name="Piezo" Type="Folder">
						<Item Name="Kinesis - BPC301 - Connect.vi" Type="VI" URL="../Kinesis_VIs/Piezo/Piezo/Kinesis - BPC301 - Connect.vi"/>
						<Item Name="Kinesis - BPC301 - Waveform LUT.vi" Type="VI" URL="../Kinesis_VIs/Piezo/Piezo/Kinesis - BPC301 - Waveform LUT.vi"/>
						<Item Name="Kinesis - BPC303 - Two Axis Scan.vi" Type="VI" URL="../Kinesis_VIs/Piezo/Piezo/Kinesis - BPC303 - Two Axis Scan.vi"/>
						<Item Name="Kinesis - KPZ101 - Connect.vi" Type="VI" URL="../Kinesis_VIs/Piezo/Piezo/Kinesis - KPZ101 - Connect.vi"/>
						<Item Name="Kinesis - KPZ101 - Waveform LUT.vi" Type="VI" URL="../Kinesis_VIs/Piezo/Piezo/Kinesis - KPZ101 - Waveform LUT.vi"/>
						<Item Name="Kinesis - KPZ101 KSG101 - Set Position.vi" Type="VI" URL="../Kinesis_VIs/Piezo/Piezo/Kinesis - KPZ101 KSG101 - Set Position.vi"/>
						<Item Name="Kinesis - PPC - Continuous Scan.vi" Type="VI" URL="../Kinesis_VIs/Piezo/Piezo/Kinesis - PPC - Continuous Scan.vi"/>
					</Item>
					<Item Name="Piezo Motor" Type="Folder">
						<Item Name="Kinesis - KIM101 - Set Jog.vi" Type="VI" URL="../Kinesis_VIs/Piezo/Piezo Motor/Kinesis - KIM101 - Set Jog.vi"/>
					</Item>
				</Item>
				<Item Name="Rack" Type="Folder">
					<Item Name="Kinesis - MPZ601 - Connect.vi" Type="VI" URL="../Kinesis_VIs/Rack/Kinesis - MPZ601 - Connect.vi"/>
					<Item Name="Kinesis - MPZ601 MNA601 - Two Axis Scan.vi" Type="VI" URL="../Kinesis_VIs/Rack/Kinesis - MPZ601 MNA601 - Two Axis Scan.vi"/>
					<Item Name="Kinesis - MST602 MNA601 - Two Axis Revector.vi" Type="VI" URL="../Kinesis_VIs/Rack/Kinesis - MST602 MNA601 - Two Axis Revector.vi"/>
					<Item Name="Kinesis - MST602 MNA601 - Two Axis Scan.vi" Type="VI" URL="../Kinesis_VIs/Rack/Kinesis - MST602 MNA601 - Two Axis Scan.vi"/>
				</Item>
				<Item Name="Simulator" Type="Folder">
					<Item Name="Kinesis - Simulated Hardware.vi" Type="VI" URL="../Kinesis_VIs/Simulator/Kinesis - Simulated Hardware.vi"/>
				</Item>
				<Item Name="Solenoid" Type="Folder">
					<Item Name="Kinesis - KSC101 - Set Operating Mode.vi" Type="VI" URL="../Kinesis_VIs/Solenoid/Kinesis - KSC101 - Set Operating Mode.vi"/>
				</Item>
				<Item Name="Strain Gauge Reader" Type="Folder">
					<Item Name="Kinesis - KSG101 - Get Max Travel Range.vi" Type="VI" URL="../Kinesis_VIs/Strain Gauge Reader/Kinesis - KSG101 - Get Max Travel Range.vi"/>
					<Item Name="Kinesis - KSG101 - Get Reading.vi" Type="VI" URL="../Kinesis_VIs/Strain Gauge Reader/Kinesis - KSG101 - Get Reading.vi"/>
				</Item>
				<Item Name="BBD_Stages.xml" Type="Document" URL="../Kinesis_VIs/BBD_Stages.xml"/>
				<Item Name="Drop Your DLL Files Here.txt" Type="Document" URL="../Kinesis_VIs/Drop Your DLL Files Here.txt"/>
				<Item Name="ftd2xx.dll" Type="Document" URL="../Kinesis_VIs/ftd2xx.dll"/>
				<Item Name="Kinesis with LabVIEW Examples.aliases" Type="Document" URL="../Kinesis_VIs/Kinesis with LabVIEW Examples.aliases"/>
				<Item Name="Kinesis with LabVIEW Examples.lvlps" Type="Document" URL="../Kinesis_VIs/Kinesis with LabVIEW Examples.lvlps"/>
				<Item Name="Kinesis with LabVIEW Examples.lvproj" Type="Document" URL="../Kinesis_VIs/Kinesis with LabVIEW Examples.lvproj"/>
				<Item Name="ReadMe.txt" Type="Document" URL="../Kinesis_VIs/ReadMe.txt"/>
				<Item Name="Thorlabs.APT.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.APT.dll"/>
				<Item Name="Thorlabs.MotionControl.Benchtop.BrushlessMotor.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.Benchtop.BrushlessMotor.dll"/>
				<Item Name="Thorlabs.MotionControl.Benchtop.BrushlessMotor.h" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.Benchtop.BrushlessMotor.h"/>
				<Item Name="Thorlabs.MotionControl.Benchtop.BrushlessMotor.lib" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.Benchtop.BrushlessMotor.lib"/>
				<Item Name="Thorlabs.MotionControl.Benchtop.BrushlessMotorCLI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.Benchtop.BrushlessMotorCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.Benchtop.BrushlessMotorUI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.Benchtop.BrushlessMotorUI.dll"/>
				<Item Name="Thorlabs.MotionControl.Benchtop.DCServo.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.Benchtop.DCServo.dll"/>
				<Item Name="Thorlabs.MotionControl.Benchtop.DCServo.h" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.Benchtop.DCServo.h"/>
				<Item Name="Thorlabs.MotionControl.Benchtop.DCServo.lib" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.Benchtop.DCServo.lib"/>
				<Item Name="ThorLabs.MotionControl.Benchtop.DCServoCLI.dll" Type="Document" URL="../Kinesis_VIs/ThorLabs.MotionControl.Benchtop.DCServoCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.Benchtop.DCServoUI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.Benchtop.DCServoUI.dll"/>
				<Item Name="Thorlabs.MotionControl.Benchtop.NanoTrak.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.Benchtop.NanoTrak.dll"/>
				<Item Name="Thorlabs.MotionControl.Benchtop.NanoTrak.h" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.Benchtop.NanoTrak.h"/>
				<Item Name="Thorlabs.MotionControl.Benchtop.NanoTrak.lib" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.Benchtop.NanoTrak.lib"/>
				<Item Name="Thorlabs.MotionControl.Benchtop.NanoTrakCLI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.Benchtop.NanoTrakCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.Benchtop.NanoTrakUI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.Benchtop.NanoTrakUI.dll"/>
				<Item Name="Thorlabs.MotionControl.Benchtop.Piezo.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.Benchtop.Piezo.dll"/>
				<Item Name="Thorlabs.MotionControl.Benchtop.Piezo.h" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.Benchtop.Piezo.h"/>
				<Item Name="Thorlabs.MotionControl.Benchtop.Piezo.lib" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.Benchtop.Piezo.lib"/>
				<Item Name="Thorlabs.MotionControl.Benchtop.PiezoCLI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.Benchtop.PiezoCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.Benchtop.PiezoUI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.Benchtop.PiezoUI.dll"/>
				<Item Name="Thorlabs.MotionControl.Benchtop.PrecisionPiezo.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.Benchtop.PrecisionPiezo.dll"/>
				<Item Name="Thorlabs.MotionControl.Benchtop.PrecisionPiezo.h" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.Benchtop.PrecisionPiezo.h"/>
				<Item Name="Thorlabs.MotionControl.Benchtop.PrecisionPiezo.lib" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.Benchtop.PrecisionPiezo.lib"/>
				<Item Name="ThorLabs.MotionControl.Benchtop.PrecisionPiezoCLI.dll" Type="Document" URL="../Kinesis_VIs/ThorLabs.MotionControl.Benchtop.PrecisionPiezoCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.Benchtop.PrecisionPiezoUI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.Benchtop.PrecisionPiezoUI.dll"/>
				<Item Name="Thorlabs.MotionControl.Benchtop.StepperMotor.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.Benchtop.StepperMotor.dll"/>
				<Item Name="Thorlabs.MotionControl.Benchtop.StepperMotor.h" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.Benchtop.StepperMotor.h"/>
				<Item Name="Thorlabs.MotionControl.Benchtop.StepperMotor.lib" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.Benchtop.StepperMotor.lib"/>
				<Item Name="Thorlabs.MotionControl.Benchtop.StepperMotorCLI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.Benchtop.StepperMotorCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.Benchtop.StepperMotorUI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.Benchtop.StepperMotorUI.dll"/>
				<Item Name="Thorlabs.MotionControl.C_API.chm" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.C_API.chm"/>
				<Item Name="Thorlabs.MotionControl.Controls.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.Controls.dll"/>
				<Item Name="Thorlabs.MotionControl.DataLogger.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.DataLogger.dll"/>
				<Item Name="Thorlabs.MotionControl.DeviceManager.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.DeviceManager.dll"/>
				<Item Name="Thorlabs.MotionControl.DeviceManagerCLI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.DeviceManagerCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.DeviceManagerUI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.DeviceManagerUI.dll"/>
				<Item Name="Thorlabs.MotionControl.DotNet_API.chm" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.DotNet_API.chm"/>
				<Item Name="Thorlabs.MotionControl.FilterFlipper.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.FilterFlipper.dll"/>
				<Item Name="ThorLabs.MotionControl.FilterFlipper.h" Type="Document" URL="../Kinesis_VIs/ThorLabs.MotionControl.FilterFlipper.h"/>
				<Item Name="Thorlabs.MotionControl.FilterFlipper.lib" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.FilterFlipper.lib"/>
				<Item Name="Thorlabs.MotionControl.FilterFlipperCLI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.FilterFlipperCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.FilterFlipperUI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.FilterFlipperUI.dll"/>
				<Item Name="Thorlabs.MotionControl.FTD2xx_Net.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.FTD2xx_Net.dll"/>
				<Item Name="Thorlabs.MotionControl.GenericMotorCLI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.GenericMotorCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.GenericMotorUI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.GenericMotorUI.dll"/>
				<Item Name="Thorlabs.MotionControl.GenericNanoTrakCLI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.GenericNanoTrakCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.GenericNanoTrakUI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.GenericNanoTrakUI.dll"/>
				<Item Name="Thorlabs.MotionControl.GenericPiezoCLI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.GenericPiezoCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.GenericPiezoUI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.GenericPiezoUI.dll"/>
				<Item Name="Thorlabs.MotionControl.IntegratedPrecisionPiezo.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.IntegratedPrecisionPiezo.dll"/>
				<Item Name="Thorlabs.MotionControl.IntegratedPrecisionPiezo.h" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.IntegratedPrecisionPiezo.h"/>
				<Item Name="Thorlabs.MotionControl.IntegratedPrecisionPiezo.lib" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.IntegratedPrecisionPiezo.lib"/>
				<Item Name="Thorlabs.MotionControl.IntegratedPrecisionPiezoCLI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.IntegratedPrecisionPiezoCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.IntegratedPrecisionPiezoUI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.IntegratedPrecisionPiezoUI.dll"/>
				<Item Name="Thorlabs.MotionControl.IntegratedStepperMotors.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.IntegratedStepperMotors.dll"/>
				<Item Name="Thorlabs.MotionControl.IntegratedStepperMotors.h" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.IntegratedStepperMotors.h"/>
				<Item Name="Thorlabs.MotionControl.IntegratedStepperMotors.lib" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.IntegratedStepperMotors.lib"/>
				<Item Name="Thorlabs.MotionControl.IntegratedStepperMotorsCLI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.IntegratedStepperMotorsCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.IntegratedStepperMotorsUI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.IntegratedStepperMotorsUI.dll"/>
				<Item Name="Thorlabs.MotionControl.Joystick.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.Joystick.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.BrushlessMotor.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.BrushlessMotor.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.BrushlessMotor.h" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.BrushlessMotor.h"/>
				<Item Name="Thorlabs.MotionControl.KCube.BrushlessMotor.lib" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.BrushlessMotor.lib"/>
				<Item Name="Thorlabs.MotionControl.KCube.BrushlessMotorCLI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.BrushlessMotorCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.BrushlessMotorUI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.BrushlessMotorUI.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.DCServo.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.DCServo.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.DCServo.h" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.DCServo.h"/>
				<Item Name="Thorlabs.MotionControl.KCube.DCServo.lib" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.DCServo.lib"/>
				<Item Name="ThorLabs.MotionControl.KCube.DCServoCLI.dll" Type="Document" URL="../Kinesis_VIs/ThorLabs.MotionControl.KCube.DCServoCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.DCServoUI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.DCServoUI.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.InertialMotor.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.InertialMotor.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.InertialMotor.h" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.InertialMotor.h"/>
				<Item Name="Thorlabs.MotionControl.KCube.InertialMotor.lib" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.InertialMotor.lib"/>
				<Item Name="Thorlabs.MotionControl.KCube.InertialMotorCLI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.InertialMotorCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.InertialMotorUI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.InertialMotorUI.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.LaserDiode.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.LaserDiode.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.LaserDiode.h" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.LaserDiode.h"/>
				<Item Name="Thorlabs.MotionControl.KCube.LaserDiode.lib" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.LaserDiode.lib"/>
				<Item Name="ThorLabs.MotionControl.KCube.LaserDiodeCLI.dll" Type="Document" URL="../Kinesis_VIs/ThorLabs.MotionControl.KCube.LaserDiodeCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.LaserDiodeUI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.LaserDiodeUI.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.LaserSource.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.LaserSource.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.LaserSource.h" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.LaserSource.h"/>
				<Item Name="Thorlabs.MotionControl.KCube.LaserSource.lib" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.LaserSource.lib"/>
				<Item Name="ThorLabs.MotionControl.KCube.LaserSourceCLI.dll" Type="Document" URL="../Kinesis_VIs/ThorLabs.MotionControl.KCube.LaserSourceCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.LaserSourceUI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.LaserSourceUI.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.LiquidCrystal.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.LiquidCrystal.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.LiquidCrystal.h" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.LiquidCrystal.h"/>
				<Item Name="Thorlabs.MotionControl.KCube.LiquidCrystal.lib" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.LiquidCrystal.lib"/>
				<Item Name="Thorlabs.MotionControl.KCube.LiquidCrystalCLI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.LiquidCrystalCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.LiquidCrystalUI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.LiquidCrystalUI.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.NanoTrak.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.NanoTrak.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.NanoTrak.h" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.NanoTrak.h"/>
				<Item Name="Thorlabs.MotionControl.KCube.NanoTrak.lib" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.NanoTrak.lib"/>
				<Item Name="Thorlabs.MotionControl.KCube.NanoTrakCLI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.NanoTrakCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.NanoTrakUI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.NanoTrakUI.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.Piezo.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.Piezo.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.Piezo.h" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.Piezo.h"/>
				<Item Name="Thorlabs.MotionControl.KCube.Piezo.lib" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.Piezo.lib"/>
				<Item Name="Thorlabs.MotionControl.KCube.PiezoCLI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.PiezoCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.PiezoUI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.PiezoUI.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.PositionAligner.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.PositionAligner.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.PositionAligner.h" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.PositionAligner.h"/>
				<Item Name="Thorlabs.MotionControl.KCube.PositionAligner.lib" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.PositionAligner.lib"/>
				<Item Name="ThorLabs.MotionControl.KCube.PositionAlignerCLI.dll" Type="Document" URL="../Kinesis_VIs/ThorLabs.MotionControl.KCube.PositionAlignerCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.PositionAlignerUI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.PositionAlignerUI.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.Solenoid.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.Solenoid.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.Solenoid.h" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.Solenoid.h"/>
				<Item Name="Thorlabs.MotionControl.KCube.Solenoid.lib" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.Solenoid.lib"/>
				<Item Name="Thorlabs.MotionControl.KCube.SolenoidCLI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.SolenoidCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.SolenoidUI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.SolenoidUI.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.StepperMotor.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.StepperMotor.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.StepperMotor.h" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.StepperMotor.h"/>
				<Item Name="Thorlabs.MotionControl.KCube.StepperMotor.lib" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.StepperMotor.lib"/>
				<Item Name="Thorlabs.MotionControl.KCube.StepperMotorCLI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.StepperMotorCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.StepperMotorUI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.StepperMotorUI.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.StrainGauge.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.StrainGauge.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.StrainGauge.h" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.StrainGauge.h"/>
				<Item Name="Thorlabs.MotionControl.KCube.StrainGauge.lib" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.StrainGauge.lib"/>
				<Item Name="ThorLabs.MotionControl.KCube.StrainGaugeCLI.dll" Type="Document" URL="../Kinesis_VIs/ThorLabs.MotionControl.KCube.StrainGaugeCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.StrainGaugeUI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KCube.StrainGaugeUI.dll"/>
				<Item Name="Thorlabs.MotionControl.Kinesis.DLLutility.exe" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.Kinesis.DLLutility.exe"/>
				<Item Name="Thorlabs.MotionControl.Kinesis.exe" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.Kinesis.exe"/>
				<Item Name="Thorlabs.MotionControl.Kinesis.exe.config" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.Kinesis.exe.config"/>
				<Item Name="Thorlabs.MotionControl.Kinesis.TestClient.exe" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.Kinesis.TestClient.exe"/>
				<Item Name="Thorlabs.MotionControl.KinesisHelp.chm" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KinesisHelp.chm"/>
				<Item Name="Thorlabs.MotionControl.KinesisSimulator.chm" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KinesisSimulator.chm"/>
				<Item Name="Thorlabs.MotionControl.KinesisSimulator.exe" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.KinesisSimulator.exe"/>
				<Item Name="Thorlabs.MotionControl.ModularRack.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.ModularRack.dll"/>
				<Item Name="ThorLabs.MotionControl.ModularRack.h" Type="Document" URL="../Kinesis_VIs/ThorLabs.MotionControl.ModularRack.h"/>
				<Item Name="Thorlabs.MotionControl.ModularRack.lib" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.ModularRack.lib"/>
				<Item Name="Thorlabs.MotionControl.ModularRack.NanoTrak.h" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.ModularRack.NanoTrak.h"/>
				<Item Name="Thorlabs.MotionControl.ModularRack.Piezo.h" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.ModularRack.Piezo.h"/>
				<Item Name="Thorlabs.MotionControl.ModularRack.StepperMotor.h" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.ModularRack.StepperMotor.h"/>
				<Item Name="Thorlabs.MotionControl.ModularRackCLI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.ModularRackCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.ModularRackUI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.ModularRackUI.dll"/>
				<Item Name="Thorlabs.MotionControl.Polarizer.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.Polarizer.dll"/>
				<Item Name="Thorlabs.MotionControl.Polarizer.h" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.Polarizer.h"/>
				<Item Name="Thorlabs.MotionControl.Polarizer.lib" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.Polarizer.lib"/>
				<Item Name="ThorLabs.MotionControl.PolarizerCLI.dll" Type="Document" URL="../Kinesis_VIs/ThorLabs.MotionControl.PolarizerCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.PolarizerUI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.PolarizerUI.dll"/>
				<Item Name="Thorlabs.MotionControl.PrivateInternal.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.PrivateInternal.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.BrushlessMotor.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.BrushlessMotor.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.BrushlessMotor.h" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.BrushlessMotor.h"/>
				<Item Name="Thorlabs.MotionControl.TCube.BrushlessMotor.lib" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.BrushlessMotor.lib"/>
				<Item Name="Thorlabs.MotionControl.TCube.BrushlessMotorCLI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.BrushlessMotorCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.BrushlessMotorUI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.BrushlessMotorUI.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.DCServo.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.DCServo.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.DCServo.h" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.DCServo.h"/>
				<Item Name="Thorlabs.MotionControl.TCube.DCServo.lib" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.DCServo.lib"/>
				<Item Name="Thorlabs.MotionControl.TCube.DCServoCLI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.DCServoCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.DCServoUI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.DCServoUI.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.InertialMotor.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.InertialMotor.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.InertialMotor.h" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.InertialMotor.h"/>
				<Item Name="Thorlabs.MotionControl.TCube.InertialMotor.lib" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.InertialMotor.lib"/>
				<Item Name="ThorLabs.MotionControl.TCube.InertialMotorCLI.dll" Type="Document" URL="../Kinesis_VIs/ThorLabs.MotionControl.TCube.InertialMotorCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.InertialMotorUI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.InertialMotorUI.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.LaserDiode.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.LaserDiode.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.LaserDiode.h" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.LaserDiode.h"/>
				<Item Name="Thorlabs.MotionControl.TCube.LaserDiode.lib" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.LaserDiode.lib"/>
				<Item Name="Thorlabs.MotionControl.TCube.LaserDiodeCLI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.LaserDiodeCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.LaserDiodeUI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.LaserDiodeUI.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.LaserSource.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.LaserSource.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.LaserSource.h" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.LaserSource.h"/>
				<Item Name="Thorlabs.MotionControl.TCube.LaserSource.lib" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.LaserSource.lib"/>
				<Item Name="Thorlabs.MotionControl.TCube.LaserSourceCLI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.LaserSourceCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.LaserSourceUI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.LaserSourceUI.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.NanoTrak.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.NanoTrak.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.NanoTrak.h" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.NanoTrak.h"/>
				<Item Name="Thorlabs.MotionControl.TCube.NanoTrak.lib" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.NanoTrak.lib"/>
				<Item Name="Thorlabs.MotionControl.TCube.NanoTrakCLI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.NanoTrakCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.NanoTrakUI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.NanoTrakUI.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.Piezo.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.Piezo.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.Piezo.h" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.Piezo.h"/>
				<Item Name="Thorlabs.MotionControl.TCube.Piezo.lib" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.Piezo.lib"/>
				<Item Name="Thorlabs.MotionControl.TCube.PiezoCLI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.PiezoCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.PiezoUI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.PiezoUI.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.Quad.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.Quad.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.Quad.h" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.Quad.h"/>
				<Item Name="Thorlabs.MotionControl.TCube.Quad.lib" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.Quad.lib"/>
				<Item Name="Thorlabs.MotionControl.TCube.QuadCLI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.QuadCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.QuadUI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.QuadUI.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.Solenoid.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.Solenoid.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.Solenoid.h" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.Solenoid.h"/>
				<Item Name="Thorlabs.MotionControl.TCube.Solenoid.lib" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.Solenoid.lib"/>
				<Item Name="Thorlabs.MotionControl.TCube.SolenoidCLI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.SolenoidCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.SolenoidUI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.SolenoidUI.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.StepperMotor.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.StepperMotor.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.StepperMotor.h" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.StepperMotor.h"/>
				<Item Name="Thorlabs.MotionControl.TCube.StepperMotor.lib" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.StepperMotor.lib"/>
				<Item Name="Thorlabs.MotionControl.TCube.StepperMotorCLI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.StepperMotorCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.StepperMotorUI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.StepperMotorUI.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.StrainGauge.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.StrainGauge.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.StrainGauge.h" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.StrainGauge.h"/>
				<Item Name="Thorlabs.MotionControl.TCube.StrainGauge.lib" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.StrainGauge.lib"/>
				<Item Name="Thorlabs.MotionControl.TCube.StrainGaugeCLI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.StrainGaugeCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.StrainGaugeUI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.StrainGaugeUI.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.TEC.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.TEC.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.TEC.h" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.TEC.h"/>
				<Item Name="Thorlabs.MotionControl.TCube.TEC.lib" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.TEC.lib"/>
				<Item Name="Thorlabs.MotionControl.TCube.TECCLI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.TECCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.TECUI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TCube.TECUI.dll"/>
				<Item Name="Thorlabs.MotionControl.TDIEngine.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TDIEngine.dll"/>
				<Item Name="Thorlabs.MotionControl.TDIEngine.h" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TDIEngine.h"/>
				<Item Name="Thorlabs.MotionControl.TDIEngine.lib" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TDIEngine.lib"/>
				<Item Name="ThorLabs.MotionControl.TDIEngineCLI.dll" Type="Document" URL="../Kinesis_VIs/ThorLabs.MotionControl.TDIEngineCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.TDIEngineUI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.TDIEngineUI.dll"/>
				<Item Name="Thorlabs.MotionControl.Tools.Common.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.Tools.Common.dll"/>
				<Item Name="Thorlabs.MotionControl.Tools.Logging.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.Tools.Logging.dll"/>
				<Item Name="Thorlabs.MotionControl.Tools.WPF.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.Tools.WPF.dll"/>
				<Item Name="Thorlabs.MotionControl.Tools.WPF.UI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.Tools.WPF.UI.dll"/>
				<Item Name="Thorlabs.MotionControl.VerticalStage.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.VerticalStage.dll"/>
				<Item Name="Thorlabs.MotionControl.VerticalStage.h" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.VerticalStage.h"/>
				<Item Name="Thorlabs.MotionControl.VerticalStage.lib" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.VerticalStage.lib"/>
				<Item Name="ThorLabs.MotionControl.VerticalStageCLI.dll" Type="Document" URL="../Kinesis_VIs/ThorLabs.MotionControl.VerticalStageCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.VerticalStageUI.dll" Type="Document" URL="../Kinesis_VIs/Thorlabs.MotionControl.VerticalStageUI.dll"/>
				<Item Name="ThorlabsDefaultSettings.xml" Type="Document" URL="../Kinesis_VIs/ThorlabsDefaultSettings.xml"/>
				<Item Name="Xceed.Wpf.Toolkit.dll" Type="Document" URL="../Kinesis_VIs/Xceed.Wpf.Toolkit.dll"/>
			</Item>
			<Item Name="PMT_VIs" Type="Folder">
				<Item Name="Close.vi" Type="VI" URL="../PMT_VIs/Close.vi"/>
				<Item Name="Count Start.vi" Type="VI" URL="../PMT_VIs/Count Start.vi"/>
				<Item Name="Count Stop.vi" Type="VI" URL="../PMT_VIs/Count Stop.vi"/>
				<Item Name="H11890api.dll" Type="Document" URL="../PMT_VIs/H11890api.dll"/>
				<Item Name="H11890api.h" Type="Document" URL="../PMT_VIs/H11890api.h"/>
				<Item Name="H11890api.lib" Type="Document" URL="../PMT_VIs/H11890api.lib"/>
				<Item Name="H11890api.lvlib" Type="Library" URL="../PMT_VIs/H11890api.lvlib"/>
				<Item Name="Logo.ctl" Type="VI" URL="../PMT_VIs/Logo.ctl"/>
				<Item Name="Open.vi" Type="VI" URL="../PMT_VIs/Open.vi"/>
				<Item Name="Read Data.vi" Type="VI" URL="../PMT_VIs/Read Data.vi"/>
				<Item Name="Read HV.vi" Type="VI" URL="../PMT_VIs/Read HV.vi"/>
				<Item Name="Read IT.vi" Type="VI" URL="../PMT_VIs/Read IT.vi"/>
				<Item Name="Read RN.vi" Type="VI" URL="../PMT_VIs/Read RN.vi"/>
				<Item Name="Set HV.vi" Type="VI" URL="../PMT_VIs/Set HV.vi"/>
				<Item Name="Set IT.vi" Type="VI" URL="../PMT_VIs/Set IT.vi"/>
				<Item Name="Set RN.vi" Type="VI" URL="../PMT_VIs/Set RN.vi"/>
				<Item Name="SM_CaseErase.vi" Type="VI" URL="../PMT_VIs/SM_CaseErase.vi"/>
				<Item Name="SM_CaseSelect.vi" Type="VI" URL="../PMT_VIs/SM_CaseSelect.vi"/>
				<Item Name="SM_Template.vi" Type="VI" URL="../PMT_VIs/SM_Template.vi"/>
			</Item>
			<Item Name="PMT_plus_Kinesis_plus_Keithley.vi" Type="VI" URL="../PMT_plus_Kinesis_plus_Keithley.vi"/>
			<Item Name="PMT_project.aliases" Type="Document" URL="../PMT_project.aliases"/>
			<Item Name="PMT_project.lvlps" Type="Document" URL="../PMT_project.lvlps"/>
			<Item Name="SHG_polarization_resolved.vi" Type="VI" URL="../SHG_polarization_resolved.vi"/>
		</Item>
		<Item Name="Dependencies" Type="Dependencies">
			<Item Name="vi.lib" Type="Folder">
				<Item Name="Autoscale Polar as Needed.vi" Type="VI" URL="/&lt;vilib&gt;/picture/polarplt.llb/Autoscale Polar as Needed.vi"/>
				<Item Name="BuildHelpPath.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/BuildHelpPath.vi"/>
				<Item Name="Calc Increment.vi" Type="VI" URL="/&lt;vilib&gt;/picture/scale.llb/Calc Increment.vi"/>
				<Item Name="Calc Scale Specs.vi" Type="VI" URL="/&lt;vilib&gt;/picture/scale.llb/Calc Scale Specs.vi"/>
				<Item Name="Check Special Tags.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Check Special Tags.vi"/>
				<Item Name="Clear Errors.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Clear Errors.vi"/>
				<Item Name="Color to RGB.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/colorconv.llb/Color to RGB.vi"/>
				<Item Name="Convert property node font to graphics font.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Convert property node font to graphics font.vi"/>
				<Item Name="Details Display Dialog.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Details Display Dialog.vi"/>
				<Item Name="DialogType.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/DialogType.ctl"/>
				<Item Name="DialogTypeEnum.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/DialogTypeEnum.ctl"/>
				<Item Name="Draw Arc.vi" Type="VI" URL="/&lt;vilib&gt;/picture/picture.llb/Draw Arc.vi"/>
				<Item Name="Draw Circle by Radius.vi" Type="VI" URL="/&lt;vilib&gt;/picture/pictutil.llb/Draw Circle by Radius.vi"/>
				<Item Name="Draw Line.vi" Type="VI" URL="/&lt;vilib&gt;/picture/picture.llb/Draw Line.vi"/>
				<Item Name="Draw Multiple Lines.vi" Type="VI" URL="/&lt;vilib&gt;/picture/picture.llb/Draw Multiple Lines.vi"/>
				<Item Name="Draw Point.vi" Type="VI" URL="/&lt;vilib&gt;/picture/picture.llb/Draw Point.vi"/>
				<Item Name="Draw Polar Grids.vi" Type="VI" URL="/&lt;vilib&gt;/picture/polarplt.llb/Draw Polar Grids.vi"/>
				<Item Name="Draw Scale.vi" Type="VI" URL="/&lt;vilib&gt;/picture/scale.llb/Draw Scale.vi"/>
				<Item Name="Draw Text at Point.vi" Type="VI" URL="/&lt;vilib&gt;/picture/picture.llb/Draw Text at Point.vi"/>
				<Item Name="Draw Text in Rect.vi" Type="VI" URL="/&lt;vilib&gt;/picture/picture.llb/Draw Text in Rect.vi"/>
				<Item Name="Error Cluster From Error Code.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Error Cluster From Error Code.vi"/>
				<Item Name="Error Code Database.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Error Code Database.vi"/>
				<Item Name="ErrWarn.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/ErrWarn.ctl"/>
				<Item Name="eventvkey.ctl" Type="VI" URL="/&lt;vilib&gt;/event_ctls.llb/eventvkey.ctl"/>
				<Item Name="Find Tag.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Find Tag.vi"/>
				<Item Name="Format Message String.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Format Message String.vi"/>
				<Item Name="General Error Handler Core CORE.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/General Error Handler Core CORE.vi"/>
				<Item Name="General Error Handler.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/General Error Handler.vi"/>
				<Item Name="Get Ready.vi" Type="VI" URL="/&lt;vilib&gt;/picture/polarplt.llb/Get Ready.vi"/>
				<Item Name="Get String Text Bounds.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Get String Text Bounds.vi"/>
				<Item Name="Get Text Rect.vi" Type="VI" URL="/&lt;vilib&gt;/picture/picture.llb/Get Text Rect.vi"/>
				<Item Name="GetHelpDir.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/GetHelpDir.vi"/>
				<Item Name="GetRTHostConnectedProp.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/GetRTHostConnectedProp.vi"/>
				<Item Name="Hilite Color.vi" Type="VI" URL="/&lt;vilib&gt;/picture/pictutil.llb/Hilite Color.vi"/>
				<Item Name="Increment Filter.vi" Type="VI" URL="/&lt;vilib&gt;/picture/scale.llb/Increment Filter.vi"/>
				<Item Name="Longest Line Length in Pixels.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Longest Line Length in Pixels.vi"/>
				<Item Name="LVBoundsTypeDef.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/miscctls.llb/LVBoundsTypeDef.ctl"/>
				<Item Name="LVRectTypeDef.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/miscctls.llb/LVRectTypeDef.ctl"/>
				<Item Name="Map Setup.vi" Type="VI" URL="/&lt;vilib&gt;/picture/scale.llb/Map Setup.vi"/>
				<Item Name="Map Value to Pixel.vi" Type="VI" URL="/&lt;vilib&gt;/picture/scale.llb/Map Value to Pixel.vi"/>
				<Item Name="Move Pen.vi" Type="VI" URL="/&lt;vilib&gt;/picture/picture.llb/Move Pen.vi"/>
				<Item Name="NI_AALBase.lvlib" Type="Library" URL="/&lt;vilib&gt;/Analysis/NI_AALBase.lvlib"/>
				<Item Name="NI_MABase.lvlib" Type="Library" URL="/&lt;vilib&gt;/measure/NI_MABase.lvlib"/>
				<Item Name="Not Found Dialog.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Not Found Dialog.vi"/>
				<Item Name="Num To Text.vi" Type="VI" URL="/&lt;vilib&gt;/picture/scale.llb/Num To Text.vi"/>
				<Item Name="PCT Pad String.vi" Type="VI" URL="/&lt;vilib&gt;/picture/picture.llb/PCT Pad String.vi"/>
				<Item Name="PG angle labels.vi" Type="VI" URL="/&lt;vilib&gt;/picture/polarplt.llb/PG angle labels.vi"/>
				<Item Name="PG angle lines.vi" Type="VI" URL="/&lt;vilib&gt;/picture/polarplt.llb/PG angle lines.vi"/>
				<Item Name="PG circles.vi" Type="VI" URL="/&lt;vilib&gt;/picture/polarplt.llb/PG circles.vi"/>
				<Item Name="PG scale.vi" Type="VI" URL="/&lt;vilib&gt;/picture/polarplt.llb/PG scale.vi"/>
				<Item Name="Plot Polar Data.vi" Type="VI" URL="/&lt;vilib&gt;/picture/polarplt.llb/Plot Polar Data.vi"/>
				<Item Name="Polar Plot with Point Options.vi" Type="VI" URL="/&lt;vilib&gt;/picture/polarplt.llb/Polar Plot with Point Options.vi"/>
				<Item Name="Search and Replace Pattern.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Search and Replace Pattern.vi"/>
				<Item Name="Set Bold Text.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Set Bold Text.vi"/>
				<Item Name="Set Pen State.vi" Type="VI" URL="/&lt;vilib&gt;/picture/picture.llb/Set Pen State.vi"/>
				<Item Name="Set String Value.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Set String Value.vi"/>
				<Item Name="Simple Error Handler.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Simple Error Handler.vi"/>
				<Item Name="Space Constant.vi" Type="VI" URL="/&lt;vilib&gt;/dlg_ctls.llb/Space Constant.vi"/>
				<Item Name="TagReturnType.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/TagReturnType.ctl"/>
				<Item Name="Three Button Dialog CORE.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Three Button Dialog CORE.vi"/>
				<Item Name="Three Button Dialog.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Three Button Dialog.vi"/>
				<Item Name="Trim Whitespace One-Sided.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Trim Whitespace One-Sided.vi"/>
				<Item Name="Trim Whitespace.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Trim Whitespace.vi"/>
				<Item Name="Validate Rectangle.vi" Type="VI" URL="/&lt;vilib&gt;/picture/scale.llb/Validate Rectangle.vi"/>
				<Item Name="whitespace.ctl" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/whitespace.ctl"/>
				<Item Name="Write Delimited Spreadsheet (DBL).vi" Type="VI" URL="/&lt;vilib&gt;/Utility/file.llb/Write Delimited Spreadsheet (DBL).vi"/>
				<Item Name="Write Delimited Spreadsheet (I64).vi" Type="VI" URL="/&lt;vilib&gt;/Utility/file.llb/Write Delimited Spreadsheet (I64).vi"/>
				<Item Name="Write Delimited Spreadsheet (string).vi" Type="VI" URL="/&lt;vilib&gt;/Utility/file.llb/Write Delimited Spreadsheet (string).vi"/>
				<Item Name="Write Delimited Spreadsheet.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/file.llb/Write Delimited Spreadsheet.vi"/>
				<Item Name="Write Spreadsheet String.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/file.llb/Write Spreadsheet String.vi"/>
			</Item>
			<Item Name="???.rtm" Type="Document" URL="../???.rtm"/>
			<Item Name="Close.vi" Type="VI" URL="../Kiethley24XX_VIs/Initialize Folder/D/Download/Keithley 24XX/Public/Close.vi"/>
			<Item Name="ClosePMT.vi" Type="VI" URL="../PMT_VIs/ClosePMT.vi"/>
			<Item Name="Configure Measurement.vi" Type="VI" URL="../Kiethley24XX_VIs/Initialize Folder/D/Download/Keithley 24XX/Public/Configure/Configure Measurement.vi"/>
			<Item Name="Configure Multipoint.vi" Type="VI" URL="../Kiethley24XX_VIs/Initialize Folder/D/Download/Keithley 24XX/Public/Configure/Low Level/Configure Multipoint.vi"/>
			<Item Name="Configure Output.vi" Type="VI" URL="../Kiethley24XX_VIs/Initialize Folder/D/Download/Keithley 24XX/Public/Configure/Configure Output.vi"/>
			<Item Name="Configure Trigger.vi" Type="VI" URL="../Kiethley24XX_VIs/Initialize Folder/D/Download/Keithley 24XX/Public/Configure/Low Level/Configure Trigger.vi"/>
			<Item Name="Enable Output.vi" Type="VI" URL="../Kiethley24XX_VIs/Initialize Folder/D/Download/Keithley 24XX/Public/Action-Status/Enable Output.vi"/>
			<Item Name="Error Query.vi" Type="VI" URL="../Kiethley24XX_VIs/Initialize Folder/D/Download/Keithley 24XX/Public/Utility/Error Query.vi"/>
			<Item Name="Fetch (Measurements).vi" Type="VI" URL="../Kiethley24XX_VIs/Initialize Folder/D/Download/Keithley 24XX/Public/Data/Low Level/Fetch (Measurements).vi"/>
			<Item Name="Initialize.vi" Type="VI" URL="../Kiethley24XX_VIs/Initialize Folder/D/Download/Keithley 24XX/Public/Initialize.vi"/>
			<Item Name="Initiate.vi" Type="VI" URL="../Kiethley24XX_VIs/Initialize Folder/D/Download/Keithley 24XX/Public/Data/Low Level/Initiate.vi"/>
			<Item Name="lvanlys.dll" Type="Document" URL="/&lt;resource&gt;/lvanlys.dll"/>
			<Item Name="mscorlib" Type="VI" URL="mscorlib">
				<Property Name="NI.PreserveRelativePath" Type="Bool">true</Property>
			</Item>
			<Item Name="Read (Multiple Points).vi" Type="VI" URL="../Kiethley24XX_VIs/Initialize Folder/D/Download/Keithley 24XX/Public/Data/Read (Multiple Points).vi"/>
			<Item Name="Thorlabs.MotionControl.Benchtop.BrushlessMotorCLI" Type="Document" URL="Thorlabs.MotionControl.Benchtop.BrushlessMotorCLI">
				<Property Name="NI.PreserveRelativePath" Type="Bool">true</Property>
			</Item>
			<Item Name="Thorlabs.MotionControl.Benchtop.BrushlessMotorCLI.dll" Type="Document" URL="/U/Kinesis LabVIEW Website Examples/Thorlabs.MotionControl.Benchtop.BrushlessMotorCLI.dll"/>
			<Item Name="Thorlabs.MotionControl.Benchtop.NanoTrakCLI.dll" Type="Document" URL="/U/Kinesis LabVIEW Website Examples/Thorlabs.MotionControl.Benchtop.NanoTrakCLI.dll"/>
			<Item Name="Thorlabs.MotionControl.Benchtop.PiezoCLI.dll" Type="Document" URL="/U/Software Training Plan/Software Training Day 2 - Thursday/Kinesis_with_LabVIEW_Examples_LV12 - v2/Thorlabs.MotionControl.Benchtop.PiezoCLI.dll"/>
			<Item Name="Thorlabs.MotionControl.Benchtop.StepperMotorCLI.dll" Type="Document" URL="../../../../../kmuraszko/Documents/Thorlabs/Motor VI/Kinesis LabVIEW/Working KPA101 Code!/Thorlabs.MotionControl.Benchtop.StepperMotorCLI.dll"/>
			<Item Name="Thorlabs.MotionControl.Benchtop.StepperMotorCLI.dll" Type="Document" URL="../../../../../nbayconich/Documents/Kinesis APT motion control programming/Kinesis labview project Nick test/Thorlabs.MotionControl.Benchtop.StepperMotorCLI.dll"/>
			<Item Name="Thorlabs.MotionControl.Controls" Type="Document" URL="Thorlabs.MotionControl.Controls">
				<Property Name="NI.PreserveRelativePath" Type="Bool">true</Property>
			</Item>
			<Item Name="Thorlabs.MotionControl.Controls.dll" Type="Document" URL="../../../../../kmuraszko/Documents/Thorlabs/Motor VI/Kinesis LabVIEW/Working KPA101 Code!/Thorlabs.MotionControl.Controls.dll"/>
			<Item Name="Thorlabs.MotionControl.Controls.dll" Type="Document" URL="../../../../../nbayconich/Documents/Kinesis APT motion control programming/Kinesis labview project Nick test/Thorlabs.MotionControl.Controls.dll"/>
			<Item Name="Thorlabs.MotionControl.Controls.dll" Type="Document" URL="/U/Kinesis LabVIEW Website Examples/Thorlabs.MotionControl.Controls.dll"/>
			<Item Name="Thorlabs.MotionControl.Controls.dll" Type="Document" URL="/U/Software Training Plan/Software Training Day 2 - Thursday/Kinesis_with_LabVIEW_Examples_LV12 - v2/Thorlabs.MotionControl.Controls.dll"/>
			<Item Name="Thorlabs.MotionControl.DeviceManagerCLI.dll" Type="Document" URL="/U/Kinesis LabVIEW Website Examples/Thorlabs.MotionControl.DeviceManagerCLI.dll"/>
			<Item Name="Thorlabs.MotionControl.GenericMotorCLI.dll" Type="Document" URL="../../../../../kmuraszko/Documents/Thorlabs/Motor VI/Kinesis LabVIEW/Working KPA101 Code!/Thorlabs.MotionControl.GenericMotorCLI.dll"/>
			<Item Name="Thorlabs.MotionControl.GenericMotorCLI.dll" Type="Document" URL="../../../../../nbayconich/Documents/Kinesis APT motion control programming/Kinesis labview project Nick test/Thorlabs.MotionControl.GenericMotorCLI.dll"/>
			<Item Name="Thorlabs.MotionControl.GenericMotorCLI.dll" Type="Document" URL="/U/Kinesis LabVIEW Website Examples/Thorlabs.MotionControl.GenericMotorCLI.dll"/>
			<Item Name="Thorlabs.MotionControl.GenericNanoTrakCLI.dll" Type="Document" URL="/U/Kinesis LabVIEW Website Examples/Thorlabs.MotionControl.GenericNanoTrakCLI.dll"/>
			<Item Name="Thorlabs.MotionControl.KCube.BrushlessMotorCLI.dll" Type="Document" URL="/U/Kinesis LabVIEW Website Examples/Thorlabs.MotionControl.KCube.BrushlessMotorCLI.dll"/>
			<Item Name="ThorLabs.MotionControl.KCube.DCServoCLI.dll" Type="Document" URL="/U/Kinesis LabVIEW Website Examples/ThorLabs.MotionControl.KCube.DCServoCLI.dll"/>
			<Item Name="ThorLabs.MotionControl.KCube.LaserSourceCLI.dll" Type="Document" URL="/U/Kinesis LabVIEW Website Examples/ThorLabs.MotionControl.KCube.LaserSourceCLI.dll"/>
			<Item Name="Thorlabs.MotionControl.KCube.SolenoidCLI.dll" Type="Document" URL="/U/Kinesis LabVIEW Website Examples/Thorlabs.MotionControl.KCube.SolenoidCLI.dll"/>
			<Item Name="Thorlabs.MotionControl.KCube.StepperMotorCLI.dll" Type="Document" URL="/U/Kinesis LabVIEW Website Examples/Thorlabs.MotionControl.KCube.StepperMotorCLI.dll"/>
			<Item Name="ThorLabs.MotionControl.KCube.StrainGaugeCLI.dll" Type="Document" URL="/U/Kinesis LabVIEW Website Examples/ThorLabs.MotionControl.KCube.StrainGaugeCLI.dll"/>
			<Item Name="Thorlabs.MotionControl.ModularRackCLI.dll" Type="Document" URL="/U/Kinesis LabVIEW Website Examples/Thorlabs.MotionControl.ModularRackCLI.dll"/>
			<Item Name="Wait for Operation Complete.vi" Type="VI" URL="../Kiethley24XX_VIs/Initialize Folder/D/Download/Keithley 24XX/Public/Data/Low Level/Wait for Operation Complete.vi"/>
			<Item Name="あああ.rtm" Type="Document" URL="../PMT_VIs/あああ.rtm"/>
		</Item>
		<Item Name="Build Specifications" Type="Build"/>
	</Item>
</Project>
