function final_array = correct_for_variation(dates, data_vals)
plot(dates, data_vals);
hold all

%find seasonal variation
[ft, rmse]= sinefit(dates, data_vals);
seasonal_var = sineval(ft, dates);
plot(dates,seasonal_var);

corrected_seasonal = data_vals - seasonal_var;
plot(dates, corrected_seasonal);

% use linear regression to find the general trend
[p, S, mu] = polyfit(dates,corrected_seasonal,1);
[general_trend, delta] = polyval(p, dates, S, mu);
plot(dates, general_trend);
final =  corrected_seasonal- general_trend;
plot(dates, final);

final_array = [dates, final];

end