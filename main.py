import fourth_stage as four

# necessary constants
R_Moon = 1738000

x_start = 0
y_start = R_Moon

Vres, Hres, m = four.blast(x_start, y_start)
from_4_to_5=open('from_4_to_5.txt', 'w')
print(round(Vres,3), round(Hres,3), file=from_4_to_5)
from_4_to_5.close()
