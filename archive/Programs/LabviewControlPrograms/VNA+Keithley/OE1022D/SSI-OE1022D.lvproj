<?xml version='1.0' encoding='UTF-8'?>
<Project Type="Project" LVVersion="21008000">
	<Item Name="我的电脑" Type="My Computer">
		<Property Name="server.app.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.control.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.tcp.enabled" Type="Bool">false</Property>
		<Property Name="server.tcp.port" Type="Int">0</Property>
		<Property Name="server.tcp.serviceName" Type="Str">我的电脑/VI服务器</Property>
		<Property Name="server.tcp.serviceName.default" Type="Str">我的电脑/VI服务器</Property>
		<Property Name="server.vi.callsEnabled" Type="Bool">true</Property>
		<Property Name="server.vi.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="specify.custom.address" Type="Bool">false</Property>
		<Item Name="sub" Type="Folder">
			<Item Name="OE1022D_Auto_Gain.vi" Type="VI" URL="/&lt;instrlib&gt;/OE1022D/Sub VI/OE1022D_Auto_Gain.vi"/>
			<Item Name="OE1022D_Auto_Phase.vi" Type="VI" URL="/&lt;instrlib&gt;/OE1022D/Sub VI/OE1022D_Auto_Phase.vi"/>
			<Item Name="OE1022D_Auto_Reserve.vi" Type="VI" URL="/&lt;instrlib&gt;/OE1022D/Sub VI/OE1022D_Auto_Reserve.vi"/>
			<Item Name="OE1022D_Auto_Scale.vi" Type="VI" URL="/&lt;instrlib&gt;/OE1022D/Sub VI/OE1022D_Auto_Scale.vi"/>
			<Item Name="OE1022D_Close.vi" Type="VI" URL="/&lt;instrlib&gt;/OE1022D/Sub VI/OE1022D_Close.vi"/>
			<Item Name="OE1022D_Configure Dynamic Reserve.vi" Type="VI" URL="/&lt;instrlib&gt;/OE1022D/Sub VI/OE1022D_Configure Dynamic Reserve.vi"/>
			<Item Name="OE1022D_Configure Filter.vi" Type="VI" URL="/&lt;instrlib&gt;/OE1022D/Sub VI/OE1022D_Configure Filter.vi"/>
			<Item Name="OE1022D_Configure Frequency.vi" Type="VI" URL="/&lt;instrlib&gt;/OE1022D/Sub VI/OE1022D_Configure Frequency.vi"/>
			<Item Name="OE1022D_Configure Harmonic.vi" Type="VI" URL="/&lt;instrlib&gt;/OE1022D/Sub VI/OE1022D_Configure Harmonic.vi"/>
			<Item Name="OE1022D_Configure Input Filter.vi" Type="VI" URL="/&lt;instrlib&gt;/OE1022D/Sub VI/OE1022D_Configure Input Filter.vi"/>
			<Item Name="OE1022D_Configure Ref Phase Channel A.vi" Type="VI" URL="/&lt;instrlib&gt;/OE1022D/Sub VI/OE1022D_Configure Ref Phase Channel A.vi"/>
			<Item Name="OE1022D_Configure Ref Phase Channel B.vi" Type="VI" URL="/&lt;instrlib&gt;/OE1022D/Sub VI/OE1022D_Configure Ref Phase Channel B.vi"/>
			<Item Name="OE1022D_Configure Reference Source.vi" Type="VI" URL="/&lt;instrlib&gt;/OE1022D/Sub VI/OE1022D_Configure Reference Source.vi"/>
			<Item Name="OE1022D_Configure Sensitivity.vi" Type="VI" URL="/&lt;instrlib&gt;/OE1022D/Sub VI/OE1022D_Configure Sensitivity.vi"/>
			<Item Name="OE1022D_Configure Sine Out Channel B.vi" Type="VI" URL="/&lt;instrlib&gt;/OE1022D/Sub VI/OE1022D_Configure Sine Out Channel B.vi"/>
			<Item Name="OE1022D_Configure Sine Out.vi" Type="VI" URL="/&lt;instrlib&gt;/OE1022D/Sub VI/OE1022D_Configure Sine Out.vi"/>
			<Item Name="OE1022D_Configure_Channel_Out.vi" Type="VI" URL="/&lt;instrlib&gt;/OE1022D/Sub VI/OE1022D_Configure_Channel_Out.vi"/>
			<Item Name="OE1022D_Configure_Setting.vi" Type="VI" URL="/&lt;instrlib&gt;/OE1022D/Sub VI/OE1022D_Configure_Setting.vi"/>
			<Item Name="OE1022D_Query_IDN.vi" Type="VI" URL="/&lt;instrlib&gt;/OE1022D/Sub VI/OE1022D_Query_IDN.vi"/>
			<Item Name="OE1022D_Read_Buffer.vi" Type="VI" URL="/&lt;instrlib&gt;/OE1022D/Sub VI/OE1022D_Read_Buffer.vi"/>
			<Item Name="OE1022D_Read_Data.vi" Type="VI" URL="/&lt;instrlib&gt;/OE1022D/Sub VI/OE1022D_Read_Data.vi"/>
			<Item Name="OE1022D_Read_MultiData.vi" Type="VI" URL="/&lt;instrlib&gt;/OE1022D/Sub VI/OE1022D_Read_MultiData.vi"/>
			<Item Name="OE1022D_Reset.vi" Type="VI" URL="/&lt;instrlib&gt;/OE1022D/Sub VI/OE1022D_Reset.vi"/>
		</Item>
		<Item Name="OE1022D Example All Data.vi" Type="VI" URL="/&lt;instrlib&gt;/OE1022D/OE1022D Example All Data.vi"/>
		<Item Name="Tree.vi" Type="VI" URL="/&lt;instrlib&gt;/OE1022D/Sub VI/Tree.vi"/>
		<Item Name="依赖关系" Type="Dependencies">
			<Item Name="instr.lib" Type="Folder">
				<Item Name="DataTransmit.vi" Type="VI" URL="/&lt;instrlib&gt;/OE1022D/Sub VI/DataTransmit.vi"/>
				<Item Name="DataType.ctl" Type="VI" URL="/&lt;instrlib&gt;/OE1022D/Sub VI/DataType.ctl"/>
				<Item Name="MulMean.vi" Type="VI" URL="/&lt;instrlib&gt;/OE1022D/Sub VI/MulMean.vi"/>
				<Item Name="OE1022D_OpenDevice.vi" Type="VI" URL="/&lt;instrlib&gt;/OE1022D/Sub VI/OE1022D_OpenDevice.vi"/>
				<Item Name="OE1022D_Query_Data.vi" Type="VI" URL="/&lt;instrlib&gt;/OE1022D/Sub VI/OE1022D_Query_Data.vi"/>
				<Item Name="OE1022D_Read 1 parameter_mean.vi" Type="VI" URL="/&lt;instrlib&gt;/OE1022D/Sub VI/OE1022D_Read 1 parameter_mean.vi"/>
				<Item Name="OE1022D_Read 1 parameter_stable.vi" Type="VI" URL="/&lt;instrlib&gt;/OE1022D/Sub VI/OE1022D_Read 1 parameter_stable.vi"/>
				<Item Name="OE1022DRandXita.vi" Type="VI" URL="/&lt;instrlib&gt;/OE1022D/Sub VI/OE1022DRandXita.vi"/>
			</Item>
			<Item Name="vi.lib" Type="Folder">
				<Item Name="NI_AALBase.lvlib" Type="Library" URL="/&lt;vilib&gt;/Analysis/NI_AALBase.lvlib"/>
				<Item Name="VISA Configure Serial Port" Type="VI" URL="/&lt;vilib&gt;/Instr/_visa.llb/VISA Configure Serial Port"/>
				<Item Name="VISA Configure Serial Port (Instr).vi" Type="VI" URL="/&lt;vilib&gt;/Instr/_visa.llb/VISA Configure Serial Port (Instr).vi"/>
				<Item Name="VISA Configure Serial Port (Serial Instr).vi" Type="VI" URL="/&lt;vilib&gt;/Instr/_visa.llb/VISA Configure Serial Port (Serial Instr).vi"/>
				<Item Name="VISA Flush IO Buffer Mask.ctl" Type="VI" URL="/&lt;vilib&gt;/Instr/_visa.llb/VISA Flush IO Buffer Mask.ctl"/>
			</Item>
			<Item Name="lvanlys.dll" Type="Document" URL="/&lt;resource&gt;/lvanlys.dll"/>
		</Item>
		<Item Name="程序生成规范" Type="Build">
			<Item Name="中大科仪-OE1022D库文件" Type="Source Distribution">
				<Property Name="Bld_buildCacheID" Type="Str">{5232951A-BA82-4487-8583-C3BC3C731CF3}</Property>
				<Property Name="Bld_buildSpecName" Type="Str">中大科仪-OE1022D库文件</Property>
				<Property Name="Bld_defaultLanguage" Type="Str">ChineseS</Property>
				<Property Name="Bld_excludedDirectory[0]" Type="Path">vi.lib</Property>
				<Property Name="Bld_excludedDirectory[0].pathType" Type="Str">relativeToAppDir</Property>
				<Property Name="Bld_excludedDirectory[1]" Type="Path">resource/objmgr</Property>
				<Property Name="Bld_excludedDirectory[1].pathType" Type="Str">relativeToAppDir</Property>
				<Property Name="Bld_excludedDirectory[2]" Type="Path">/D/windows/file/LabVIEW Data/InstCache</Property>
				<Property Name="Bld_excludedDirectoryCount" Type="Int">3</Property>
				<Property Name="Bld_localDestDir" Type="Path">../MY</Property>
				<Property Name="Bld_localDestDirType" Type="Str">relativeToCommon</Property>
				<Property Name="Bld_previewCacheID" Type="Str">{090D82E3-E587-47AE-A869-55C365D6C6A5}</Property>
				<Property Name="Bld_version.major" Type="Int">1</Property>
				<Property Name="Destination[0].destName" Type="Str">目标目录</Property>
				<Property Name="Destination[0].libraryName" Type="Str">中大科仪 OE1022D 库文件.lvlib</Property>
				<Property Name="Destination[0].path" Type="Path">../MY</Property>
				<Property Name="Destination[0].preserveHierarchy" Type="Bool">true</Property>
				<Property Name="Destination[1].destName" Type="Str">支持目录</Property>
				<Property Name="Destination[1].path" Type="Path">../MY/data</Property>
				<Property Name="DestinationCount" Type="Int">2</Property>
				<Property Name="Source[0].itemID" Type="Str">{4AF90070-4196-43E6-976E-3FE8FB152226}</Property>
				<Property Name="Source[0].properties[0].type" Type="Str">Remove front panel</Property>
				<Property Name="Source[0].properties[0].value" Type="Bool">false</Property>
				<Property Name="Source[0].properties[1].type" Type="Str">Remove block diagram</Property>
				<Property Name="Source[0].properties[1].value" Type="Bool">true</Property>
				<Property Name="Source[0].properties[2].type" Type="Str">Password</Property>
				<Property Name="Source[0].properties[2].value" Type="Str">c3Npb2UxMDIyZA==</Property>
				<Property Name="Source[0].propertiesCount" Type="Int">3</Property>
				<Property Name="Source[0].type" Type="Str">Container</Property>
				<Property Name="Source[1].destinationIndex" Type="Int">0</Property>
				<Property Name="Source[1].itemID" Type="Ref"></Property>
				<Property Name="Source[1].sourceInclusion" Type="Str">Include</Property>
				<Property Name="Source[1].type" Type="Str">VI</Property>
				<Property Name="Source[2].destinationIndex" Type="Int">0</Property>
				<Property Name="Source[2].itemID" Type="Ref"></Property>
				<Property Name="Source[2].sourceInclusion" Type="Str">Include</Property>
				<Property Name="Source[2].type" Type="Str">VI</Property>
				<Property Name="Source[3].destinationIndex" Type="Int">0</Property>
				<Property Name="Source[3].itemID" Type="Ref">/我的电脑/Tree.vi</Property>
				<Property Name="Source[3].sourceInclusion" Type="Str">Include</Property>
				<Property Name="Source[3].type" Type="Str">VI</Property>
				<Property Name="Source[4].Container.applyInclusion" Type="Bool">true</Property>
				<Property Name="Source[4].Container.applyPassword" Type="Bool">true</Property>
				<Property Name="Source[4].destinationIndex" Type="Int">0</Property>
				<Property Name="Source[4].itemID" Type="Ref">/我的电脑/sub</Property>
				<Property Name="Source[4].properties[0].type" Type="Str">Password</Property>
				<Property Name="Source[4].properties[0].value" Type="Str">c3Npb2UxMDIyZA==</Property>
				<Property Name="Source[4].propertiesCount" Type="Int">1</Property>
				<Property Name="Source[4].sourceInclusion" Type="Str">Include</Property>
				<Property Name="Source[4].type" Type="Str">Container</Property>
				<Property Name="SourceCount" Type="Int">5</Property>
			</Item>
		</Item>
	</Item>
</Project>
