data = load('data_packets.dat');
begin_hour = 16;

time = data(:,1);

received_if = data(:,2);
sent_if = data(:,3);
diff_received_if = data(:,4); 
diff_sent_if = data(:,5);

received_ip = data(:,6);
sent_ip = data(:,7);
diff_received_ip = data(:,8); 
diff_sent_ip = data(:,9);


figure
hold on
plot(time, received_if)
plot(time, sent_if)
title('Absolute values [Interface]');
xlabel('Time (min)');
ylabel('Number of packets');
legend('Received', 'Sent');
hold off

figure
hold on
plot(time, diff_received_if)
plot(time, diff_sent_if)
title('Difference values [Interface]');
xlabel('Time (min)');
ylabel('Number of packets added');
legend('Received', 'Sent');
hold off

figure
hold on
plot(time, received_ip)
plot(time, sent_ip)
title('Absolute values [IP]');
xlabel('Time (min)');
ylabel('Number of packets');
legend('Received', 'Sent');
hold off

figure
hold on
plot(time, diff_received_ip)
plot(time, diff_sent_ip)
title('Difference values [IP]');
xlabel('Time (min)');
ylabel('Number of packets added');
legend('Received', 'Sent');
hold off

[max_diff_received_if, t1] = max(diff_received_if);
time(t1)
[max_diff_sent_if, t2] = max(diff_sent_if);
time(t2)
[max_diff_received_ip, t3] = max(diff_received_ip);
time(t3)
[max_diff_sent_ip, t4] = max(diff_sent_ip);
time(t4)

hour_peak = mod(begin_hour+time(t1)/60, 24)
fprintf('A peak was reached around %dh50\n', hour_peak)

