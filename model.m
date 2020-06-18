omega_n=0.84;
dzeta=8.4e-10;
k=3.35;
numerator = [k*omega_n*omega_n];
denominator = [1,2*dzeta*omega_n,omega_n*omega_n];
ts = 0.005;
sys_dyskretny = tf(numerator,denominator,ts);
sys_ref=tf([1 -2 7],[ 1 0 0.125 -0.4375],ts);
hold on
impulse(sys_dyskretny)
impulse(sys_ref)
legend('moj','ref')
hold off


