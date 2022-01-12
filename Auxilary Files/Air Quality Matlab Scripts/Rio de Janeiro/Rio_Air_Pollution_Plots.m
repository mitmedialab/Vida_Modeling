%% Read spreadsheet and import the data into MATLAB

rio_data = readtable('Rio Data Updated 1 Trimmed.csv');
sorted = rmmissing(sortrows(rio_data, 3), 'DataVariables', {'PM10'}); %sort by the ID number and remove NaN

%% Separate into different geographical regions by region ID

%find unique IDs
rio_split_indexes= zeros(8, 2);
ID = rio_data(:,3);
IDcell = table2array(ID);
[C, ia] = unique(sorted.CodNum, 'stable'); %determine index of first instance of each unique ID num

%divide into separate lists by ID
AV = sorted(ia(1):ia(2)-1, :); %AV = 1
BG = sorted(ia(2):ia(3)-1, :); %BG = 2
CA = sorted(ia(3):ia(4)-1, :); %CA = 3
CG = sorted(ia(4):ia(5)-1, :); %CG = 4
IR = sorted(ia(5):ia(6)-1, :); %IR = 5
PG = sorted(ia(6):ia(7)-1, :); %PG = 6
SC = sorted(ia(7):ia(8)-1, :); %SC = 7
SP = sorted(ia(8):end, :); %SP = 8

%% Plot all unaltered data on one plot
clf
[dates_BG,pm10_vals_BG, datetimes_BG] = pm10(BG);
plot1 = plot(dates_BG, pm10_vals_BG);
plot1.Color(4) = 0.5;

hold
[dates_CG,pm10_vals_CG, datetimes_CG] = pm10(CG);
plot2 = plot(dates_CG, pm10_vals_CG);
plot2.Color(4) = 0.5;

[dates_CA,pm10_vals_CA, datetimes_CA] = pm10(CA);
plot3 = plot(dates_CA, pm10_vals_CA);
plot3.Color(4) = 0.5;

[dates_AV,pm10_vals_AV, datetimes_AV] = pm10(AV);
plot4 = plot(dates_AV, pm10_vals_AV);
plot4.Color(4) = 0.5;

[dates_IR,pm10_vals_IR, datetimes_IR] = pm10(IR);
plot5 = plot(dates_IR, pm10_vals_IR);
plot5.Color(4) = 0.5;

[dates_PG,pm10_vals_PG, datetimes_PG] = pm10(PG);
plot6 = plot(dates_PG, pm10_vals_PG);
plot6.Color(4) = 0.5;

[dates_SC,pm10_vals_SC, datetimes_SC] = pm10(SC);
plot7 = plot(dates_SC, pm10_vals_SC);
plot7.Color(4) = 0.5;

[dates_SP,pm10_vals_SP, datetimes_SP] = pm10(SP);
plot8 = plot(dates_SP, pm10_vals_SP);
plot8.Color(4) = 0.5
legend('BG', 'CG', 'CA', 'AV', 'IR', 'PG', 'SC', 'SP')
datetick('x','keeplimits')
grid
title('Rio de Janeiro PM10 Measurements');
xlabel('Date');
ylabel('PM10') ;

%% Calculating Weekly Means
BG_week_array_means = weeklymean(datetimes_BG, pm10_vals_BG);
%% Plot Mean Corrected Data

%% for BG
figure
plot(dates_BG, pm10_vals_BG)
hold all
corrected_pm10_means_BG = correct_for_variation(dates_BG, BG_week_array_means(:,3));

title("BG PM10 Means")
datetick('x','keeplimits')
legend("Unsmoothed Data", "Weekly-Averaged Data", "Seasonal Variation", "Seasonal Corrected Data", "Annual Variation", "Final Corrected Data")
plotbrowser('toggle')

%% Calculating weekly medians
BG_week_array_medians = weeklymedian(datetimes_BG, pm10_vals_BG, 'yyyy/MM/dd HH:mm:ss');
%% Plot median corrected data

