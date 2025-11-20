/******************************************************************************
 * This module serves as the ebrick-core wrapper for the HLS-generated adder.
 * It adapts the adder to act as a UMI Device (Slave) accessible by the 
 * PicoRV32 processor.
 * 
 * The structural flow is as follows:
 *      1. Wire Declarations: Defining internal connections.
 *      2. Protocol Bridging: Instantiating 'umi2axilite' to convert incoming
 *         UMI packets into AXI4-Lite transactions.
 *      3. IP Instantiation: Connecting the 'vadd' HLS core.
 * 
 * Notably, because this module acts as a leaf-node slave, it does not require
 * address decoding or routing logic. It simply processes valid requests and 
 * returns responses to the initiator (Source Address).
 ****************************************************************************/
`default_nettype none
`include "/work/ebrick_demo_adder/ebrick_demo/testbench/umi_macros.vh"

module adder_core #(
    parameter DW  = 32,
    parameter AW  = 64,
    parameter CW  = 32,
    parameter IDW = 16,
    parameter RW  = 32
) (
    // Standard ebrick control signals
    input               clk,
    input               nreset,
    input               go,
    input      [IDW-1:0] chipid, // Chip ID is now an input
    output     [RW-1:0]  status,

    // Standard UMI Device Port (for receiving requests)
    // In this simple 1-bit adder, this is the only UMI port we need.
    `UMI_INPUT(udev_req, DW, CW, AW),
    `UMI_OUTPUT(udev_resp, DW, CW, AW),

    // Unused UMI Host Port (required for a standard interface, but tied off)
    `UMI_OUTPUT_ARRAY(uhost_req, DW, CW, AW, 1),
    `UMI_INPUT_ARRAY(uhost_resp, DW, CW, AW, 1)
);

    // Tie off unused standard signals
    assign status = {RW{1'b0}}; // Not providing any status for now
    assign uhost_req_valid = 1'b0; // We are not a UMI host
    // No need to drive other uhost signals since valid is 0.

    // Internal AXI4-Lite wires
    wire [63:0]  axi_awaddr; 
    wire axi_awvalid; 
    wire axi_awready;
    wire [31:0] axi_wdata;  
    wire [3:0]  axi_wstrb; 
    wire axi_wvalid; 
    wire axi_wready;
    wire [1:0]  axi_bresp;  
    wire axi_bvalid;  
    wire axi_bready;
    wire [63:0]  axi_araddr; 
    wire axi_arvalid; 
    wire axi_arready;
    wire [31:0] axi_rdata;  
    wire [1:0]  axi_rresp; 
    wire axi_rvalid; 
    wire axi_rready;

    // Instantiate the UMI to AXI-Lite Bridge
    umi2axilite #(
        .CW(CW),
        .AW(AW),
        .DW(DW)
    ) adder_bridge (
        .clk(clk),
        .nreset(nreset),

        // Connect bridge's UMI port to the wrapper's UMI port
        `UMI_CONNECT(udev_req, udev_req),
        `UMI_CONNECT(udev_resp, udev_resp),

        // Bridge's AXI port drives the adder
        .axi_awaddr(axi_awaddr), 
        .axi_awprot(), 
        .axi_awvalid(axi_awvalid), 
        .axi_awready(axi_awready),
        .axi_wdata(axi_wdata), 
        .axi_wstrb(axi_wstrb), 
        .axi_wvalid(axi_wvalid), 
        .axi_wready(axi_wready),
        .axi_bresp(axi_bresp), 
        .axi_bvalid(axi_bvalid), 
        .axi_bready(axi_bready),
        .axi_araddr(axi_araddr), 
        .axi_arprot(), 
        .axi_arvalid(axi_arvalid), 
        .axi_arready(axi_arready),
        .axi_rdata(axi_rdata), 
        .axi_rresp(axi_rresp), 
        .axi_rvalid(axi_rvalid), 
        .axi_rready(axi_rready)
    );

    // Instantiate the "raw" Vitis HLS Adder
    vadd adder_inst (
        .ap_clk(clk),
        .ap_rst_n(nreset), // The `go` signal could be used here for finer control if needed

        .s_axi_CTRL_BUS_AWVALID(axi_awvalid), 
        .s_axi_CTRL_BUS_AWREADY(axi_awready), 
        .s_axi_CTRL_BUS_AWADDR(axi_awaddr[5:0]),
        .s_axi_CTRL_BUS_WVALID(axi_wvalid), 
        .s_axi_CTRL_BUS_WREADY(axi_wready), 
        .s_axi_CTRL_BUS_WDATA(axi_wdata),
        .s_axi_CTRL_BUS_WSTRB(axi_wstrb), 
        .s_axi_CTRL_BUS_ARVALID(axi_arvalid), 
        .s_axi_CTRL_BUS_ARREADY(axi_arready),
        .s_axi_CTRL_BUS_ARADDR(axi_araddr[5:0]), 
        .s_axi_CTRL_BUS_RVALID(axi_rvalid), 
        .s_axi_CTRL_BUS_RREADY(axi_rready),
        .s_axi_CTRL_BUS_RDATA(axi_rdata), 
        .s_axi_CTRL_BUS_RRESP(axi_rresp), 
        .s_axi_CTRL_BUS_BVALID(axi_bvalid),
        .s_axi_CTRL_BUS_BREADY(axi_bready), 
        .s_axi_CTRL_BUS_BRESP(axi_bresp), 
        .interrupt()
    );

endmodule
`default_nettype wire