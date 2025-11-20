------------------------------------------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------INSTRUCTIONS FOR SETTING UP EBRICK--------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------------------------------------
Step 1:	Install the version of Silicon Compiler 34.3. Follow the installation instructions from the link:
	https://docs.siliconcompiler.com/en/v0.34.3/user_guide/installation.html
	And especially the 'Install from GitHub Repo (Linux/MacOS)' section. See the Silicon Compiler README .txt before using 
	ebrick demo.

Step 2:	Download the Verilator and Surelog tools if you haven't download them in the previous step. The install scripts located in:
	/siliconcompiler/siliconcompiler/toolscripts/ubuntu24/install-verilator.sh	
	/siliconcompiler/siliconcompiler/toolscripts/ubuntu24/install-surelog.sh
	For Ubuntu 24 setup.

Step 3:	Download the RISCV-GNU-Toolchain from the proper tar.xz file located in the link:
	https://github.com/riscv-collab/riscv-gnu-toolchain/releases
	Follow the commands:
	- cd /home (go to your home directory)
	- wget <URL_to_your_file>.tar.xz (download the tar.xz. Recommended the 'riscv64-elf-ubuntu-24.04-gcc.tar.xz' pack)
	- tar -xJf riscv64-elf-ubuntu-24.04-gcc.tar.xz -C /opt (Unpack the file and move it into /opt folder.)
	- echo 'export PATH=$PATH:/opt/riscv/bin' >> ~/.bashrc (add this into the ./bashrc file)
