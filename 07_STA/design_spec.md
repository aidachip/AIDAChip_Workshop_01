# Design Specification: SoC Timing Requirements

## Overview

This document specifies the timing requirements for the SoC design to be used for SDC constraint development.

## Clock Domains

### Primary Clocks

| Clock Name | Frequency | Period | Source | Description |
|------------|-----------|--------|--------|-------------|
| clk_sys | 500 MHz | 2.0 ns | External, Port clk_sys_p | Main system clock |
| clk_cpu | 1.0 GHz | 1.0 ns | PLL output, derived from clk_sys | CPU core clock |
| clk_mem | 333 MHz | 3.0 ns | External, Port clk_mem_p | Memory interface clock |
| clk_io | 100 MHz | 10.0 ns | External, Port clk_io_p | I/O interface clock |

### Generated Clocks

| Clock Name | Source | Division | Description |
|------------|--------|----------|-------------|
| clk_sys_div2 | clk_sys | ÷2 | Divided clock for low-power logic |
| clk_cpu_div4 | clk_cpu | ÷4 | Debug interface clock |

### Clock Relationships

- **clk_sys ↔ clk_cpu**: Synchronous (both from same PLL)
- **clk_sys ↔ clk_mem**: Asynchronous
- **clk_sys ↔ clk_io**: Asynchronous
- **clk_mem ↔ clk_io**: Asynchronous

## Clock Uncertainty

| Corner | Clock | Setup Uncertainty | Hold Uncertainty |
|--------|-------|-------------------|------------------|
| Slow | All | 100 ps | 50 ps |
| Fast | All | 80 ps | 80 ps |
| Nominal | All | 90 ps | 60 ps |

## I/O Timing

### Input Ports (synchronized to clk_sys)

| Port | Clock | Max Delay | Min Delay | Notes |
|------|-------|-----------|-----------|-------|
| data_in[31:0] | clk_sys | 0.5 ns | 0.1 ns | Main data input |
| ctrl_in[7:0] | clk_sys | 0.4 ns | 0.1 ns | Control signals |
| valid_in | clk_sys | 0.3 ns | 0.1 ns | Data valid |

### Output Ports (synchronized to clk_sys)

| Port | Clock | Max Delay | Min Delay | Notes |
|------|-------|-----------|-----------|-------|
| data_out[31:0] | clk_sys | 0.6 ns | 0.1 ns | Main data output |
| ready_out | clk_sys | 0.4 ns | 0.1 ns | Ready signal |
| error_out | clk_sys | 0.5 ns | 0.1 ns | Error flag |

### I/O Interface Ports (synchronized to clk_io)

| Port | Clock | Max Delay | Min Delay | Notes |
|------|-------|-----------|-----------|-------|
| io_bus[15:0] | clk_io | 2.0 ns | 0.5 ns | External I/O bus |
| io_valid | clk_io | 1.5 ns | 0.5 ns | I/O valid |
| io_ready | clk_io | 1.5 ns | 0.5 ns | I/O ready |

### Memory Interface Ports (synchronized to clk_mem)

| Port | Clock | Max Delay | Min Delay | Notes |
|------|-------|-----------|-----------|-------|
| mem_addr[31:0] | clk_mem | 0.8 ns | 0.2 ns | Memory address |
| mem_data[63:0] | clk_mem | 0.8 ns | 0.2 ns | Memory data |
| mem_cmd[3:0] | clk_mem | 0.6 ns | 0.2 ns | Memory command |

## Special Timing Paths

### False Paths

| From | To | Reason |
|------|-----|--------|
| reset_n | All FFs | Asynchronous reset |
| test_mode | All FFs | Static test configuration |
| clk_io domain | clk_mem domain | No direct paths (through sync) |

### Multicycle Paths

| From | To | Setup Cycles | Hold Cycles | Reason |
|------|-----|--------------|-------------|--------|
| cfg_reg* | All endpoints | 3 | 2 | Configuration registers (written once) |
| status_reg* | All endpoints | 2 | 1 | Status registers (slow read) |

### Clock Domain Crossings

| From Domain | To Domain | Synchronizer | Max Delay |
|-------------|-----------|--------------|-----------|
| clk_io | clk_sys | 2-FF sync | 1.5 × clk_sys period |
| clk_sys | clk_io | 2-FF sync | 1.5 × clk_io period |
| clk_mem | clk_sys | 2-FF sync | 1.5 × clk_sys period |

## Constraints Summary

1. All clocks should have source latency of 0.2-0.3 ns modeled
2. Use `set_clock_groups -asynchronous` for async clock relationships
3. Memory interface has tight timing - may need separate constraint file
4. CPU clock domain has highest frequency - priority for timing closure
5. All async crossings use 2-FF synchronizers - constrain appropriately
