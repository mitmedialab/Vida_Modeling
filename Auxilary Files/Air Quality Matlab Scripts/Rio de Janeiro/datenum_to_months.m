function nummonths = datenum_to_months(numdays) 

numweeks = round(numdays/7);
numdaysvec = datevec(numdays);
nummonths = numdaysvec(1)*12 + numdaysvec(2) - 1;

end