# -*- coding: utf-8 -*-
"""
Integration tests for validation

@author: Tomas Krizek
"""

from geomopcontext.data.format import parse_format
from geomopcontext.data.con import parse_con
from geomopcontext.data.autocorrect import expand
from geomopcontext.validator.validator import Validator


def test_validation():
    input_dir = 'data/con'
    valid_files = [
        'dual_por_sorp.con',
        'compatible.con',
        'decay_gmsh.con',
        'decay_vtk.con',
        'dual_por.con',
        'dual_por_linear.con',
        'dual_por_pade.con',
        'dual_por_sorp.con',
        'dual_por_sorp_linear.con',
        'dual_por_time.con',
        'flow_21d.con',
        'flow_32d.con',
        'flow_bddc.con',
        'flow.con',
        'flow_decay_long_gmsh.con',
        'flow_decay_long_vtk.con',
        'flow_decay_molar_mass_vtk.con',
        'flow_dirichlet.con',
        'flow_gmsh.con',
        'flow_implicit.con',  # had an unescaped line-break
        'flow_implicit_elementwise.con',
        'flow_implicit_fields_gmsh.con',
        'flow_implicit_old.con',
        'flow_implicit_time_dep.con',
        'flow_large_cube_gmsh.con',
        'flow_large_cube_vtk.con',
        'flow_MH.con',
        'flow_neumann.con',
        'flow_old_gmsh.con',
        'flow_old_vtk.con',
        'flow_robin.con',
        'flow_small_cube.con',
        'flow_time_dep.con',
        'flow_vtk_fbc.con',
        'flow_vtk_piezo.con',
        'flow_vtk_simple.con',
        'freundlich_new.con',
        'freundlich_var.con',
        'langmuir_new.con',
        'langmuir_var.con',
        'linear_new.con',
        'linear_var.con',
        'lin_react_gmsh.con',
        'lin_react_vtk.con',
        'neumann_robin_implicit.con',
        'noncompatible_P0.con',
        'noncompatible_P1.con',
        'output_input_fields.con',
        'short_pulse_explicit.con',
        'short_pulse_implicit.con',
        'test_20.con',
        'trans_explicit.con',
    ]
    its = parse_format('data/format/1.8.2.json')
    validator = Validator()

    for filename in valid_files:
        data = parse_con(input_dir + '/' + filename)
        data = expand(data, its)

        validator.validate(data, its)

        # print(filename)
        # print(validator.console_log())
        assert validator.valid == True


def test_invalid():
#     1D2D.con
# INVALID
# /problem/primary_equation: Missing obligatory key 'balance' in record Steady_MH
# /problem/primary_equation/output: Missing obligatory key 'output_fields' in record DarcyMHOutput
# /problem/primary_equation: Missing obligatory key 'input_fields' in record Steady_MH

# flow_decay_gmsh.con
# INVALID
# /problem/primary_equation/output: Missing obligatory key 'output_fields' in record DarcyMHOutput
# /problem/primary_equation: Missing obligatory key 'input_fields' in record Steady_MH
# /problem/primary_equation: Missing obligatory key 'balance' in record Steady_MH
# /problem/secondary_equation: Missing obligatory key 'input_fields' in record TransportOperatorSplitting
# /problem/secondary_equation: Missing obligatory key 'output_stream' in record TransportOperatorSplitting
# /problem/secondary_equation: Missing obligatory key 'balance' in record TransportOperatorSplitting

# test_20_sorp_rock.con
# /problem/primary_equation/output: Missing obligatory key 'output_fields' in record DarcyMHOutput
# /problem/secondary_equation: Missing obligatory key 'output_stream' in record TransportOperatorSplitting

# trans_implicit.con
# INVALID
# /problem/primary_equation/output: Missing obligatory key 'output_fields' in record DarcyMHOutput
# /problem/primary_equation: Missing obligatory key 'balance' in record Steady_MH
# /problem/primary_equation: Missing obligatory key 'input_fields' in record Steady_MH
# /problem/secondary_equation: Invalid TYPE 'AdvectionDiffusion_DG' for Transport

    pass

