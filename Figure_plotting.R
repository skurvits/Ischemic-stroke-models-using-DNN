library("tidyverse")
library("ggplot2")
library("ggpubr")
library("ggVennDiagram")
library("ggsci")
library("ggvenn")

Case_Control_joonis <- function(ccdata, plotname) {
#Case and control groups comparison figure

  ccdata$I63_CASE <-  as.factor(ccdata$I63_CASE)
  ccdata$sex <-  as.factor(ccdata$sex)
  
  t_cases <- ccdata %>%filter(I63_CASE == 1)
  juhudicd10 <- unique(names(sort(table(t_cases$ICD10))))
  
  t_controls <- ccdata %>%filter(I63_CASE == 0)
  #sort(table(t_controls$ICD10))
  
  kontrollidicd10 <- unique(names(sort(table(t_controls$ICD10))))
  
  
  plot_A <- ccdata %>% distinct(s_code, .keep_all = TRUE)
  
  means <- aggregate(birth_year ~  I63_CASE, plot_A, mean)
  
  pA <- ggplot(plot_A, aes(fill=I63_CASE, y=age_at_measurement, x=sex)) + 
    geom_boxplot() + 
    theme_minimal(base_size = 14)+
    scale_fill_locuszoom(name="Group", labels=c("Control","Case")) +
    scale_x_discrete(labels=c("Male", "Female")) +
    labs(x="Sex", y="Age")
  
  
  pB<- ggplot(ccdata, aes(fill=I63_CASE, y=count_analytes, x=sex)) + 
    geom_boxplot() + 
    theme_minimal(base_size = 14)+
    scale_fill_locuszoom(name="Group", labels=c("Control","Case")) +
    scale_x_discrete(labels=c("Male", "Female")) +
   labs(x="Sex", y="Nr of analytes")
  
  x <- list(
    Controls = kontrollidicd10, 
    Cases = juhudicd10)
  
  mypal = pal_locuszoom()(7)
  pD <- ggvenn(
    x, fill_color = mypal[1:3], columns = c("Controls", "Cases")) +
    labs(title ="Unique ICD10 codes present")
  
  ggarrange(pA, pB, pD, labels = c("A","B", "D"),
           common.legend = TRUE, legend = "bottom", ncol=3, nrow=1) %>%
    ggexport(filename = plotname, width = 660)

  return("Done")
}



#Sensitivity analysis figure
#Data for plotting:
#ICD-10 codes present only for the cases group
only_cases = c("A09", "A56", "B02", "B18", "B23", "C79", "C85", "D10", "D25", "D80", "E13", "E16", "F04", "F20", "F45", "G46", "G57", "G70", "H04", "H43", "H47",
              "H66", "H82", "I34", "I35", "I36", "I89", "I97", "J09", "J14", "J95", "K26", "L04", "L23", "L43", "L85", "M53", "M60", "N03", "N08", "N12", "N23",
              "N32", "N61", "O70", "O91", "R02", "R09", "R19", "R93", "T22", "X41", "X64", "Y52", "Y60", "Z98", "D27", "F03", "Y44", "K92", "Z10", "I69")

TabNet_sens_auc <- c() #List on AUC values
FastAI_sens_auc <- c() #List on AUC values
RF_sens_auc <- c() #List on AUC values



TabNet_hist <- data.frame(TabNet_sens_auc)

mypal = pal_locuszoom()(7)
p_tabnet<-ggplot(TabNet_hist, aes(x=TabNet_sens_auc)) + 
  geom_histogram(fill=mypal[1], color= "black") +
  theme_minimal(base_size = 14)+
  labs(x="AUC value", y="Count") + 
  geom_vline(aes(xintercept = 0.908),
  color=mypal[5], linetype="dashed", size=1)


FastAI_hist <- data.frame(FastAI_sens_auc)

mypal = pal_locuszoom()(7)
p_fastai<-ggplot(FastAI_hist, aes(x=FastAI_sens_auc)) + 
  geom_histogram(fill=mypal[1], color= "black") +
  theme_minimal(base_size = 14)+
  labs(x="AUC value", y="Count") + 
  geom_vline(aes(xintercept = 0.879),
             color=mypal[5], linetype="dashed", size=1)


RFI_hist <- data.frame(RF_sens_auc)

mypal = pal_locuszoom()(7)
p_rf<-ggplot(RFI_hist, aes(x=RF_sens_auc)) + 
  geom_histogram(fill=mypal[1], color= "black") +
  theme_minimal(base_size = 14)+
  labs(x="AUC value", y="Count") +
  geom_vline(aes(xintercept = 0.9423747276688453),
  color=mypal[5], linetype="dashed", size=1)



ggarrange(p_rf, p_fastai, p_tabnet, labels = c("Random Forest", "FastAI", "TabNet"),
          common.legend = TRUE, legend = "bottom", nrow=1)
