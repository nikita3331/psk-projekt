omega_n=0.84;
dzeta=8.4e-10;
k=3.35;
numerator = [k*omega_n*omega_n];
denominator = [1,2*dzeta*omega_n,omega_n*omega_n];
ts = 0.005;
sys_dyskretny = tf(numerator,denominator,ts);
sys_nowy=tf([3.35],[ 4.74 1 0],ts);
bode(sys_dyskretny)

