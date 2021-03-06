from SloppyCell.ReactionNetworks import *

net = IO.from_SBML_file('BIOMD0000000002.xml')
net.set_initial_var_value('B', 1)
net.set_var_constant('L', True)

# There are many fewer free parameters in the model than indicated in the
# SBML file. Here we add the rules required to translate between the parameters
# Edelstein actually consider and those used in the equations.
net.add_parameter('B_k_on', 1.5e8)
net.add_parameter('B_k_off', 8000)
net.add_parameter('BAp', 0.2)
net.add_parameter('BA_k_2', 3e4)
net.add_parameter('AB_k_2', 7e2)

net.add_parameter('A_k_on', 1.5e8)
net.add_parameter('A_k_off', 8.64)
net.add_parameter('AIp', 0.99)
net.add_parameter('AI_k_2', 20.0)
net.add_parameter('IA_k_2', 0.81)

net.add_parameter('I_k_on', 1.5e8)
net.add_parameter('I_k_off', 4.0)
net.add_parameter('IDp', 0.99)
net.add_parameter('ID_k_2', 5e-2)
net.add_parameter('DI_k_2', 1.2e-3)

net.add_parameter('D_k_on', 1.5e8)
net.add_parameter('D_k_off', 4.0)

net.add_parameter('B_K_d')
net.add_assignment_rule('B_K_d', 'B_k_off/B_k_on')
net.add_parameter('A_K_d')
net.add_assignment_rule('A_K_d', 'A_k_off/A_k_on')
net.add_parameter('I_K_d')
net.add_assignment_rule('I_K_d', 'I_k_off/I_k_on')
net.add_parameter('D_K_d')
net.add_assignment_rule('D_K_d', 'D_k_off/D_k_on')
net.add_parameter('BAc')
net.add_assignment_rule('BAc', 'A_K_d/B_K_d')
net.add_parameter('AIc')
net.add_assignment_rule('AIc', 'I_K_d/A_K_d')
net.add_parameter('IDc')
net.add_assignment_rule('IDc', 'D_K_d/I_K_d')

net.add_assignment_rule('kf_0', '2 * B_k_on')
net.add_assignment_rule('kr_0', 'B_k_off')
net.add_assignment_rule('kf_1', 'B_k_on')
net.add_assignment_rule('kr_1', '2 * B_k_off')
net.add_assignment_rule('kf_2', 'BA_k_2')
net.add_assignment_rule('kr_2', 'AB_k_2')
net.add_assignment_rule('kf_3', '2 * A_k_on')
net.add_assignment_rule('kr_3', 'A_k_off')
net.add_assignment_rule('kf_4', 'A_k_on')
net.add_assignment_rule('kr_4', '2 * A_k_off')
net.add_assignment_rule('kf_6', 'BA_k_2*BAc**(1 - BAp)')
net.add_assignment_rule('kr_6', 'AB_k_2/BAc**BAp')
net.add_assignment_rule('kf_5', 'kf_6*BAc**(1 - BAp)')
net.add_assignment_rule('kr_5', 'kr_6/BAc**BAp')
net.add_assignment_rule('kf_7', '2 * I_k_on')
net.add_assignment_rule('kr_7', 'I_k_off')
net.add_assignment_rule('kf_8', 'I_k_on')
net.add_assignment_rule('kr_8', '2 * I_k_off')
net.add_assignment_rule('kf_10', 'AI_k_2*AIc**(1 - AIp)')
net.add_assignment_rule('kr_10', 'IA_k_2/AIc**AIp')
net.add_assignment_rule('kf_9', 'kf_10*AIc**(1 - AIp)')
net.add_assignment_rule('kr_9', 'kr_10/AIc**AIp')
net.add_assignment_rule('kf_11', 'AI_k_2')
net.add_assignment_rule('kr_11', 'IA_k_2')
net.add_assignment_rule('kf_12', '2 * D_k_on')
net.add_assignment_rule('kr_12', 'D_k_off')
net.add_assignment_rule('kf_13', 'D_k_on')
net.add_assignment_rule('kr_13', '2 * D_k_off')
net.add_assignment_rule('kf_14', 'ID_k_2')
net.add_assignment_rule('kr_14', 'DI_k_2')
net.add_assignment_rule('kf_16', 'ID_k_2*IDc**(1 - IDp)')
net.add_assignment_rule('kr_16', 'DI_k_2/IDc**IDp')
net.add_assignment_rule('kf_15', 'kf_16*IDc**(1 - IDp)')
net.add_assignment_rule('kr_15', 'kr_16/IDc**IDp')

net1 = net.copy('progression')
net1.set_initial_var_value('L', 1e-5)

traj = Dynamics.integrate(net1, [0, 20])
vals = traj.last_dynamic_var_values()
net2 = net.copy('recovery')
net2.set_dyn_var_ics(vals)
net2.set_initial_var_value('L', 0)

networks = [net1, net2]
int_times = [(10**-5, 10**2), (10**-3, 10**4)]
