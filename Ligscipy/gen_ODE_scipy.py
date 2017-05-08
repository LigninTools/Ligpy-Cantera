#!/usr/bin/pythons
# -*- coding: utf-8 -*-

import sciligpy_utils as lig
import constants as const


def heating(species_IC='Pseudotsuga_menziesii', heating_rate=2.7, T0=25, Tmax=500):
    reactionlist, rateconstantlist, compositionlist, module_dir = lig.set_paths()
    y_list = lig.get_specieslist(reactionlist)
    speciesindices, indices_to_species = lig.get_speciesindices(y_list)
    kmatrix = lig.build_k_matrix(rateconstantlist)
    rate_list = lig.build_rates_list_kexp(rateconstantlist, reactionlist, speciesindices)
    species_rxns = lig.build_species_rxns_dict(reactionlist)
    dydt_expressions = lig.build_dydt_list(rate_list, y_list, species_rxns)
    PLIGC_0, PLIGH_0, PLIGO_0 = lig.define_initial_composition(compositionlist, species_IC)

    with open(module_dir+'ODE_scipy/solve_ODEs_heating_%s.py' % species_IC, 'w') as f:
        beginning = "#!/usr/bin/pythons\n" \
                    "# -*- coding: utf-8 -*-\n\n" \
                    "from scipy.integrate import odeint\n" \
                    "import time\n" \
                    "import numpy as np\n\n\n" \
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

        f.write('def run():\n\tstart = time.time()\n')
        # define values of parameters
        f.write('\talpha = %s\n\tR = %s\n' % (heating_rate, const.GAS_CONST))
        f.write('\t# A, n, E values\n')
        for i in range(len(kmatrix)):
            f.write('\tA%s = %s\n\tn%s = %s\n\tE%s = %s\n' % (i, kmatrix[i][0], i, kmatrix[i][1], i, kmatrix[i][2]))

        # define initial condition
        f.write('\n\t# Initial conditions\n')
        f.write('\tT0 = %s\n' %(T0+273.15))
        f.write('\tPLIGC = %s\n\tPLIGH = %s\n\tPLIGO = %s\n' % (PLIGC_0, PLIGH_0, PLIGO_0))
        IC = ''
        for i in y_list:
            if i == 'PLIGC' or i == 'PLIGH' or i == 'PLIGO':
                continue
            else:
                IC += ('%s = ' % i)
        IC += '0'
        f.write('\t' + IC + '\n\n')

        # define ODE solver parameters
        f.write('\t# ODE solver parameters\n')
        f.write('\tabserr = %s\n' % const.ABSOLUTE_TOLERANCE)
        f.write('\trelerr = %s\n' % const.RELATIVE_TOLERANCE)
        stoptime = (Tmax-T0) / heating_rate
        f.write('\tstoptime = %s\n' %stoptime)
        f.write('\tnumpoints = %s\n\n' %(round(stoptime/0.1)))

        f.write('\tt = [stoptime * float(i) / (numpoints - 1) for i in range(numpoints)]\n')
        y0 = '\ty0 = [T0'
        for spec in y_list:
            y0 += ', %s' % spec
        y0 += ']\n'
        f.write(y0)

        p = '\tp = [alpha, R'
        for i in range(len(kmatrix)):
            p += ', A%s, n%s, E%s' % (i, i, i)
        p += ']\n'
        f.write(p)

        """
        f.write('\nstep = 0\n')
        f.write("with open('sol_heating_%s.dat', 'a') as f:\n" %species_IC)
        f.write('\tprint(t[0], "\\t".join(str(y) for y in y0), sep="\\t", file=f)\n')
        f.write('\twhile step < (len(t)-1):\n')
        f.write('\t\tysol = odeint(ODEs, y0, [t[step], t[step+1]], args=(p,), atol=abserr, rtol=relerr)\n')
        f.write('\t\tysol[1] = ysol[1].clip(min=0)\n')
        """
        f.write('\n\tysol = odeint(ODEs, y0, t, args=(p,), atol=abserr, rtol=relerr, mxstep=5000)\n\n')
        f.write("\twith open('sol_heating_%s.dat', 'w') as f:\n" %species_IC)
        f.write("\t\tdata_format = '{:15.10f}' * %s\n" %(len(y_list)+2))
        """
        ysol = ''
        for i in range(len(y_list)):
            ysol += 'yy[%s], ' % i
        """
        f.write('\t\tfor tt, yy in zip(t, ysol):\n')
        f.write('\t\t\tprint(data_format.format(tt, *yy), file=f)\n')
        f.write('\t\tend = time.time()\n\t\trun_time = end - start\n\t\tprint(run_time, file=f)\n\n\n')

        f.write("if __name__ == '__main__':\n\trun()")



def isothermal(species_IC='Pseudotsuga_menziesii', continue_simu=True, T=500):

    reactionlist, rateconstantlist, compositionlist, module_dir = lig.set_paths()
    y_list = lig.get_specieslist(reactionlist)
    speciesindices, indices_to_species = lig.get_speciesindices(y_list)
    kmatrix = lig.build_k_matrix(rateconstantlist)
    rate_list = lig.build_rates_list_kexp(rateconstantlist, reactionlist, speciesindices)
    species_rxns = lig.build_species_rxns_dict(reactionlist)
    dydt_expressions = lig.build_dydt_list(rate_list, y_list, species_rxns)
    PLIGC_0, PLIGH_0, PLIGO_0 = lig.define_initial_composition(compositionlist, species_IC)

    stoptime = 2000
    IC = [0] * len(y_list)
    IC[speciesindices['PLIGC']] = PLIGC_0
    IC[speciesindices['PLIGH']] = PLIGH_0
    IC[speciesindices['PLIGO']] = PLIGO_0

    """
    if continue_simu is True:
        with open('sol_heating_%s.dat' %species_IC, 'r') as f:
            pre_result = f.readlines()[-2]
            pre_time = eval(pre_result[0])
            T = eval(pre_result[1]) - 273.15
            stoptime = 2000 - pre_time

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
        """

if __name__ == "__main__":
    heating()