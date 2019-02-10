#Updated on  NOV 2011 after Zelig's correction
#Prepara os graficos e as analises do Paper de Oxford (meu capítulo)
#Rodando no MAC
#Importante:  No Antes de rodar o codigo é importante escolher AS VARIAVEIS.
#               Pode-se utilizar uma escala economica de tres ou quatro pontos, e a escala ideologica anual ou comparavel entre anos...
#Added unique case ID to cluster SEs



library(Zelig)
library(xtable)
rm(list=ls(all=TRUE))
if(.Platform$OS.type=="unix"){
#run.from <- "~/DATA"
run.from <- "~/Dropbox/DATA"
#options(encoding = 'iso-8859-1')
#options(encoding = 'latin1')
options(encoding = 'native.enc')
}else{
run.from <-"//Files/zucco" 
}
setwd(paste(run.from,"/PLIO-Oxford/Paper-ECPR",sep=""))

load("EconDataSet.Rdta")

z4 <- zelig(econ4~ rescaledraw * as.factor(year), model = "ologit", data = the.data)  #THIS IS THE REGRESSION
z <- zelig(econ~ ideo * as.factor(year), model = "ologit", data = the.data) 

sum(predict(z)==as.character(z$model$econ))/length(predict(z)) 

#First differences: Change in the prob of answering state sector dominante and pure market economy, in changing from 2 to 9 ideologically
fd.all<-NULL
for(i in 1:length(levels(the.data$year))){
    y <- levels(the.data$year)[i]
    x.l <- setx(z, ideo=2,year=y)
    x.r <- setx(z, ideo=9,year=y)
    sim.x <- sim(z,x=x.l, x1=x.r) 
    ev.l <- summary(sim.x)$qi.stats$ev[c("PREDOMÍNIO ESTATAL","MERCADO"),] #get expected values for the two responses when ideo=left (2)
    fd  <- summary(sim.x)$qi.stats$fd[c("PREDOMÍNIO ESTATAL","MERCADO"),] #get first dif for the two responses when ideo=left changes to 9
    rr  <- summary(sim.x)$qi.stats$r[c("PREDOMÍNIO ESTATAL","MERCADO"),] #get risk rations for the two responses when mstr=left 
    year.data <- cbind(as.numeric(y),ev.l,fd,rr)
    fd.all <- rbind(fd.all,year.data)
}

#### Plot a typical left and right legislator in each year
backbarplot <- function(z,x1,x2,cat=4){ #plot predicted probabilities of two different scenarios...
    mat <- matrix(c(1,2,3),nrow=1,ncol=3)
    layout(mat,widths=c(0.4,0.2,0.4,heights=1))
    par(mar=c(4,0.4,1.2,0))
    barplot(-summary(sim(z,x1))$qi.stats$ev[,1],cex.names=0.6, beside = TRUE,  xpd=FALSE,horiz = TRUE,ylab="",bty="n",names.arg=FALSE, las=2,xlim=c(-1,0),xaxt="n")
    axis(side=1,at=seq(0,-1,-0.2),labels= seq(0.0,1.0,0.2),las=2)
    mtext(paste("Left"),side=3,line=-0.1,cex=1.2)
    mtext("Predicted Probability",side=1,line=2.4,cex=1)
    the.names <- levels(summary(z)$model[,1])
    the.names <-gsub("Predominantly Statist","Predominatly\nStatist",the.names)
    the.names <-gsub("State-Market Equilibrium" ,"State-Market\nParity",the.names)
    the.names <-gsub("Market Economy","Market\nEconomy",the.names)
    the.names <-gsub("ESTATAL","STATE LED",the.names)
    plot(c(-1,1),c(0.5,length(the.names)+0.5),type="n", bty="n",xaxt="n",yaxt="n",ylab="",xlab="")
    text(rep(0,4),1:4-0.1,labels=the.names,cex=1,pos=3)
    par(mar=c(4,0,1.2,0.4))
    barplot(summary(sim(z,x2))$qi.stats$ev[,1],cex.names=0.6, beside = TRUE,  xpd=FALSE,horiz = TRUE,ylab="",bty="n",names.arg=FALSE, las=2 ,xlim=c(0,1),xaxt="n")
    axis(side=1,at=seq(0,1,0.2),labels= seq(0.0,1.0,0.2),las=2)
    mtext("Predicted Probability",side=1,line=2.4,cex=1)
    mtext(paste("Right"),side=3,line=-0.1,cex=1.2)
    tab <- data.frame(prob.esquerda=summary(sim(z,x1))$qi.stats$ev[,1],prob.direita=summary(sim(z,x2))$qi.stats$ev[,1],ano=yr,resposta=names(summary(sim(z,x1))$qi.stats$ev[,1]))
    rownames(tab) <- 1:nrow(tab)
    return(tab)
}
   
z4 <- zelig(econ4~ rescaled * as.factor(year), model = "ologit", data = the.data)  #THIS IS THE REGRESSION
z <- zelig(econ~ rescaled * as.factor(year), model = "ologit", data = the.data)  #THIS IS THE REGRESSION

my.table <- NULL
for(y in 1:length(levels(the.data$year))){
    yr<-as.numeric(levels(the.data$year))[y]
    x.l <- setx(z, rescaled=quantile(the.data$rescaled,probs=0.1,na.rm=T),year=yr)
    x.r <- setx(z, rescaled=quantile(the.data$rescaled,probs=0.9,na.rm=T),year=yr)
    jpeg(file=paste("figbars",yr,"BAYES.jpg",sep=""),width=6,height=4,units="in",res=400)
    tab <- backbarplot(z,x.l,x.r,cat=3)
    dev.off()
    my.table <- rbind(my.table,tab)
    #savePlot(paste("H:/LatexFiles/PLIO2009/figbars",yr,sep=""),type="pdf")
}
my.table[20,1:2]-my.table[4,1:2]
my.table[18,1:2]-my.table[2,1:2]
my.table[17,1:2]+my.table[18,1:2]-(my.table[2,1:2]+my.table[1,1:2])

