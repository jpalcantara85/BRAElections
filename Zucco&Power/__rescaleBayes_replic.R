## Performs the rescaling of legislators responses to ideological self placement
## and placement of other parites, presented in the LAPS 2012 article.

## Requires two additional files to run:
## 1) the data (in file PowerALL.Rdta)
## 2) the jags model (in file rescalingmodel.txt)

## Place the three files in the same folder, change the paths accordingly, and source the code

## This routine uses Jags, so it only runs on a MAC
## To run on a PC, need to change the jags.model line to rbugs sintax, and change the handling of the output
## Saves a dignoasis plot, raw output, and meaningful results


library(rjags)
library(coda)
library(MCMCpack)
library(car)
library(reshape)

run.from <- "~/Dropbox/DATA"

setwd(paste(run.from,"/PLIO-Oxford/Paper-ECPR",sep=""))
load(paste(run.from,"/PLIO-Oxford/RescalePLIO/PowerALL.Rdta",sep="")) #path to datafile


#### define imputatoin function before running actual rescaling

inputeNA <- function(xx){ 
	### This function does TWO different imputations
	### For cases where self placement is missing, impute the one's placement of own party
  	### I also implemented a different methods here, to predice one's own plcement, but it is almost identical to the simpker methods, above.
	### For missing placements of parties, performs a rocking regression imputation

	lr <- xx[,grep("LR",names(xx))][,-1]
    parties <- gsub("LR","",names(lr))

	m<-function(x){ which(parties==x)}
	own.party.placement <- own.party <- as.numeric(lapply(xx$PP,m)) #identifies which columns has one's own party's placement
	for(i in 1:nrow(xx)){own.party.placement[i] <- if(is.null(lr[i,own.party[i]])){NA}else{lr[i,own.party[i]]}}
	cat("Used placement of own's party in",sum(is.na(own.party.placement[is.na(xx$LRCLASS)])==F),"out of",sum(is.na(xx$LRCLASS)),"cases of missing self placment\n")
		xx$LRCLASS[is.na(xx$LRCLASS)]<-own.party.placement[is.na(xx$LRCLASS)]
	      #alternative method inspired by reviewer: predict instead of assume it is the same
        reg <- lm(xx$LRCLASS~own.party.placement*I(own.party.placement>5.5))
        pred.party.placement <- predict(reg,newdata=data.frame(own.party.placement=own.party.placement[is.na(xx$LRCLASS)]))
        #xx$LRCLASS[is.na(xx$LRCLASS)]<-pred.party.placement #uncomment this to use the alternative method. It is almost identifcal to the simpler method        
    lr.nona<-na.omit(lr)                                    #exclude all missing cases  
    pij<- t(lr.nona)           #matrix of placements
    centered.pij<- sweep(pij,2,apply(pij,2,mean)) #center legislator's classifications
    pca <- old.pca <- prcomp(t(centered.pij),center=FALSE)$rotation[,1] #first columns of decomposition of matrix of placements, with replaced NA
    if(sign(sum(sign(pca)))<=0){
        pca  <- old.pca <- pca * -1}                        #Make sure there are more positives than negatives to make beta positives
    pstr<- cbind(cons=rep(1,length(pca)),pj=pca/sd(pca))#add a constant vector and use the "standarized" first dimension of decomposition as true placements,
    rownames(pstr)<-parties
    old.coefs<-coefs <-solve(t(pstr)%*%pstr) %*% t(pstr)%*%pij         #regression
    rownames(old.coefs)<-rownames(coefs)<-c("a","b")                             
    
    #Rocking imputation for NA's
    reps<-50
    pij<- t(lr[,paste("LR",parties,sep="")])                #pij with NA
    colnames(pij) <- rownames(lr)                          #for some reason, t() does not preserve colnames in 2009 data (!)
    imputed<-is.na(pij)                                     #NA's in original pij matrix
    allpstr<-pstr[,2]                                       #Store convergence of pstr's
    allcoefs<-list(a=matrix(NA,ncol=reps,nrow=length(na.action(lr.nona))),
                   b=matrix(NA,ncol=reps,nrow=length(na.action(lr.nona))))  #store convergence of coefs for missing pij's
    coefs.mean<-apply(coefs,1,mean)                         #compute mean coeffs 
    seeds <- matrix(rep(pstr %*% coefs.mean,ncol(pij))
              ,nrow=nrow(pij),byrow=FALSE)                  #compute matrix of mean predicted values as seeds for missing values
    pij[which(imputed==TRUE)]<-seeds[which(imputed==TRUE)]  #replace NA's with seed values
    centered.pij<- sweep(pij,2,apply(pij,2,mean))           #center legislator's classifications
    
    for(j in 1:reps){                        
        pca <- prcomp(t(centered.pij),center=FALSE)$rotation[,1] #first columns of decomposition of matrix of placements, with replaced NA
        pca <- pca * sign(old.pca)/sign(pca)                #make sure sign matches old.pca. PCA Sign is arbitrary.
        pstr<- cbind(cons=rep(1,length(pca)),pj=pca/sd(pca))#add a constant vector and use the "standarized" first dimension of decomposition as true placements,
        rownames(pstr)<-parties                              #name the matrix rows
        coefs <-solve(t(pstr)%*%pstr) %*% t(pstr)%*%pij     #regression, estimated coefficients
        rownames(coefs)<-c("a","b")                             
        predicted<-pstr%*%coefs                             #compute predicted values
        pij[which(imputed==TRUE)]<-predicted[which(imputed==TRUE)]   #replace original NA's with new predicted values
        centred.pij<- sweep(pij,2,apply(pij,2,mean))        #center legislator's classifications
        allpstr<-cbind(allpstr,pstr[,2])                    #Store convergence data for pstr
        allcoefs[["a"]][,j]<- coefs["a",na.action(lr.nona)] #Store convergence data for alphas
        allcoefs[["b"]][,j]<- coefs["b",na.action(lr.nona)] #Store convergence data for betas
                                                            #Multiply by the sign to ensure "positive" betas    
        } 

cat("Found and imputed",sum(is.na(xx[,names(lr)])),"NAs out of", prod(dim(lr)),"obs",sum(is.na(xx[,names(lr)]))/prod(dim(lr)),"%\n")
xx[,names(lr)]    <-  t(pij)
return(xx)
}


