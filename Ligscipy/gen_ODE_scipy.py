#!/usr/bin/pythons
# -*- coding: utf-8 -*-

import os

import sciligpy_utils as lig
import constants as const


def heating(species_IC='Pseudotsuga_menziesii', heating_rate=2.7, T0=25, Tmax=500):
    reactionlist, rateconstantlist, compositionlist, module_dir = lig.set_paths()
    y_list = lig.get_specieslist(reactionlist)
    speciesindices, indices_to_species = lig.get_speciesindices(y_list)
    kmatrix = lig.build_k_matrix(rateconstantlist)
    rate_list = lig.build_rates_list_kexp(rateconstantlist, reactionlist, speciesindices, indices_to_species)
    species_rxns = lig.build_species_rxns_dict(reactionlist)
    dydt_expressions = lig.build_dydt_list(rate_list, y_list, species_rxns)
    PLIGC_0, PLIGH_0, PLIGO_0 = lig.define_initial_composition(compositionlist, species_IC)

    with open(module_dir+'ODE_scipy/solve_ODEs_heating_%s.py' % species_IC, 'w') as f:
        beginning = "#!/usr/bin/pythons\n" \
                    "# -*- coding: utf-8 -*-\n\n" \
                    "from scipy.integrate import odeint\n" \
                    "import time\n" \
                    "import numpy as np\n\n\n" \
                    "start = time.time()\n" \
                    "def ODEs(y, t, p):\n"
        f.write(beginning)

        # define y in function
        y = '\tT'
        for spec in y_list:
            y += (', ' + spec)
        y += ' = y'
        f.write(y + '\n')

        # define parameters in function
        parameters = '\talpha, R, A0, n0, E0'
        for i in range(1, len(kmatrix)):
            parameters += ', A%s, n%s, E%s' % (i, i, i)
        parameters += ' = p\n'
        f.write(parameters)

        # define ODEs in function
        dydt = '\tdydt = [alpha'
        for ODE in dydt_expressions:
            dydt += (', \n\t\t\t' + ODE.split('=')[1][1:-2])
        dydt += ']'
        f.write(dydt + '\n')
        f.write('\treturn dydt\n\n')

        # define values of parameters
        f.write('alpha = %s\nR = %s\n' % (heating_rate, const.GAS_CONST))
        f.write('# A, n, E values\n')
        for i in range(len(kmatrix)):
            f.write('A%s = %s\nn%s = %s\nE%s = %s\n' % (i, kmatrix[i][0], i, kmatrix[i][1], i, kmatrix[i][2]))

        # define initial condition
        f.write('\n# Initial conditions\n')
        f.write('T0 = %s\n' %(T0+273.15))
        f.write('PLIGC = %s\nPLIGH = %s\nPLIGO = %s\n' % (PLIGC_0, PLIGH_0, PLIGO_0))
        IC = ''
        for i in y_list:
            if i == 'PLIGC' or i == 'PLIGH' or i == 'PLIGO':
                continue
            else:
                IC += ('%s = ' % i)
        IC += '0'
        f.write(IC + '\n\n')

        f.write('# ODE solver parameters\n')
        f.write('abserr = %s\n' % const.ABSOLUTE_TOLERANCE)
        f.write('relerr = %s\n' % const.RELATIVE_TOLERANCE)
        stoptime = (Tmax-T0) / heating_rate
        f.write('stoptime = %s\n' %stoptime)
        f.write('numpoints = %s\n\n' %(round(stoptime/0.02)))

        f.write('t = [stoptime * float(i) / (numpoints - 1) for i in range(numpoints)]\n')
        y0 = 'y0 = [T0'
        for spec in y_list:
            y0 += ', %s' % spec
        y0 += ']\n'
        f.write(y0)

        p = 'p = [alpha, R'
        for i in range(len(kmatrix)):
            p += ', A%s, n%s, E%s' % (i, i, i)
        p += ']\n'
        f.write(p)

        f.write('\nysol = odeint(ODEs, y0, t, args=(p,), atol=abserr, rtol=relerr)\n\n')

        f.write("with open('sol_heating_%s.dat', 'w') as f:\n" % (species_IC))

        ysol = ''
        for i in range(len(y_list) + 1):
            ysol += 'yy[%s], ' % i
        f.write('\tfor tt, yy in zip(t, ysol):\n')
        f.write('\t\tprint(tt, %sfile=f)\n' % ysol)
        f.write('\tend = time.time()\n\trun_time = end - start\n\tprint(run_time, file=f)')


