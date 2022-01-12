function week_array = weeklymedian(datetimes, data_vals, input_format_string)

weeks = week(datetime(datetimes, 'InputFormat', input_format_string));
week_array = [data_vals weeks];
week_array(1,3) = 0; %placeholder for medians

weekly_meds = [];
med = [week_array(1, 1)];
num_in_week = 1;
for day = 2:size(week_array, 1)
    week_num = week_array(day, 2);
    if week_num == week_array(day-1,2)
        med(end + 1) = week_array(day, 1);
        num_in_week = num_in_week+1;
    else
        med_for_the_week = median(med);
        weekly_meds(end+1)  = med_for_the_week;
        week_array(day-num_in_week:day-1, 3) = med_for_the_week;
        med = [week_array(day,1)];
        num_in_week = 1;
    end
end

end