### assemble single file in long format 
powerALL <- lapply(powerALL,inputeNA)
tmp <- lapply(powerALL,melt.data.frame,id.vars=c("CASEID","PP","NAME","STATE","LRCLASS"),variable_name = "PARTY_PLACED")	
the.data <- do.call("rbind",tmp)
the.data$YEAR <- factor(gsub("\\..*$","",gsub("power","",rownames(the.data))))
the.data$PARTY_PLACED <- gsub("LR","",the.data$PARTY_PLACED)
	the.data$PARTY_PLACED <- ifelse(the.data$PARTY_PLACED=="PP"&the.data$YEAR==1993,"PPold",the.data$PARTY_PLACED)
	the.data$PARTY_PLACED <- factor(car::recode(the.data$PARTY_PLACED,"'PFL'='DEM';c('PPB','PPR','PDS','PP')='PP';'PCB'='PPS';'PL'='PR'"))

#Avoid dropping just because party is missing
the.data$PP[is.na(the.data$PP)] <- "OUTRO" #avoid NA's


#### Preparing the data #######################################
the.data <- na.omit(the.data) #### no imputation, using only observed values
the.data$NAME <- factor(the.data$NAME) #only needed because of na.omit
the.data$PARTYYEAR <- factor(paste(the.data$PARTY_PLACED,the.data$YEAR,sep=""))
the.data$W <- as.numeric(the.data$PARTY_PLACED)
the.data$K <- as.numeric(the.data$PARTYYEAR)
the.data$N <- as.numeric(the.data$NAME)
the.data$NAMEYEAR <- factor(paste(the.data$NAME,the.data$YEAR,sep=""))
the.data$NY <- as.numeric(the.data$NAMEYEAR)

M <- the.data$LRCLASS
TT <- nrow(the.data)
P <- the.data$value
Y <- as.numeric(the.data$YEAR)
YS <- length(unique(Y))
N <- the.data$N   #legislators
NS <- length(unique(N))
K <- the.data$K   #partyyears
KS <- length(unique(K))
NY <- the.data$NY  #legislatoryears
NYS <- length(unique(NY))
W <- the.data$W  #parties
WS <- length(unique(W))

