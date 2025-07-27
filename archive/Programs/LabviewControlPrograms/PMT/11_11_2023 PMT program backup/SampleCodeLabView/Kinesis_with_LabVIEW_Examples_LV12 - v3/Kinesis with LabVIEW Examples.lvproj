<?xml version='1.0' encoding='UTF-8'?>
<Project Type="Project" LVVersion="21008000">
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
		<Item Name="SampleCodeLabView" Type="Folder">
			<Item Name="EXE" Type="Folder">
				<Item Name="data" Type="Folder">
					<Item Name="H11890api.dll" Type="Document" URL="../../EXE/data/H11890api.dll"/>
				</Item>
				<Item Name="SampleSoftwareH11890.aliases" Type="Document" URL="../../EXE/SampleSoftwareH11890.aliases"/>
				<Item Name="SampleSoftwareH11890.exe" Type="Document" URL="../../EXE/SampleSoftwareH11890.exe"/>
				<Item Name="SampleSoftwareH11890.ini" Type="Document" URL="../../EXE/SampleSoftwareH11890.ini"/>
			</Item>
			<Item Name="Installer" Type="Folder">
				<Item Name="bin" Type="Folder">
					<Item Name="dp" Type="Folder">
						<Item Name="data.cab" Type="Document" URL="../../Installer/bin/dp/data.cab"/>
						<Item Name="DevPartDef.xml" Type="Document" URL="../../Installer/bin/dp/DevPartDef.xml"/>
						<Item Name="install.msi" Type="Document" URL="../../Installer/bin/dp/install.msi"/>
					</Item>
					<Item Name="p0" Type="Folder">
						<Item Name="MU" Type="Folder">
							<Item Name="MetaUninstaller.msi" Type="Document" URL="../../Installer/bin/p0/MU/MetaUninstaller.msi"/>
							<Item Name="MetaUninstaller_mft.cab" Type="Document" URL="../../Installer/bin/p0/MU/MetaUninstaller_mft.cab"/>
							<Item Name="MetaUninstallerR1.cab" Type="Document" URL="../../Installer/bin/p0/MU/MetaUninstallerR1.cab"/>
						</Item>
					</Item>
					<Item Name="p1" Type="Folder">
						<Item Name="VC2008MSMs" Type="Folder">
							<Item Name="VC2008MSMs_x64.msi" Type="Document" URL="../../Installer/bin/p1/VC2008MSMs/VC2008MSMs_x64.msi"/>
							<Item Name="VC2008MSMs_x86.msi" Type="Document" URL="../../Installer/bin/p1/VC2008MSMs/VC2008MSMs_x86.msi"/>
							<Item Name="VC2008MSMs_x86_mft.cab" Type="Document" URL="../../Installer/bin/p1/VC2008MSMs/VC2008MSMs_x86_mft.cab"/>
							<Item Name="x64.cab" Type="Document" URL="../../Installer/bin/p1/VC2008MSMs/x64.cab"/>
							<Item Name="x86.cab" Type="Document" URL="../../Installer/bin/p1/VC2008MSMs/x86.cab"/>
						</Item>
					</Item>
					<Item Name="p2" Type="Folder">
						<Item Name="sslLVRTE" Type="Folder">
							<Item Name="ssl_LVRTEsupp.msi" Type="Document" URL="../../Installer/bin/p2/sslLVRTE/ssl_LVRTEsupp.msi"/>
							<Item Name="ssl_LVRTEsupp_mft.cab" Type="Document" URL="../../Installer/bin/p2/sslLVRTE/ssl_LVRTEsupp_mft.cab"/>
							<Item Name="sslLVRTE.cab" Type="Document" URL="../../Installer/bin/p2/sslLVRTE/sslLVRTE.cab"/>
						</Item>
					</Item>
					<Item Name="p3" Type="Folder">
						<Item Name="NI_De00" Type="Folder">
							<Item Name="dep_framework.msi" Type="Document" URL="../../Installer/bin/p3/NI_De00/dep_framework.msi"/>
							<Item Name="dep_framework_mft.cab" Type="Document" URL="../../Installer/bin/p3/NI_De00/dep_framework_mft.cab"/>
							<Item Name="NI_De00.cab" Type="Document" URL="../../Installer/bin/p3/NI_De00/NI_De00.cab"/>
						</Item>
					</Item>
					<Item Name="p4" Type="Folder">
						<Item Name="CVI_LowLevelDriverOriginal.msi" Type="Document" URL="../../Installer/bin/p4/CVI_LowLevelDriverOriginal.msi"/>
						<Item Name="CVI_LowLevelDriverOriginal_mft.cab" Type="Document" URL="../../Installer/bin/p4/CVI_LowLevelDriverOriginal_mft.cab"/>
						<Item Name="CVI_LowLevelDriverUpdated.msi" Type="Document" URL="../../Installer/bin/p4/CVI_LowLevelDriverUpdated.msi"/>
						<Item Name="lldrvo.cab" Type="Document" URL="../../Installer/bin/p4/lldrvo.cab"/>
						<Item Name="lldrvu.cab" Type="Document" URL="../../Installer/bin/p4/lldrvu.cab"/>
					</Item>
					<Item Name="p5" Type="Folder">
						<Item Name="KillBit.msi" Type="Document" URL="../../Installer/bin/p5/KillBit.msi"/>
						<Item Name="KillBit64.msi" Type="Document" URL="../../Installer/bin/p5/KillBit64.msi"/>
						<Item Name="KillBit_mft.cab" Type="Document" URL="../../Installer/bin/p5/KillBit_mft.cab"/>
					</Item>
					<Item Name="p6" Type="Folder">
						<Item Name="mDNSResponder.msi" Type="Document" URL="../../Installer/bin/p6/mDNSResponder.msi"/>
						<Item Name="mDNSResponder_W64.msi" Type="Document" URL="../../Installer/bin/p6/mDNSResponder_W64.msi"/>
					</Item>
					<Item Name="p7" Type="Folder">
						<Item Name="NITra00.cab" Type="Document" URL="../../Installer/bin/p7/NITra00.cab"/>
						<Item Name="NITra01.cab" Type="Document" URL="../../Installer/bin/p7/NITra01.cab"/>
						<Item Name="NITraceEngine.msi" Type="Document" URL="../../Installer/bin/p7/NITraceEngine.msi"/>
						<Item Name="NITraceEngine64.msi" Type="Document" URL="../../Installer/bin/p7/NITraceEngine64.msi"/>
						<Item Name="NITraceEngine_mft.cab" Type="Document" URL="../../Installer/bin/p7/NITraceEngine_mft.cab"/>
					</Item>
					<Item Name="p8" Type="Folder">
						<Item Name="NI_Sy00.cab" Type="Document" URL="../../Installer/bin/p8/NI_Sy00.cab"/>
						<Item Name="NI_Sy01.cab" Type="Document" URL="../../Installer/bin/p8/NI_Sy01.cab"/>
						<Item Name="NI_SysStatePub.msi" Type="Document" URL="../../Installer/bin/p8/NI_SysStatePub.msi"/>
						<Item Name="NI_SysStatePub64.msi" Type="Document" URL="../../Installer/bin/p8/NI_SysStatePub64.msi"/>
						<Item Name="NI_SysStatePub_mft.cab" Type="Document" URL="../../Installer/bin/p8/NI_SysStatePub_mft.cab"/>
					</Item>
					<Item Name="p9" Type="Folder">
						<Item Name="ni_gmp.cab" Type="Document" URL="../../Installer/bin/p9/ni_gmp.cab"/>
						<Item Name="ni_gmp.msi" Type="Document" URL="../../Installer/bin/p9/ni_gmp.msi"/>
						<Item Name="ni_gmp64.cab" Type="Document" URL="../../Installer/bin/p9/ni_gmp64.cab"/>
						<Item Name="ni_gmp64.msi" Type="Document" URL="../../Installer/bin/p9/ni_gmp64.msi"/>
						<Item Name="ni_gmp_mft.cab" Type="Document" URL="../../Installer/bin/p9/ni_gmp_mft.cab"/>
					</Item>
					<Item Name="p10" Type="Folder">
						<Item Name="LVRT_00" Type="Folder">
							<Item Name="LVRT_00.cab" Type="Document" URL="../../Installer/bin/p10/LVRT_00/LVRT_00.cab"/>
							<Item Name="LVRT_00_chs.mst" Type="Document" URL="../../Installer/bin/p10/LVRT_00/LVRT_00_chs.mst"/>
							<Item Name="LVRT_00_deu.mst" Type="Document" URL="../../Installer/bin/p10/LVRT_00/LVRT_00_deu.mst"/>
							<Item Name="LVRT_00_fra.mst" Type="Document" URL="../../Installer/bin/p10/LVRT_00/LVRT_00_fra.mst"/>
							<Item Name="LVRT_00_jpn.mst" Type="Document" URL="../../Installer/bin/p10/LVRT_00/LVRT_00_jpn.mst"/>
							<Item Name="LVRT_00_kor.mst" Type="Document" URL="../../Installer/bin/p10/LVRT_00/LVRT_00_kor.mst"/>
							<Item Name="LVRT_NBFifo_2013.msi" Type="Document" URL="../../Installer/bin/p10/LVRT_00/LVRT_NBFifo_2013.msi"/>
							<Item Name="LVRT_NBFifo_2013_mft.cab" Type="Document" URL="../../Installer/bin/p10/LVRT_00/LVRT_NBFifo_2013_mft.cab"/>
						</Item>
					</Item>
					<Item Name="p11" Type="Folder">
						<Item Name="niauth.cab" Type="Document" URL="../../Installer/bin/p11/niauth.cab"/>
						<Item Name="niauth.msi" Type="Document" URL="../../Installer/bin/p11/niauth.msi"/>
						<Item Name="niauth64.cab" Type="Document" URL="../../Installer/bin/p11/niauth64.cab"/>
						<Item Name="niauth64.msi" Type="Document" URL="../../Installer/bin/p11/niauth64.msi"/>
						<Item Name="niauth_mft.cab" Type="Document" URL="../../Installer/bin/p11/niauth_mft.cab"/>
					</Item>
					<Item Name="p12" Type="Folder">
						<Item Name="nicurl.cab" Type="Document" URL="../../Installer/bin/p12/nicurl.cab"/>
						<Item Name="nicurl.msi" Type="Document" URL="../../Installer/bin/p12/nicurl.msi"/>
						<Item Name="nicurl64.cab" Type="Document" URL="../../Installer/bin/p12/nicurl64.cab"/>
						<Item Name="nicurl64.msi" Type="Document" URL="../../Installer/bin/p12/nicurl64.msi"/>
						<Item Name="nicurl_mft.cab" Type="Document" URL="../../Installer/bin/p12/nicurl_mft.cab"/>
					</Item>
					<Item Name="p13" Type="Folder">
						<Item Name="svcloc" Type="Folder">
							<Item Name="nisvcloc.msi" Type="Document" URL="../../Installer/bin/p13/svcloc/nisvcloc.msi"/>
							<Item Name="nisvcloc_mft.cab" Type="Document" URL="../../Installer/bin/p13/svcloc/nisvcloc_mft.cab"/>
							<Item Name="svcloc.cab" Type="Document" URL="../../Installer/bin/p13/svcloc/svcloc.cab"/>
							<Item Name="svcloc_chs.mst" Type="Document" URL="../../Installer/bin/p13/svcloc/svcloc_chs.mst"/>
							<Item Name="svcloc_deu.mst" Type="Document" URL="../../Installer/bin/p13/svcloc/svcloc_deu.mst"/>
							<Item Name="svcloc_fra.mst" Type="Document" URL="../../Installer/bin/p13/svcloc/svcloc_fra.mst"/>
							<Item Name="svcloc_jpn.mst" Type="Document" URL="../../Installer/bin/p13/svcloc/svcloc_jpn.mst"/>
							<Item Name="svcloc_kor.mst" Type="Document" URL="../../Installer/bin/p13/svcloc/svcloc_kor.mst"/>
						</Item>
					</Item>
					<Item Name="p14" Type="Folder">
						<Item Name="sys_w00" Type="Folder">
							<Item Name="ni_syswebsrvr.msi" Type="Document" URL="../../Installer/bin/p14/sys_w00/ni_syswebsrvr.msi"/>
							<Item Name="ni_syswebsrvr_mft.cab" Type="Document" URL="../../Installer/bin/p14/sys_w00/ni_syswebsrvr_mft.cab"/>
							<Item Name="sys_w00.cab" Type="Document" URL="../../Installer/bin/p14/sys_w00/sys_w00.cab"/>
							<Item Name="sys_w00_chs.mst" Type="Document" URL="../../Installer/bin/p14/sys_w00/sys_w00_chs.mst"/>
							<Item Name="sys_w00_deu.mst" Type="Document" URL="../../Installer/bin/p14/sys_w00/sys_w00_deu.mst"/>
							<Item Name="sys_w00_fra.mst" Type="Document" URL="../../Installer/bin/p14/sys_w00/sys_w00_fra.mst"/>
							<Item Name="sys_w00_jpn.mst" Type="Document" URL="../../Installer/bin/p14/sys_w00/sys_w00_jpn.mst"/>
							<Item Name="sys_w00_kor.mst" Type="Document" URL="../../Installer/bin/p14/sys_w00/sys_w00_kor.mst"/>
						</Item>
					</Item>
					<Item Name="p15" Type="Folder">
						<Item Name="LOGOS00.cab" Type="Document" URL="../../Installer/bin/p15/LOGOS00.cab"/>
						<Item Name="LOGOS_XT.cab" Type="Document" URL="../../Installer/bin/p15/LOGOS_XT.cab"/>
						<Item Name="LogosXT.msi" Type="Document" URL="../../Installer/bin/p15/LogosXT.msi"/>
						<Item Name="LogosXT64.msi" Type="Document" URL="../../Installer/bin/p15/LogosXT64.msi"/>
						<Item Name="LogosXT_mft.cab" Type="Document" URL="../../Installer/bin/p15/LogosXT_mft.cab"/>
					</Item>
					<Item Name="p16" Type="Folder">
						<Item Name="LVRTE00" Type="Folder">
							<Item Name="LVRTE00.cab" Type="Document" URL="../../Installer/bin/p16/LVRTE00/LVRTE00.cab"/>
							<Item Name="LVRTE00_chs.mst" Type="Document" URL="../../Installer/bin/p16/LVRTE00/LVRTE00_chs.mst"/>
							<Item Name="LVRTE00_deu.mst" Type="Document" URL="../../Installer/bin/p16/LVRTE00/LVRTE00_deu.mst"/>
							<Item Name="LVRTE00_fra.mst" Type="Document" URL="../../Installer/bin/p16/LVRTE00/LVRTE00_fra.mst"/>
							<Item Name="LVRTE00_jpn.mst" Type="Document" URL="../../Installer/bin/p16/LVRTE00/LVRTE00_jpn.mst"/>
							<Item Name="LVRTE00_kor.mst" Type="Document" URL="../../Installer/bin/p16/LVRTE00/LVRTE00_kor.mst"/>
							<Item Name="NIWebServer_LVRTE.msi" Type="Document" URL="../../Installer/bin/p16/LVRTE00/NIWebServer_LVRTE.msi"/>
							<Item Name="NIWebServer_LVRTE_mft.cab" Type="Document" URL="../../Installer/bin/p16/LVRTE00/NIWebServer_LVRTE_mft.cab"/>
						</Item>
					</Item>
					<Item Name="p17" Type="Folder">
						<Item Name="ni_error" Type="Folder">
							<Item Name="ni_error.cab" Type="Document" URL="../../Installer/bin/p17/ni_error/ni_error.cab"/>
							<Item Name="ni_error_chs.mst" Type="Document" URL="../../Installer/bin/p17/ni_error/ni_error_chs.mst"/>
							<Item Name="ni_error_deu.mst" Type="Document" URL="../../Installer/bin/p17/ni_error/ni_error_deu.mst"/>
							<Item Name="ni_error_fra.mst" Type="Document" URL="../../Installer/bin/p17/ni_error/ni_error_fra.mst"/>
							<Item Name="ni_error_jpn.mst" Type="Document" URL="../../Installer/bin/p17/ni_error/ni_error_jpn.mst"/>
							<Item Name="ni_error_kor.mst" Type="Document" URL="../../Installer/bin/p17/ni_error/ni_error_kor.mst"/>
							<Item Name="ni_error_report.msi" Type="Document" URL="../../Installer/bin/p17/ni_error/ni_error_report.msi"/>
							<Item Name="ni_error_report_mft.cab" Type="Document" URL="../../Installer/bin/p17/ni_error/ni_error_report_mft.cab"/>
						</Item>
					</Item>
					<Item Name="p18" Type="Folder">
						<Item Name="ni_sysweb_base.msi" Type="Document" URL="../../Installer/bin/p18/ni_sysweb_base.msi"/>
						<Item Name="ni_sysweb_base64.msi" Type="Document" URL="../../Installer/bin/p18/ni_sysweb_base64.msi"/>
						<Item Name="ni_sysweb_base_mft.cab" Type="Document" URL="../../Installer/bin/p18/ni_sysweb_base_mft.cab"/>
						<Item Name="sys_w00.cab" Type="Document" URL="../../Installer/bin/p18/sys_w00.cab"/>
						<Item Name="sys_w01.cab" Type="Document" URL="../../Installer/bin/p18/sys_w01.cab"/>
					</Item>
					<Item Name="p19" Type="Folder">
						<Item Name="activ32.cab" Type="Document" URL="../../Installer/bin/p19/activ32.cab"/>
						<Item Name="activ32_chs.mst" Type="Document" URL="../../Installer/bin/p19/activ32_chs.mst"/>
						<Item Name="activ32_deu.mst" Type="Document" URL="../../Installer/bin/p19/activ32_deu.mst"/>
						<Item Name="activ32_fra.mst" Type="Document" URL="../../Installer/bin/p19/activ32_fra.mst"/>
						<Item Name="activ32_jpn.mst" Type="Document" URL="../../Installer/bin/p19/activ32_jpn.mst"/>
						<Item Name="activ32_kor.mst" Type="Document" URL="../../Installer/bin/p19/activ32_kor.mst"/>
						<Item Name="activ64.cab" Type="Document" URL="../../Installer/bin/p19/activ64.cab"/>
						<Item Name="activ64_chs.mst" Type="Document" URL="../../Installer/bin/p19/activ64_chs.mst"/>
						<Item Name="activ64_deu.mst" Type="Document" URL="../../Installer/bin/p19/activ64_deu.mst"/>
						<Item Name="activ64_fra.mst" Type="Document" URL="../../Installer/bin/p19/activ64_fra.mst"/>
						<Item Name="activ64_jpn.mst" Type="Document" URL="../../Installer/bin/p19/activ64_jpn.mst"/>
						<Item Name="activ64_kor.mst" Type="Document" URL="../../Installer/bin/p19/activ64_kor.mst"/>
						<Item Name="activex.msi" Type="Document" URL="../../Installer/bin/p19/activex.msi"/>
						<Item Name="activex64.msi" Type="Document" URL="../../Installer/bin/p19/activex64.msi"/>
						<Item Name="activex_mft.cab" Type="Document" URL="../../Installer/bin/p19/activex_mft.cab"/>
					</Item>
					<Item Name="p20" Type="Folder">
						<Item Name="tdms.cab" Type="Document" URL="../../Installer/bin/p20/tdms.cab"/>
						<Item Name="tdms.msi" Type="Document" URL="../../Installer/bin/p20/tdms.msi"/>
						<Item Name="tdms64.cab" Type="Document" URL="../../Installer/bin/p20/tdms64.cab"/>
						<Item Name="tdms64.msi" Type="Document" URL="../../Installer/bin/p20/tdms64.msi"/>
						<Item Name="tdms64_chs.mst" Type="Document" URL="../../Installer/bin/p20/tdms64_chs.mst"/>
						<Item Name="tdms64_deu.mst" Type="Document" URL="../../Installer/bin/p20/tdms64_deu.mst"/>
						<Item Name="tdms64_fra.mst" Type="Document" URL="../../Installer/bin/p20/tdms64_fra.mst"/>
						<Item Name="tdms64_jpn.mst" Type="Document" URL="../../Installer/bin/p20/tdms64_jpn.mst"/>
						<Item Name="tdms64_kor.mst" Type="Document" URL="../../Installer/bin/p20/tdms64_kor.mst"/>
						<Item Name="tdms_chs.mst" Type="Document" URL="../../Installer/bin/p20/tdms_chs.mst"/>
						<Item Name="tdms_deu.mst" Type="Document" URL="../../Installer/bin/p20/tdms_deu.mst"/>
						<Item Name="tdms_fra.mst" Type="Document" URL="../../Installer/bin/p20/tdms_fra.mst"/>
						<Item Name="tdms_jpn.mst" Type="Document" URL="../../Installer/bin/p20/tdms_jpn.mst"/>
						<Item Name="tdms_kor.mst" Type="Document" URL="../../Installer/bin/p20/tdms_kor.mst"/>
						<Item Name="tdms_mft.cab" Type="Document" URL="../../Installer/bin/p20/tdms_mft.cab"/>
					</Item>
					<Item Name="p21" Type="Folder">
						<Item Name="ni_ssl.msi" Type="Document" URL="../../Installer/bin/p21/ni_ssl.msi"/>
						<Item Name="ni_ssl64.msi" Type="Document" URL="../../Installer/bin/p21/ni_ssl64.msi"/>
						<Item Name="ni_ssl_mft.cab" Type="Document" URL="../../Installer/bin/p21/ni_ssl_mft.cab"/>
						<Item Name="ssl.cab" Type="Document" URL="../../Installer/bin/p21/ssl.cab"/>
						<Item Name="ssl64.cab" Type="Document" URL="../../Installer/bin/p21/ssl64.cab"/>
						<Item Name="ssl64_chs.mst" Type="Document" URL="../../Installer/bin/p21/ssl64_chs.mst"/>
						<Item Name="ssl64_deu.mst" Type="Document" URL="../../Installer/bin/p21/ssl64_deu.mst"/>
						<Item Name="ssl64_fra.mst" Type="Document" URL="../../Installer/bin/p21/ssl64_fra.mst"/>
						<Item Name="ssl64_jpn.mst" Type="Document" URL="../../Installer/bin/p21/ssl64_jpn.mst"/>
						<Item Name="ssl64_kor.mst" Type="Document" URL="../../Installer/bin/p21/ssl64_kor.mst"/>
						<Item Name="ssl_chs.mst" Type="Document" URL="../../Installer/bin/p21/ssl_chs.mst"/>
						<Item Name="ssl_deu.mst" Type="Document" URL="../../Installer/bin/p21/ssl_deu.mst"/>
						<Item Name="ssl_fra.mst" Type="Document" URL="../../Installer/bin/p21/ssl_fra.mst"/>
						<Item Name="ssl_jpn.mst" Type="Document" URL="../../Installer/bin/p21/ssl_jpn.mst"/>
						<Item Name="ssl_kor.mst" Type="Document" URL="../../Installer/bin/p21/ssl_kor.mst"/>
					</Item>
					<Item Name="p22" Type="Folder">
						<Item Name="ni_sysappsrvr.msi" Type="Document" URL="../../Installer/bin/p22/ni_sysappsrvr.msi"/>
						<Item Name="ni_sysappsrvr64.msi" Type="Document" URL="../../Installer/bin/p22/ni_sysappsrvr64.msi"/>
						<Item Name="ni_sysappsrvr_mft.cab" Type="Document" URL="../../Installer/bin/p22/ni_sysappsrvr_mft.cab"/>
						<Item Name="sys_a00.cab" Type="Document" URL="../../Installer/bin/p22/sys_a00.cab"/>
						<Item Name="sys_a00_chs.mst" Type="Document" URL="../../Installer/bin/p22/sys_a00_chs.mst"/>
						<Item Name="sys_a00_deu.mst" Type="Document" URL="../../Installer/bin/p22/sys_a00_deu.mst"/>
						<Item Name="sys_a00_fra.mst" Type="Document" URL="../../Installer/bin/p22/sys_a00_fra.mst"/>
						<Item Name="sys_a00_jpn.mst" Type="Document" URL="../../Installer/bin/p22/sys_a00_jpn.mst"/>
						<Item Name="sys_a00_kor.mst" Type="Document" URL="../../Installer/bin/p22/sys_a00_kor.mst"/>
						<Item Name="sys_a01.cab" Type="Document" URL="../../Installer/bin/p22/sys_a01.cab"/>
						<Item Name="sys_a01_chs.mst" Type="Document" URL="../../Installer/bin/p22/sys_a01_chs.mst"/>
						<Item Name="sys_a01_deu.mst" Type="Document" URL="../../Installer/bin/p22/sys_a01_deu.mst"/>
						<Item Name="sys_a01_fra.mst" Type="Document" URL="../../Installer/bin/p22/sys_a01_fra.mst"/>
						<Item Name="sys_a01_jpn.mst" Type="Document" URL="../../Installer/bin/p22/sys_a01_jpn.mst"/>
						<Item Name="sys_a01_kor.mst" Type="Document" URL="../../Installer/bin/p22/sys_a01_kor.mst"/>
					</Item>
					<Item Name="p23" Type="Folder">
						<Item Name="mkl.msi" Type="Document" URL="../../Installer/bin/p23/mkl.msi"/>
						<Item Name="mkl64.msi" Type="Document" URL="../../Installer/bin/p23/mkl64.msi"/>
						<Item Name="MKL2000.cab" Type="Document" URL="../../Installer/bin/p23/MKL2000.cab"/>
						<Item Name="MKL2000_chs.mst" Type="Document" URL="../../Installer/bin/p23/MKL2000_chs.mst"/>
						<Item Name="MKL2000_deu.mst" Type="Document" URL="../../Installer/bin/p23/MKL2000_deu.mst"/>
						<Item Name="MKL2000_fra.mst" Type="Document" URL="../../Installer/bin/p23/MKL2000_fra.mst"/>
						<Item Name="MKL2000_jpn.mst" Type="Document" URL="../../Installer/bin/p23/MKL2000_jpn.mst"/>
						<Item Name="MKL2000_kor.mst" Type="Document" URL="../../Installer/bin/p23/MKL2000_kor.mst"/>
						<Item Name="MKL2013.cab" Type="Document" URL="../../Installer/bin/p23/MKL2013.cab"/>
						<Item Name="MKL2013_chs.mst" Type="Document" URL="../../Installer/bin/p23/MKL2013_chs.mst"/>
						<Item Name="MKL2013_deu.mst" Type="Document" URL="../../Installer/bin/p23/MKL2013_deu.mst"/>
						<Item Name="MKL2013_fra.mst" Type="Document" URL="../../Installer/bin/p23/MKL2013_fra.mst"/>
						<Item Name="MKL2013_jpn.mst" Type="Document" URL="../../Installer/bin/p23/MKL2013_jpn.mst"/>
						<Item Name="MKL2013_kor.mst" Type="Document" URL="../../Installer/bin/p23/MKL2013_kor.mst"/>
						<Item Name="mkl_mft.cab" Type="Document" URL="../../Installer/bin/p23/mkl_mft.cab"/>
					</Item>
					<Item Name="p24" Type="Folder">
						<Item Name="MDF" Type="Folder">
							<Item Name="EULADepo.cab" Type="Document" URL="../../Installer/bin/p24/MDF/EULADepo.cab"/>
							<Item Name="EULADepot.msi" Type="Document" URL="../../Installer/bin/p24/MDF/EULADepot.msi"/>
							<Item Name="MDFSupport.msi" Type="Document" URL="../../Installer/bin/p24/MDF/MDFSupport.msi"/>
							<Item Name="MDFSupport1.cab" Type="Document" URL="../../Installer/bin/p24/MDF/MDFSupport1.cab"/>
							<Item Name="MDFSupport_mft.cab" Type="Document" URL="../../Installer/bin/p24/MDF/MDFSupport_mft.cab"/>
							<Item Name="NIYouLAs.bin" Type="Document" URL="../../Installer/bin/p24/MDF/NIYouLAs.bin"/>
						</Item>
					</Item>
					<Item Name="p25" Type="Folder">
						<Item Name="lvrteres" Type="Folder">
							<Item Name="LV2013rteres.msi" Type="Document" URL="../../Installer/bin/p25/lvrteres/LV2013rteres.msi"/>
							<Item Name="LV2013rteres_mft.cab" Type="Document" URL="../../Installer/bin/p25/lvrteres/LV2013rteres_mft.cab"/>
							<Item Name="lvrteres.cab" Type="Document" URL="../../Installer/bin/p25/lvrteres/lvrteres.cab"/>
							<Item Name="lvrteres_chs.mst" Type="Document" URL="../../Installer/bin/p25/lvrteres/lvrteres_chs.mst"/>
							<Item Name="lvrteres_deu.mst" Type="Document" URL="../../Installer/bin/p25/lvrteres/lvrteres_deu.mst"/>
							<Item Name="lvrteres_fra.mst" Type="Document" URL="../../Installer/bin/p25/lvrteres/lvrteres_fra.mst"/>
							<Item Name="lvrteres_jpn.mst" Type="Document" URL="../../Installer/bin/p25/lvrteres/lvrteres_jpn.mst"/>
							<Item Name="lvrteres_kor.mst" Type="Document" URL="../../Installer/bin/p25/lvrteres/lvrteres_kor.mst"/>
						</Item>
					</Item>
					<Item Name="p26" Type="Folder">
						<Item Name="logos.cab" Type="Document" URL="../../Installer/bin/p26/logos.cab"/>
						<Item Name="logos.msi" Type="Document" URL="../../Installer/bin/p26/logos.msi"/>
						<Item Name="logos64.cab" Type="Document" URL="../../Installer/bin/p26/logos64.cab"/>
						<Item Name="logos64.msi" Type="Document" URL="../../Installer/bin/p26/logos64.msi"/>
						<Item Name="logos64_chs.mst" Type="Document" URL="../../Installer/bin/p26/logos64_chs.mst"/>
						<Item Name="logos64_deu.mst" Type="Document" URL="../../Installer/bin/p26/logos64_deu.mst"/>
						<Item Name="logos64_fra.mst" Type="Document" URL="../../Installer/bin/p26/logos64_fra.mst"/>
						<Item Name="logos64_jpn.mst" Type="Document" URL="../../Installer/bin/p26/logos64_jpn.mst"/>
						<Item Name="logos64_kor.mst" Type="Document" URL="../../Installer/bin/p26/logos64_kor.mst"/>
						<Item Name="logos_chs.mst" Type="Document" URL="../../Installer/bin/p26/logos_chs.mst"/>
						<Item Name="logos_deu.mst" Type="Document" URL="../../Installer/bin/p26/logos_deu.mst"/>
						<Item Name="logos_fra.mst" Type="Document" URL="../../Installer/bin/p26/logos_fra.mst"/>
						<Item Name="logos_jpn.mst" Type="Document" URL="../../Installer/bin/p26/logos_jpn.mst"/>
						<Item Name="logos_kor.mst" Type="Document" URL="../../Installer/bin/p26/logos_kor.mst"/>
						<Item Name="logos_mft.cab" Type="Document" URL="../../Installer/bin/p26/logos_mft.cab"/>
					</Item>
					<Item Name="p27" Type="Folder">
						<Item Name="LV2013rtdnet.msi" Type="Document" URL="../../Installer/bin/p27/LV2013rtdnet.msi"/>
						<Item Name="LV2013runtime.msi" Type="Document" URL="../../Installer/bin/p27/LV2013runtime.msi"/>
						<Item Name="LV2013runtime_mft.cab" Type="Document" URL="../../Installer/bin/p27/LV2013runtime_mft.cab"/>
						<Item Name="lvrte.cab" Type="Document" URL="../../Installer/bin/p27/lvrte.cab"/>
						<Item Name="lvrte_chs.mst" Type="Document" URL="../../Installer/bin/p27/lvrte_chs.mst"/>
						<Item Name="lvrte_deu.mst" Type="Document" URL="../../Installer/bin/p27/lvrte_deu.mst"/>
						<Item Name="lvrte_fra.mst" Type="Document" URL="../../Installer/bin/p27/lvrte_fra.mst"/>
						<Item Name="lvrte_jpn.mst" Type="Document" URL="../../Installer/bin/p27/lvrte_jpn.mst"/>
						<Item Name="lvrte_kor.mst" Type="Document" URL="../../Installer/bin/p27/lvrte_kor.mst"/>
						<Item Name="lvrtenet.cab" Type="Document" URL="../../Installer/bin/p27/lvrtenet.cab"/>
					</Item>
					<Item Name="p28" Type="Folder">
						<Item Name="MStudioCW3DGraph.cab" Type="Document" URL="../../Installer/bin/p28/MStudioCW3DGraph.cab"/>
						<Item Name="MStudioCW3DGraph.msi" Type="Document" URL="../../Installer/bin/p28/MStudioCW3DGraph.msi"/>
						<Item Name="MStudioCW3DGraph_mft.cab" Type="Document" URL="../../Installer/bin/p28/MStudioCW3DGraph_mft.cab"/>
					</Item>
				</Item>
				<Item Name="license" Type="Folder">
					<Item Name="Apache 2.0 License - English.pdf" Type="Document" URL="../../Installer/license/Apache 2.0 License - English.pdf"/>
					<Item Name="Boost 1.0 License - English.pdf" Type="Document" URL="../../Installer/license/Boost 1.0 License - English.pdf"/>
					<Item Name="BSD 3-clause License - English.rtf" Type="Document" URL="../../Installer/license/BSD 3-clause License - English.rtf"/>
					<Item Name="CryptoPP 5.6 License - English.pdf" Type="Document" URL="../../Installer/license/CryptoPP 5.6 License - English.pdf"/>
					<Item Name="FreeType License - English.txt" Type="Document" URL="../../Installer/license/FreeType License - English.txt"/>
					<Item Name="GNU Lesser General Public License - English.rtf" Type="Document" URL="../../Installer/license/GNU Lesser General Public License - English.rtf"/>
					<Item Name="LLVM License - English.rtf" Type="Document" URL="../../Installer/license/LLVM License - English.rtf"/>
					<Item Name="MARS 1.0 License - English.pdf" Type="Document" URL="../../Installer/license/MARS 1.0 License - English.pdf"/>
					<Item Name="Microsoft Public License_license.pdf" Type="Document" URL="../../Installer/license/Microsoft Public License_license.pdf"/>
					<Item Name="MIT 1.0 License - English.rtf" Type="Document" URL="../../Installer/license/MIT 1.0 License - English.rtf"/>
					<Item Name="MIT-X License.rtf" Type="Document" URL="../../Installer/license/MIT-X License.rtf"/>
					<Item Name="MIT-X YAJL Style License.rtf" Type="Document" URL="../../Installer/license/MIT-X YAJL Style License.rtf"/>
					<Item Name="Mozilla Public License 2.0.rtf" Type="Document" URL="../../Installer/license/Mozilla Public License 2.0.rtf"/>
					<Item Name="NI Released License Agreement - English.rtf" Type="Document" URL="../../Installer/license/NI Released License Agreement - English.rtf"/>
					<Item Name="NI Released License Agreement - French.rtf" Type="Document" URL="../../Installer/license/NI Released License Agreement - French.rtf"/>
					<Item Name="NI Released License Agreement - German.rtf" Type="Document" URL="../../Installer/license/NI Released License Agreement - German.rtf"/>
					<Item Name="NI Released License Agreement - Italian.rtf" Type="Document" URL="../../Installer/license/NI Released License Agreement - Italian.rtf"/>
					<Item Name="NI Released License Agreement - Japanese.rtf" Type="Document" URL="../../Installer/license/NI Released License Agreement - Japanese.rtf"/>
					<Item Name="NI Released License Agreement - Korean.rtf" Type="Document" URL="../../Installer/license/NI Released License Agreement - Korean.rtf"/>
					<Item Name="NI Released License Agreement - Simplified Chinese.rtf" Type="Document" URL="../../Installer/license/NI Released License Agreement - Simplified Chinese.rtf"/>
					<Item Name="NI Released License Agreement - Spanish.rtf" Type="Document" URL="../../Installer/license/NI Released License Agreement - Spanish.rtf"/>
					<Item Name="NICTA 1.0 License - English.pdf" Type="Document" URL="../../Installer/license/NICTA 1.0 License - English.pdf"/>
					<Item Name="OpenSSL 1.0 License - English.pdf" Type="Document" URL="../../Installer/license/OpenSSL 1.0 License - English.pdf"/>
					<Item Name="UPX 1.0 license - English.pdf" Type="Document" URL="../../Installer/license/UPX 1.0 license - English.pdf"/>
					<Item Name="WordNet 2.1 License - English.txt" Type="Document" URL="../../Installer/license/WordNet 2.1 License - English.txt"/>
					<Item Name="wxWindows 3.1 License - English.pdf" Type="Document" URL="../../Installer/license/wxWindows 3.1 License - English.pdf"/>
					<Item Name="zlib License - English.pdf" Type="Document" URL="../../Installer/license/zlib License - English.pdf"/>
				</Item>
				<Item Name="supportfiles" Type="Folder">
					<Item Name="customResource0017.dll" Type="Document" URL="../../Installer/supportfiles/customResource0017.dll"/>
					<Item Name="merged.cab" Type="Document" URL="../../Installer/supportfiles/merged.cab"/>
					<Item Name="niPie.exe" Type="Document" URL="../../Installer/supportfiles/niPie.exe"/>
					<Item Name="nires0017.dll" Type="Document" URL="../../Installer/supportfiles/nires0017.dll"/>
					<Item Name="nistdtrans0007.mst" Type="Document" URL="../../Installer/supportfiles/nistdtrans0007.mst"/>
					<Item Name="nistdtrans0012.mst" Type="Document" URL="../../Installer/supportfiles/nistdtrans0012.mst"/>
					<Item Name="nistdtrans0017.mst" Type="Document" URL="../../Installer/supportfiles/nistdtrans0017.mst"/>
					<Item Name="nistdtrans0018.mst" Type="Document" URL="../../Installer/supportfiles/nistdtrans0018.mst"/>
					<Item Name="nistdtrans2052.mst" Type="Document" URL="../../Installer/supportfiles/nistdtrans2052.mst"/>
					<Item Name="nistdtransbase.mst" Type="Document" URL="../../Installer/supportfiles/nistdtransbase.mst"/>
				</Item>
				<Item Name="nidist.id" Type="Document" URL="../../Installer/nidist.id"/>
				<Item Name="setup.exe" Type="Document" URL="../../Installer/setup.exe"/>
				<Item Name="setup.ini" Type="Document" URL="../../Installer/setup.ini"/>
			</Item>
			<Item Name="Kinesis_with_LabVIEW_Examples_LV12 - v3" Type="Folder">
				<Item Name="Laser Source" Type="Folder">
					<Item Name="Kinesis - KLSnnn - Set Power.vi" Type="VI" URL="../Laser Source/Kinesis - KLSnnn - Set Power.vi"/>
				</Item>
				<Item Name="Motor" Type="Folder">
					<Item Name="Kinesis - KDC101 - Motor Status Changed (Reg Event Callback)" Type="Folder">
						<Item Name="Kinesis - KDC101 - Motor Status Changed (Callback VI).vi" Type="VI" URL="../Motor/Kinesis - KDC101 - Motor Status Changed (Reg Event Callback)/Kinesis - KDC101 - Motor Status Changed (Callback VI).vi"/>
						<Item Name="Kinesis - KDC101 - Motor Status Changed.vi" Type="VI" URL="../Motor/Kinesis - KDC101 - Motor Status Changed (Reg Event Callback)/Kinesis - KDC101 - Motor Status Changed.vi"/>
					</Item>
					<Item Name="Kinesis - BBD202 - Two Axis Scan.vi" Type="VI" URL="../Motor/Kinesis - BBD202 - Two Axis Scan.vi"/>
					<Item Name="Kinesis - KBD101 - Get Status Bits.vi" Type="VI" URL="../Motor/Kinesis - KBD101 - Get Status Bits.vi"/>
					<Item Name="Kinesis - KBD101 - Set Trigger Parameters.vi" Type="VI" URL="../Motor/Kinesis - KBD101 - Set Trigger Parameters.vi"/>
					<Item Name="Kinesis - KBD101 - Set Velocity Parameters.vi" Type="VI" URL="../Motor/Kinesis - KBD101 - Set Velocity Parameters.vi"/>
					<Item Name="Kinesis - KDC101 - Build Device List.vi" Type="VI" URL="../Motor/Kinesis - KDC101 - Build Device List.vi"/>
					<Item Name="Kinesis - KDC101 - Connect.vi" Type="VI" URL="../Motor/Kinesis - KDC101 - Connect.vi"/>
					<Item Name="Kinesis - KDC101 - Get Position.vi" Type="VI" URL="../Motor/Kinesis - KDC101 - Get Position.vi"/>
					<Item Name="Kinesis - KDC101 - Move Absolute.vi" Type="VI" URL="../Motor/Kinesis - KDC101 - Move Absolute.vi"/>
					<Item Name="Kinesis - KDC101 - No Front Panel.vi" Type="VI" URL="../Motor/Kinesis - KDC101 - No Front Panel.vi"/>
					<Item Name="Kinesis - KST101 - Move Relative.vi" Type="VI" URL="../Motor/Kinesis - KST101 - Move Relative.vi"/>
				</Item>
				<Item Name="Nanotrak" Type="Folder">
					<Item Name="Kinesis - BNT - Connect.vi" Type="VI" URL="../Nanotrak/Kinesis - BNT - Connect.vi"/>
					<Item Name="Kinesis - BNT - Set Circle Home Position.vi" Type="VI" URL="../Nanotrak/Kinesis - BNT - Set Circle Home Position.vi"/>
					<Item Name="Kinesis - KNA - Latch Trak.vi" Type="VI" URL="../Nanotrak/Kinesis - KNA - Latch Trak.vi"/>
					<Item Name="Kinesis - KNA - Set Circle Diameter.vi" Type="VI" URL="../Nanotrak/Kinesis - KNA - Set Circle Diameter.vi"/>
					<Item Name="Kinesis - KNA - Set Loop Gain.vi" Type="VI" URL="../Nanotrak/Kinesis - KNA - Set Loop Gain.vi"/>
					<Item Name="Kinesis - KNA - Set Phase Component.vi" Type="VI" URL="../Nanotrak/Kinesis - KNA - Set Phase Component.vi"/>
				</Item>
				<Item Name="Piezo" Type="Folder">
					<Item Name="Piezo" Type="Folder">
						<Item Name="Kinesis - BPC301 - Connect.vi" Type="VI" URL="../Piezo/Piezo/Kinesis - BPC301 - Connect.vi"/>
						<Item Name="Kinesis - BPC301 - Waveform LUT.vi" Type="VI" URL="../Piezo/Piezo/Kinesis - BPC301 - Waveform LUT.vi"/>
						<Item Name="Kinesis - BPC303 - Two Axis Scan.vi" Type="VI" URL="../Piezo/Piezo/Kinesis - BPC303 - Two Axis Scan.vi"/>
						<Item Name="Kinesis - KPZ101 - Connect.vi" Type="VI" URL="../Piezo/Piezo/Kinesis - KPZ101 - Connect.vi"/>
						<Item Name="Kinesis - KPZ101 - Waveform LUT.vi" Type="VI" URL="../Piezo/Piezo/Kinesis - KPZ101 - Waveform LUT.vi"/>
						<Item Name="Kinesis - KPZ101 KSG101 - Set Position.vi" Type="VI" URL="../Piezo/Piezo/Kinesis - KPZ101 KSG101 - Set Position.vi"/>
						<Item Name="Kinesis - PPC - Continuous Scan.vi" Type="VI" URL="../Piezo/Piezo/Kinesis - PPC - Continuous Scan.vi"/>
					</Item>
					<Item Name="Piezo Motor" Type="Folder">
						<Item Name="Kinesis - KIM101 - Set Jog.vi" Type="VI" URL="../Piezo/Piezo Motor/Kinesis - KIM101 - Set Jog.vi"/>
					</Item>
				</Item>
				<Item Name="Rack" Type="Folder">
					<Item Name="Kinesis - MPZ601 - Connect.vi" Type="VI" URL="../Rack/Kinesis - MPZ601 - Connect.vi"/>
					<Item Name="Kinesis - MPZ601 MNA601 - Two Axis Scan.vi" Type="VI" URL="../Rack/Kinesis - MPZ601 MNA601 - Two Axis Scan.vi"/>
					<Item Name="Kinesis - MST602 MNA601 - Two Axis Revector.vi" Type="VI" URL="../Rack/Kinesis - MST602 MNA601 - Two Axis Revector.vi"/>
					<Item Name="Kinesis - MST602 MNA601 - Two Axis Scan.vi" Type="VI" URL="../Rack/Kinesis - MST602 MNA601 - Two Axis Scan.vi"/>
				</Item>
				<Item Name="Simulator" Type="Folder">
					<Item Name="Kinesis - Simulated Hardware.vi" Type="VI" URL="../Simulator/Kinesis - Simulated Hardware.vi"/>
				</Item>
				<Item Name="Solenoid" Type="Folder">
					<Item Name="Kinesis - KSC101 - Set Operating Mode.vi" Type="VI" URL="../Solenoid/Kinesis - KSC101 - Set Operating Mode.vi"/>
				</Item>
				<Item Name="Strain Gauge Reader" Type="Folder">
					<Item Name="Kinesis - KSG101 - Get Max Travel Range.vi" Type="VI" URL="../Strain Gauge Reader/Kinesis - KSG101 - Get Max Travel Range.vi"/>
					<Item Name="Kinesis - KSG101 - Get Reading.vi" Type="VI" URL="../Strain Gauge Reader/Kinesis - KSG101 - Get Reading.vi"/>
				</Item>
				<Item Name="Drop Your DLL Files Here.txt" Type="Document" URL="../Drop Your DLL Files Here.txt"/>
				<Item Name="ftd2xx.dll" Type="Document" URL="../ftd2xx.dll"/>
				<Item Name="Kinesis with LabVIEW Examples.aliases" Type="Document" URL="../Kinesis with LabVIEW Examples.aliases"/>
				<Item Name="Kinesis with LabVIEW Examples.lvlps" Type="Document" URL="../Kinesis with LabVIEW Examples.lvlps"/>
				<Item Name="ReadMe.txt" Type="Document" URL="../ReadMe.txt"/>
				<Item Name="Thorlabs.APT.dll" Type="Document" URL="../Thorlabs.APT.dll"/>
				<Item Name="Thorlabs.MotionControl.Benchtop.BrushlessMotor.dll" Type="Document" URL="../Thorlabs.MotionControl.Benchtop.BrushlessMotor.dll"/>
				<Item Name="Thorlabs.MotionControl.Benchtop.BrushlessMotorCLI.dll" Type="Document" URL="../Thorlabs.MotionControl.Benchtop.BrushlessMotorCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.Benchtop.BrushlessMotorUI.dll" Type="Document" URL="../Thorlabs.MotionControl.Benchtop.BrushlessMotorUI.dll"/>
				<Item Name="Thorlabs.MotionControl.Benchtop.DCServo.dll" Type="Document" URL="../Thorlabs.MotionControl.Benchtop.DCServo.dll"/>
				<Item Name="ThorLabs.MotionControl.Benchtop.DCServoCLI.dll" Type="Document" URL="../ThorLabs.MotionControl.Benchtop.DCServoCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.Benchtop.DCServoUI.dll" Type="Document" URL="../Thorlabs.MotionControl.Benchtop.DCServoUI.dll"/>
				<Item Name="Thorlabs.MotionControl.Benchtop.NanoTrak.dll" Type="Document" URL="../Thorlabs.MotionControl.Benchtop.NanoTrak.dll"/>
				<Item Name="Thorlabs.MotionControl.Benchtop.NanoTrakCLI.dll" Type="Document" URL="../Thorlabs.MotionControl.Benchtop.NanoTrakCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.Benchtop.NanoTrakUI.dll" Type="Document" URL="../Thorlabs.MotionControl.Benchtop.NanoTrakUI.dll"/>
				<Item Name="Thorlabs.MotionControl.Benchtop.Piezo.dll" Type="Document" URL="../Thorlabs.MotionControl.Benchtop.Piezo.dll"/>
				<Item Name="Thorlabs.MotionControl.Benchtop.PiezoCLI.dll" Type="Document" URL="../Thorlabs.MotionControl.Benchtop.PiezoCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.Benchtop.PiezoUI.dll" Type="Document" URL="../Thorlabs.MotionControl.Benchtop.PiezoUI.dll"/>
				<Item Name="Thorlabs.MotionControl.Benchtop.PrecisionPiezo.dll" Type="Document" URL="../Thorlabs.MotionControl.Benchtop.PrecisionPiezo.dll"/>
				<Item Name="ThorLabs.MotionControl.Benchtop.PrecisionPiezoCLI.dll" Type="Document" URL="../ThorLabs.MotionControl.Benchtop.PrecisionPiezoCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.Benchtop.PrecisionPiezoUI.dll" Type="Document" URL="../Thorlabs.MotionControl.Benchtop.PrecisionPiezoUI.dll"/>
				<Item Name="Thorlabs.MotionControl.Benchtop.StepperMotor.dll" Type="Document" URL="../Thorlabs.MotionControl.Benchtop.StepperMotor.dll"/>
				<Item Name="Thorlabs.MotionControl.Benchtop.StepperMotorCLI.dll" Type="Document" URL="../Thorlabs.MotionControl.Benchtop.StepperMotorCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.Benchtop.StepperMotorUI.dll" Type="Document" URL="../Thorlabs.MotionControl.Benchtop.StepperMotorUI.dll"/>
				<Item Name="Thorlabs.MotionControl.Controls.dll" Type="Document" URL="../Thorlabs.MotionControl.Controls.dll"/>
				<Item Name="Thorlabs.MotionControl.DataLogger.dll" Type="Document" URL="../Thorlabs.MotionControl.DataLogger.dll"/>
				<Item Name="Thorlabs.MotionControl.DeviceManager.dll" Type="Document" URL="../Thorlabs.MotionControl.DeviceManager.dll"/>
				<Item Name="Thorlabs.MotionControl.DeviceManagerCLI.dll" Type="Document" URL="../Thorlabs.MotionControl.DeviceManagerCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.DeviceManagerUI.dll" Type="Document" URL="../Thorlabs.MotionControl.DeviceManagerUI.dll"/>
				<Item Name="Thorlabs.MotionControl.FilterFlipper.dll" Type="Document" URL="../Thorlabs.MotionControl.FilterFlipper.dll"/>
				<Item Name="Thorlabs.MotionControl.FilterFlipperCLI.dll" Type="Document" URL="../Thorlabs.MotionControl.FilterFlipperCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.FilterFlipperUI.dll" Type="Document" URL="../Thorlabs.MotionControl.FilterFlipperUI.dll"/>
				<Item Name="Thorlabs.MotionControl.FTD2xx_Net.dll" Type="Document" URL="../Thorlabs.MotionControl.FTD2xx_Net.dll"/>
				<Item Name="Thorlabs.MotionControl.GenericMotorCLI.dll" Type="Document" URL="../Thorlabs.MotionControl.GenericMotorCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.GenericMotorUI.dll" Type="Document" URL="../Thorlabs.MotionControl.GenericMotorUI.dll"/>
				<Item Name="Thorlabs.MotionControl.GenericNanoTrakCLI.dll" Type="Document" URL="../Thorlabs.MotionControl.GenericNanoTrakCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.GenericNanoTrakUI.dll" Type="Document" URL="../Thorlabs.MotionControl.GenericNanoTrakUI.dll"/>
				<Item Name="Thorlabs.MotionControl.GenericPiezoCLI.dll" Type="Document" URL="../Thorlabs.MotionControl.GenericPiezoCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.GenericPiezoUI.dll" Type="Document" URL="../Thorlabs.MotionControl.GenericPiezoUI.dll"/>
				<Item Name="Thorlabs.MotionControl.IntegratedPrecisionPiezo.dll" Type="Document" URL="../Thorlabs.MotionControl.IntegratedPrecisionPiezo.dll"/>
				<Item Name="Thorlabs.MotionControl.IntegratedPrecisionPiezoCLI.dll" Type="Document" URL="../Thorlabs.MotionControl.IntegratedPrecisionPiezoCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.IntegratedPrecisionPiezoUI.dll" Type="Document" URL="../Thorlabs.MotionControl.IntegratedPrecisionPiezoUI.dll"/>
				<Item Name="Thorlabs.MotionControl.IntegratedStepperMotors.dll" Type="Document" URL="../Thorlabs.MotionControl.IntegratedStepperMotors.dll"/>
				<Item Name="Thorlabs.MotionControl.IntegratedStepperMotorsCLI.dll" Type="Document" URL="../Thorlabs.MotionControl.IntegratedStepperMotorsCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.IntegratedStepperMotorsUI.dll" Type="Document" URL="../Thorlabs.MotionControl.IntegratedStepperMotorsUI.dll"/>
				<Item Name="Thorlabs.MotionControl.Joystick.dll" Type="Document" URL="../Thorlabs.MotionControl.Joystick.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.BrushlessMotor.dll" Type="Document" URL="../Thorlabs.MotionControl.KCube.BrushlessMotor.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.BrushlessMotorCLI.dll" Type="Document" URL="../Thorlabs.MotionControl.KCube.BrushlessMotorCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.BrushlessMotorUI.dll" Type="Document" URL="../Thorlabs.MotionControl.KCube.BrushlessMotorUI.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.DCServo.dll" Type="Document" URL="../Thorlabs.MotionControl.KCube.DCServo.dll"/>
				<Item Name="ThorLabs.MotionControl.KCube.DCServoCLI.dll" Type="Document" URL="../ThorLabs.MotionControl.KCube.DCServoCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.DCServoUI.dll" Type="Document" URL="../Thorlabs.MotionControl.KCube.DCServoUI.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.InertialMotor.dll" Type="Document" URL="../Thorlabs.MotionControl.KCube.InertialMotor.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.InertialMotorCLI.dll" Type="Document" URL="../Thorlabs.MotionControl.KCube.InertialMotorCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.InertialMotorUI.dll" Type="Document" URL="../Thorlabs.MotionControl.KCube.InertialMotorUI.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.LaserDiode.dll" Type="Document" URL="../Thorlabs.MotionControl.KCube.LaserDiode.dll"/>
				<Item Name="ThorLabs.MotionControl.KCube.LaserDiodeCLI.dll" Type="Document" URL="../ThorLabs.MotionControl.KCube.LaserDiodeCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.LaserDiodeUI.dll" Type="Document" URL="../Thorlabs.MotionControl.KCube.LaserDiodeUI.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.LaserSource.dll" Type="Document" URL="../Thorlabs.MotionControl.KCube.LaserSource.dll"/>
				<Item Name="ThorLabs.MotionControl.KCube.LaserSourceCLI.dll" Type="Document" URL="../ThorLabs.MotionControl.KCube.LaserSourceCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.LaserSourceUI.dll" Type="Document" URL="../Thorlabs.MotionControl.KCube.LaserSourceUI.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.LiquidCrystal.dll" Type="Document" URL="../Thorlabs.MotionControl.KCube.LiquidCrystal.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.LiquidCrystalCLI.dll" Type="Document" URL="../Thorlabs.MotionControl.KCube.LiquidCrystalCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.LiquidCrystalUI.dll" Type="Document" URL="../Thorlabs.MotionControl.KCube.LiquidCrystalUI.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.NanoTrak.dll" Type="Document" URL="../Thorlabs.MotionControl.KCube.NanoTrak.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.NanoTrakCLI.dll" Type="Document" URL="../Thorlabs.MotionControl.KCube.NanoTrakCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.NanoTrakUI.dll" Type="Document" URL="../Thorlabs.MotionControl.KCube.NanoTrakUI.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.Piezo.dll" Type="Document" URL="../Thorlabs.MotionControl.KCube.Piezo.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.PiezoCLI.dll" Type="Document" URL="../Thorlabs.MotionControl.KCube.PiezoCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.PiezoUI.dll" Type="Document" URL="../Thorlabs.MotionControl.KCube.PiezoUI.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.PositionAligner.dll" Type="Document" URL="../Thorlabs.MotionControl.KCube.PositionAligner.dll"/>
				<Item Name="ThorLabs.MotionControl.KCube.PositionAlignerCLI.dll" Type="Document" URL="../ThorLabs.MotionControl.KCube.PositionAlignerCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.PositionAlignerUI.dll" Type="Document" URL="../Thorlabs.MotionControl.KCube.PositionAlignerUI.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.Solenoid.dll" Type="Document" URL="../Thorlabs.MotionControl.KCube.Solenoid.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.SolenoidCLI.dll" Type="Document" URL="../Thorlabs.MotionControl.KCube.SolenoidCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.SolenoidUI.dll" Type="Document" URL="../Thorlabs.MotionControl.KCube.SolenoidUI.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.StepperMotor.dll" Type="Document" URL="../Thorlabs.MotionControl.KCube.StepperMotor.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.StepperMotorCLI.dll" Type="Document" URL="../Thorlabs.MotionControl.KCube.StepperMotorCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.StepperMotorUI.dll" Type="Document" URL="../Thorlabs.MotionControl.KCube.StepperMotorUI.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.StrainGauge.dll" Type="Document" URL="../Thorlabs.MotionControl.KCube.StrainGauge.dll"/>
				<Item Name="ThorLabs.MotionControl.KCube.StrainGaugeCLI.dll" Type="Document" URL="../ThorLabs.MotionControl.KCube.StrainGaugeCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.KCube.StrainGaugeUI.dll" Type="Document" URL="../Thorlabs.MotionControl.KCube.StrainGaugeUI.dll"/>
				<Item Name="Thorlabs.MotionControl.ModularRack.dll" Type="Document" URL="../Thorlabs.MotionControl.ModularRack.dll"/>
				<Item Name="Thorlabs.MotionControl.ModularRackCLI.dll" Type="Document" URL="../Thorlabs.MotionControl.ModularRackCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.ModularRackUI.dll" Type="Document" URL="../Thorlabs.MotionControl.ModularRackUI.dll"/>
				<Item Name="Thorlabs.MotionControl.Polarizer.dll" Type="Document" URL="../Thorlabs.MotionControl.Polarizer.dll"/>
				<Item Name="ThorLabs.MotionControl.PolarizerCLI.dll" Type="Document" URL="../ThorLabs.MotionControl.PolarizerCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.PolarizerUI.dll" Type="Document" URL="../Thorlabs.MotionControl.PolarizerUI.dll"/>
				<Item Name="Thorlabs.MotionControl.PrivateInternal.dll" Type="Document" URL="../Thorlabs.MotionControl.PrivateInternal.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.BrushlessMotor.dll" Type="Document" URL="../Thorlabs.MotionControl.TCube.BrushlessMotor.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.BrushlessMotorCLI.dll" Type="Document" URL="../Thorlabs.MotionControl.TCube.BrushlessMotorCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.BrushlessMotorUI.dll" Type="Document" URL="../Thorlabs.MotionControl.TCube.BrushlessMotorUI.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.DCServo.dll" Type="Document" URL="../Thorlabs.MotionControl.TCube.DCServo.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.DCServoCLI.dll" Type="Document" URL="../Thorlabs.MotionControl.TCube.DCServoCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.DCServoUI.dll" Type="Document" URL="../Thorlabs.MotionControl.TCube.DCServoUI.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.InertialMotor.dll" Type="Document" URL="../Thorlabs.MotionControl.TCube.InertialMotor.dll"/>
				<Item Name="ThorLabs.MotionControl.TCube.InertialMotorCLI.dll" Type="Document" URL="../ThorLabs.MotionControl.TCube.InertialMotorCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.InertialMotorUI.dll" Type="Document" URL="../Thorlabs.MotionControl.TCube.InertialMotorUI.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.LaserDiode.dll" Type="Document" URL="../Thorlabs.MotionControl.TCube.LaserDiode.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.LaserDiodeCLI.dll" Type="Document" URL="../Thorlabs.MotionControl.TCube.LaserDiodeCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.LaserDiodeUI.dll" Type="Document" URL="../Thorlabs.MotionControl.TCube.LaserDiodeUI.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.LaserSource.dll" Type="Document" URL="../Thorlabs.MotionControl.TCube.LaserSource.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.LaserSourceCLI.dll" Type="Document" URL="../Thorlabs.MotionControl.TCube.LaserSourceCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.LaserSourceUI.dll" Type="Document" URL="../Thorlabs.MotionControl.TCube.LaserSourceUI.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.NanoTrak.dll" Type="Document" URL="../Thorlabs.MotionControl.TCube.NanoTrak.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.NanoTrakCLI.dll" Type="Document" URL="../Thorlabs.MotionControl.TCube.NanoTrakCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.NanoTrakUI.dll" Type="Document" URL="../Thorlabs.MotionControl.TCube.NanoTrakUI.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.Piezo.dll" Type="Document" URL="../Thorlabs.MotionControl.TCube.Piezo.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.PiezoCLI.dll" Type="Document" URL="../Thorlabs.MotionControl.TCube.PiezoCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.PiezoUI.dll" Type="Document" URL="../Thorlabs.MotionControl.TCube.PiezoUI.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.Quad.dll" Type="Document" URL="../Thorlabs.MotionControl.TCube.Quad.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.QuadCLI.dll" Type="Document" URL="../Thorlabs.MotionControl.TCube.QuadCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.QuadUI.dll" Type="Document" URL="../Thorlabs.MotionControl.TCube.QuadUI.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.Solenoid.dll" Type="Document" URL="../Thorlabs.MotionControl.TCube.Solenoid.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.SolenoidCLI.dll" Type="Document" URL="../Thorlabs.MotionControl.TCube.SolenoidCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.SolenoidUI.dll" Type="Document" URL="../Thorlabs.MotionControl.TCube.SolenoidUI.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.StepperMotor.dll" Type="Document" URL="../Thorlabs.MotionControl.TCube.StepperMotor.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.StepperMotorCLI.dll" Type="Document" URL="../Thorlabs.MotionControl.TCube.StepperMotorCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.StepperMotorUI.dll" Type="Document" URL="../Thorlabs.MotionControl.TCube.StepperMotorUI.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.StrainGauge.dll" Type="Document" URL="../Thorlabs.MotionControl.TCube.StrainGauge.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.StrainGaugeCLI.dll" Type="Document" URL="../Thorlabs.MotionControl.TCube.StrainGaugeCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.StrainGaugeUI.dll" Type="Document" URL="../Thorlabs.MotionControl.TCube.StrainGaugeUI.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.TEC.dll" Type="Document" URL="../Thorlabs.MotionControl.TCube.TEC.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.TECCLI.dll" Type="Document" URL="../Thorlabs.MotionControl.TCube.TECCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.TCube.TECUI.dll" Type="Document" URL="../Thorlabs.MotionControl.TCube.TECUI.dll"/>
				<Item Name="Thorlabs.MotionControl.TDIEngine.dll" Type="Document" URL="../Thorlabs.MotionControl.TDIEngine.dll"/>
				<Item Name="ThorLabs.MotionControl.TDIEngineCLI.dll" Type="Document" URL="../ThorLabs.MotionControl.TDIEngineCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.TDIEngineUI.dll" Type="Document" URL="../Thorlabs.MotionControl.TDIEngineUI.dll"/>
				<Item Name="Thorlabs.MotionControl.Tools.Common.dll" Type="Document" URL="../Thorlabs.MotionControl.Tools.Common.dll"/>
				<Item Name="Thorlabs.MotionControl.Tools.Logging.dll" Type="Document" URL="../Thorlabs.MotionControl.Tools.Logging.dll"/>
				<Item Name="Thorlabs.MotionControl.Tools.WPF.dll" Type="Document" URL="../Thorlabs.MotionControl.Tools.WPF.dll"/>
				<Item Name="Thorlabs.MotionControl.Tools.WPF.UI.dll" Type="Document" URL="../Thorlabs.MotionControl.Tools.WPF.UI.dll"/>
				<Item Name="Thorlabs.MotionControl.VerticalStage.dll" Type="Document" URL="../Thorlabs.MotionControl.VerticalStage.dll"/>
				<Item Name="ThorLabs.MotionControl.VerticalStageCLI.dll" Type="Document" URL="../ThorLabs.MotionControl.VerticalStageCLI.dll"/>
				<Item Name="Thorlabs.MotionControl.VerticalStageUI.dll" Type="Document" URL="../Thorlabs.MotionControl.VerticalStageUI.dll"/>
				<Item Name="Xceed.Wpf.Toolkit.dll" Type="Document" URL="../Xceed.Wpf.Toolkit.dll"/>
			</Item>
			<Item Name="Waveform Spreadsheets" Type="Folder">
				<Item Name="TEST FILE.xlsx" Type="Document" URL="../../Waveform Spreadsheets/TEST FILE.xlsx"/>
			</Item>
			<Item Name="Close.vi" Type="VI" URL="../../Close.vi"/>
			<Item Name="Count Start.vi" Type="VI" URL="../../Count Start.vi"/>
			<Item Name="Count Stop.vi" Type="VI" URL="../../Count Stop.vi"/>
			<Item Name="Demo Main.vi" Type="VI" URL="../../Demo Main.vi"/>
			<Item Name="DemoProject.aliases" Type="Document" URL="../../DemoProject.aliases"/>
			<Item Name="DemoProject.lvlps" Type="Document" URL="../../DemoProject.lvlps"/>
			<Item Name="DemoProject.lvproj" Type="Document" URL="../../DemoProject.lvproj"/>
			<Item Name="H11890api.dll" Type="Document" URL="../../H11890api.dll"/>
			<Item Name="H11890api.h" Type="Document" URL="../../H11890api.h"/>
			<Item Name="H11890api.lib" Type="Document" URL="../../H11890api.lib"/>
			<Item Name="H11890api.lvlib" Type="Library" URL="../../H11890api.lvlib"/>
			<Item Name="Logo.ctl" Type="VI" URL="../../Logo.ctl"/>
			<Item Name="Open.vi" Type="VI" URL="../../Open.vi"/>
			<Item Name="Read Data.vi" Type="VI" URL="../../Read Data.vi"/>
			<Item Name="Read HV.vi" Type="VI" URL="../../Read HV.vi"/>
			<Item Name="Read IT.vi" Type="VI" URL="../../Read IT.vi"/>
			<Item Name="Read RN.vi" Type="VI" URL="../../Read RN.vi"/>
			<Item Name="Set HV.vi" Type="VI" URL="../../Set HV.vi"/>
			<Item Name="Set IT.vi" Type="VI" URL="../../Set IT.vi"/>
			<Item Name="Set RN.vi" Type="VI" URL="../../Set RN.vi"/>
			<Item Name="SM_CaseErase.vi" Type="VI" URL="../../SM_CaseErase.vi"/>
			<Item Name="SM_CaseSelect.vi" Type="VI" URL="../../SM_CaseSelect.vi"/>
			<Item Name="SM_Template.vi" Type="VI" URL="../../SM_Template.vi"/>
			<Item Name="test 1_ outside while loop" Type="Document" URL="../../test 1_ outside while loop"/>
			<Item Name="test 2_inside check number" Type="Document" URL="../../test 2_inside check number"/>
		</Item>
		<Item Name="Dependencies" Type="Dependencies">
			<Item Name="vi.lib" Type="Folder">
				<Item Name="NI_AALBase.lvlib" Type="Library" URL="/&lt;vilib&gt;/Analysis/NI_AALBase.lvlib"/>
				<Item Name="NI_MABase.lvlib" Type="Library" URL="/&lt;vilib&gt;/measure/NI_MABase.lvlib"/>
				<Item Name="Write Delimited Spreadsheet (DBL).vi" Type="VI" URL="/&lt;vilib&gt;/Utility/file.llb/Write Delimited Spreadsheet (DBL).vi"/>
				<Item Name="Write Delimited Spreadsheet (I64).vi" Type="VI" URL="/&lt;vilib&gt;/Utility/file.llb/Write Delimited Spreadsheet (I64).vi"/>
				<Item Name="Write Delimited Spreadsheet (string).vi" Type="VI" URL="/&lt;vilib&gt;/Utility/file.llb/Write Delimited Spreadsheet (string).vi"/>
				<Item Name="Write Delimited Spreadsheet.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/file.llb/Write Delimited Spreadsheet.vi"/>
				<Item Name="Write Spreadsheet String.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/file.llb/Write Spreadsheet String.vi"/>
			</Item>
			<Item Name="???.rtm" Type="Document" URL="../../???.rtm"/>
			<Item Name="lvanlys.dll" Type="Document" URL="/&lt;resource&gt;/lvanlys.dll"/>
			<Item Name="mscorlib" Type="VI" URL="mscorlib">
				<Property Name="NI.PreserveRelativePath" Type="Bool">true</Property>
			</Item>
			<Item Name="Thorlabs.MotionControl.Benchtop.BrushlessMotorCLI.dll" Type="Document" URL="/U/Kinesis LabVIEW Website Examples/Thorlabs.MotionControl.Benchtop.BrushlessMotorCLI.dll"/>
			<Item Name="Thorlabs.MotionControl.Benchtop.NanoTrakCLI.dll" Type="Document" URL="/U/Kinesis LabVIEW Website Examples/Thorlabs.MotionControl.Benchtop.NanoTrakCLI.dll"/>
			<Item Name="Thorlabs.MotionControl.Benchtop.PiezoCLI.dll" Type="Document" URL="/U/Software Training Plan/Software Training Day 2 - Thursday/Kinesis_with_LabVIEW_Examples_LV12 - v2/Thorlabs.MotionControl.Benchtop.PiezoCLI.dll"/>
			<Item Name="Thorlabs.MotionControl.Controls.dll" Type="Document" URL="/U/Kinesis LabVIEW Website Examples/Thorlabs.MotionControl.Controls.dll"/>
			<Item Name="Thorlabs.MotionControl.Controls.dll" Type="Document" URL="/U/Software Training Plan/Software Training Day 2 - Thursday/Kinesis_with_LabVIEW_Examples_LV12 - v2/Thorlabs.MotionControl.Controls.dll"/>
			<Item Name="Thorlabs.MotionControl.DeviceManagerCLI.dll" Type="Document" URL="/U/Kinesis LabVIEW Website Examples/Thorlabs.MotionControl.DeviceManagerCLI.dll"/>
			<Item Name="Thorlabs.MotionControl.GenericMotorCLI.dll" Type="Document" URL="/U/Kinesis LabVIEW Website Examples/Thorlabs.MotionControl.GenericMotorCLI.dll"/>
			<Item Name="Thorlabs.MotionControl.GenericNanoTrakCLI.dll" Type="Document" URL="/U/Kinesis LabVIEW Website Examples/Thorlabs.MotionControl.GenericNanoTrakCLI.dll"/>
			<Item Name="Thorlabs.MotionControl.KCube.BrushlessMotorCLI.dll" Type="Document" URL="/U/Kinesis LabVIEW Website Examples/Thorlabs.MotionControl.KCube.BrushlessMotorCLI.dll"/>
			<Item Name="ThorLabs.MotionControl.KCube.LaserSourceCLI.dll" Type="Document" URL="/U/Kinesis LabVIEW Website Examples/ThorLabs.MotionControl.KCube.LaserSourceCLI.dll"/>
			<Item Name="Thorlabs.MotionControl.KCube.SolenoidCLI.dll" Type="Document" URL="/U/Kinesis LabVIEW Website Examples/Thorlabs.MotionControl.KCube.SolenoidCLI.dll"/>
			<Item Name="Thorlabs.MotionControl.KCube.StepperMotorCLI.dll" Type="Document" URL="/U/Kinesis LabVIEW Website Examples/Thorlabs.MotionControl.KCube.StepperMotorCLI.dll"/>
			<Item Name="ThorLabs.MotionControl.KCube.StrainGaugeCLI.dll" Type="Document" URL="/U/Kinesis LabVIEW Website Examples/ThorLabs.MotionControl.KCube.StrainGaugeCLI.dll"/>
			<Item Name="Thorlabs.MotionControl.ModularRackCLI.dll" Type="Document" URL="/U/Kinesis LabVIEW Website Examples/Thorlabs.MotionControl.ModularRackCLI.dll"/>
		</Item>
		<Item Name="Build Specifications" Type="Build"/>
	</Item>
</Project>
