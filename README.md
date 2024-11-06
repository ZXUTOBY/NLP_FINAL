After the evaluation and analysis, we will compare our model's prediction on the answers and the real answers. We could check token by token, see what is the accuracy of our answer. Such process need another python file that process the original dataset and the output we got after the evaluation. 

If we have a good prediction, we could start thinking about the different ways of training ensemble model and assess its performance comparing to the single model we trained. 

If we do not have a good prediction on answers, we need to figure out more training methods, like training two models for predicting answer, one is for predicting the starting token, and another is for predicting ending token. 