function week_array = weeklymean(datetimes, data_vals)

weeks = week(datetime(datetimes, 'InputFormat', 'yyyy/MM/dd HH:mm:ss'));
week_array = [data_vals weeks];
week_array(1,3) = 0; %placeholder for means

weekly_avgs = [];
avg = [week_array(1, 1)];
num_in_week = 1;
for day = 2:size(week_array, 1)
    week_num = week_array(day, 2);
    if week_num == week_array(day-1,2)
        avg(end + 1) = week_array(day, 1);
        num_in_week = num_in_week+1;
    else
        avg_for_the_week = sum(avg)/size(avg,2);
        weekly_avgs(end+1)  = avg_for_the_week;
        week_array(day-num_in_week:day-1, 3) = avg_for_the_week;
        avg = [week_array(day,1)];
        num_in_week = 1;
    end
end

end