figure
plot(dates_BG, pm10_vals_BG);
hold all
corrected_pm10_medians_BG = correct_for_variation(dates_BG, BG_week_array_medians(:,3));
title("BG PM10 Medians")
xlabel('Date')
ylabel('PM10 Measurements')
datetick('x','keeplimits')
legend("Unsmoothed Data", "Weekly Median", "Seasonal Variation", "Seasonal Corrected Data", "Annual Variation", "Final Corrected Data")
plotbrowser('toggle')


%% Divide data at March 2020
[pm10_preCovid_BG, pm10_postCovid_BG] = trimdata('2020/03/01 00:00:00', corrected_pm10_medians_BG);
%% Plot normalized histogram/distribution of pre and post Covid data

clf
figure
hist_preCovid_BG = histogram(pm10_preCovid_BG, 'Normalization', 'pdf')
hist_preCovid_BG.BinWidth = 1;
hold
hist_postCovid_BG = histogram(pm10_postCovid_BG, 'Normalization', 'pdf')
hist_postCovid_BG.BinWidth = 1;
title("PM10 Histograms BG")
legend("Before 03/01/2020", "Post 03/01/2020")
ylabel('Probability')
xlabel('Corrected PM10 Value')

normalized_preCovid = hist_preCovid_BG.Values;
normalized_postCovid = hist_postCovid_BG.Values;


%% Anderson Darling Test and Two-Sample T-Test

%AD Test
mu_preCovid = mean(normalized_preCovid)
sigma_preCovid = std(normalized_preCovid);
dist = makedist('normal','mu',mu_preCovid,'sigma',sigma_preCovid);
mu_postCovid = mean(normalized_postCovid)
[h_ad,p_ad] = adtest(normalized_preCovid,'Distribution',dist) %1 for reject null


%Two Sample T Test

[h_tt,p_tt] = ttest2(normalized_preCovid,normalized_postCovid)

%% Show Map of DeltaMean (Note: Requires Mapping Toolbox )

clf
MapLatLimit = [-22.8 -23.1];
MapLonLimit = [-43.8 -43.1];
bairros = shaperead('Bairros.shp')
axesm('MapProjection', 'eqaconic', 'MapParallels', [],...
  'MapLatLimit', MapLatLimit, 'MapLonLimit', MapLonLimit,...
  'GLineStyle', '-')
geoshow(bairros, 'DisplayType', 'polygon', 'FaceColor','white')

for i = 1:size(bairros,1)
    [bairros(i).('deltaMean')] = 0;
end

%% Need to input table with number, deltaMean, and display name

datacells = {98 'Centro' 0.0108*1/.0119; 142 'Copacobana' -0.0153*1/.956; 118 'Tijuca' 0.0063*1/.0839; 22 'Iraja' 0.0046*1/.6295; 20 'Bangu' 0.007*1/.2645; 8 'Campo Grande' 0.0081*1/.3806; 152 'Pedra de Guaratiba' 0.0018*1/.7844; 88 'Sao Cristovao' 0.0057*1/.3913};
datatable = cell2table(datacells, 'VariableNames', {'Number', 'Name', 'DeltaMean'});
%%
clf

for i = 1:size(datatable,1)
    bairros(datatable(i,:).Number).deltaMean = datatable(i,:).DeltaMean;
end
%%
maxdeltaMean = 1.2;
mindeltaMean = -0.01;
color = flipud(parula(numel(bairros)));
densityColors = makesymbolspec('Polygon', {'deltaMean', ...
   [mindeltaMean maxdeltaMean], 'FaceColor', color});

geoshow(bairros, 'DisplayType', 'polygon', ...
   'SymbolSpec', densityColors)
title ({'P-Value Weighted Change in PM10 Emission Mean Post March 2020 (Data until 04/30/21)', ...
   'in  μg/m3'})
caxis([mindeltaMean maxdeltaMean])
colormap(color)
colorbar
for i = 1:size(datatable,1)
    meanValue = mean(bairros(datatable(i,:).Number).BoundingBox)
    text(meanValue(1),meanValue(2),datatable(i,:).Name)
end
yyaxis right
ylabel('Change in Mean of PM10 Measurements')
