runplot_plungedistinct_int<-function(e){
  parampd<-pgls_models_list5[e][[1]]$model$coef[1]+
    log(subset(longdfplotting,longdfplotting$earmeasures==yvarnames[e]&longdfplotting$plungedistinct=="Underwater pursuit")$Head.mass..g.)*
    (pgls_models_list5[e][[1]]$model$coef[2])
  paramsf<-(pgls_models_list5[e][[1]]$model$coef[1]+pgls_models_list5[e][[1]]$model$coef[4])+
    log(subset(longdfplotting,longdfplotting$earmeasures==yvarnames[e])$Head.mass..g.)*
    (pgls_models_list5[e][[1]]$model$coef[2]+pgls_models_list5[e][[1]]$model$coef[7])
  paramsT<-(pgls_models_list5[e][[1]]$model$coef[1]+pgls_models_list5[e][[1]]$model$coef[5])+
    log(subset(longdfplotting,longdfplotting$earmeasures==yvarnames[e])$Head.mass..g.)*
    (pgls_models_list5[e][[1]]$model$coef[2]+pgls_models_list5[e][[1]]$model$coef[8])
  paramsplg<-(pgls_models_list5[e][[1]]$model$coef[1]+pgls_models_list5[e][[1]]$model$coef[3])+
    log(subset(longdfplotting,longdfplotting$earmeasures==yvarnames[e])$Head.mass..g.)*
    (pgls_models_list5[e][[1]]$model$coef[2]+pgls_models_list5[e][[1]]$model$coef[6])
  p<-ggplot(subset(longdfplotting,longdfplotting$earmeasures==yvarnames[e]), 
            aes(x = log(Head.mass..g.), y = log(earmeasureval), label = Binomial), 
            factor = as.factor(plungedistinct))+
    theme_classic()+
    theme(legend.position = "none")+
    geom_point(aes(color = plungedistinct))+
    scale_color_manual(values=c("green","black","darkgrey","blue","green","darkgray","darkgreen","corns2lk4","blue"))+
    geom_line(data = subset(longdfplotting,longdfplotting$earmeasures==yvarnames[e]&longdfplotting$plungedistinct=="Underwater pursuit"),
              aes(x = log(Head.mass..g.),y = parampd), col = "green")+
    geom_line(data = subset(longdfplotting,longdfplotting$earmeasures==yvarnames[e]),
              aes(x = log(Head.mass..g.),
                  y = paramsf), col = "darkgrey")+
    geom_line(data = subset(longdfplotting,longdfplotting$earmeasures==yvarnames[e]),
              aes(x = log(Head.mass..g.),y = paramsT), col = "blue")+
    geom_line(data = subset(longdfplotting,longdfplotting$earmeasures==yvarnames[e]),
              aes(x = log(Head.mass..g.),y = paramsplg), col = "black")+
    #scale_x_log10()+
    #scale_y_log10()+
    #geom_text_repel(aes(label = Orderpdonly))+
    ylab(paste0("log(",yvarnames[e],")"))
  p
  #ggExtra::ggMarginal(p, type = "boxplot", groupColour = TRUE, margins = "y")#add marginal plot to 'p' object
}