def isothermal(species_IC='Pseudotsuga_menziesii', continue_reaction=True, T=500):
    if continue_reaction == True:
        with open('sol_heating_%s.dat' %species_IC, 'r') as f:
            pre_result = f.readlines()[-2]
            pre_time = eval(pre_result[0])
            T = eval(pre_result[1]) - 273.15
            stoptime = 2000 - pre_time

    reactionlist, rateconstantlist, compositionlist, module_dir = lig.set_paths()
    y_list = lig.get_specieslist(reactionlist)
    speciesindices, indices_to_species = lig.get_speciesindices(y_list)
    rate_list = lig.build_rates_list(rateconstantlist, reactionlist, speciesindices, indices_to_species, T+273.15)
    species_rxns = lig.build_species_rxns_dict(reactionlist)
    dydt_expressions = lig.build_dydt_list(rate_list, y_list, species_rxns)
    kmatrix = lig.build_k_matrix(rateconstantlist)
    kvaluelist = lig.get_k_value_list(T, kmatrix)
    PLIGC_0, PLIGH_0, PLIGO_0 = lig.define_initial_composition(compositionlist, species_IC)

    with open(module_dir+'ODE_scipy/solve_ODEs_T%s_%s.py' %(T, species_IC), 'w') as f:
        beginning = "#!/usr/bin/pythons\n" \
                    "# -*- coding: utf-8 -*-\n\n" \
                    "from scipy.integrate import odeint\n" \
                    "import time\n" \
                    "start = time.time()\n" \
                    "def ODEs(y, t, p):\n"
        f.write(beginning)

        # define y in function
        y = '\t' + y_list[0]
        for i in y_list[1:]:
            y += (', ' + i)
        y += ' = y'
        f.write(y + '\n')

        # define parameters in function
        p = '\tk_%s_0' % T
        for i in range(1, len(kvaluelist)):
            p += ', k_%s_%s' % (T, i)
        p += ' = p'
        f.write(p + '\n')

        # define ODEs in function
        dydt = '\tdydt = [%s' % dydt_expressions[0].split('=')[1][1:-2]
        for ODE in dydt_expressions[1:]:
            dydt += (', \n\t\t\t' + ODE.split('=')[1][1:-2])
        dydt += ']'
        f.write(dydt + '\n')
        f.write('\treturn dydt\n\n')

        # define values of parameters
        f.write('# k values\n')
        for i in range(len(kvaluelist)):
            f.write('k_%s_%s = %s\n' % (T, i, kvaluelist[i]))

        # define initial condition
        f.write('\n# Initial conditions\n')
        f.write('PLIGC = %s\nPLIGH = %s\nPLIGO = %s\n' % (PLIGC_0, PLIGH_0, PLIGO_0))
        IC = ''
        for i in y_list:
            if i == 'PLIGC' or i == 'PLIGH' or i == 'PLIGO':
                continue
            else:
                IC += ('%s = ' % i)
        IC += '0'
        f.write(IC + '\n\n')

        f.write('# ODE solver parameters\n')
        f.write('abserr = %s\n' % const.ABSOLUTE_TOLERANCE)
        f.write('relerr = %s\n' % const.RELATIVE_TOLERANCE)
        f.write('stoptime = 2000\n')
        f.write('numpoints = 10000\n\n')

        f.write('t = [stoptime * float(i) / (numpoints - 1) for i in range(numpoints)]\n')
        y0 = 'y0 = [' + y_list[0]
        for spec in y_list[1:]:
            y0 += ', %s' % spec
        y0 += ']'
        f.write(y0)

        p = '\np = [k_%s_0' % T
        for i in range(1, len(kvaluelist)):
            p += ', k_%s_%s' % (T, i)
        p += ']\n'
        f.write(p)

        f.write('\nysol = odeint(ODEs, y0, t, args=(p,), atol=abserr, rtol=relerr)\n\n')

        f.write("with open('sol_T%s_%s.dat', 'w') as f:\n" % (T, species_IC))

        ysol = ''
        for i in range(len(y_list)):
            ysol += 'yy[%s], ' % i
        f.write('\tfor tt, yy in zip(t, ysol):\n')
        f.write('\t\tprint(tt, %sfile=f)\n' % ysol)