#### Plot the identification with markets in the right
ideoplot <- function(x,sig=0.1,bt=F){ #strange issue prevens passing year as a argynebt to setx
    my.cols <-  c(gray(0.3),gray(0.5),gray(0.7))#gray.colors(3)
   #  my.cols <-  c(gray(0.8),gray(0.85),gray(0.9))#very light
    state.dominant <- pure.market <- equilibrium <- pure.state <- NULL
    for(i in 1:nrow(x)){  tmp.sims <- sim(z,x[i,],bootstrap=bt)
    					  the.sims <- summary(tmp.sims)$qi.stats$ev
    					  pb <- c(0+sig/2,1-sig/2)
    					  the.sims <- cbind(the.sims,t(apply(tmp.sims$qi$ev,2,quantile,probs=pb)))
                         pure.market <- rbind(pure.market,the.sims["Market Economy",])
                         equilibrium <- rbind( equilibrium,the.sims["State-Market Equilibrium",])
                         state.dominant <- rbind( state.dominant,the.sims["Predominantly Statist",])
    if(is.element("Statist",rownames(the.sims))){
                         pure.state <- rbind( pure.state,the.sims["Statist",])}}
    plot(range(x[,2]),c(0,1),type="n",ylab="",xlab="")
    #lines(1:10,pure.state[,1],col=2)
    lb=5;ub=6 #select the costum SE to columns to plot
    polygon(x=c(x[,2],x[nrow(x):1,2]),
            y=c(state.dominant[,lb],state.dominant[nrow(x):1,ub]),
            density=-90,angle=45,col = my.cols[1],lty = 3)
    polygon(x=c(x[,2],x[nrow(x):1,2]),,
            y=c(equilibrium[,lb],equilibrium[nrow(x):1,ub]),
            density=-90,angle=90,col = my.cols[2],lty = 3)
    polygon(x=c(x[,2],x[nrow(x):1,2]),,
            y=c(pure.market[,lb],pure.market[nrow(x):1,ub]),
            density=-100,angle=-45,col = my.cols[3],lty = 3)
    lines(x[,2],state.dominant[,1],col= 1,lwd=2)#my.cols[1])
    lines(x[,2],equilibrium[,1],col=  1,lwd=2)#my.cols[2])
    lines(x[,2],pure.market[,1],col= 1,lwd=2)#  my.cols[3])

    mtext("Ideology",side=1,line=2,cex=1.2)
    mtext(paste("Predicted Probabities in",jj),side=2,line=2.2,cex=1.2)
    legend(x="topleft",legend=rownames(the.sims),fil=my.cols,angle=45,density=-c(70,70,90),bty="n",cex=1.2)
   }


### For figures, used 3 category response only
levels(the.data$econ) <- c("Predominantly Statist","State-Market Equilibrium","Market Economy")
levels(the.data$econ4) <- c("Statist","Predominantly Statist","State-Market Parity","Market Economy")
z <- zelig(econ~ rescaled * year, model = "ologit", data = the.data) #econ is the 3 step

for(jj in levels(the.data$year)){
	#ideospan <- as.numeric(quantile(the.data$rescaledraw,probs=seq(0.005,0.995,by=0.1),na.rm=T))
	ideospan <-seq(-2,2,length=12)#as.numeric(quantile(the.data$rescaled,probs=seq(0.02,0.98,length=12),na.rm=T))
	
	x <- setx(z, rescaled=ideospan,year=as.factor(jj))
	jpeg(file=paste("figstatemarket",jj,"BAYES.jpg",sep=""),width=5,height=5,units="in",res=400)
	par(mar=c(3,3.2,.5,.2))
    ideoplot(x,sig=0.1,bt=F) 
     dev.off()
    cat("done with",jj,"\n")
   }


### Generate table for main body of LAPS paper
print(xtable(summary(z)$coef))
write.csv(summary(z)$coef,file="output_regressiontable.csv")

### Generate table for appendix of LAPS paper comparing the two models
stack.zelig <- function(y,name="reg"){  
	x<-summary(y)                       
 core<-stack(data.frame(round(rbind(x$coefficients[,1],x$coefficients[,2],x$coefficients[,3]),3)))
 core$ind<-as.character(core$ind)
 names(core)[1]<-name
 core$type <- rep(1:3,nrow(core)/3)
 core<-rbind(core,data.frame(reg=nrow(y$model),ind="zN",type=4))
 dv <- gsub("(.*)\\s~.*","\\1",y$call[2])
 tmp <-data.frame(reg=as.numeric(table(y$model[,dv])),ind=paste("z",levels(y$model[,dv]),sep=""),type=4)
 core <- rbind(core,tmp)
 return(core)} 
tab.z <- stack.zelig(z)
tab.z4 <- stack.zelig(z4)
the.table <- merge(tab.z4,tab.z,by=c("ind","type"),all=T) 
the.table$ind <- ifelse(the.table$type==1|the.table$type==4,the.table$ind,NA)
print(xtable(the.table[,-2]),include.rownames=F) 
write.csv(the.table[,-2],file="output_appendixtable.csv",row.names=F) 

 