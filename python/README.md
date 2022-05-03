# Captcha Cracking

A Captcha cracking tool based on CNN and LSTM


## Dataset
109K captcha images with labels (names) <br>
<a> https://drive.google.com/file/d/1nalIGeKAJk9OaFrmLALEJC56lAxyE7K6/view </a>

## Model
CNN + LSTM - > CRNN text recognition <br>
<a> https://dl.acm.org/doi/abs/10.1145/3297067.3297073 </a>
<br>
Based on Resnet34 Torchvision - Transfer Learning <br>
<a> https://pytorch.org/vision/stable/generated/torchvision.models.resnet34.html </a>

## Train + Test
0.8/0.2 split <br>

99.33% Accuracy on 21838 samples (20% test)

## Error prediction samples
16 random samples chosen as an example to show how the model misclassifies <br>
![alt tag](https://github.com/orel1212/MyWorks/blob/main/Deep%20Learning/CaptchaCracking/captcha_errors.JPG)

## Files
### Captcha_Cracking_CRNN_train.ipynb.ipynb
running notebook of the code of the train
### Captcha_Cracking_CRNN_test.ipynb
running notebook of the code of the test
### captcha_dataset.py 
dataset class
### crnn_model.py
crnn class
### utils.py
misc. functions and decoder class

## Dependencies
Python 3.8 <br>
Pytorch <br>
Numpy

## Made by Orel Lavie and Tamir Gabay
<a> https://github.com/tamirgabgab </a>
