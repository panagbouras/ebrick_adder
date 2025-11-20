# Ebrick Adder
This GitHub repository presents a project based on [ebrick-demo](https://github.com/zeroasiccorp/ebrick-demo) by [Zero ASIC](https://www.zeroasic.com). More specifically, it adds a new chiplet to the existing workflow. The new chiplet is a simple 1-bit adder component, produced by High Level Synthesis (HLS), utilizing the AXI4-Lite protocol. This repository documents the connections between the chiplets, the code architecture, and the steps required to integrate new chiplets into the ebrick framework. This project uses SiliconCompiler version 0.34.3. The ebrick framework is currently incompatible with versions 0.35.0 and later due to significant API changes (specifically, the refactoring of the Chip class into distinct ASIC and FPGA classes).

## Signal Connections
The diagram below illustrates the system connections between the ebrick components. The system is established via three primary UMI connections, centered around the Python Monitor which acts as a central router (interposer).

First, the 'Core to Monitor' connection allows the PicoRV32 processor to act as a UMI Host, sending requests to and receiving responses from the Python Monitor. The Monitor is responsible for routing this data to the appropriate destination based on the memory address.

If the address targets system memory, the Monitor interacts with the UMI RAM. Since the RAM is modeled entirely in Python software, it does not require a separate Switchboard queue; it communicates directly with the Monitor to handle read/write requests.

If the address targets the accelerator, the Monitor uses the 'Monitor to Adder' connection. Here, the Python Monitor acts as the UMI Host, forwarding data from the PicoRV32 to the HLS-Adder for processing. The Adder then sends the response back to the Monitor, which prints the information (and also can forwards it back to the PicoRV32, if is modified properly).

Finally, the 'Monitor to GPIO' connection allows the Python script to act as an external controller. It sends commands to the UMI GPIO block, which then drives physical control signals—such as nreset and go—directly to the PicoRV32 hardware.

<img width="941" height="655" alt="image" src="https://github.com/user-attachments/assets/7176caec-0666-4751-9a3c-0d55842cf6b6" />

## Code Architecture
An ebrick project comprises various files, each serving a specific purpose in the design and simulation flow:
* *RTL Code:* The source code for the actual hardware logic (e.g., the `picorv32.v` processor or the `vadd.v` HLS-generated adder).
* *Core Wrappers (*_core.v):* Files like `ebrick_core.v` and `adder_core.v` serve as integration wrappers. Their primary function is Protocol Adaptation. Τhey convert standard protocols (like AXI4-Lite) into the UMI protocol used by the ebrick ecosystem. Additionally, they handle signal routing (e.g. address decoding in ebrick_core) and port mapping.
* *umi_macros.vh:* A header file containing Verilog macros used to simplify the declaration and instantiation of UMI interfaces.
* *testbench.sv:* The top-level Verilog simulation file. It instantiates the ebrick cores and connects their UMI ports to Switchboard modules (queues), allowing the hardware simulation to communicate with the external Python environment.
* *test_prv32.py:* The Python simulation monitor. This script acts as the router (Network-on-Chip) for the simulation. It directs packets between the CPU, the memory, and the adder chiplet.
* *umi_ram.py:* A Python software model of the system RAM. It responds to UMI read/write requests sent by the simulation monitor.
* *ebrick_memory_map.vh / .h:* These files define the global memory map (addresses and Chip IDs) for the system. The .vh file is used by the hardware address decoder, while the .h file is used by the C firmware.
* *hello.c:* The firmware (scenario) for the test. This C code runs on the PicoRV32 processor, orchestrating the test sequence and initiating communication with the other chiplets.
* *Configuration Files:* <br />
  &rarr; config.vlt: Verilator configuration (waivers) to suppress non-critical lint warnings. <br />
  &rarr; init.S & link.ld: Startup code and linker scripts required to compile C code for the RISC-V architecture. <br />
  &rarr; ebrick.py: The main build script based on SiliconCompiler. It manages the project dependencies, imports source files, and executes the desired flow (e.g., running the testbench or generating an ASIC layout).

## Integration Steps
**Step 1: Add the RTL Code**<br />
Add the new RTL source code into the `rtl/` folder. The component must expose a standard interface, typically an AXI4-Lite protocol.

**Step 2: Create a Core Wrapper**<br />
Create an "ebrick core" wrapper (e.g., `adder_core.v`) to adapt the RTL to the ebrick ecosystem. This wrapper serves as a protocol bridge between the system's UMI interface and your component's native interface. Depending on the component's role, instantiate the appropriate converter: use `umi2axilite` if your component acts as a Slave (like the adder), or `axilite2umi` if it acts as a Master (like a processor).

**Step 3: Define the Memory Map**<br />
Open `ebrick_memory_map.vh` (and `ebrick_memory_map.h`) and define a unique 16-bit Chip ID (CHIPID) and the corresponding address range for the new component.

**Step 4: Update the Build Script**<br />
Modify `ebrick.py` to include the new source files. Use the `chip.input()` command to register both the new core wrapper and the original RTL files.

**Step 5: Configuration & Lint Waivers**<br />
Update `config.vlt` to suppress non-critical warnings. Add lint_off directives for the new RTL files (especially if they are HLS-generated).

**Step 6: Implement Hardware Address Decoding (Crucial Step)** <br />
Modify `rtl/ebrick_core.v`. You must update the address decoding logic to recognize the 32-bit address range of your new component and route those packets to the specific Chip ID defined in Step 3.

**Step 7: Instantiate in Testbench**<br />
Add the new core to `testbench.sv`. Instantiate the module, define the necessary UMI wires, and connect the UMI ports to new Switchboard queues (using `queue_to_umi_sim` and `umi_to_queue_sim`).

**Step 8: Update the Python Monitor** <br />
Modify `test_prv32.py`. Initialize the new Switchboard queues and update the main routing loop (while True). You must add logic to check the destination Chip ID of incoming packets and route them to the appropriate chiplet queue.

**Step 9: Write the Firmware** <br />
Update `hello.c`. Define the memory-mapped registers using 32-bit local addresses (mapped to the range used in Step 6) and write the C code to interact with the hardware.

