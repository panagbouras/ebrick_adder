#!/usr/bin/env python3

# Copyright (c) 2024 Zero ASIC Corporation
# This code is licensed under Apache License 2.0 (see LICENSE for details)


import os
import umi
import lambdalib
from siliconcompiler import Chip
from siliconcompiler.targets import asap7_demo
from siliconcompiler.flows import lintflow


def __add_ebrick_sources(chip):
    # Sets the current directory as a SiliconCompiler package named 'ebrick_demo'  
    chip.register_source(
        'ebrick_demo',   
        os.path.abspath(os.path.dirname(__file__)))

    # Add ebrick_core.v file into the ebrick_demo package
    chip.input('rtl/ebrick_core.v', package='ebrick_demo')
    chip.input('rtl/adder_core.v', package='ebrick_demo')
    
    # Add the folder config to the ebrick_demo package
    chip.add('option', 'idir', 'config', package='ebrick_demo')

    # The following lines integrate necessary external SC packages
    chip.use(umi)
    chip.use(lambdalib)

    # Tells SiliconCompiler that the module named ebrick_core is the top-level entity
    chip.set('option', 'entrypoint', 'ebrick_core')


def setup_core_design(chip):
    # Calls this function to initialize the set-up 
    __add_ebrick_sources(chip)

    # Creates a new external package called picorv32 that is drawn from GitHub 
    chip.register_source(
        name='picorv32',
        path='git+https://github.com/YosysHQ/picorv32.git',
        ref='a7b56fc81ff1363d20fd0fb606752458cd810552')

    # Adds the picorv32.v file from GitHub to our SC package called picorv32
    chip.input('picorv32.v', package='picorv32')

    #Add the HLS adder files
    chip.input('rtl/vadd.v', package='ebrick_demo')
    chip.input('rtl/vadd_CTRL_BUS_s_axi.v', package='ebrick_demo')

    # Add your library imports here
    '''
    This comment indicates where future developers could add other specific IP cores
    or libraries necessary for a complex EBRICK (e.g., custom accelerators, specialized
    peripherals, or other necessary memory files).
    '''

def __setup_asicflow(chip):
    # Setup asic flow

    # The design with this macro is signaled that it is being processed for synthesis
    chip.add('option', 'define', 'SYNTHESIS')

    '''
    The value returned by chip.get('asic', 'logiclib') is always a list of library names like
    ['asap7sc7p5t_20'] or similar. In typical ASIC flows, the first library listed in logiclib 
    is assumed to be the main standard cell library
    '''
    mainlib = chip.get('asic', 'logiclib')[0]  # This is set by the target
    #Adds the proper constraint file into the ebrick_demo package
    chip.input(f'implementation/{mainlib}.sdc', package='ebrick_demo')

    # Setup physical constraints
    # This sets a target utilization limit for standard cells within the core area to 30%
    chip.set('constraint', 'density', 30)

    # Provide tool specific settings
    '''
    This provides a specific tuning variable for the Global Placement (GPL) tool within OpenRoad. 
    A placement adjustment of '0.2' often refers to how aggressively cells are spread out during 
    the initial global placement phase. This is used to balance density and wire length, aiming to 
    improve routability before detailed placement.
    '''
    chip.set('tool', 'openroad', 'task', 'place', 'var',
             'gpl_uniform_placement_adjustment',
             '0.2')

    #Checks the chip's pdk
    pdk = chip.get('option', 'pdk')
    if pdk == 'asap7':
        # Change pin placement settings to allow for multiple layers
        # to avoid pin placement congestion
        stackup = chip.get('option', 'stackup')
        ''' 
        This configuration explicitly instructs the OpenRoad tool (via PDK variables) to allow pin placement 
        for the module to use multiple, higher metal layers. The vertical pins are allowed on Metal 3 (M3) and 
        Metal 5 (M5). The horizontal pins are allowed on Metal 4 (M4) and Metal 6 (M6)
        '''
        chip.set('pdk', pdk, 'var', 'openroad', 'pin_layer_vertical', stackup, [
            'M3',
            'M5'
        ])
        chip.set('pdk', pdk, 'var', 'openroad', 'pin_layer_horizontal', stackup, [
            'M4',
            'M6'
        ])
        # Change minimum pin placement distance to 3 tracks for tasks
        # which impact pin placement to reduce routing congestion
        for task in ('floorplan', 'place'):
            chip.add('tool', 'openroad', 'task', task, 'var', 'ppl_arguments', [
                '-min_distance_in_tracks',
                '-min_distance', '3'])
    elif pdk == 'skywater130':
        # Change pin placement settings to allow for multiple layers
        # to avoid pin placement congestion
        stackup = chip.get('option', 'stackup')
        chip.set('pdk', pdk, 'var', 'openroad', 'pin_layer_vertical', stackup, [
            'met2',
            'met4'
        ])
        chip.set('pdk', pdk, 'var', 'openroad', 'pin_layer_horizontal', stackup, [
            'met1',
            'met3'
        ])


