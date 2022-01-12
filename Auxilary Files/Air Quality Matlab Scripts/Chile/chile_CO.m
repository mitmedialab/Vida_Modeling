function [dates, CO, datetimes] = chile_CO(array)
    CO_data = array(:,2);
    CO_temp = table2array((CO_data));
    CO = str2double(CO_temp);
    
    date_time = array(:,1);
    datecell = table2array(date_time);
    datetimes_length = size(date_time,1);

    datetimes = strings(datetimes_length, 1);
    for i = 1:datetimes_length
        datetimes(i)= char(datecell(i));
    end
    dates = datenum(datetimes);
end