`	 - source ~/.bashrc (Run the modified ./bashrc)
	- which riscv64-elf-ubuntu-24.04-gcc (The final phase is to confirm that the installation and integration were successful.)

Step 4:	Install the ebrick essentials with the 'pip' command described in: https://github.com/zeroasiccorp/ebrick-demo.

Step 5:	Delete the silicon compiler 29.0 that has been downloaded inside the folder: 
	/work/venv/lib64/python3.12/site-packages/
	And its siliconcompiler-0.29.0.dist-info file also. Check if the 34.3 version works with  'sc -version' command.	

Step 6:	If a Verilator problem occurs that can't understand its version, install the locals using the command:
	apt-get update && apt-get install -y locales && locale-gen en_US.UTF-8 && update-locale LANG=en_US.UTF-8

Step 7:	If any problem occurs with not finding the proper version of RISCV-GNU-Toolchain check the file 
	'/ebrick-demo/ebrick_demo/testbench/program/riscv.py' for the correct prefix arg.

------------------------------------------------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------AXI4-Lite Protocol Signals-----------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------------------------------------
The AXI4-Lite plays a crucial role in ebrick design. More specifically, the rtl-designs produced by HLS, have integrated the AXI4-Lite 
protocol in them. The UMI library can then transform the AXI protocol into UMI protocol used by the E-BRICK for chiplet design. A
table with all the AXI4-Lite signals is presented below:

- M_AXI_ denotes the Master's signals and S_AXI_  the Slave's to make the distinction clear.
- N refers to the address width (e.g., 32-bits).
- M refers to the data width (e.g., 32-bits for the PicoRV32 processor).

AXI4-LITE MASTER INTERFACE SIGNALS  
Signal Type		Signal Name	Bits		Direction		Description
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Global Signals		M_AXI_ACLK	1		Input		Clock. All signals are synchronous to the rising edge of this clock.
Global Signals		M_AXI_ARESETN	1		Input		Active-Low Reset. Resets the master interface.
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Write Address Channel	M_AXI_AWVALID	1		Output		Write Address Valid. Driven by the Master to indicate a valid write address and control information is available.
Write Address Channel	M_AXI_AWREADY	1		Input		Write Address Ready. Driven by the Slave to indicate it is ready to accept a write address.
Write Address Channel	M_AXI_AWADDR	[N-1:0]		Output		Write Address. The address for the write transaction.
Write Address Channel	M_AXI_AWPROT	[2:0]		Output		Write Protection Type. Describes privilege, security, and access type.
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Write Data Channel		M_AXI_WVALID	1		Output		Write Data Valid. Driven by the Master to indicate that valid write data and strobes are available.
Write Data Channel		M_AXI_WREADY	1		Input		Write Data Ready. Driven by the Slave to indicate it is ready to accept write data.
Write Data Channel		M_AXI_WDATA	[M-1:0]		Output		Write Data. The data to be written to the slave.
Write Data Channel		M_AXI_WSTRB	[M/8-1:0]	Output		Write Strobes. Byte-enables for WDATA. WSTRB[i] corresponds to WDATA[(8*i)+7 : 8*i]
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Write Response Channel	M_AXI_BVALID	1		Input		Write Response Valid. Driven by the Slave to indicate a valid write response is available.
Write Response Channel	M_AXI_BREADY	1		Output		Write Response Ready. Driven by the Master to indicate it is ready to accept a write response.
Write Response Channel	M_AXI_BRESP	[1:0]		Input		Write Response. Status of the write transaction (e.g., 00=OKAY, 10=SLVERR).
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Read Address Channel	M_AXI_ARVALID	1		Output		Read Address Valid. Driven by the Master to indicate a valid read address and control information is available.
Read Address Channel	M_AXI_ARREADY	1		Input		Read Address Ready. Driven by the Slave to indicate it is ready to accept a read address.
Read Address Channel	M_AXI_ARADDR	[N-1:0]		Output		Read Address. The address for the read transaction.
Read Address Channel	M_AXI_ARPROT	[2:0]		Output		Read Protection Type. Describes privilege, security, and access type.
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Read Data Channel		M_AXI_RVALID	1		Input		Read Data Valid. Driven by the Slave to indicate that valid read data is available.
Read Data Channel		M_AXI_RREADY	1		Output		Read Data Ready. Driven by the Master to indicate it is ready to accept the read data.
Read Data Channel		M_AXI_RDATA	[M-1:0]		Input		Read Data. The data read from the slave.
Read Data Channel		M_AXI_RRESP	[1:0]		Input		ead Response. Status of the read transaction (e.g., 00=OKAY, 10=SLVERR).

AXI4-LITE SLAVE INTERFACE SIGNALS  
Signal Type		Signal Name	Bits		Direction		Description
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Global Signals		S_AXI_ACLK	1		Input		Clock. All signals are synchronous to the rising edge of this clock.
Global Signals		S_AXI_ARESETN	1		Input		Active-Low Reset. Resets the slave interface.
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Write Address Channel	S_AXI_AWVALID	1		Input		Write Address Valid. Driven by the Master to indicate a valid write address and control information is available.
Write Address Channel	S_AXI_AWREADY	1		Output		Write Address Ready. Driven by the Slave to indicate it is ready to accept a write address.
Write Address Channel	S_AXI_AWADDR	[N-1:0]		Input		Write Address. The address for the write transaction.
Write Address Channel	S_AXI_AWPROT	[2:0]		Input		Write Protection Type. Describes privilege, security, and access type.
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Write Data Channel		S_AXI_WVALID	1		Input		Write Data Valid. Driven by the Master to indicate that valid write data and strobes are available.
Write Data Channel		S_AXI_WREADY	1		Output		Write Data Ready. Driven by the Slave to indicate it is ready to accept write data.
Write Data Channel		S_AXI_WDATA	[M-1:0]		Input		Write Data. The data to be written to the slave.
Write Data Channel		S_AXI_WSTRB	[M/8-1:0]	Input		Write Strobes. Byte-enables for WDATA. WSTRB[i] corresponds to WDATA[(8*i)+7 : 8*i].
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Write Response Channel	S_AXI_BVALID	1		Output		Write Response Valid. Driven by the Slave to indicate a valid write response is available.
Write Response Channel	S_AXI_BREADY	1		Input		Write Response Ready. Driven by the Master to indicate it is ready to accept a write response.
Write Response Channel	S_AXI_BRESP	[1:0]		Output		Write Response. Status of the write transaction (e.g., 00=OKAY, 10=SLVERR).
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Read Address Channel	S_AXI_ARVALID	1		Input		Read Address Valid. Driven by the Master to indicate a valid read address and control information is available.
Read Address Channel	S_AXI_ARREADY	1		Output		Read Address Ready. Driven by the Slave to indicate it is ready to accept a read address.
Read Address Channel	S_AXI_ARADDR	[N-1:0]		Input		Read Address. The address for the read transaction.
Read Address Channel	S_AXI_ARPROT	[2:0]		Input		Read Protection Type. Describes privilege, security, and access type.
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Read Data Channel		S_AXI_RVALID	1	Output	Read Data Valid. Driven by the Slave to indicate that valid read data is available.
Read Data Channel		S_AXI_RREADY	1	Input	Read Data Ready. Driven by the Master to indicate it is ready to accept the read data.
Read Data Channel		S_AXI_RDATA	[M-1:0]	Output	Read Data. The data read from the slave.
Read Data Channel		S_AXI_RRESP	[1:0]	Output	Read Response. Status of the read transaction (e.g., 00=OKAY, 10=SLVERR).

We can easily observe that the signals are paired. Every category has a Master-Slave signal pair in order to enstablish an efficient communication between these two devices. 

------------------------------------------------------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------CLINKS Explaination---------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------------------------------------
A CLINK (Chiplet Link) is the fundamental, standardized I/O port for a single ebrick chiplet. It serves as both the physical and logical building block for all communication between 
chiplets. An ebrick-core is a seperate chiple, and CLINK define many key characteristics of this chiplet:
- Physical Definition: A CLINK occupies a standard 1x1 mm square area on the chiplet's surface. A single chiplet is defined as a W x H grid of CLINKs (e.g., a 2x2 chiplet has 4 CLINKs).
- Logical Functionality: Each CLINK contains a complete, independent UMI interface. It also contains resources for other I/O like GPIO and analog signals.
- Architectural Purpose: The primary goal of the CLINK is to enable modularity and scalability. 

If we have a chiplet that need to communicate with 2 devices, it is not necessary to create 2 CLINKS. With the UMI protocol, the chiplet can communicate with all the other devices, by
using the proper address. Having multiple CLINKs on a single chiplet is a strategy for achieving high performance through parallelism. It is not about the number of devices you can talk to.
- Massive Bandwidth Increase: The total data throughput of a chiplet is the bandwidth of one CLINK multiplied by the number of CLINKs.
- Simultaneous Communication: Multiple CLINKs allow a chiplet to communicate with multiple neighbors at the exact same time, which is essential for efficient routing in a complex network of chiplets.

In summary, a CLINK is a port not a wire. The number of CLINKs on a chiplet defines its I/O capacity and parallel communication capability, not the number of other chiplets it can address.
	<----------------- W=2 mm ----------------->
  ^   	+----------------------	+-----------+----------+
  |   	|           	     	|           		|
  |  	|      CLINK[0,0]	|        CLINK[0,1]	|
  |   	|           		|           		|
H=2mm   	+----------------------	+-----------+----------+
  | 	|           		|           		|
  |      	|      CLINK[1,0]	|        CLINK[1,1]	|
  |      	|           		|           		|
  v      	+----------------------	+-----------+----------+

------------------------------------------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------UMI Protocol Signals--------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------------------------------------
The UMI protocol has some parameters that they are fundamental to understanding the size and shape of all the UMI ports:

Parameter	Full Name	Default Value	Description
W		Brick Width	2		The width of the chiplet in mm, setting the number of CLINKs on the X-axis.
H		Brick Height	2		The height of the chiplet in mm, setting the number of CLINKs on the Y-axis.
CW		Command Width	32		The number of bits in the UMI packet's command field.
AW		Address Width	64		The number of bits in the UMI packet's address fields (dstaddr, srcaddr).
DW		Data Width	32		The number of bits in the UMI packet's data payload field.
IDW		Chip ID Width	16		Crucial for Networking. Defines the number of bits used for the unique chiplet ID within the UMI address. 
RW		Register Width	32		Defines the width of the generic ctrl and status ports. This provides a simple, non-UMI way to control or get status from the core. For example, status[0] is the CPU's trap signal.

An example of a huge-port declaration, like output [W*H*DW-1:0] uhost_req_data, is described below. Let's use the values: W=2, H=2, DW=32:
- Total CLINKs: W * H = 2 * 2 = 4
- Data bits per CLINK: DW = 32
- Total uhost_req_data width: W * H * DW = 4 * 32 = 128 bits.

The AXI protocol is channel-based. It has separate, dedicated channels for addresses and data (Write Address, Write Data, Read Address, Read Data, etc.). However UMI is a packet-based protocol. 
All the information for a transaction—command, address, data—is bundled into a single "packet" and sent at once. This makes it very suitable for networked systems like the ebrick fabric, where packets 
can be routed from a source to a destination. A UMI interface is divided into two main parts, a Request path and a Response path.

In our ebrick module, we have ports prefixed with uhost and udev. These represent the two roles a module can play in the UMI protocol:
- uhost (UMI Host): This is the Master or Initiator. The uhost interface is used to send requests out into the fabric and receive responses back.
- udev (UMI Device): This is the Slave or Target. The udev interface is used to receive requests from other components in the fabric and send responses back. 

MASTER INTERFACE SIGNALS (uhost)
Path		Signal Name		Bits		Direction		Description
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Request		uhost_req_valid		[W*H-1:0]	Output		Request Valid. One bit per CLINK. The core asserts this to indicate a valid request packet is being sent.
Request		uhost_req_ready		[W*H-1:0]	Input		Request Ready. One bit per CLINK. The system asserts this to indicate it's ready to accept a request packet. A 
									transfer occurs when valid and ready are both high.
Request		uhost_req_cmd		[W*H*CW-1:0]	Output		Command. The command packet, containing the opcode (e.g., READ, WRITE, ATOMIC), size of the transaction, and other 
									control flags.
Request		uhost_req_dstaddr		[W*H*AW-1:0]	Output		Destination Address. The full address of the target device. This includes the target's ChipID and its internal memory address. 
									This is how the fabric routes the packet.
Request		uhost_req_srcaddr		[W*H*AW-1:0]	Output		Source Address. The address of the initiator (this core). This is crucial so the target device knows where to send the response back to.
Request		uhost_req_data		[W*H*DW-1:0]	Output		Data. The data payload. For a WRITE request, this is the data to be written. For a READ request, this field is typically ignored.
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Response 	uhost_resp_valid		[W*H-1:0]	Input		Response Valid. One bit per CLINK. The system asserts this to indicate a valid response packet is available for the core.
Response 	uhost_resp_ready		[W*H-1:0]	Output		Response Ready. One bit per CLINK. The core asserts this to indicate it's ready to accept a response packet.
Response		uhost_resp_cmd		[W*H*CW-1:0]	Input		Response Command. The command of the response packet. For a read, this will indicate a successful read response. 
									For a write, it acknowledges the write is complete.
Response		uhost_resp_dstaddr	[W*H*AW-1:0]	Input		Destination Address. When a response comes back, its dstaddr will match the srcaddr of the original request, confirming it's for this core.
Response		uhost_resp_srcaddr	[W*H*AW-1:0]	Input		Source Address. This indicates which device sent the response (i.e., the dstaddr of the original request).
Response		uhost_resp_data		[W*H*DW-1:0]	Input		Response Data. The data payload. For a READ response, this field contains the data that was read from memory. 
									For a WRITE response, this field is typically ignored.
SLAVE INTERFACE SIGNALS (udev)
Path		Signal Name		Bits		Direction		Description
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Request		udev_req_valid		[W*H-1:0]	Input		Request Valid. Asserted by an external master to indicate a valid request packet is being sent to this core.
Request		udev_req_ready		[W*H-1:0]	Output		Request Ready. This core would assert this to indicate it's ready to accept a request packet from an external master.
Request		udev_req_cmd		[W*H*CW-1:0]	Input		Command. The command packet from the external master (e.g., READ from a memory location inside this core).
Request		udev_req_dstaddr		[W*H*AW-1:0]	Input		Destination Address. The address the external master wants to access within this core.
Request		udev_req_srcaddr		[W*H*AW-1:0]	Input		Source Address. The address of the external master that sent the request.
Request		udev_req_data		[W*H*DW-1:0]	Input		Data. The data payload from the external master for a WRITE operation.
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Response 	udev_resp_valid		[W*H-1:0]	Output		Response Valid. This core would assert this to send a valid response packet back to the external master.
Response 	udev_resp_ready		[W*H-1:0]	Input		Response Ready. The external master asserts this to indicate it's ready to accept the response packet.
Response 	udev_resp_cmd		[W*H*CW-1:0]	Output		Response Command. The command of the response packet (e.g., READ_RESP).
Response 	udev_resp_dstaddr		[W*H*AW-1:0]	Output		Destination Address. The destination of the response, which is the srcaddr of the original request.
Response 	udev_resp_srcaddr		[W*H*AW-1:0]	Output		Source Address. The source of the response, which is this core's address.
Response 	udev_resp_data		[W*H*DW-1:0]	Output		Response Data. For a READ request, this would contain the data read from this core's internal memory.

The structure of a UMI Address of 64-bits:
Bits	Width	Field Name	Description
[63:56]	8 bits	Reserved		Unused for now, set to zero.
[55:40]	16 bits	Chip ID		The most important field for routing. This unique ID identifies the target component.
[39:0]	40 bits	Address Space	The "local" address within the target component. Once the packet arrives at the correct chiplet, this part of the address is used to access a specific register or memory location.

------------------------------------------------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------UMI GPIO----------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------------------------------------
The umi_gpio module in this module is not a general-purpose I/O block. Instead, it serves as the central Simulation Control Peripheral. It is a simple UMI device that acts as a bridge, allowing the Python test script to control 
the most critical signals of the Verilog simulation. Some key responsibilities are to drive global control signals like nreset and go. Also it monitors core status with the input, which is connected to the status wire from the ebrick_core. 
This allows the Python script to read the CPU's status by sending a UMI read request to the umi_gpio module.

------------------------------------------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------Code Architecture-----------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------------------------------------
An EBRICK project consists many files that have different purposes:
- rtl code: The code of our harware component (e.g. a processor PicoRV32 or an adder)
- core code: Files like 'ebrick_core', or 'adder_core' are just wrappers of their corresponding rtl code.  They transform the AXI4-Lite protocol, generated by HLS, to the ebrick-friendly protocol of UMI. Also they wrap the rtl code with 
  other useful adaptations like signal routing (if needed).
- umi_macros.vh: Contains useful macros used for setting up the UMI protocol.
- umi_ram.py: Simple software model of a UMI RAM memory.
- testbench.sv: Instantiates the ebrick cores and connects its UMI ports to switchboard module sso that the design can be driven from Python.
- test_prv32.py: The script for testing multiple chiplets with UMI connection.
- ebrick_memory_map.vh: This file contains all the addresses in the circuit. The corresponding C-file is 'ebrick_memory_map.h'.
- hello.c: The scenario of our test. This is a file that creates all the information, and generally the sequence  of chiplet communication.
- Configuration files: Included 'config.vlt', 'init.S', 'link.ld'. Each folder contains different type of configurations.
- ebrick.py: The main function. It imports all the files and selects if a test or asic script will be excecuted.

------------------------------------------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------Integrating a Seperate Chiplet-----------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------------------------------------
Step 1: Add the RTL
Add the new RTL source code into the rtl/ folder. The component must expose a standard interface, typically an AXI4-Lite Slave protocol (for control/registers) or AXI4-Stream (for data).

Step 2: Create a Core Wrapper
Create an "ebrick core" wrapper (e.g., adder_core.v) to adapt the RTL to the ebrick ecosystem. This wrapper serves as a protocol bridge between the system's UMI interface and your component's native interface. Depending on the 
component's role, instantiate the appropriate converter: use umi2axilite if your component acts as a Slave (like the adder), or axilite2umi if it acts as a Master (like a processor).

Step 3: Define the Memory Map
Open ebrick_memory_map.vh (and ebrick_memory_map.h) and define a unique 16-bit Chip ID (CHIPID) and the corresponding address range for the new component.

Step 4: Update the Build Script
Modify ebrick.py to include the new source files. Use the chip.input() command to register both the new core wrapper and the original RTL files.

Step 5: Configuration & Lint Waivers
Update config.vlt to suppress non-critical warnings. Add lint_off directives for the new RTL files (especially if they are HLS-generated).

Step 6: Implement Hardware Address Decoding (Crucial Step)
Modify rtl/ebrick_core.v. You must update the address decoding logic to recognize the 32-bit address range of your new component and route those packets to the specific Chip ID defined in Step 3.

Step 7: Instantiate in Testbench
Add the new core to testbench.sv. Instantiate the module, define the necessary UMI wires, and connect the UMI ports to new Switchboard queues (using queue_to_umi_sim and umi_to_queue_sim).

Step 8: Update the Python Monitor
Modify test_prv32.py. Initialize the new Switchboard queues and update the main routing loop (while True). You must add logic to check the destination Chip ID of incoming packets and route them to the appropriate chiplet queue.

Step 9: Write the Firmware
Update hello.c. Define the memory-mapped registers using 32-bit local addresses (mapped to the range used in Step 6) and write the C code to interact with the hardware.








