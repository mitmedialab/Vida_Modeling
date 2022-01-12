function [preCovid, postCovid] = trimdata(date_string, data_array)
cutoff = datenum(datetime(date_string, 'InputFormat', 'yyyy/MM/dd HH:mm:ss'));
dates = data_array(:,1);
cutoff_index = find(dates > cutoff, 1);

data = data_array(:,2);
preCovid = data(1:cutoff_index-1);
postCovid = data(cutoff_index:end);


end