def __setup_lintflow(chip):
    # Change job name to avoid overwriting asicflow
    chip.set('option', 'jobname',
             f'{chip.get("option", "jobname")}_lint')

    # Import lintflow
    chip.use(lintflow)

    '''
    Add tool specific settings. Its purpose is to suppress specific warnings or errors 
    generated by the Verilator linting tool for certain files or module patterns.
    '''
    chip.add('tool', 'verilator', 'task', 'lint', 'file', 'config',
             'config/config.vlt', package='ebrick_demo')


def __setup_testbench(chip):
    # Remove the entrypoint setting as this will need to be the testbench
    chip.unset('option', 'entrypoint')

    # Add tool specific settings. This time the Verilator performs compile instead of lint
    chip.set('tool', 'verilator', 'task', 'compile', 'file', 'config',
             'config/config.vlt', package='ebrick_demo')


def setup(chip, testbench=False):
    # The first step is always to call this function as it performs the fundamental setup, regardless of the flow.
    setup_core_design(chip)

    #Select teh run asic/lint/testbench
    if not testbench:
        flow = chip.get('option', 'flow')
        if flow == 'asicflow':
            __setup_asicflow(chip)
        elif flow == 'lintflow':
            __setup_lintflow(chip)
        else:
            raise ValueError(f'{flow} is not recognized')
    else:
        __setup_testbench(chip)

    return chip


def main():
    chip = Chip("ebrick-demo")

    chip.set('option', 'jobname','job0')

    # needed because the test imports ebrick
    from ebrick_adder.testbench.test_prv32 import run_test as run_test_prv32

    #The functions that contain the Switchboard logic necessary to build and run the Verilator simulation.
    run_test_map = {
        'test_prv32': run_test_prv32,
    }

    args = chip.create_cmdline(
        # Lists standard SiliconCompiler global switches that should be accepted
        switchlist=['-target',
                    '-flow',
                    '-clean',
                    '-jobname',
                    '-quiet',
                    '-remote'],
        # Defines custom, application-specific arguments, specifically those controlling simulation tests
        additional_args={
            '-test': {
                'type': str,
                'nargs': '?',
                'const': 'test_prv32',
                'choices': list(run_test_map.keys()),
                'help': 'run a test, defaulting to test_prv32',
                'sc_print': False
            },
            '-trace': {
                'action': 'store_true',
                'help': "dump waveforms during simulation",
                'sc_print': False
            },
            '-fast': {
                'action': 'store_true',
                'help': "don't build the simulator if one is found",
                'sc_print': False
            }
        }
    )

    # If selected run test
    if args['test']:
        run_test_map[args['test']](
            trace=args['trace'],
            fast=args['fast']
        )
        return

    # Else excecute either lint either asic-flow 
    # Lintflow is the default flow
    chip.set('option', 'flow', 'lintflow', clobber=False)

    if not chip.get('option', 'pdk'):
        # load the target if it wasn't specified at the CLI
        chip.load_target(asap7_demo)

    # Setup chip
    setup(chip)

    chip.run()
    chip.summary()
    chip.snapshot()


if __name__ == "__main__":
    main()
