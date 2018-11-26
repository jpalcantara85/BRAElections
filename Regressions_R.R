require(AER, stargazer)

### Used option 'None' back in Python
dataset = read.csv("main_2002-2014_gov.csv")

dataset$is_capital = as.factor(dataset$is_capital)
dataset$macroregion_id = as.factor(dataset$macroregion_id)

model1 = ivreg(deltaVotes_13 ~ IPW + EPW + macroregion_id + is_capital + log(pop) + log(gdp) + f_foreign + f_college + f_white + f_manu + f_comm + fVOTES_45 | IPWiv + EPWiv, data = dataset)
model2 = ivreg(deltaVotes_13 ~ IPW + EPW + macroregion_id + is_capital + log(pop) + log(gdp) + f_foreign + f_college + f_white + f_manu + f_comm + fVOTES_45 | IPWiv + EPWiv + macroregion_id, data = dataset)
model3 = ivreg(deltaVotes_13 ~ IPW + EPW + macroregion_id + is_capital + log(pop) + log(gdp) + f_foreign + f_college + f_white + f_manu + f_comm + fVOTES_45 | IPWiv + EPWiv + macroregion_id + is_capital, data = dataset)
model4 = ivreg(deltaVotes_13 ~ IPW + EPW + macroregion_id + is_capital + log(pop) + log(gdp) + f_foreign + f_college + f_white + f_manu + f_comm + fVOTES_45 | IPWiv + EPWiv + macroregion_id + is_capital + log(pop), data = dataset)
model5 = ivreg(deltaVotes_13 ~ IPW + EPW + macroregion_id + is_capital + log(pop) + log(gdp) + f_foreign + f_college + f_white + f_manu + f_comm + fVOTES_45 | IPWiv + EPWiv + macroregion_id + is_capital + log(pop) + log(gdp), data = dataset)
model6 = ivreg(deltaVotes_13 ~ IPW + EPW + macroregion_id + is_capital + log(pop) + log(gdp) + f_foreign + f_college + f_white + f_manu + f_comm + fVOTES_45 | IPWiv + EPWiv + macroregion_id + is_capital + log(pop) + log(gdp) + fVOTES_45, data = dataset)

model6B = ivreg(deltaVotes_13 ~ IPW + EPW + macroregion_id + is_capital + log(pop) + log(gdp) + f_foreign + f_college + f_white + f_manu + f_comm + fVOTES_11 + fVOTES_12 + fVOTES_14 + fVOTES_15 + fVOTES_17 + fVOTES_25 + fVOTES_41 + fVOTES_43 + fVOTES_44 + fVOTES_45 | IPWiv + EPWiv + macroregion_id + is_capital + log(pop) + log(gdp) + fVOTES_11 + fVOTES_12 + fVOTES_14 + fVOTES_15 + fVOTES_17 + fVOTES_25 + fVOTES_41 + fVOTES_43 + fVOTES_44 + fVOTES_45, data = dataset)

stargazer(model1, model2, model3, model4, model5, model6, model6B, type = "latex", title = "Import/Export Exposures and Governor Elections Outcomes 2002-2014 for PT")

model7 = ivreg(deltaVotes_45 ~ IPW + EPW + macroregion_id + is_capital + log(pop) + log(gdp) + f_foreign + f_college + f_white + f_manu + f_comm + fVOTES_13 | IPWiv + EPWiv, data = dataset)
model8 = ivreg(deltaVotes_45 ~ IPW + EPW + macroregion_id + is_capital + log(pop) + log(gdp) + f_foreign + f_college + f_white + f_manu + f_comm + fVOTES_13 | IPWiv + EPWiv + macroregion_id, data = dataset)
model9 = ivreg(deltaVotes_45 ~ IPW + EPW + macroregion_id + is_capital + log(pop) + log(gdp) + f_foreign + f_college + f_white + f_manu + f_comm + fVOTES_13 | IPWiv + EPWiv + macroregion_id + is_capital, data = dataset)
model10 = ivreg(deltaVotes_45 ~ IPW + EPW + macroregion_id + is_capital + log(pop) + log(gdp) + f_foreign + f_college + f_white + f_manu + f_comm + fVOTES_13 | IPWiv + EPWiv + macroregion_id + is_capital + log(pop), data = dataset)
model11 = ivreg(deltaVotes_45 ~ IPW + EPW + macroregion_id + is_capital + log(pop) + log(gdp) + f_foreign + f_college + f_white + f_manu + f_comm + fVOTES_13 | IPWiv + EPWiv + macroregion_id + is_capital + log(pop) + log(gdp), data = dataset)
model12 = ivreg(deltaVotes_45 ~ IPW + EPW + macroregion_id + is_capital + log(pop) + log(gdp) + f_foreign + f_college + f_white + f_manu + f_comm + fVOTES_13 | IPWiv + EPWiv + macroregion_id + is_capital + log(pop) + log(gdp) + fVOTES_13, data = dataset)

model12B = ivreg(deltaVotes_45 ~ IPW + EPW + macroregion_id + is_capital + log(pop) + log(gdp) + f_foreign + f_college + f_white + f_manu + f_comm + fVOTES_11 + fVOTES_12 + fVOTES_14 + fVOTES_15 + fVOTES_17 + fVOTES_25 + fVOTES_41 + fVOTES_43 + fVOTES_44 + fVOTES_13 | IPWiv + EPWiv + macroregion_id + is_capital + log(pop) + log(gdp) + fVOTES_11 + fVOTES_12 + fVOTES_14 + fVOTES_15 + fVOTES_17 + fVOTES_25 + fVOTES_41 + fVOTES_43 + fVOTES_44 + fVOTES_13, data = dataset)

stargazer(model7, model8, model9, model10, model11, model12, model12B, type = "latex", title = "Import/Export Exposures and Governor Elections Outcomes 2002-2014 for PSDB")
