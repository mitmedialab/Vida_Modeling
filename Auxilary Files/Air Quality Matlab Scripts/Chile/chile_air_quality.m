clear all
%% Read spreadsheet and import the data into MATLAB
%the spreadsheet is a compiled spreadsheet of all the measurements in the 
%Metropolitana region for all of the years stitched together - if doing 
%this for other parameter, make sure that the regions are lined up properly

chile_data = readtable('Chile_CO_Data_Compiled.csv');
%% Sort into different regions
%grab the appropriate columns and remove NaN vals

IN = rmmissing(chile_data(7:end, [1 2]),1); %Independencia
LF = rmmissing(chile_data(7:end, [1 3]),1);%La Florida
LC = rmmissing(chile_data(7:end, [1 4]),1); %Las Condes
ST = rmmissing(chile_data(7:end, [1 5]),1); %Santiago
PD = rmmissing(chile_data(7:end, [1 6]),1); %Pudahuel
CR = rmmissing(chile_data(7:end, [1 7]),1); %Cerrillos
EB = rmmissing(chile_data(7:end, [1 8]),1); %El Bosque
CN = rmmissing(chile_data(7:end, [1 9]),1); %Cerro Navia
PA = rmmissing(chile_data(7:end, [1 10]),1); %Puente Alto
TL = rmmissing(chile_data(7:end, [1 11]),1); %Talagante
QL = rmmissing(chile_data(7:end, [1 12]),1); %Quilicura

%% Plot all unaltered CO data
%separate into vectors for dates (as doubles for plotting purposes), the
%sensor measurements, and the actual date

[dates_IN, CO_vals_IN, datetimes_IN] = chile_CO(IN);
plot1 = plot(dates_IN, CO_vals_IN) %plot
plot1.Color(4) = 0.5; %lower transparency of plot

hold

[dates_LF, CO_vals_LF, datetimes_LF] = chile_CO(LF);
plot2 = plot(dates_LF, CO_vals_LF)
plot2.Color(4) = 0.5;

[dates_LC, CO_vals_LC, datetimes_LC] = chile_CO(LC);
plot3 = plot(dates_LC, CO_vals_LC)
plot3.Color(4) = 0.5;

[dates_ST, CO_vals_ST, datetimes_ST] = chile_CO(ST);
plot4 = plot(dates_ST, CO_vals_ST)
plot4.Color(4) = 0.5;

[dates_PD, CO_vals_PD, datetimes_PD] = chile_CO(PD);
plot5 = plot(dates_PD, CO_vals_PD)
plot5.Color(4) = 0.5;

[dates_CR, CO_vals_CR, datetimes_CR] = chile_CO(CR);
plot6 = plot(dates_CR, CO_vals_CR)
plot6.Color(4) = 0.5;

[dates_EB, CO_vals_EB, datetimes_EB] = chile_CO(EB);
plot7 = plot(dates_EB, CO_vals_EB)
plot7.Color(4) = 0.5;

[dates_CN, CO_vals_CN, datetimes_CN] = chile_CO(CN);
plot8 = plot(dates_CN, CO_vals_CN)
plot8.Color(4) = 0.5;

[dates_PA, CO_vals_PA, datetimes_PA] = chile_CO(PA);
plot9 = plot(dates_PA, CO_vals_PA)
plot9.Color(4) = 0.5;

[dates_TL, CO_vals_TL, datetimes_TL] = chile_CO(TL);
plot10 = plot(dates_TL, CO_vals_TL)
plot10.Color(4) = 0.5;

[dates_QL, CO_vals_QL, datetimes_QL] = chile_CO(QL);
plo11 = plot(dates_QL, CO_vals_QL)
plot11.Color(4) = 0.5;

legend("Independencia (IN)", "La Florida (LF)", "Las Condes (LC)", "Santiago (ST)", "Pudahuel (PD)", "Cerrillos (CR)", "El Bosque (EB)", "Cerro Navia (CN)","Puente Alto (PA)", "Talagante (TL)", "Quilicura (QL)")
datetick('x','keeplimits')
grid
title('Chile Metropolitana CO Measurements');
xlabel('Date');
ylabel('CO') ;

%% Calculate and plot weekly medians
%calculates the weekly median, takes the format for the date column 
IN_week_array_medians = weeklymedian(datetimes_IN, CO_vals_IN, "MM/dd/yyyy HH:mm"); 

figure
plot(dates_IN, CO_vals_IN);
hold all
corrected_CO_medians_IN = correct_for_variation(dates_IN, IN_week_array_medians(:,3));

title("IN CO Medians")
xlabel('Date')
ylabel('CO Measurements')
datetick('x','keeplimits')
legend("Unsmoothed Data", "Weekly Median", "Seasonal Variation", "Seasonal Corrected Data", "Annual Variation", "Final Corrected Data")
plotbrowser('toggle')

%% Divide data at March 2020
%creates two vectors of data, using one date in YYYY/MM/DD HH:MM:SS as a
%dividing point

[CO_preCovid_IN, CO_postCovid_IN] = trimdata('2020/03/01 00:00:00', corrected_CO_medians_IN);
%% Plot normalized histogram/distribution of pre and post Covid data
%plots normalized histograms for the two vectors of data

clf
figure
hist_preCovid_IN = histogram(CO_preCovid_IN, 'Normalization', 'pdf')
hist_preCovid_IN.BinWidth = .05;
hold
hist_postCovid_IN = histogram(CO_postCovid_IN, 'Normalization', 'pdf')
hist_postCovid_IN.BinWidth = .05;
title("CO Histograms IN")
legend("Before 03/01/2020", "Post 03/01/2020")
ylabel('Probability')
xlabel('Corrected CO Value')

normalized_preCovid = hist_preCovid_IN.Values;
normalized_postCovid = hist_postCovid_IN.Values;
%% Anderson Darling Test and Two-Sample T-Test
%run the Anderson Darling test - how well the sample fits a normal
%distribution
%run the two-sample t-test - how well the mean of two sets of data match

%AD Test
mu_preCovid = mean(normalized_preCovid)
sigma_preCovid = std(normalized_preCovid);
dist = makedist('normal','mu',mu_preCovid,'sigma',sigma_preCovid);
mu_postCovid = mean(normalized_postCovid)
[h_ad,p_ad] = adtest(normalized_preCovid,'Distribution',dist) %1 for reject null


%Two Sample T Test
[h_tt,p_tt] = ttest2(normalized_preCovid,normalized_postCovid)