## Legislator-year format
tmp<-melt(the.data,id=c("NAMEYEAR","PP","YEAR"),measure="LRCLASS")
the.data.ly<-cast(tmp,formula = NAMEYEAR+ PP+ YEAR ~variable , fun.aggregate="mean")     
the.data.ly$NAME <- factor(gsub("(.*)(\\d\\d\\d\\d)$","\\1",the.data.ly$NAMEYEAR))

MM <- the.data.ly$LRCLASS
YY <- as.numeric(the.data.ly$YEAR)
NN <- as.numeric(the.data.ly$NAME)
PP <- as.numeric(factor(as.character(the.data.ly$PP)))
     
cat("\nMean Party Placement and SD in Whole Sample",mean(P,na.rm=T),sd(P,na.rm=T))
cat("\nMean Self Placement and SD in While Sample",    mean(MM,na.rm=T),sd(MM,na.rm=T))
prev<-0
for(rr in 100:100){
cat("\nTwo step procedure with normalization after imputation\nObs",TT,"\nLegislators",NS,"\nLegislator Years",NYS,"\n")  
flush.console()                
jags <- jags.model('rescalingmodel.txt',##uses legislator specific a and b
                   data = list('P' = P, 'NYS'=NYS, 'KS'=KS, 'NS'=NS, 'YS'=YS, 'N'=N, 
                   'K'=K, 'MM'=MM, 'YY'=YY, 'NN'=NN, 'Y'=Y, 'M'=M),
                   n.chains = 1,
                   n.adapt = 1000)
                                     
update(jags, 10000,progress.bar="text",by=500)#10000
out <- jags.samples(jags,
             c('pp', 'a', 'b','d','g','mstr','taup','tauz','taum','ppraw','mstrraw','ppalt'),
             5000,thin=5)#5000

flush.console()
#### Extract results #######################################             
party <- data.frame(party=levels(the.data$PARTYYEAR),
				valueperaw = summary(out$ppraw,mean)$stat,
				valueseraw = sqrt(summary(out$ppraw,var)$stat),
				valuepe=summary(out$pp,mean)$stat,
				valuese=sqrt(summary(out$pp,var)$stat),
				valuepealt = summary(out$ppalt,mean)$stat,
				valuesealt = sqrt(summary(out$ppalt,var)$stat)
				)
party$year <- as.numeric(gsub("\\D","",party$party))
party$party <- factor(gsub("\\d","",party$party))

legis <- data.frame(legis = levels(the.data$NAME),
					legiscode = 1:NS,
					rescaledraw = summary(out$mstrraw,mean)$stat,
					rescaledraw.se = sqrt(summary(out$mstrraw,var)$stat),
					rescaled = summary(out$mstr,mean)$stat,
					rescaled.se = sqrt(summary(out$mstr,var)$stat)) #get mst by legis
tmp <- ddply(the.data, .(NAME, YEAR, LRCLASS, PP), "nrow")
legis.yr <- merge(tmp,legis,by.x="NAME",by.y="legis",all.x=T)  #compare with actual placements

year <- data.frame(year = levels(the.data$YEAR),
					yearcode = 1:YS,
					estd = summary(out$d,mean)$stat,
					estg = summary(out$g,mean)$stat)

ab <- data.frame(#nameyear= levels(the.data$NAMEYEAR),
				#nameyearcode = 1:NYS,
				esta = summary(out$a,mean)$stat,
				estb = summary(out$b,mean)$stat)		

Phat <- ab$esta[the.data$N] + 
		ab$estb[the.data$N] * party$valueperaw[the.data$K]
		
Phat <- ab$esta[N] + ab$estb[N] * (year$estd[Y] +  year$estg[Y] * party$valueperaw[K])		
R2all <- var(Phat)/var(P)
R2year <- as.numeric(by(Phat,Y,var)/by(P,Y,var))
R2 <- c(R2all,R2year)
names(R2) <- c("All","1990","1993","1997","2001","2005","2009")	
flush.console()					
				
	taus <- list(taup=summary(out$taup,mean)$stat	,
	taum = summary(out$taum,mean)$stat	, tauz=summary(out$tauz,mean)$stat)							
results <- list(party=party,legis=legis.yr, year=year, r2=R2, taus=taus, ab=ab, call=jags)

save(results, file=paste("out_estimates","-",rr,".RData",sep=""))
save(out, file=paste("out_outraw","-",rr,".RData",sep=""))


####
jpeg(file=paste("out_diagnosticplots","-",rr,".jpg",sep=""),width=15,height=10,units="in",res=150)
par(mfrow=c(2,3))
boxplot(rescaled~LRCLASS,data=results$legis)

x<-party;pe.string="valuepe";se.string="valuese"
	pe <- x[,pe.string]
    se <- x[,se.string]
    x$party <- factor(x$party,levels=names(sort(by(x[,pe.string],x$party,mean,na.rm=TRUE)))) #figure out best ordering of parties
    parties <-  levels(x$party) #levels preservs ordering
    plot(range(na.omit(c(pe-1.64*se,pe+1.64*se))),c(1,length(parties)), type="n",yaxt="n",xaxt="n",ylab="",xlab="")
    axis(2,at=1:length(parties),labels=parties,srt=90,las=2,tick=FALSE,cex.axis=1.3)
    mtext(expression("" %<-% Esquerda),side=1,line=.5, adj = 0,cex=1.5)
    mtext(expression(Direita %->% ""),side=1,line=.5, adj = 1,cex=1.5)
    for(p in 1:length(parties)){
        by.party <- subset(x,party==parties[p])
        pe <- by.party[,pe.string]
        se <- by.party[,se.string]
        ys <-  seq(p+.22,p-0.22,length=length(unique(x$year)))[1:nrow(by.party)] #y coordinates
        points(pe,ys,pch=20,cex=1.3)
        for(i in 1:nrow(by.party)){lines(c(pe[i]-1.64*se[i],pe[i]+1.64*se[i]), c(ys[i],ys[i]),lwd=2)  }}


tmp <- data.frame(rbind(data.frame(est=results$legis$rescaled,se=results$legis$rescaled.se,type=1),data.frame(est=party$valuepe,se=party$valuese,type=2)))
tmp$ord <- ord <- sort(tmp$est,index.return=T)$ix
plot(tmp$est[ord],1:nrow(tmp),ylab="",cex=21,bg="white",type="n") 
		 segments(x0=tmp$est[ord]-1.64*tmp$se[ord],
		 y0=1:nrow(tmp),
		 x1=tmp$est[ord]+1.64*tmp$se[ord],
		 y1=1:nrow(tmp),col=tmp$type[ord])
		 points(tmp$est[ord],1:nrow(tmp),ylab="",cex=1,pch=ifelse(tmp$type[ord]==1,21,3),col=ifelse(tmp$type[ord]==1,"white","red"),bg=ifelse(tmp$type[ord]==1,gray(0.7),2))

if(prev>0){
r <- results
load(paste("out_estimates","-",prev,".RData",sep=""))
r.old <- results
plot(r$party$valuepe,r.old$party$valuepe,col=factor(r$party$year),pch=19,xlab=paste("Parties\nRun",rr),ylab=paste("Run",prev))
abline(0,1)
points(r$party$valuepe[nrow(r$party)],r.old$party$valuepe[nrow(r$party)],pch=17,cex=2)
plot(r$legis$rescaled,r.old$legis$rescaled,col=factor(r$legis$YEAR),pch=19,xlab=paste("Legislators\nRun",rr),ylab=paste("Run",prev))
abline(0,1)
plot(r$year$estg,r.old$year$estg,xlab=paste("Gammas and Betas\nRun",rr),ylab=paste("Run",prev),cex=2,ylim=c(-1,3),xlim=c(-1,3),pch=3)
points(r$ab$estb,r.old$ab$estb,col=2,pch=19,cex=0.5)
points(r$year$estg,r.old$year$estg,col=1,cex=2,pch=2)
abline(0,1)
}
dev.off()

cat("Average SE on parties",mean(party$valuese),"\n")
cat("Average SE on legislators",mean(legis$rescaled.se),"\n")
cat("Average beta on legislators",mean(ab$estb),"\n")
cat("R2");print(R2)
prev<-rr
cat("\nDone with",rr,"\n")
flush.console()	




}



